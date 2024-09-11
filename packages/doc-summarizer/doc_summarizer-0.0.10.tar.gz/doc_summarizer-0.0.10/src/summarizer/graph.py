from langchain_openai import ChatOpenAI
from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_core.language_models import BaseLanguageModel

import operator
from typing import Annotated, List, Literal, TypedDict, Union

from langchain.chains.combine_documents.reduce import (
    acollapse_docs,
    split_list_of_docs
)
from langchain_core.documents import Document
from langgraph.constants import Send
from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph


# llm = ChatOpenAI(model="gpt-4o-mini")

# map_prompt = hub.pull("rlm/map-prompt")
# reduce_prompt = hub.pull("rlm/reduce-prompt")
    
# map_chain = map_prompt | llm | StrOutputParser()            # ??? Global?? async? gather? httpx import for example? how? why? 
# reduce_chain = reduce_prompt | llm | StrOutputParser()


class OverallState(TypedDict):
    contents: List[Document]
    merged_contents: List[List[Document]]
    summaries: Annotated[list, operator.add]
    collected_summaries: List[Document]
    merged_collected_summaries: List[List[Document]]
    reduced_summaries: Annotated[list, operator.add]
    final_summary: str


class SummaryState(TypedDict):
    content: str

class ReduceSummaryState(TypedDict):
    content: str

    
class SummarizeGraph():
    """
    Containing Lang Graph implementation for Map Reduce Summarization. 
    
    Attributes:
        llm (BaseLanguageModel): Langchain language model.
        max_token (int): Maximum token allowed for llm. Used for chunking strategy.
    
    Methods: 
        load_graph() -> "CompiledStateGraph"
        display_graph()
        get_summary(self, docs: Union[Document | List[Document]]) -> str:
    
    Example Usage (sync): 
        import dotenv
        dotenv.load_dotenv()
        from langchain_openai import ChatOpenAI
        from langchain_community.document_loaders import PyPDFLoader
        llm = ChatOpenAI(model="gpt-4o-mini")
        loader = PyPDFLoader('test.pdf')
        docs = loader.load()

        graph = SummarizeGraph(llm, max_token=1000)
        app = graph.load_graph()
        graph.display_graph()

        for step in app.stream(
                {"contents": [doc for doc in docs]},
                {"recursion_limit": 10},
            ):
                print(list(step.keys()))
         
    Example Usage (async):
        import asyncio
        async def main():
            async for step in app.astream(
                {"contents": [doc for doc in docs]},
                {"recursion_limit": 10},
            ):
                print(list(step.keys()))
            print(step)
        asyncio.run(main())
        
    Example Usage (none stream):
        app.invoke({"contents": [doc for doc in docs]}, {"recursion_limit": 10})
    
    Example Usage (simple easy setup):
        graph = SummarizeGraph(llm, max_token=1000)
        res = graph.get_summary(docs=docs)

    """
    
    def __init__(self, llm: BaseLanguageModel, max_token: int) -> None:
        self.llm = llm
        self.max_token = max_token
        
        self.map_prompt = hub.pull("rlm/map-prompt")
        self.reduce_prompt = hub.pull("rlm/reduce-prompt")
        
        self.map_chain = self.map_prompt | llm | StrOutputParser()            # ??? Global?? async? gather? httpx import for example? how? why? 
        self.reduce_chain = self.reduce_prompt | llm | StrOutputParser()

        self.compiled_graph = None
        
    def _length_function(self, documents: List[Document]) -> int:
        """Get number of tokens for input contents."""
        return sum(self.llm.get_num_tokens(doc.page_content) for doc in documents)

    def _merge_documents(self, state: OverallState):
        docs = state["contents"]
        merged_docs = split_list_of_docs(
            docs, self._length_function, self.max_token
        )
        
        return {"merged_contents": merged_docs}


    async def _generate_summary(self, state: SummaryState):
        response = await self.map_chain.ainvoke(state["content"])
        return {"summaries": [response]}

    def _generate_summary(self, state: SummaryState):
        response = self.map_chain.invoke(state["content"])
        return {"summaries": [response]}

    def _map_summaries(self, state: OverallState):
        return [
            Send("_generate_summary", {"content": content}) for content in state["merged_contents"]
        ]


    def _collect_summaries(self, state: OverallState):
        return {
            "collected_summaries": [Document(summary) for summary in state["summaries"]]
        }

    #########

    def _merge_collected_documents(self, state: OverallState):
        docs = state["collected_summaries"]
        merged_docs = split_list_of_docs(
            docs, self._length_function, self.max_token
        )
        
        return {"merged_collected_summaries": merged_docs}


    async def _reduce_summary(self, state: ReduceSummaryState):
        response = await self.reduce_chain.ainvoke(state["content"])
        return {"reduced_summaries": [response]}
    
    def _reduce_summary(self, state: ReduceSummaryState):
        response = self.reduce_chain.invoke(state["content"])
        return {"reduced_summaries": [response]}
    
    def _map_collected_summaries(self, state: OverallState):
        return [
            Send("_reduce_summary", {"content": content}) for content in state["merged_collected_summaries"]
        ]

    def _collect_reduced_summaries(self, state: OverallState):
        return {
            "collected_summaries": [Document(summary) for summary in state["reduced_summaries"]]
        }

    # This represents a conditional edge in the graph that determines
    # if we should collapse the summaries or not
    def _should_reduce(
        self, 
        state: OverallState,
    ) -> Literal["_merge_collected_documents", "_generate_final_summary"]:
        num_tokens = self._length_function(state["collected_summaries"])
        if num_tokens > self.max_token:
            return "_merge_collected_documents"
        else:
            return "_generate_final_summary"


    # Here we will generate the final summary
    async def _generate_final_summary(self, state: OverallState):
        response = await self.reduce_chain.ainvoke(state["collected_summaries"])
        return {"final_summary": response}

    def _generate_final_summary(self, state: OverallState):
        response = self.reduce_chain.invoke(state["collected_summaries"])
        return {"final_summary": response}
    
    def load_graph(self) -> "CompiledStateGraph":
        # Nodes:
        graph = StateGraph(OverallState)

        graph.add_node("_merge_documents", self._merge_documents)  
        graph.add_node("_generate_summary", self._generate_summary)  
        graph.add_node("_collect_summaries", self._collect_summaries)
        graph.add_node("_merge_collected_documents", self._merge_collected_documents)
        graph.add_node("_reduce_summary", self._reduce_summary)
        graph.add_node("_collect_reduced_summaries", self._collect_reduced_summaries)
        graph.add_node("_generate_final_summary", self._generate_final_summary)

        # Edges:
        graph.add_edge(START, "_merge_documents")
        graph.add_conditional_edges("_merge_documents", self._map_summaries, ["_generate_summary"])
        graph.add_edge("_generate_summary", "_collect_summaries")

        graph.add_conditional_edges("_collect_summaries", self._should_reduce)
        graph.add_conditional_edges("_collect_reduced_summaries", self._should_reduce)

        graph.add_conditional_edges("_merge_collected_documents", self._map_collected_summaries, ["_reduce_summary"])
        graph.add_edge("_reduce_summary", "_collect_reduced_summaries")

        graph.add_edge("_generate_final_summary", END)

        self.compiled_graph = graph.compile()
    
        return self.compiled_graph
    
    def display_graph(self):
        from IPython.display import Image
        Image(self.compiled_graph.get_graph().draw_mermaid_png())
        
    def get_summary(self, docs: Union[Document | List[Document]]) -> str:
        if not self.compiled_graph:
            self.load_graph()
            
        graph_output = self.compiled_graph.invoke({"contents": [doc for doc in docs]}, {"recursion_limit": 10})
        return graph_output['final_summary']


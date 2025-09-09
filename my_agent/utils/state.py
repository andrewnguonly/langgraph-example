from langgraph.graph import add_messages
from langchain_core.messages import BaseMessage
from typing_extensions import TypedDict, Annotated, Sequence

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

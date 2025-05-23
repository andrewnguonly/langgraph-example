from typing import TypedDict, Annotated, Sequence

from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph
from langchain_core.messages import BaseMessage
from pydantic import BaseModel

from pydantic import ValidationError
from langgraph.graph import add_messages


class CrashExampleConfig(BaseModel):
    task_id: str = "2997$10071"
    model_name: str = "claude-3-7-sonnet@20250219"

class CrashExampleState(TypedDict, total=False):
    task_id: str
    messages: Annotated[Sequence[BaseMessage], add_messages]


def start_task(
    state: CrashExampleState,
    config: RunnableConfig,
) -> CrashExampleState:
    try:
        conf = CrashExampleConfig.from_runnable_config(config)
    except ValidationError as e:
        error_msg = f"Error: Failed to parse configuration: {e}"
        raise ValidationError(error_msg)

    return {
        "messages": [
            AIMessage(
                content=f"Success: {state['task_id']}"
            )
        ]
    }


graph = StateGraph(CrashExampleState, config_schema=CrashExampleConfig)
graph.add_node("start_task", action=start_task)

graph.set_entry_point("start_task")

graph.add_edge("start_task", END)

memory = MemorySaver()
graph = graph.compile(
    checkpointer=memory
)

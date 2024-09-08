from typing import Sequence
from langchain.tools import BaseTool
from langchain_core.language_models.base import LanguageModelLike
from langchain_core.runnables import RunnableBinding
from .agent_types import create_openai_func_call_agent_executor, create_react_agent_executor


class Runnable(RunnableBinding):
    agent_execution_mode: str
    tools: Sequence[BaseTool]
    llm: LanguageModelLike
    assistant_message: str

    def __init__(
        self,
        *,
        agent_execution_mode: str,
        tools: Sequence[BaseTool],
        llm: LanguageModelLike,
        assistant_message: str,
    ) -> None:
        
        if agent_execution_mode == "FuncCall":
            agent_executor_object = create_openai_func_call_agent_executor
        else:
            agent_executor_object = create_react_agent_executor
        agent_executor = agent_executor_object(tools, llm, assistant_message)
        agent_executor = agent_executor.with_config({"recursion_limit": 50})
        super().__init__(
            tools=tools,
            llm=llm,
            agent_execution_mode=agent_execution_mode,
            assistant_message=assistant_message,
            bound=agent_executor, return_intermediate_steps=True
        )
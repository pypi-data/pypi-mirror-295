# reference：https://github.com/maxtheman/opengpts/blob/d3425b1ba80aec48953a327ecd9a61b80efb0e69/backend/app/agent_types/openai_agent.py
import json

from langchain.tools import BaseTool
from langchain_core.utils.function_calling import convert_to_openai_tool
from langchain_core.language_models.base import LanguageModelLike
from langchain_core.messages import  SystemMessage, ToolMessage
from langgraph.graph import END
from langgraph.graph.message import MessageGraph
from langgraph.prebuilt import ToolExecutor, ToolInvocation
from typing import Any


def create_openai_func_call_agent_executor(tools: list[BaseTool], llm: LanguageModelLike,
                                        system_message: str, **kwargs):

    async def _get_messages(messages):
        msgs = []
        for m in messages:
            if isinstance(m, ToolMessage):
                _dict = m.dict()
                _dict['content'] = str(_dict['content'])
                m_c = ToolMessage(**_dict)
                msgs.append(m_c)
            else:
                msgs.append(m)

        return [SystemMessage(content=system_message)] + msgs

    if tools:
        llm_with_tools = llm.bind(tools=[convert_to_openai_tool(t) for t in tools])
    else:
        llm_with_tools = llm
    agent = _get_messages | llm_with_tools
    tool_executor = ToolExecutor(tools)

    # Define the function that determines whether to continue or not
    def should_continue(messages):
        # If there is no FuncCall, then we finish
        last_message = messages[-1]
        if not last_message.tool_calls:
            return "end"
        # Otherwise if there is, we continue
        else:
            return "continue"

    # Define the function to execute tools
    async def call_tool(messages):
        actions: list[ToolInvocation] = []
        # Based on the continue condition
        # we know the last message involves a FuncCall
        last_message = messages[-1]
        for tool_call in last_message.additional_kwargs['tool_calls']:
            function = tool_call['function']
            function_name = function['name']
            _tool_input = json.loads(function['arguments'] or '{}')
            # We construct an ToolInvocation from the function_call
            actions.append(ToolInvocation(
                tool=function_name,
                tool_input=_tool_input,
            ))
        # We call the tool_executor and get back a response
        responses = await tool_executor.abatch(actions, **kwargs)
        # We use the response to create a ToolMessage
        tool_messages = [
            ToolMessage(
                tool_call_id=tool_call['id'],
                content=response,
                additional_kwargs={'name': tool_call['function']['name']},
            )
            for tool_call, response in zip(last_message.additional_kwargs['tool_calls'], responses)
        ]
        return tool_messages

    workflow = MessageGraph()

    # Define the two nodes we will cycle between
    workflow.add_node('agent', agent)
    workflow.add_node('action', call_tool)

    # Set the entrypoint as `agent`
    # This means that this node is the first one called
    workflow.set_entry_point('agent')

    # We now add a conditional edge
    workflow.add_conditional_edges(
        # First, we define the start node. We use `agent`.
        # This means these are the edges taken after the `agent` node is called.
        'agent',
        # Next, we pass in the function that will determine which node is called next.
        should_continue,
        # Finally we pass in a mapping.
        # The keys are strings, and the values are other nodes.
        # END is a special node marking that the graph should finish.
        # What will happen is we will call `should_continue`, and then the output of that
        # will be matched against the keys in this mapping.
        # Based on which one it matches, that node will then be called.
        {
            # If `tools`, then we call the tool node.
            'continue': 'action',
            # Otherwise we finish.
            'end': END,
        },
    )

    # We now add a normal edge from `tools` to `agent`.
    # This means that after `tools` is called, `agent` node is called next.
    workflow.add_edge('action', 'agent')

    # Finally, we compile it!
    # This compiles it into a LangChain Runnable,
    # meaning you can use it as you would any other runnable
    return workflow.compile()

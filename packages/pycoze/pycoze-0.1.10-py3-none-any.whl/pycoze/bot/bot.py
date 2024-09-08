import json
from langchain_openai import ChatOpenAI
from .base import import_tools
from .agent import run_agent, Runnable, INPUT_MESSAGE, output
import asyncio
from langchain_core.messages import HumanMessage


def load_role_setting(bot_setting_file:str):
    with open(bot_setting_file, "r", encoding="utf-8") as f:
        return json.load(f)

def load_tools(bot_setting_file:str):
    with open(bot_setting_file, "r", encoding="utf-8") as f:
        role_setting = json.load(f)
        
    tools = []
    for tool_id in role_setting["tools"]:
        tools.extend(import_tools(tool_id))
    return tools




def chat(bot_setting_file:str, llm_file:str):
    history = []

    while True:
        message = input()
        role_setting = load_role_setting(bot_setting_file)
        tools = load_tools(bot_setting_file)
        if not message.startswith(INPUT_MESSAGE):
            raise ValueError("Invalid message")
        message = json.loads(message[len(INPUT_MESSAGE):])["content"]
        print("user:", message)
        
        with open(llm_file, "r", encoding="utf-8") as f:
            cfg = json.load(f)
            chat = ChatOpenAI(api_key=cfg["apiKey"], base_url=cfg['baseURL'], model=cfg["model"], temperature=role_setting["temperature"])


        agent = Runnable(agent_execution_mode='FuncCall', # 'FuncCall' or 'ReAct'，大模型支持FuncCall的话就用FuncCall
                                                tools=tools,
                                                llm=chat,
                                                assistant_message=role_setting["prompt"],)

        history += [HumanMessage(content=message)]
        result = asyncio.run(run_agent(agent, history))
        output("assistant", result, history)


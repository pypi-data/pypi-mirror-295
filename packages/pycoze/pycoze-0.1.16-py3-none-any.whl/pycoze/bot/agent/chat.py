import json
from langchain_core.messages import HumanMessage, AIMessage


INPUT_MESSAGE = "INPUT_MESSAGE=>"
_OUTPUT_MESSAGE = "OUTPUT_MESSAGE=>"
_INFOMATION_MESSAGE = "INFOMATION_MESSAGE=>"
_LOG = "LOG=>"



def log(content, *args, end='\n', **kwargs):
    print(_LOG + content, *args, end=end, **kwargs)


def output(role, content, history):
    print(_OUTPUT_MESSAGE + json.dumps({"role": role, "content": content}))
    if role == "assistant":
        history.append(AIMessage(content=content))
        
    elif role == "user":
        history.append(HumanMessage(content=content))
    else:
        raise ValueError("Invalid role")
    return history

def info(role, content):
     print(_INFOMATION_MESSAGE + json.dumps({"role": role, "content": content}))

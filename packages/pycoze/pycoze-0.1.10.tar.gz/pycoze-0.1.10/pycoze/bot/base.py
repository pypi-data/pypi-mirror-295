import sys
import os
import argparse
import importlib
from langchain.agents import tool as _tool
import types
import langchain_core

def wrapped_tool(tool, module_path):
    old_tool_fun = tool.func
    def _wrapped_tool(*args, **kwargs):
        print(f"调用了{tool.name}")
        old_path = os.getcwd()
        try:
            sys.path.insert(0, module_path)  # 插入到第一个位置
            os.chdir(module_path)
            result = old_tool_fun(*args, **kwargs)
        finally:
            sys.path.remove(module_path)
            os.chdir(old_path)
        print(f"{tool.name}调用完毕,结果为:", result)
        return result
    return _wrapped_tool


def import_tools(tool_id):
    tool_path = "../../tool"
    old_path = os.getcwd()
    module_path = os.path.join(tool_path, tool_id)
    module_path = os.path.normpath(os.path.abspath(module_path))
    
    if not os.path.exists(module_path):
        return []
    
    # 保存当前的 sys.modules 状态
    original_modules = sys.modules.copy()
    
    try:
        sys.path.insert(0, module_path)  # 插入到第一个位置
        os.chdir(module_path)
        module = importlib.import_module("tool")
        export_tools = getattr(module, "export_tools")
        temp_list = []
        for tool in export_tools:
            assert isinstance(tool, langchain_core.tools.StructuredTool) or isinstance(tool, types.FunctionType), f"Tool is not a StructuredTool or function: {tool}"
            if isinstance(tool, types.FunctionType) and not isinstance(tool, langchain_core.tools.StructuredTool):
                temp_list.append(_tool(tool))
        export_tools = temp_list
                
    except Exception as e:
        sys.path.remove(module_path)
        os.chdir(old_path)
        return []
    
    # 卸载模块并恢复 sys.modules 状态
    importlib.invalidate_caches()
    for key in list(sys.modules.keys()):
        if key not in original_modules:
            del sys.modules[key]
    
    sys.path.remove(module_path)
    os.chdir(old_path)
    
    for tool in export_tools:
        tool.func = wrapped_tool(tool, module_path)
    
    return export_tools


def read_arg(param: str, is_path=False):
    parser = argparse.ArgumentParser()
    parser.add_argument(param, nargs='?', help=f'Parameter {param}')
    args = parser.parse_args()
    value = getattr(args, param.lstrip('-'))
    # 如果是路径并且有引号，去掉引号
    if is_path and value and value.startswith('"') and value.endswith('"'):
        value = value[1:-1]

    return value

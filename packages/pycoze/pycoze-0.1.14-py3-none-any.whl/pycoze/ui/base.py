import json
from pycoze import utils
import json
import inspect


params_file = utils.read_arg('params_file', True)
params = None
try:
    with open(params_file, 'r', encoding='utf-8') as f:
        params = json.load(f)
except Exception as e:
    print(e)

def get_ui():
    if params is None:
        return {}
    stack = inspect.stack()
    stack_files = list(reversed([s.filename.replace('\\', '/') for s in stack]))
    match_item = None
    for f in stack_files:
        for v in params["uiRecords"]:
            if v["uiFile"] == f:
                match_item = v
                break
        if match_item:
            break

    if not match_item:
        raise Exception("uiRecords not found for file")

    by = match_item["by"]

    for i in range(10):
        try:
            if by == 'file':
                json_file = match_item["Jsonfile"]
                with open(json_file, "r", encoding='utf-8') as f:
                    return json.load(f)
            else:
                assert by == 'node'
                workflow_file = match_item["workflowFile"]
                node_id = match_item["nodeId"]
                with open(workflow_file, "r", encoding='utf-8') as f:
                    cells = json.load(f)["graph"]["cells"]
                    node = [cell for cell in cells if cell["id"] == node_id][0]
                    return json.loads(node["data"]["ui"])
        except Exception as e:
            if i == 9:
                raise e

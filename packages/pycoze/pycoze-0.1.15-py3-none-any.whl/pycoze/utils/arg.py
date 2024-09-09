import argparse
import sys
import json

def read_arg(param, is_path=False):
    args = sys.argv[1:]
    parser = argparse.ArgumentParser()
    parser.add_argument(param, nargs='?', help=f'Parameter {param}')
    args = parser.parse_known_args(args)[0]
    value = getattr(args, param.lstrip('-'))
    # 如果是路径并且有引号，去掉引号
    if is_path and value and value.startswith('"') and value.endswith('"'):
        value = value[1:-1]

    return value

def read_params():
  params_file = read_arg('params_file', True)
  params = None
  try:
      with open(params_file, 'r', encoding='utf-8') as f:
          params = json.load(f)
  except Exception as e:
      print(e)
  return params

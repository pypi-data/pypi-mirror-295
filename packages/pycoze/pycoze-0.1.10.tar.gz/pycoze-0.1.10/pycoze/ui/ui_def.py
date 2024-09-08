from .base import get_ui
from .typ import useDefaultType
from typing import Union, List
from .color import hex_to_rgb, rgb_to_hsl, ColorFormat
import sys



def useDefault(name, default):
    ui_data = get_ui()
    if name not in ui_data:
        return default
    return useDefaultType(ui_data[name], default)


def get_ui_text():
    ui = get_ui()
    output = ''
    for key, value in ui.items():
        output += f'{key}: {value}\n'
    return output


def label(name, tip="", hide_if="", style="", cls=""):
    pass


def number(name,
           default,
           min=-sys.maxsize - 1,
           max=sys.maxsize,
           step=1,
           tip="",
           hide_if="",
           style="",
           cls="") -> Union[int, float]:  # 注意Python3.9不兼容int|float
    return useDefault(name, default)


def text(name, default, tip="", hide_if="", style="", cls="") -> str:
    return useDefault(name, default)


def textarea(name, default, tip="", hide_if="", style="", cls="") -> str:
    return useDefault(name, default)


def password(name, default, tip="", hide_if="", style="", cls="") -> str:
    return useDefault(name, default)


def color(name, default, color_format: ColorFormat = "hex", tip="", hide_if="", style="", cls="") -> str:
    rgbhex = useDefault(name, default)
    if color_format == "hex":
        return rgbhex
    elif color_format == "rgb":
        return hex_to_rgb(rgbhex)
    elif color_format == "hsl":
        return rgb_to_hsl(hex_to_rgb(rgbhex))
    return rgbhex


def checkbox(name, default, tip="", hide_if="", style="", cls="") -> bool:
    return useDefault(name, default)


def single_select(name, default: Union[str, int, float, bool], options, tip="", hide_if="", style="", cls=""):
    return useDefault(name, default)


def multi_select(name,
                 default: Union[List[str], List[int], List[float], List[bool]],
                 options,
                 tip="",
                 hide_if="",
                 style="",
                 cls=""):
    return useDefault(name, default)


def file(name, default: Union[str, List[str]], is_multiple: bool, tip="", hide_if="", style="", cls="") -> str:
    return useDefault(name, default)


def folder(name, default: Union[str, List[str]], is_multiple: bool, tip="", hide_if="", style="", cls="") -> str:
    return useDefault(name, default)


def folder_tree(name, root="", default: List[str] = None, tip="", hide_if="", style="", cls="") -> dict:
    if default is None:
        default = []
    return useDefault(name, default)


def image(name, default: Union[str, List[str]], is_multiple: bool=False, tip="", hide_if="", style="", cls="") -> str:
    return useDefault(name, default)


def audio(name, default: Union[str, List[str]], is_multiple: bool=False, tip="", hide_if="", style="", cls="") -> str:
    return useDefault(name, default)


def video(name, default: Union[str, List[str]], is_multiple: bool=False, tip="", hide_if="", style="", cls="") -> str:
    return useDefault(name, default)


def seed(name, default=0, tip="", hide_if="", style="", cls="") -> int:
    return useDefault(name, default)



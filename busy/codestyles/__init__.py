"""初期化モジュール.

各モジュールのパブリックな関数・クラスと
エディタのスタイルオブジェクトを返すget_code_style関数を提供します。

"""
import os

from .base import BaseCodeStyle
from .python import PythonCodeStyle
from .html import HTMLCodeStyle


def get_code_style(editor_frame, path=None):
    """エディタのスタイルオブジェクトを返す."""
    if path is None:
        return BaseCodeStyle(editor_frame)
    else:
        _, extension = os.path.splitext(path)
        if extension == '.py':
            return PythonCodeStyle(editor_frame)
        elif extension == '.html':
            return HTMLCodeStyle(editor_frame)
        else:
            return BaseCodeStyle(editor_frame)

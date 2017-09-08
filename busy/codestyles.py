from contextlib import contextmanager
import io
import os
import sys
import tkinter as tk
import traceback

from flake8.api import legacy as flake8

from busy import mediator


@contextmanager
def stdoutIO():
    """一時的にstdoutを変更する"""
 
    old = sys.stdout
    sys.stdout = io.StringIO()
    yield sys.stdout
    sys.stdout = old


class NoneCodeStyle:

    def tab(self, editor_frame):
        pass

    def lint(self, editor_frame):
        pass

class PythonCodeStyle(NoneCodeStyle):

    def tab(self, editor_frame):
        editor_frame.text.insert(tk.INSERT, " " * 4)
        return 'break'

    def lint(self, editor_frame):
        if editor_frame.path:
            output = ''
            with stdoutIO() as stdout:
                error = ''
                try:
                    style_guide = flake8.get_style_guide()
                    report = style_guide.check_files([editor_frame.path])
                except:
                    error = traceback.format_exc()
                finally:
                    output = stdout.getvalue() + error
            if output:
                mediator.event.update_lint(text=output)

def get_code_style(path=None):
    if path is None:
        return NoneCodeStyle()
    else:
        _, extension = os.path.splitext(path)
        if extension == '.py':
            return PythonCodeStyle()
        else:
            return NoneCodeStyle()
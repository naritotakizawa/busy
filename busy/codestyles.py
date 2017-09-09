from contextlib import contextmanager
import io
import os
import sys
import tkinter as tk
import traceback

from flake8.api import legacy as flake8
from pygments import lex
from pygments.lexers import PythonLexer

from busy import mediator


@contextmanager
def stdout_io():
    """一時的にstdoutを変更する"""
    old = sys.stdout
    sys.stdout = io.StringIO()
    yield sys.stdout
    sys.stdout = old


class NoneCodeStyle:
    """デフォルトのエディタスタイル."""

    def __init__(self, editor_frame):
        self.editor = editor_frame
        self.text = editor_frame.text

    def tab(self):
        """タブキー押下時."""
        pass

    def lint(self):
        """スタイルガイドのチェックを行う."""
        pass

    def highlight(self):
        """文字をハイライトする."""
        pass


class PythonCodeStyle(NoneCodeStyle):
    """Pythonのエディタスタイル."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text.tag_configure('Token.Keyword', foreground='#CC7A00')
        self.text.tag_configure('Token.Keyword.Constant', foreground='#CC7A00')
        self.text.tag_configure(
            'Token.Keyword.Declaration', foreground='#CC7A00')
        self.text.tag_configure(
            'Token.Keyword.Namespace', foreground='#CC7A00')
        self.text.tag_configure('Token.Keyword.Pseudo', foreground='#CC7A00')
        self.text.tag_configure('Token.Keyword.Reserved', foreground='#CC7A00')
        self.text.tag_configure('Token.Keyword.Type', foreground='#CC7A00')

        self.text.tag_configure('Token.Name.Class', foreground='#003D99')
        self.text.tag_configure('Token.Name.Exception', foreground='#003D99')
        self.text.tag_configure('Token.Name.Function', foreground='#003D99')
        self.text.tag_configure(
            'Token.Name.Builtin.Pseudo', foreground='#003D99')
        self.text.tag_configure('Token.Name.Decorator', foreground='#003D99')
        self.text.tag_configure('Token.Name.Variable.Magic', foreground='#003D99')

        self.text.tag_configure('Token.Operator', foreground='#CC7A00')
        self.text.tag_configure('Token.Operator.Word', foreground='#CC7A00')

        self.text.tag_configure(
            'Token.Literal.String.Doc', foreground='#B80000')
        self.text.tag_configure('Token.Comment.Single', foreground='#B80000')

        self.text.tag_configure(
            'Token.Literal.String.Double', foreground='#248F24')
        self.text.tag_configure(
            'Token.Literal.String.Single', foreground='#248F24')

    def tab(self):
        """タブキー押下時."""
        self.text.insert(tk.INSERT, " " * 4)
        return 'break'

    def lint(self):
        """スタイルガイドのチェックを行う."""
        if self.editor.path:
            output = ''
            with stdout_io() as stdout:
                error = ''
                try:
                    style_guide = flake8.get_style_guide()
                    style_guide.check_files([self.editor.path])
                except:
                    error = traceback.format_exc()
                finally:
                    output = stdout.getvalue() + error
            if output:
                mediator.event.update_lint(text=output)

    def highlight(self):
        """文字をハイライトする."""
        self.text.mark_set('range_start', '1.0')
        data = self.text.get('1.0', 'end-1c')
        for token, content in lex(data, PythonLexer()):
            self.text.mark_set(
                'range_end', 'range_start+{0}c'.format(len(content))
            )
            self.text.tag_add(str(token), 'range_start', 'range_end')
            self.text.mark_set('range_start', 'range_end')


def get_code_style(editor_frame, path=None):
    """エディタのスタイルオブジェクトを返す."""
    if path is None:
        return NoneCodeStyle(editor_frame)
    else:
        _, extension = os.path.splitext(path)
        if extension == '.py':
            return PythonCodeStyle(editor_frame)
        else:
            return NoneCodeStyle(editor_frame)

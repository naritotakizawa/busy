from contextlib import contextmanager
import io
import os
import sys
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


class BaseCodeStyle:
    """デフォルトのエディタスタイルであり、各スタイルの基底クラス."""

    one_indent = ' \t'  # タブ
    next_is_indent = ('(', '{', '[')  # これらの後にエンターを押すと、次行はインデント一つたされる

    def __init__(self, editor_frame):
        self.editor = editor_frame
        self.text = editor_frame.text
        self.indent_length = len(self.one_indent)

    def indent(self):
        """タブキー押下時、インデント."""
        # 選択部分の始まりと終わりの行番号を取得
        first, last = self.editor.get_selection_indices()
        if first and last:
            for row in range(first, last+1):
                index = '{0}.0'.format(row)
                self.text.insert(index, self.one_indent)
        else:
            # 特にドラッグで選択せず、普通にインデントをしたい場合
            self.text.insert('insert', self.one_indent)
        return 'break'

    def dedent(self):
        """Ctrl+B、逆インデント."""
        # 選択部分の始まりと終わりの行番号を取得
        first, last = self.editor.get_selection_indices()
        if first and last:
            for row in range(first, last+1):
                # 各行のテキスト
                current_line_text = self.text.get('{0}.0'.format(row), '{0}.end'.format(row))

                # 各行の最初がインデントならば、それを消す
                indent_range_text = current_line_text[:self.indent_length]
                if indent_range_text == self.one_indent:
                    start_pos = '{0}.0'.format(row)
                    end_pos = '{0}.{1}'.format(row, self.indent_length)
                    self.text.delete(start_pos, end_pos)

        return 'break'

    def back_space(self):
        """バックスペース時に、インデントがあれば上手く消す."""
        # カーソル位置までの行テキスト
        current_line_text = self.editor.get_line_text_before_cursor()

        # カーソルの列番号(何文字めにカーソルがあるか)を取得
        _, col = self.editor.get_line_number()

        # カーソル位置の前の部分がインデントならば、インデント毎消す
        indent_range_text = current_line_text[col-self.indent_length:col]
        if indent_range_text == self.one_indent:
            self.text.delete('insert -{0}c'.format(self.indent_length), 'insert')
            return 'break'

    def get_indent_num(self, text):
        """先頭に何個インデントがあるかを返す.

        行の先頭に何個インデントがあるかを調べたい場合に使ってください。
        one_indentが\t(タブならば)、'\t\t\taaa'.count('\t')→3 のような内容になります。
        '\t\t\taa\taaa\t'のような、行の途中や最後にインデントが入ってもカウントされるのに注意してください。

        """
        return text.count(self.one_indent)

    def enter_indent(self):
        """エディタでのエンター押下時にインデントを調整する."""
        # カーソルがある位置までの、行のテキスト
        current_line_text = self.editor.get_line_text_before_cursor()
        indent_num = self.get_indent_num(current_line_text)  # インデントの数
        origin_indent = self.one_indent * indent_num  # その行のインデント

        # カーソル前の文字が{ [ ( : 等の場合、元々のインデントに一つインデントを足して字下げ
        if current_line_text and current_line_text[-1] in self.next_is_indent:
            insert_text = '\n' + origin_indent + self.one_indent

        # それ以外ならば、元々のインデントに合わせる
        else:
            insert_text = '\n' + origin_indent

        self.text.insert('insert', insert_text)
        return 'break'

    def lint(self):
        """スタイルガイドのチェックを行う."""
        pass

    def line_highlight(self):
        """現在行をハイライトする."""
        pass

    def all_highlight(self):
        """全行をハイライトする."""
        pass


class PythonCodeStyle(BaseCodeStyle):
    """Pythonのエディタスタイル."""

    one_indent = ' ' * 4  # 半角スペース4つ
    next_is_indent = ('(', '{', '[', ':')  # これらの後にエンターを押すと、次行はインデント一つたされる

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.create_text_tag()

    def create_text_tag(self):
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
            'Token.Name.Function.Magic', foreground='#003D99')
        self.text.tag_configure(
            'Token.Name.Builtin.Pseudo', foreground='#003D99')
        self.text.tag_configure('Token.Name.Decorator', foreground='#003D99')
        self.text.tag_configure(
            'Token.Name.Variable.Magic', foreground='#003D99')

        self.text.tag_configure('Token.Operator', foreground='#CC7A00')
        self.text.tag_configure('Token.Operator.Word', foreground='#CC7A00')

        self.text.tag_configure(
            'Token.Literal.String.Doc', foreground='#B80000')
        self.text.tag_configure('Token.Comment.Single', foreground='#B80000')

        self.text.tag_configure(
            'Token.Literal.String.Double', foreground='#248F24')
        self.text.tag_configure(
            'Token.Literal.String.Single', foreground='#248F24')

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
            mediator.event.update_lint(text=output)

    def _highlight(self, start_pos, text):
        """テキストをハイライトする."""
        self.text.mark_set('range_start', start_pos)
        for token, content in lex(text, PythonLexer()):
            self.text.mark_set(
                'range_end', 'range_start+{0}c'.format(len(content))
            )
            self.text.tag_add(str(token), 'range_start', 'range_end')
            self.text.mark_set('range_start', 'range_end')

    def line_highlight(self):
        """現在行をハイライトする."""
        # ハイライト開始位置(現在行のはじめ)と、現在行のテキスト取得
        row, col = self.editor.get_line_number()
        start = '{0}.0'.format(row)
        current_line_text = self.editor.get_line_text()
    
        # その行のハイライトを一度解除する
        for tag in self.text.tag_names():
            self.text.tag_remove(tag, start, start+' lineend')

        # ハイライトする
        self._highlight(start, current_line_text)

    def all_highlight(self):
        """全行をハイライトする."""
        # 全てのテキストを取得
        all_text = self.editor.get_src()

        # 全てのハイライトを一度解除する
        for tag in self.text.tag_names():
            self.text.tag_remove(tag, '1.0', 'end')

        # ハイライトする
        self._highlight('1.0', all_text)


def get_code_style(editor_frame, path=None):
    """エディタのスタイルオブジェクトを返す."""
    if path is None:
        return BaseCodeStyle(editor_frame)
    else:
        _, extension = os.path.splitext(path)
        if extension == '.py':
            return PythonCodeStyle(editor_frame)
        else:
            return BaseCodeStyle(editor_frame)

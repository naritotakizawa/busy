"""Pythonコードのスタイル."""
from pygments import lex
from pygments.lexers import PythonLexer

from busy import mediator
from busy.codestyles import BaseCodeStyle
from busy.utils import run_flake8


class PythonCodeStyle(BaseCodeStyle):
    """Pythonのエディタスタイル."""

    one_indent = ' ' * 4  # 半角スペース4つ
    next_is_indent = ['(', '{', '[', ':']  # これらの後にエンターを押すと、次行はインデント一つたされる

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.create_text_tag()

    def create_text_tag(self):
        """タグの定義."""
        # 黄色く表示する
        self.text.tag_configure(
            'Token.Keyword', foreground='#CC7A00'
        )  # def class if for else return pass with try except finally print
        self.text.tag_configure(
            'Token.Keyword.Namespace', foreground='#CC7A00')  # from import
        self.text.tag_configure(
            'Token.Name.Decorator', foreground='#CC7A00')  # @deco
        self.text.tag_configure(
            'Token.Operator.Word', foreground='#CC7A00')  # and, in

        # 青く表示する
        self.text.tag_configure(
            'Token.Name.Namespace', foreground='#003D99'
        )  # import a のa
        self.text.tag_configure(
            'Token.Name.Class', foreground='#003D99')  # クラス名
        self.text.tag_configure(
            'Token.Name.Exception', foreground='#003D99')  # エラー名
        self.text.tag_configure(
            'Token.Name.Function', foreground='#003D99')  # 関数名
        self.text.tag_configure(
            'Token.Name.Function.Magic', foreground='#003D99')  # __init__
        self.text.tag_configure(
            'Token.Name.Builtin', foreground='#003D99'
        )  # len range input enumerate dir
        self.text.tag_configure(
            'Token.Name.Builtin.Pseudo', foreground='#003D99')  # self cls

        # 緑表示する
        self.text.tag_configure(
            'Token.Literal.String.Doc', foreground='#248F24'  # """docstring"""
        )
        self.text.tag_configure(
            'Token.Literal.String.Double', foreground='#248F24')  # "文字"
        self.text.tag_configure(
            'Token.Literal.String.Single', foreground='#248F24')  # '文字'

        # 赤表示する
        self.text.tag_configure(
            'Token.Comment.Single', foreground='#dc143c')  # #コメント
        self.text.tag_configure(
            'Token.Literal.Number.Integer', foreground='#dc143c')  # 1 2 数字
        self.text.tag_configure(
            'Token.Literal.String.Escape', foreground='#dc143c')  # \t \n
        self.text.tag_configure(
            'Token.Operator', foreground='#dc143c')  # . + - / * == =

        # 黒く表示
        self.text.tag_configure(
            'Token.Punctuation', foreground='#000000')  # : [] () {} ,
        self.text.tag_configure(
            'Token.Name', foreground='#000000')  # 変数名など

    def lint(self):
        """スタイルガイドのチェックを行う."""
        if self.editor.path:
            output = run_flake8(self.editor.path)
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

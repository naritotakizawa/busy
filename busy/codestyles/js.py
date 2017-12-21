"""HTMLコードのスタイル."""
from pygments import lex
from pygments.lexers.javascript import JavascriptLexer

from busy.codestyles import BaseCodeStyle


class JSCodeStyle(BaseCodeStyle):
    """JavaScriptのエディタスタイル."""

    one_indent = ' ' * 2  # 半角スペース2つ
    next_is_indent = ['{']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.create_text_tag()

    def create_text_tag(self):
        """タグの定義."""
        # 青く表示する
        self.text.tag_configure(
            'Token.Keyword.Declaration', foreground='#003D99')  # function
        self.text.tag_configure(
            'Token.Operator', foreground='#003D99')  # + - * /

        # 黄色く表示する
        self.text.tag_configure(
            'Token.Name.Other', foreground='#CC7A00')  # 関数名

        # 黒く表示する
        self.text.tag_configure(
            'Token.Punctuation', foreground='#000000')  # {} ()

        # 赤表示する
        self.text.tag_configure(
            'Token.Literal.String.Single', foreground='#dc143c')  # 'aaa'
        self.text.tag_configure(
            'Token.Literal.String.Double', foreground='#dc143c')  # 'aaa'
        self.text.tag_configure(
            'Token.Comment.Single', foreground='#dc143c')  # //comment
        self.text.tag_configure(
            'Token.Literal.Number.Integer', foreground='#dc143c')  # 10

    def _highlight(self, start_pos, text):
        """テキストをハイライトする."""
        self.text.mark_set('range_start', start_pos)
        for token, content in lex(text, JavascriptLexer()):
            print(content, token)
            self.text.mark_set(
                'range_end', 'range_start+{0}c'.format(len(content))
            )
            self.text.tag_add(str(token), 'range_start', 'range_end')
            self.text.mark_set('range_start', 'range_end')

    def line_highlight(self):
        """現在行をハイライトする."""
        # 現在行のテキストを取得
        current_line_text = self.editor.get_line_text()

        start = 'insert linestart'
        end = 'insert lineend'

        # その行のハイライトを一度解除する
        for tag in self.text.tag_names():
            self.text.tag_remove(tag, start, end)

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

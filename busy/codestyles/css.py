"""CSSコードのスタイル."""
from pygments import lex
from pygments.lexers.css import CssLexer

from busy.codestyles import BaseCodeStyle


class CSSCodeStyle(BaseCodeStyle):
    """CSSのエディタスタイル."""

    one_indent = ' ' * 2  # 半角スペース2つ
    next_is_indent = ['{']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.create_text_tag()

    def create_text_tag(self):
        """タグの定義."""
        # 黄色く表示する
        self.text.tag_configure(
            'Token.Name.Tag', foreground='#CC7A00')  # html body p
        self.text.tag_configure(
            'Token.Name.Namespace', foreground='#CC7A00')  # id名
        self.text.tag_configure(
            'Token.Name.Class', foreground='#CC7A00')  # クラス名

        # 青く表示する
        self.text.tag_configure(
            'Token.Punctuation', foreground='#003D99')  # {} ; . : 

        # 緑表示する
        self.text.tag_configure(
            'Token.Keyword', foreground='#248F24')  # margin padding

        # 赤表示する
        self.text.tag_configure(
            'Token.Literal.Number.Integer', foreground='#dc143c')  # 10

        # 黒く表示
        self.text.tag_configure(
            'Token.Keyword.Type', foreground='#000000')  # px

    def _highlight(self, start_pos, text):
        """テキストをハイライトする."""
        self.text.mark_set('range_start', start_pos)
        for token, content in lex(text, CssLexer()):
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

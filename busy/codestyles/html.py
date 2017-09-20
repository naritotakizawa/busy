"""HTMLコードのスタイル."""
from pygments import lex
from pygments.lexers.html import HtmlLexer

from busy.codestyles import BaseCodeStyle


class HTMLCodeStyle(BaseCodeStyle):
    """HTMLのエディタスタイル."""

    one_indent = ' ' * 2  # 半角スペース2つ
    next_is_indent = []  # 次行でインデント強制させる文字はなし

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.create_text_tag()

    def create_text_tag(self):
        """タグの定義."""
        # 黄色く表示する
        self.text.tag_configure(
            'Token.Name.Tag', foreground='#CC7A00')  # html body p

        # 青く表示する
        self.text.tag_configure(
            'Token.Punctuation', foreground='#003D99')  # < >

        # 緑表示する
        self.text.tag_configure(
            'Token.Name.Attribute', foreground='#248F24')  # lang value href

        # 赤表示する
        self.text.tag_configure(
            'Token.Comment', foreground='#dc143c')  # <!-- -->
        self.text.tag_configure(
            'Token.Literal.String', foreground='#dc143c')  # "en"

        # 黒く表示
        self.text.tag_configure(
            'Operator', foreground='#000000')  # =
        self.text.tag_configure(
            'Token.Comment.Preproc', foreground='#000000')  # <!DOCTYPE html>

    def _highlight(self, start_pos, text):
        """テキストをハイライトする."""
        self.text.mark_set('range_start', start_pos)
        for token, content in lex(text, HtmlLexer()):
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

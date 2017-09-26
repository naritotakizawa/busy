"""Pythonコードのスタイル."""
import tkinter as tk

from pygments import lex
from pygments.lexers import PythonLexer

from busy import mediator
from busy.codestyles import BaseCodeStyle
from busy.utils import run_flake8


# 組み込みの関数や例外の名前リスト
import __main__
builtins = __main__.__builtins__
BUILTIN_KEYWORD = [x for x in dir(builtins) if not x.startswith('__')]


class PythonCodeStyle(BaseCodeStyle):
    """Pythonのエディタスタイル."""

    one_indent = ' ' * 4  # 半角スペース4つ
    next_is_indent = ['(', '{', '[', ':']  # これらの後にエンターを押すと、次行はインデント一つたされる

    def __init__(self, *args, **kwargs):
        """初期化."""
        super().__init__(*args, **kwargs)
        self.var_name_list = set()
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

    def tab(self):
        """タブを押した際の処理."""
        first, last = self.editor.get_selection_indices()
        # 範囲選択時は、インデント処理
        if first and last:
            return self.indent()
        else:
            # カーソル位置の前がタブ、スペース、空文字、改行ならばインデント処理
            before_insert_text = self.text.get('insert-1c', 'insert')
            if before_insert_text in (' ', '\t', '\n', ''):
                return self.indent()
            else:
                return self.auto_complete()

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
            # import名、関数名、クラス名は補完リストに使うので保存しておく
            if str(token) in ('Token.Name.Namespace', 'Token.Name.Class', 'Token.Name.Function'):
                self.var_name_list.add(content)

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

        # 全ての候補リストを初期化
        self.var_name_list = set()

        # ハイライトする
        self._highlight('1.0', all_text)

    def auto_complete(self):
        """コード補完."""
        auto_complete_list = tk.Listbox(self.text)

        # エンターでそのキーワードを選択
        auto_complete_list.bind('<Return>', self.selection)

        # エスケープ、タブ、他の場所をクリックで補完リスト削除
        auto_complete_list.bind('<Escape>', self.remove_list)
        auto_complete_list.bind('<Tab>', self.remove_list)
        auto_complete_list.bind('<FocusOut>', self.remove_list)

        # (x,y,width,height,baseline)
        x, y, _, height, _ = self.text.dlineinfo(
            'insert')
        # 現在のカーソル位置のすぐ下に補完リストを貼る
        auto_complete_list.place(x=x, y=y+height)

        # 補完リストの候補を作成
        for word in self.get_keywords():
            auto_complete_list.insert(tk.END, word)

        # 補完リストをフォーカスし、0番目を選択している状態に
        auto_complete_list.focus_set()
        auto_complete_list.selection_set(0)
        self.auto_complete_list = auto_complete_list  # self.でアクセスできるように
        return 'break'

    def selection(self, event=None):
        """コード補完リストでの選択後の処理."""
        # リストの選択位置を取得
        select_index = self.auto_complete_list.curselection()
        if select_index:
            # リストの表示名を取得
            value = self.auto_complete_list.get(select_index)

            # 現在入力中の単語位置の取得
            _, start, end = self.editor.get_current_insert_word()
            self.text.delete(start, end)
            self.text.insert('insert', value)
            self.remove_list()

    def remove_list(self, event=None):
        """コード補完リストの削除処理."""
        self.auto_complete_list.destroy()
        self.text.focus()

    def get_keywords(self):
        """コード補完リストの候補キーワードを作成する."""
        # 現在入力中の単語を取得
        text, _, _ = self.editor.get_current_insert_word()
        # 自作のクラス名や関数名+組み込みの関数、例外クラス
        keywords = list(self.var_name_list) + BUILTIN_KEYWORD
        return [x for x in keywords if x.startswith(text) or x.startswith(text.title())]

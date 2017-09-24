import tkinter as tk
import tkinter.ttk as ttk
from busy.codestyles import get_code_style
from busy.frames import SearchBox, ReplaceBox


class CustomText(tk.Text):
    """Textの、イベントを拡張したウィジェット."""

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.tk.eval('''
            proc widget_proxy {widget widget_command args} {

                # call the real tk widget command with the real args
                set result [uplevel [linsert $args 0 $widget_command]]

                # generate the event for certain types of commands
                if {([lrange $args 0 1] == {xview moveto}) ||
                    ([lrange $args 0 1] == {xview scroll}) ||
                    ([lrange $args 0 1] == {yview moveto}) ||
                    ([lrange $args 0 1] == {yview scroll})} {

                    event generate  $widget <<Scroll>> -when tail
                }

                if {([lindex $args 0] in {insert replace delete})} {

                    event generate  $widget <<Change>> -when tail
                }

                # return the result from the real widget command
                return $result
            }
            ''')
        self.tk.eval('''
            rename {widget} _{widget}
            interp alias {{}} ::{widget} {{}} widget_proxy {widget} _{widget}
        '''.format(widget=str(self)))


class EditorFrame(ttk.Frame):
    """エディタ部分のウィジェット."""

    def __init__(self, master, path=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.create_widgets()
        self.create_event()
        self.path = path

    @property
    def path(self):
        """属性pathのゲッター。セッターを使うので利用."""
        return self._path

    @path.setter
    def path(self, opening_file_path):
        """属性pathのセッター.

        ファイルパスから、適切なエディタのスタイルオブジェクトを取得する

        """
        self._path = opening_file_path
        self.code_style = get_code_style(self, opening_file_path)

    def create_widgets(self):
        # 入力欄、行番号欄、スクロール部分を作成
        self.text = CustomText(self, font=('Helvetica', 14))
        self.linenumbers = tk.Canvas(self, width=40)
        self.vsb = ttk.Scrollbar(
            self, orient=tk.VERTICAL, command=self.text.yview)

        # 入力欄にスクロールを紐付け
        self.text.configure(yscrollcommand=self.vsb.set)

        # 左から行番号、入力欄、スクロールウィジェット
        self.linenumbers.grid(row=0, column=0, sticky=(tk.N, tk.S))
        self.text.grid(row=0, column=1, sticky=(tk.N, tk.S, tk.W, tk.E))
        self.vsb.grid(row=0, column=2, sticky=(tk.N, tk.S))

        # 縦と、コード入力欄のみ拡大されるように
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        # 内容に応じて勝手に大きくなるのを防ぐ
        self.grid_propagate(False)

    def create_event(self):
        """イベントの設定."""
        # テキスト内でのスクロール時
        self.text.bind('<<Scroll>>', self.update_line_number)

        # テキストの変更時
        self.text.bind('<<Change>>', self.line_highlight)
        self.text.bind('<<Change>>', self.update_line_number, '+')

        self.text.bind('<Tab>', self.indent)  # Tab押下時(インデント)
        self.text.bind('<Control-Key-bracketright>', self.indent)  # Ctrl+]押下時(インデント)
        self.text.bind('<Control-Key-bracketleft>', self.dedent)  # Ctrl+[押下時(逆インデント)

        # エンター押下時
        self.text.bind('<Return>', self.enter_indent)

        # バックスペース押下時
        self.text.bind('<BackSpace>', self.back_space)

        # Ctrl+A押下時(全選択)
        self.text.bind('<Control-a>', self.select_all)

        # Ctrl+L押下時、全行ハイライト
        self.text.bind("<Control-l>", self.all_highlight)

        # ウィジェットのサイズが変わった際。行番号の描画を行う
        self.text.bind('<Configure>', self.update_line_number)

        # Ctrl+Fで検索ボックス
        self.text.bind('<Control-f>', self.create_search_box)

        # Ctrl+Fで検索ボックス
        self.text.bind('<Control-h>', self.create_replace_box)

    def update_line_number(self, event=None):
        """行番号の描画."""
        # 現在の行番号を全て消す
        self.linenumbers.delete(tk.ALL)

        # 今見えている範囲での、0番目0列がエディタ内の何行目かを取得
        first_row = self.text.index('@0,0')
        first_row_number = int(first_row.split('.')[0])

        # エディタの最終行
        last_row = self.text.index('end')
        last_row_number = int(last_row.split('.')[0])

        for row_number in range(first_row_number, last_row_number):
            # 各行の座標等のデータを取得
            # (3, 705, 197, 13, 18) のように帰る(x,y,width,height,baseline)
            dline = self.text.dlineinfo('{0}.0'.format(row_number))

            # 下にスクロールしたあと、上にスクロールした場合なんかはdlineがNoneの可能性あり
            # dlineinfoは、あくまでText内の「見えている範囲」で判断する
            # なので、本来100行あるText内で上にスクロールし、80行目以降が非表示なんかになると
            # dlineinfo('80.0')以降はNoneを返してきます
            # 行番号は見えている範囲だけ表示されればいいので、適切にbreakすれば問題ナッシング
            if dline is None:
                break
            else:
                y = dline[1]  # y座標を取得

            # (x座標, y座標, 方向, 表示テキスト)を渡して行番号のテキストを作成
            self.linenumbers.create_text(
                3, y, anchor=tk.NW, text=row_number, font=('Helvetica', 14))

    def get_src(self):
        """エディタの内容を返す."""
        return self.text.get('1.0', 'end-1c')

    def get_line_text(self):
        """現在の行のテキストを返す."""
        return self.text.get('insert linestart', 'insert lineend')

    def get_line_text_before_cursor(self):
        """カーソルまでの現在の行のテキストを返す."""
        return self.text.get('insert linestart', 'insert')

    def get_line_number(self):
        """現在の行番号、列番号を整数で返す."""
        pos = self.text.index('insert')
        row, col = [int(x) for x in pos.split('.')]
        return row, col

    def get_selection_indices(self):
        """選択部分の始まりと終わりの行番号を返す."""
        try:
            # 7.5 10.5 のように取得される
            first = self.text.index('sel.first')
            last = self.text.index('sel.last')
            # 7と10の部分を抜き出す
            first_row_number = int(first.split('.')[0])
            last_row_number = int(last.split('.')[0])
            return first_row_number, last_row_number
        except tk.TclError:
            return None, None

    def select_all(self, event=None):
        """テキストを全て選択する."""
        self.text.tag_add('sel', '1.0', 'end')
        return 'break'

    def create_search_box(self, event):
        """テキスト検索ボックスの作成."""
        window = tk.Toplevel(self)
        window.title('Search')
        box = SearchBox(window, self.text)
        box.pack()
        return 'break'

    def create_replace_box(self, event):
        """テキスト置換ボックスの作成."""
        window = tk.Toplevel(self)
        window.title('Replace')
        box = ReplaceBox(window, self.text)
        box.pack()
        return 'break'

    def lint(self):
        """コードのスタイルガイドチェック."""
        return self.code_style.lint()

    def indent(self, event=None):
        """タブキー押下時(インデント)."""
        return self.code_style.indent()

    def dedent(self, event=None):
        """Ctrl+B 逆インデント."""
        return self.code_style.dedent()

    def line_highlight(self, event=None):
        """現在行をハイライトする."""
        return self.code_style.line_highlight()

    def all_highlight(self, event=None):
        """全行をハイライトする."""
        return self.code_style.all_highlight()

    def enter_indent(self, event=None):
        """エンター時のインデントを調節する."""
        return self.code_style.enter_indent()

    def back_space(self, event=None):
        """バックスペース時に、インデントがあれば上手く消す."""
        return self.code_style.back_space()


if __name__ == '__main__':
    root = tk.Tk()
    app = EditorFrame(root)
    app.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))
    root.columnconfigure(0, weight=1, minsize=100)
    root.rowconfigure(0, weight=1, minsize=100)
    root.mainloop()

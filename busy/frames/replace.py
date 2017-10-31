"""tk.Textの置換機能を提供するモジュール"""
import tkinter as tk
import tkinter.ttk as ttk


class ReplaceBox(ttk.Frame):
    """テキスト置換ボックス."""

    def __init__(self, master, text_widget, *args, **kwargs):
        """初期化

        text_widget引数に、tk.Textウィジェットを渡してください

        """
        super().__init__(master, *args, **kwargs)
        self.target_text = text_widget  # 置換する対象となるTextウィジェット
        self.create_widgets()
        self.from_text.focus()  # 入力欄にフォーカスしとく

    def create_widgets(self):
        """ウィジェットの作成."""
        # 置換前文字列入力欄
        self.from_text_var = tk.StringVar()
        self.from_text = ttk.Entry(self, textvariable=self.from_text_var)

        # 置換後文字列入力欄
        self.to_text_var = tk.StringVar()
        self.to_text = ttk.Entry(self, textvariable=self.to_text_var)

        # 置換実行ボタン
        self.button = ttk.Button(self, text='replace')
        self.button.bind('<Button-1>', self.replace)

        ttk.Label(self, text='from').grid(
            row=0, column=0, sticky=(tk.N, tk.S, tk.W, tk.E))
        self.from_text.grid(row=0, column=1, sticky=(tk.N, tk.S, tk.W, tk.E))
        ttk.Label(self, text='to').grid(
            row=1, column=0, sticky=(tk.N, tk.S, tk.W, tk.E))
        self.to_text.grid(row=1, column=1, sticky=(tk.N, tk.S, tk.W, tk.E))
        self.button.grid(row=2, column=2, sticky=(tk.N, tk.S, tk.W, tk.E))

    def replace(self, event=None):
        """文字の一括置換を行う."""
        # 現在選択中の部分を解除
        self.target_text.tag_remove('sel', '1.0', 'end')

        from_text = self.from_text_var.get()
        to_text = self.to_text_var.get()

        start_index = '1.0'
        while True:
            pos = self.target_text.search(
                from_text, start_index, stopindex='end')
            if not pos:  # 検索文字がもう見つからなければbreak
                break

            # 見つかった位置の置換前文字列を削除
            from_text_end = '{0} + {1}c'.format(pos, len(from_text))
            self.target_text.delete(pos, from_text_end)

            # その位置に置換後文字を挿入
            self.target_text.insert(pos, to_text)

            # その位置を選択状態にして、わかりやすく
            to_text_end = '{0} + {1}c'.format(pos, len(to_text))
            self.target_text.tag_add('sel', pos, to_text_end)
            start_index = to_text_end  # 最後から+置換後文字数を起点に、再検索


def create_replace_box(text_widget, title='Replace Box'):
    """置換ボックスを作成する関数

    args:
        text_widget: tk.Textウィジェット
        title: 置換ボックスのタイトル

    """
    window = tk.Toplevel()
    window.title(title)
    box = ReplaceBox(window, text_widget)
    box.pack()


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Replace Test')
    text = tk.Text(root)
    text.pack()
    root.bind(
        '<Control-h>',
        lambda event: create_replace_box(text_widget=text),
    )
    root.mainloop()

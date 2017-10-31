"""テキスト検索ボックスを提供するモジュール

create_search_box関数に、tk.Textウィジェットを渡せば利用できます。

"""
import tkinter as tk
import tkinter.ttk as ttk


class SearchBox(ttk.Frame):
    """テキスト検索ボックス."""

    def __init__(self, master, text_widget, *args, **kwargs):
        """初期化

        text_widget引数に、tk.Textウィジェットを渡してください
        """
        super().__init__(master, *args, **kwargs)
        self.target_text = text_widget  # 検索する対象となるTextウィジェット
        self.create_widgets()
        self.last_text = ''
        self.all_pos = []
        self.next_pos_index = 0
        self.text.focus()  # 入力欄にフォーカスしとく

    def create_widgets(self):
        """ウィジェットの作成."""
        # 検索文字の入力欄と、紐付けるStringVar
        self.text_var = tk.StringVar()
        self.text = ttk.Entry(self, textvariable=self.text_var)
        self.text.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.W, tk.E))

        # エンターキーで検索実行される
        self.text.bind('<Return>', self.search)

    def search_start(self, text):
        """検索の初回処理."""
        # 各変数の初期化
        self.next_pos_index = 0
        self.all_pos = []

        # はじめは1.0から検索し、見つかれば、それの最後+1文字の時点から再検索
        # all_posには、['1.7', '3,1', '5.1'...]のような検索文字が見つかった地点の最初のインデックスが入っていく
        start_index = '1.0'
        while True:
            pos = self.target_text.search(text, start_index, stopindex='end')
            if not pos:  # 検索文字がもう見つからければbreak
                break
            self.all_pos.append(pos)
            start_index = '{0} + 1c'.format(pos)  # 最後から+1文字を起点に、再検索

        # 最初のマッチ部分、all_pos[0]を選択させておく
        self.search_next(text)

    def search_next(self, text):
        """検索の続きの処理."""
        try:
            # 今回のマッチ部分の取得を試みる
            pos = self.all_pos[self.next_pos_index]
        except IndexError:
            # all_posが空でなくIndexErrorならば、全てのマッチを見た、ということ
            # なのでnext_post_indexを0にし、最初からまたマッチを見せる
            if self.all_pos:
                self.next_pos_index = 0
                self.search_next(text)
        else:
            # 次のマッチ部分を取得できればここ
            start = pos
            end = '{0} + {1}c'.format(pos, len(text))

            # マッチ部分〜マッチ部分+文字数分 の範囲を選択する
            self.target_text.tag_add('sel', start, end)

            # インサートカーソルをマッチした部分に入れ、スクロールもしておく
            self.target_text.mark_set('insert', start)
            self.target_text.see('insert')

            # 次回取得分のために+1
            self.next_pos_index += 1

    def search(self, event=None):
        """文字の検索を行う."""
        # 現在選択中の部分を解除
        self.target_text.tag_remove('sel', '1.0', 'end')

        # 現在検索ボックスに入力されてる文字
        now_text = self.text_var.get()

        if not now_text:
            # 空欄だったら処理しない
            pass
        elif now_text != self.last_text:
            # 前回の入力と違う文字なら、検索を最初から行う
            self.search_start(now_text)
        else:
            # 前回の入力と同じなら、検索の続きを行う
            self.search_next(now_text)

        # 今回の入力を、「前回入力文字」にする
        self.last_text = now_text


def create_search_box(text_widget, title='Search Box'):
    """検索ボックスを作成する関数

    args:
        text_widget: tk.Textウィジェット
        title: 検索ボックスのタイトル

    """
    window = tk.Toplevel()
    window.title(title)
    box = SearchBox(window, text_widget)
    box.pack()


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Search Test')
    text = tk.Text(root)
    text.pack()
    root.bind(
        '<Control-f>',
        lambda event: create_search_box(text_widget=text),
    )
    root.mainloop()

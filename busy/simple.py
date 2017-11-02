"""Busy-Simpleエディタの実行用モジュール."""
import tkinter as tk
import tkinter.ttk as ttk

from busy import mediator
from busy.frames import EditorNoteBook


class BusySimple(ttk.Frame):
    """busy-simple 時のシンプルエディタ用フレーム"""

    def __init__(self, master=None):
        super().__init__(master)
        self.create_widgets()
        self.create_mediator()
        self.create_global_shortcuts()

    def create_widgets(self):
        """ウィジェットの作成、配置."""
        self.note_frame = EditorNoteBook(self)
        self.note_frame.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

    def create_mediator(self):
        """イベント仲介オブジェクトの作成."""
        mediator.set_mediator(
            self, self.note_frame,
            default_mediator_cls=mediator.SimpleMediator
        )

    def create_global_shortcuts(self):
        """ショートカットキーの作成.

        ここにはウィジェットがアクティブ状態じゃなくても実行したいイベントのショートカットを登録してください。
        つまり、いちいちツリーのどこかをクリックしないとF4でルートディレクトリが変更できないのは不便なので、
        そういった場合はここに書いています。

        ウィジェットがアクティブ状態じゃないと使わせたくないイベントは、各フレームで定義しています。
        特にエディタの機能はアクティブ状態じゃないと使うのは戸惑うので、editor.pyで定義しています。
        """
        self.master.bind('<Control-KeyPress-s>', mediator.event.save_file)
        self.master.bind('<Control-KeyPress-d>', mediator.event.delete_tab)
        self.master.bind('<Control-KeyPress-n>', mediator.event.new_file)
        self.master.bind('<Control-KeyPress-o>', mediator.event.open_file)


def main():
    root = tk.Tk()
    root.title('Busy Simple Editor')
    app = BusySimple(root)
    app.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    mediator.event.new_file()  # タブを一つ追加
    root.mainloop()


if __name__ == '__main__':
    main()

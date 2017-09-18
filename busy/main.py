"""Busyエディタの実行用モジュール."""
import tkinter as tk
import tkinter.ttk as ttk

from busy import mediator
from busy.frames import PathTreeFrame, InfoFrame, EditorNoteBook, EditorMenu


class Busy(ttk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.create_widgets()
        self.create_mediator()
        self.create_global_shortcuts()

    def create_widgets(self):
        """ウィジェットの作成、配置."""
        self.path_frame = PathTreeFrame(self)
        self.note_frame = EditorNoteBook(self)
        self.info_frame = InfoFrame(self)

        self.path_frame.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.note_frame.grid(row=0, column=1, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.info_frame.grid(
            row=1, column=0, columnspan=2, sticky=(tk.N, tk.S, tk.E, tk.W))

        self.path_frame.grid_propagate(False)
        self.note_frame.grid_propagate(False)
        self.info_frame.grid_propagate(False)

        self.columnconfigure(0, weight=1, minsize=100)
        self.columnconfigure(1, weight=3, minsize=100)
        self.rowconfigure(0, weight=3, minsize=100)
        self.rowconfigure(1, weight=1, minsize=100)

    def create_mediator(self):
        """イベント仲介オブジェクトの作成."""
        mediator.set_mediator(
            self, self.info_frame, self.path_frame, self.note_frame
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
        self.master.bind('<F4>', mediator.event.change_dir)
        self.master.bind('<F5>', mediator.event.update_dir)


def main():
    root = tk.Tk()
    root.title('Busy Editor')
    app = Busy(root)
    root['menu'] = EditorMenu()  # メニューの登録
    app.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    root.mainloop()


if __name__ == '__main__':
    main()

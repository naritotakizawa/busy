import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from busy import mediator
from busy.frames import EditorFrame


class EditorNoteBook(ttk.Notebook):
    """エディタを管理するのNoteBookウィジェット."""

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.editor_list = []

    def add_tab(self, event=None, path=None):
        """新しいタブを追加する."""
        # エディタの作成
        editor = EditorFrame(self, path)

        # パスの指定がなければ、new file という名前がタブに入る
        if path is None:
            name = 'new file'

        # パスの指定があれば、エディタにそのファイルの内容を読み込み、ファイル名をタブに
        else:
            name = os.path.basename(path)
            with open(path, 'r', encoding='utf-8') as file:
                editor.text.insert(tk.INSERT, file.read())
                editor.all_highlight()

        # NoteBookにエディタを追加
        self.add(editor, text=name)

        # エディタの参照を保持するため、リストに格納
        self.editor_list.append(editor)

        # 今開いたタブを選択する
        now_open_tab = self.tabs()[-1]
        self.select(now_open_tab)

    def save_file(self, event=None, initial_dir=os.curdir):
        """開いているエディタの内容を保存する."""
        # そもそもタブを開いてなければ処理しない
        if not self.tabs():
            return 'break'
        # 現在開いているエディタと、中身を取得
        current_editor, _ = self.get_current_editor()
        src = current_editor.get_src()

        # 新規ファイルだった場合は、ファイル名を指定させて保存
        if current_editor.path is None:
            file = filedialog.asksaveasfile(mode='w', initialdir=initial_dir)
            if file:
                file.write(src)
                current_editor.path = file.name
                # タブの表示名を変更
                self.tab(current_editor, text=os.path.basename(file.name))
        # 更新
        else:
            with open(current_editor.path, 'w') as file:
                file.write(src)

        # セーブ後にコードのチェック
        current_editor.lint()

        # 保存したと表示する
        if current_editor.path:
            mediator.event.add_history(
                text='save {0}'.format(current_editor.path)
            )

    def delete_tab(self, event=None):
        """選択中のタブを削除する."""
        # そもそもタブを開いてなければ処理しない
        if not self.tabs():
            return 'break'
        current_editor_id, index = self.get_current_editor()
        self.forget(current_editor_id)
        self.editor_list.pop(index)

    def get_current_editor(self):
        """選択中のタブIDと、indexを返す."""
        # このindexは、self.tabs内でのタブのindexであり
        # self.editor_listのindexでもある
        index = self.index(self.select())
        return self.editor_list[index], index

    def open_file(self, event=None, file_path=None, initial_dir=os.curdir):
        """ファイルを開く."""
        if file_path is None:
            file_path = filedialog.askopenfilename(initialdir=initial_dir)
        if file_path:
            return self.add_tab(path=file_path)


if __name__ == '__main__':
    root = tk.Tk()
    app = EditorNoteBook(root)
    app.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))
    root.bind('<Control-KeyPress-s>', app.save_file)
    root.bind('<Control-KeyPress-d>', app.delete_tab)
    root.bind('<Control-KeyPress-n>', app.add_tab)
    root.bind('<Control-KeyPress-o>', app.open_file)
    app.add_tab()  # 新規ファイルを開いておこう
    root.columnconfigure(0, weight=1, minsize=100)
    root.rowconfigure(0, weight=1, minsize=100)
    root.mainloop()

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

    def add_tab(self, path=None):
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

        # NoteBookにエディタを追加
        self.add(editor, text=name)

        # エディタの参照を保持するため、リストに格納
        self.editor_list.append(editor)

        # 今開いたタブを選択する
        now_open_tab = self.tabs()[-1]
        self.select(now_open_tab)

    def save_file(self, event):
        """開いているエディタの内容を保存する."""
        # 現在開いているエディタと、中身を取得
        current_editor, index = self.get_current_editor()
        src = current_editor.get_src()

        # 新規ファイルだった場合は、ファイル名を指定させて保存
        if current_editor.path is None:
            file = filedialog.asksaveasfile(mode='w')
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

    def delete_tab(self, event):
        """選択中のタブを削除する."""
        current_editor_id, index = self.get_current_editor()
        self.forget(current_editor_id)
        self.editor_list.pop(index)

    def get_current_editor(self):
        """選択中のタブIDと、indexを返す."""
        # このindexは、self.tabs内でのタブのindexであり
        # self.editor_listのindexでもある
        index = self.index(self.select())
        return self.editor_list[index], index


if __name__ == '__main__':
    root = tk.Tk()
    app = EditorNoteBook(root)
    app.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))
    root.bind('<Control-KeyPress-s>', mediator.event.save_file)
    root.bind('<Control-KeyPress-d>', mediator.event.delete_tab)
    root.bind('<Control-KeyPress-n>', mediator.event.new_file)
    root.bind('<Control-KeyPress-o>', mediator.event.open_file)
    root.columnconfigure(0, weight=1, minsize=100)
    root.rowconfigure(0, weight=1, minsize=100)
    root.mainloop()

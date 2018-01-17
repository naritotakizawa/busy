import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog, messagebox
from busy.frames import EditorFrame


class EditorNoteBook(ttk.Notebook):
    """エディタを管理するのNoteBookウィジェット."""

    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

    def add_tab(self, event=None, path=None):
        """新しいタブを追加する."""

        # エディタの作成
        editor = EditorFrame(self, path)

        # パスの指定がなければ、new file という名前がタブに入る
        if path is None:
            name = 'new file'
            # ファイルから読み込んだ際、初回insertでonchangeが走るので
            # それと合わせるためにカウントを+1
            editor.change_count += 1

        # パスの指定があれば
        else:
            # ファイルの内容を読み込み、ファイル名をタブに
            name = os.path.basename(path)
            with open(path, 'r', encoding='utf-8') as file:
                editor.text.insert('1.0', file.read())
                editor.all_highlight()

        # NoteBookにエディタを追加
        self.add(editor, text=name)

        # 今開いたタブを選択する
        now_open_tab = self.tabs()[-1]
        self.select(now_open_tab)
        return 'break'

    def save_file(self, event=None, initial_dir=os.curdir):
        """開いているエディタの内容を保存する."""
        # そもそもタブを開いてなければ処理しない
        if not self.tabs():
            return 'break'
        # 現在開いているエディタと、中身を取得
        current_editor = self.get_current_editor()
        src = current_editor.get_src()

        # 新規ファイルだった場合は、ファイル名を指定させて保存
        if current_editor.path is None:
            file_name = filedialog.asksaveasfilename(initialdir=initial_dir)
            if file_name:
                with open(file_name, 'w', encoding='utf-8') as file:
                    file.write(src)

                current_editor.path = file.name
                # タブの表示名を変更
                self.tab(current_editor, text=os.path.basename(file.name))
        # 更新
        else:
            with open(current_editor.path, 'w', encoding='utf-8') as file:
                file.write(src)

        # セーブ後にコードのチェック、全てハイライト、変更フラグをFalse、タブ名の*を消去
        current_editor.lint()
        current_editor.all_highlight()
        current_editor.changed = False
        self.reset_tab_name()

    def save_as(self, event=None, initial_dir=os.curdir):
        """開いているエディタの内容を保存する."""
        # そもそもタブを開いてなければ処理しない
        if not self.tabs():
            return 'break'
        # 現在開いているエディタと、中身を取得
        current_editor = self.get_current_editor()
        src = current_editor.get_src()

        # 保存するファイル名を取得し、基のソースで書き込む
        file_name = filedialog.asksaveasfilename(initialdir=initial_dir)
        if file_name:
            with open(file_name, 'w', encoding='utf-8') as file:
                file.write(src)

        # セーブ後にコードのチェック、全てハイライト、変更フラグをFalse、タブ名の*を消去
        current_editor.lint()
        current_editor.all_highlight()
        current_editor.changed = False
        self.reset_tab_name()

    def _delete_tab(self):
        """タブを削除"""
        current = self.select()
        self.forget(current)

    def delete_tab(self, event=None):
        """選択中のタブを削除する."""
        # そもそもタブを開いてなければ処理しない
        if not self.tabs():
            return 'break'
        current_editor = self.get_current_editor()
        # 変更済みで、保存していないよの確認で「No」だと何もしない
        if current_editor.changed:
            if messagebox.askyesno(message='保存していませんが、よろしいですか'):
                self._delete_tab()
        else:
            self._delete_tab()

    def get_current_editor(self):
        """選択中のエディタを返す"""
        current_widget_name = self.select().split('.')[-1]
        text_widget = self.children[current_widget_name]
        return text_widget

    def open_file(self, event=None, file_path=None, initial_dir=os.curdir):
        """ファイルを開く."""
        if file_path is None:
            file_path = filedialog.askopenfilename(initialdir=initial_dir)

        if file_path:
            # そのパスで既に開いたタブがあるかを確認
            for tab in self.tabs():
                widget_name = tab.split('.')[-1]
                editor = self.children[widget_name]
                if editor.path == file_path:
                    self.select(tab)
                    return 'break'

            return self.add_tab(path=file_path)

    def change_tab_name(self, event=None):
        """タブ名に「*」を入れる"""
        current_tab = self.select()
        tab_name = self.tab(current_tab)['text'].replace('*', '')
        self.tab(current_tab, text='*' + tab_name)

    def reset_tab_name(self, event=None):
        """タブ名の*を消す"""
        current_tab = self.select()
        tab_name = self.tab(current_tab)['text'].replace('*', '')
        self.tab(current_tab, text=tab_name)


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Busy Simple')
    app = EditorNoteBook(root)
    app.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))
    root.bind('<Control-KeyPress-s>', app.save_file)
    root.bind('<Control-KeyPress-d>', app.delete_tab)
    root.bind('<Control-KeyPress-n>', app.add_tab)
    root.bind('<Control-KeyPress-o>', app.open_file)
    app.add_tab()  # 新規ファイルを開いておこう
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    root.mainloop()

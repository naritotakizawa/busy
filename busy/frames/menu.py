"""エディタのメニュー部分の機能を提供するモジュール.

root['menu'] = EditorMenu()
のように利用してください。
動作を軽く確認したい場合は、このモジュールを単独で実行してください(python menu.py)

"""
import tkinter as tk

from busy import mediator


class EditorMenu(tk.Menu):

    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.create_file_menu()
        self.create_edit_menu()
        self.create_tree_menu()

    def create_file_menu(self):
        """Fileメニューの作成."""
        menu_file = tk.Menu(self)
        menu_file.add_command(label='New', command=mediator.event.new_file, accelerator='Ctrl+N')
        menu_file.add_command(label='Open', command=mediator.event.open_file, accelerator='Ctrl+O')
        menu_file.add_command(label='Save', command=mediator.event.save_file, accelerator='Ctrl+S')
        menu_file.add_command(label='Delete', command=mediator.event.delete_tab, accelerator='Ctrl+D')
        self.add_cascade(menu=menu_file, label='File')

    def create_edit_menu(self):
        """Editメニューの作成(エディタの機能)."""
        menu_edit = tk.Menu(self)
        menu_edit.add_command(label='Indent', command=mediator.event.indent, accelerator='Ctrl+]')
        menu_edit.add_command(label='Dedent', command=mediator.event.dedent, accelerator='Ctrl+[')
        menu_edit.add_command(label='Select All', command=mediator.event.select_all, accelerator='Ctrl+A')
        menu_edit.add_command(label='HighLight', command=mediator.event.highlight, accelerator='Ctrl+L')
        menu_edit.add_command(label='Search', command=mediator.event.search, accelerator='Ctrl+F')
        menu_edit.add_command(label='Replace', command=mediator.event.replace, accelerator='Ctrl+H')
        self.add_cascade(menu=menu_edit, label='Edit')

    def create_tree_menu(self):
        """Treeメニューの作成(ファイル・ディレクトリ一覧の操作)."""
        menu_tree = tk.Menu(self)
        menu_tree.add_command(label='Change Root', command=mediator.event.change_dir, accelerator='F4')
        menu_tree.add_command(label='Update', command=mediator.event.update_dir, accelerator='F5')
        self.add_cascade(menu=menu_tree, label='Tree')


def main():
    root = tk.Tk()
    root.title('Menu Test')
    root['menu'] = EditorMenu()
    root.mainloop()


if __name__ == '__main__':
    main()

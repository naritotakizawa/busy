import datetime
import tkinter as tk
import tkinter.ttk as ttk


class InfoFrame(ttk.Frame):
    """お知らせなどを表示するFrame."""

    def __init__(self, master=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.create_widgets()

    def create_widgets(self):
        # 左側、履歴
        self.history = tk.Text(self, font=('Helvetica', 14))
        ysb_history = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.history.yview)
        self.history.configure(yscroll=ysb_history.set)

        # 右側、スタイルチェック
        self.lint = tk.Text(self, font=('Helvetica', 14))
        ysb_lint = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.lint.yview)
        self.lint.configure(yscroll=ysb_lint.set)

        self.history.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        ysb_history.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.lint.grid(row=0, column=2, sticky=(tk.N, tk.S, tk.E, tk.W))
        ysb_lint.grid(row=0, column=3, sticky=(tk.N, tk.S))

        self.columnconfigure(0, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)

    def add_history(self, text):
        """履歴にテキストを追加する."""
        now = datetime.datetime.now()
        now_text = '{0.hour}時{0.minute}分{0.second}秒 '.format(now)
        result = now_text + text + '\n'
        self.history.insert(tk.END, result)

    def clear_history(self):
        """履歴欄をクリアする."""
        self.history.delete('1.0', tk.END)
    
    def update_history(self, text):
        """履歴欄を更新する."""
        self.clear_history()
        self.add_history(text)

    def add_lint(self, text):
        """スタイルチェック欄にテキストを追加する."""
        text = text + '\n'
        self.lint.insert(tk.END, text)

    def clear_lint(self):
        """スタイルチェック欄をクリアする."""
        self.lint.delete('1.0', tk.END)
    
    def update_lint(self, text):
        """スタイルチェック欄を更新する."""
        self.clear_lint()
        self.add_lint(text)

def main():
    root = tk.Tk()
    app = InfoFrame(root)
    app.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    root.mainloop()


if __name__ == '__main__':
    main()





import datetime
import tkinter as tk
import tkinter.ttk as ttk


class InfoFrame(ttk.Frame):
    """お知らせなどを表示するFrame."""

    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.create_widgets()

    def create_widgets(self):
        self.lint = tk.Text(self, font=('Helvetica', 14))
        ysb_lint = ttk.Scrollbar(
            self, orient=tk.VERTICAL, command=self.lint.yview)
        self.lint.configure(yscroll=ysb_lint.set)

        self.lint.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        ysb_lint.grid(row=0, column=1, sticky=(tk.N, tk.S))

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

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

from tkinter import filedialog


class BaseMediator:
    """テスト用のイベント仲介オブジェクト.

    例えばnote.pyを直接実行する、等の部品毎のテストをする場合に使ってください。

    """
    def __getattr__(self, name):
        """呼ばれたメソッド名と引数を出力する."""
        def inner(*args, **kwargs):
            print('call', name, args, kwargs)
        return inner


class EventMediator:
    """遠く離れたウィジェット間でのやりとりを仲介するクラス."""

    def __init__(self, main_frame, info_frame, path_frame, note_frame):
        self.main_frame = main_frame
        self.info_frame = info_frame
        self.path_frame = path_frame
        self.note_frame = note_frame

    def save_file(self, event=None):
        """ファイルの保存."""
        self.note_frame.save_file(event)

    def delete_tab(self, event=None):
        """タブの削除."""
        if self.note_frame.tabs():
            self.note_frame.delete_tab(event)

    def new_file(self, event=None):
        """新規ファイルを開く."""
        self.note_frame.add_tab()

    def open_file(self, event=None, file_path=None):
        """ファイルを開く."""
        if file_path is None:
            file_path = filedialog.askopenfilename()
        if file_path:
            self.note_frame.add_tab(file_path)

    def add_history(self, text):
        """履歴にテキストを追加する."""
        self.info_frame.add_history(text)

    def clear_history(self):
        """履歴欄をクリアする."""
        self.info_frame.clear_history()

    def update_history(self, text):
        """履歴欄を更新する."""
        self.info_frame.update_history(text)

    def add_lint(self, text):
        """スタイルチェック欄にテキストを追加する."""
        self.info_frame.add_lint(text)

    def clear_lint(self):
        """スタイルチェック欄をクリアする."""
        self.info_frame.clear_lint()

    def update_lint(self, text):
        """スタイルチェック欄を更新する."""
        self.info_frame.update_lint(text)


event = BaseMediator()


def set_mediator(*widgets):
    MediatorClass = EventMediator  # Todo settings.py等から参照クラスを決めたい
    event = MediatorClass(*widgets)
    globals()['event'] = event

"""各ウィジェットやクラス間でのやり取りを仲介する機能を提供します.

このモジュールを利用することで、
self.mastet.master.display_frame....
のようなわずらわしいコードを失くすことができます。単純なショートカットとしても利用できます。

更にMockMediatorを使うことで、各Frameを単独で実行することも容易にしています。(python note.py等)

"""


class MockMediator:
    """テスト、デバッグ用のイベント仲介クラス.

    set_mediator関数を使わなかった場合(note.py自体を実行した場合等)は、このクラスが使われます。
    これはモックとして動作します。
    本来他ウィジェットと連携する予定の処理が呼ばれてもエラーにならず、その処理が呼ばれたことを出力します。

    """

    def __getattr__(self, name):
        """呼ばれたメソッド名と引数を出力する."""
        def inner(*args, **kwargs):
            print('call', name, args, kwargs)
        return inner


class EventMediator:
    """遠く離れたウィジェット間でのやりとりを仲介するデフォルトのクラス."""

    def __init__(self, main_frame, info_frame, path_frame, note_frame):
        """各フレームの参照を保持する."""
        self.main_frame = main_frame
        self.info_frame = info_frame
        self.path_frame = path_frame
        self.note_frame = note_frame

    def save_file(self, event=None, initial_dir=None):
        """ファイルの保存."""
        if initial_dir is None:
            initial_dir = self.path_frame.root_path
        self.note_frame.save_file(event=event, initial_dir=initial_dir)

    def delete_tab(self, event=None):
        """タブの削除."""
        self.note_frame.delete_tab(event=event)

    def new_file(self, event=None):
        """新規ファイルを開く."""
        self.note_frame.add_tab(event=event)

    def open_file(self, event=None, file_path=None, initial_dir=None):
        """ファイルを開く."""
        if initial_dir is None:
            initial_dir = self.path_frame.root_path
        self.note_frame.open_file(
            event=event, file_path=file_path, initial_dir=initial_dir
        )

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

    def update_dir(self, event=None):
        """ツリーのディレクトリを更新する."""
        self.path_frame.update_dir(event=None)

    def change_dir(self, event=None):
        """ツリーのルートディレクトリを変更する."""
        self.path_frame.change_dir(event=None)


event = MockMediator()


# Todo settings.py等で、具象メディエーターを設定できるようにしたい
def set_mediator(*widgets, default_mediator_cls=EventMediator):
    """メディエーターを設定する."""
    event = default_mediator_cls(*widgets)
    globals()['event'] = event

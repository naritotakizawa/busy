"""各ウィジェットやクラス間でのやり取りを仲介する機能を提供します.

このモジュールを利用することで、
self.mastet.master.display_frame....
のようなわずらわしいコードを失くすことができ、グローバルなショートカットとして利用できます。

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
        return self.note_frame.save_file(event=event, initial_dir=initial_dir)

    def delete_tab(self, event=None):
        """タブの削除."""
        return self.note_frame.delete_tab(event=event)

    def new_file(self, event=None):
        """新規ファイルを開く."""
        return self.note_frame.add_tab(event=event)

    def open_file(self, event=None, file_path=None, initial_dir=None):
        """ファイルを開く."""
        if initial_dir is None:
            initial_dir = self.path_frame.root_path
        return self.note_frame.open_file(
            event=event, file_path=file_path, initial_dir=initial_dir
        )

    def add_lint(self, text):
        """スタイルチェック欄にテキストを追加する."""
        return self.info_frame.add_lint(text)

    def clear_lint(self):
        """スタイルチェック欄をクリアする."""
        return self.info_frame.clear_lint()

    def update_lint(self, text):
        """スタイルチェック欄を更新する."""
        return self.info_frame.update_lint(text)

    def update_dir(self, event=None):
        """ツリーのディレクトリを更新する."""
        return self.path_frame.update_dir(event=event)

    def change_dir(self, event=None):
        """ツリーのルートディレクトリを変更する."""
        return self.path_frame.change_dir(event=event)

    def indent(self, event=None):
        """インデント."""
        # 開いているエディタがなければ処理しない
        if not self.note_frame.tabs():
            return 'break'
        current_editor = self.note_frame.get_current_editor()
        return current_editor.indent(event=event)

    def dedent(self, event=None):
        """逆インデント."""
        # 開いているエディタがなければ処理しない
        if not self.note_frame.tabs():
            return 'break'
        current_editor = self.note_frame.get_current_editor()
        return current_editor.dedent(event=event)

    def highlight(self, event=None):
        """ハイライト."""
        # 開いているエディタがなければ処理しない
        if not self.note_frame.tabs():
            return 'break'
        current_editor = self.note_frame.get_current_editor()
        return current_editor.all_highlight(event=event)

    def select_all(self, event=None):
        """テキスト全選択."""
        # 開いているエディタがなければ処理しない
        if not self.note_frame.tabs():
            return 'break'
        current_editor = self.note_frame.get_current_editor()
        return current_editor.select_all(event=event)

    def search(self, event=None):
        """テキスト検索."""
        # 開いているエディタがなければ処理しない
        if not self.note_frame.tabs():
            return 'break'
        current_editor = self.note_frame.get_current_editor()
        return current_editor.create_search_box(event=event)

    def replace(self, event=None):
        """テキスト置換."""
        # 開いているエディタがなければ処理しない
        if not self.note_frame.tabs():
            return 'break'
        current_editor = self.note_frame.get_current_editor()
        return current_editor.create_replace_box(event=event)

    def change_tab_name(self, event=None):
        """タブ名に*を入れる"""
        return self.note_frame.change_tab_name()


event = MockMediator()


# Todo settings.py等で、具象メディエーターを設定できるようにしたい
def set_mediator(*widgets, default_mediator_cls=EventMediator):
    """メディエーターを設定する."""
    event = default_mediator_cls(*widgets)
    globals()['event'] = event

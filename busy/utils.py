"""便利な機能を集めたモジュール."""
from contextlib import contextmanager
import io
import subprocess
import sys
import traceback

from flake8.api import legacy as flake8

if sys.platform == 'win32':
    encoding = 'cp932'
else:
    encoding = 'utf-8'


def run_cmd(cmd):
    """コマンドを実行する.

    args:
        cmd: 実行コマンドとなる文字列

    return:
        コマンド実行の結果出力
    """
    # stdoutとstderrを一緒に取り出す
    ret = subprocess.run(
        cmd, timeout=15, shell=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        encoding=encoding,
    )
    return ret.stdout


@contextmanager
def stdout_io():
    """一時的にstdoutを変更する."""
    old = sys.stdout
    sys.stdout = io.StringIO()
    yield sys.stdout
    sys.stdout = old


def run_flake8(*path):
    """flake8を実行する.

    flake8を実行する場合は、run_cmdにflake8コマンドを渡すよりも
    こちらのほうが、一般的にパフォーマンスがよくなります

    args:
        path: flake8を実行するためのパス。複数渡せます

    return:
        flake8の結果出力
    """
    output = ''
    with stdout_io() as stdout:
        error = ''
        try:
            style_guide = flake8.get_style_guide()
            style_guide.check_files(path)
        except:
            error = traceback.format_exc()
        finally:
            output = stdout.getvalue() + error
    return output

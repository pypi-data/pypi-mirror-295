import re
import subprocess

from jkl import exceptions
from jkl.models import Pane, Session, Window


class Tmux:
    cmd = "tmux"

    @classmethod
    def _run(cls, *subcmd: str) -> subprocess.CompletedProcess:
        result = subprocess.run([cls.cmd, *subcmd], capture_output=True)
        try:
            result.check_returncode()
        except subprocess.CalledProcessError as e:
            raise exceptions.TmuxRunException.from_called_process_error(
                "got non-zero exit code", e
            )
        return result

    @staticmethod
    def _parse_result(result: subprocess.CompletedProcess) -> str:
        try:
            return result.stdout.decode("utf-8").strip()
        except Exception as e:
            raise exceptions.TmuxParseException from e

    @classmethod
    def run(cls, *subcmd: str) -> str:
        result = cls._run(*subcmd)
        return cls._parse_result(result)

    @classmethod
    def list_sessions(cls) -> list[Session]:
        format = "#{session_id}:#{session_name}:#{session_attached}"
        pattern = r"^(.+):(.+):(\d+)$"

        try:
            sessions_listing = cls.run("list-sessions", "-F", format)
        except exceptions.TmuxRunException as e:
            err_msg = e.stderr.decode("utf-8")
            if "no server running" in err_msg or "error connecting to" in err_msg:
                return []
            raise

        sessions = []
        for line in sessions_listing.split("\n"):
            match = re.fullmatch(pattern, line)
            session = Session(match.group(1), match.group(2), int(match.group(3)))
            session.windows = cls.list_windows(session)
            sessions.append(session)

        return sessions

    @classmethod
    def list_windows(cls, session: Session) -> list[Window]:
        format = "#{window_id}:#{window_active}:#{window_name}"
        pattern = r"^(.+):(\d):(.+)$"

        windows = []
        for line in cls.run("list-windows", "-t", session.id, "-F", format).split("\n"):
            match = re.fullmatch(pattern, line)
            window = Window(
                match.group(1), bool(match.group(2)), match.group(3), session
            )
            window.panes = cls.list_panes(window)
            windows.append(window)

        return windows

    @classmethod
    def list_panes(cls, window: Window) -> list[Pane]:
        format = "#{pane_id}:#{pane_active}:#{pane_title}:#{pane_pid}"
        pattern = r"^(.+):(\d):(.+):(\d+)$"

        panes = []
        for line in cls.run("list-panes", "-t", window.id, "-F", format).split("\n"):
            match = re.fullmatch(pattern, line)
            panes.append(
                Pane(
                    match.group(1),
                    bool(match.group(2)),
                    match.group(3),
                    int(match.group(4)),
                    window,
                )
            )

        return panes

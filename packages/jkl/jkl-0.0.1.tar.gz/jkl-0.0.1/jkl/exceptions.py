import subprocess


class TmuxException(Exception):
    pass


class TmuxRunException(TmuxException, subprocess.CalledProcessError):
    def __init__(self, message: str | bytes, *args, **kwargs):
        self.message = message
        super().__init__(*args, **kwargs)

    def __str__(self):
        return f"{self.message}\nstdout: {self.stdout}\nstderr: {self.stderr}"

    @classmethod
    def from_called_process_error(
        cls, message: str, e: subprocess.CalledProcessError
    ) -> "TmuxRunException":
        return cls(message, e.returncode, e.cmd, e.output, e.stderr)


class TmuxParseException(TmuxException):
    pass

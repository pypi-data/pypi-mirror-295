from __future__ import annotations

import os
import subprocess
import time
from dataclasses import dataclass
from getpass import getpass
from tempfile import NamedTemporaryFile
from typing import Literal, Self, get_args
from uuid import uuid4
from warnings import warn


@dataclass
class Result:
    std_in: str
    return_code: int
    std_out: str
    std_err: str
    env: dict | None = None


@dataclass
class PasswordStrategy:
    ask: bool = False
    env: str = ""


Mode = Literal["-e", "-v"]
VALID_MODES: list[Mode] = list(get_args(Mode))


class Shell:
    def __init__(
        self,
        executable: str = "",
        wait_time: int = 0.01,
        *,
        track_env: bool = False,
        passwd_strat: PasswordStrategy | None = None,
    ) -> None:
        if not executable:
            executable = os.environ.get("SHELL", "/bin/bash")
        self._std_out = NamedTemporaryFile("rb+")
        self._std_err = NamedTemporaryFile("rb+")
        self._proc = subprocess.Popen(
            [executable],
            stdin=subprocess.PIPE,
            stdout=self._std_out,
            stderr=self._std_err,
        )
        self._wait_time = wait_time
        self._track_env = track_env
        if passwd_strat is not None:
            if passwd_strat.ask and not passwd_strat.env:
                self.passwd = getpass("Password: ")
            if passwd_strat.env:
                self.passwd = os.environ.get(passwd_strat.env)

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:  # noqa: ANN001
        self.close()

    def _reset_std_out(self) -> None:
        self._std_out.truncate(0)
        self._std_out.seek(0)

    def _reset_std_err(self) -> None:
        self._std_err.truncate(0)
        self._std_err.seek(0)

    @staticmethod
    def _combine_results(results: list[Result]) -> Result:
        std_in = "\n".join(result.std_in for result in results)
        std_out = "\n".join(result.std_out for result in results)
        std_err = "\n".join(result.std_err for result in results)
        return Result(
            std_in.strip(),
            results[-1].return_code,
            std_out.strip(),
            std_err.strip(),
            results[-1].env,
        )

    def _get_last_line_in_file(self, file: NamedTemporaryFile) -> str:
        pos = file.tell()
        err = None
        try:
            file.seek(-2, os.SEEK_END)
            while file.read(1) != b"\n":
                file.seek(-2, os.SEEK_CUR)
        except OSError:
            file.seek(0)
            err = True
        line = self._read_line(file)
        if not err:
            file.seek(pos)
        return line.rstrip()

    @staticmethod
    def _read_line(file: NamedTemporaryFile) -> str:
        return file.readline().decode("utf-8")

    def _std_out_read(self, uuid: str) -> tuple[str, int]:
        while uuid != self._get_last_line_in_file(self._std_out):
            time.sleep(self._wait_time)
        self._std_out.seek(0)
        lines = []
        line = self._read_line(self._std_out)
        while True:
            if line.rstrip() == uuid:
                break
            lines.append(line)
            line = self._read_line(self._std_out)
        std_out = "".join(line for line in lines[:-1])
        return_code = lines[-1]
        self._reset_std_out()
        return std_out.rstrip(), int(return_code)

    def _std_err_read(self) -> str:
        self._std_err.seek(0)
        std_err = "".join(line.decode("utf-8") for line in self._std_err.readlines())
        self._reset_std_err()
        return std_err.rstrip()

    def sudo_exec(self, cmd: str, modes: list[Mode] | None = None) -> Result:
        pw = getpass("Password: ") if not self.passwd else self.passwd
        cmds = [cmd]
        if modes is None:
            modes = []
        silent = "-v" not in modes
        if "-e" in modes:
            return self._exec_error_mode(cmds, silent=silent)[0]
        return self._exec(cmd, silent=silent, pw=pw)

    def _exec(self, cmd: str, *, silent: bool = True, pw: str | None = None) -> Result:
        uuid = str(uuid4())
        std_in = cmd
        for mode in VALID_MODES:
            if mode in cmd:
                cmd = cmd.replace(f"set {mode}", "")
                warn(
                    f"Do not use 'set {mode}' in the cmd directly. Pass it in the"
                    "`modes` argument of the `exec`/`exec_all` call",
                    stacklevel=1,
                )
        if not silent and cmd:
            print(cmd)
        if pw is None:
            self._proc.stdin.write(f"{cmd}\necho $?\necho {uuid}\n".encode())
        else:
            self._proc.stdin.write(
                f"sudo -S {cmd}\n{pw}\necho $?\necho {uuid}\n".encode()
            )
        self._proc.stdin.flush()
        std_out, return_code = self._std_out_read(uuid)
        env = None
        if self._track_env:
            self._proc.stdin.write(f"env\necho $?\necho {uuid}\n".encode())
            self._proc.stdin.flush()
            env, _ = self._std_out_read(uuid)
            env = {line.split("=")[0]: line.split("=")[1] for line in env.split("\n")}
        return Result(std_in, return_code, std_out, self._std_err_read(), env)

    def _exec_error_mode(self, cmds: list[str], *, silent: bool = True) -> list[Result]:
        results = []
        for cmd in cmds:
            result = self._exec(cmd, silent=silent)
            results.append(result)
            if result.return_code != 0:
                break
        return results

    def exec(self, *cmds: str, modes: list[Mode] | None = None) -> Result:
        return self._combine_results(self.exec_all(list(cmds), modes))

    def exec_all(
        self, cmds: list[str], modes: list[Mode] | None = None
    ) -> list[Result]:
        if modes is None:
            modes = []
        silent = "-v" not in modes
        if "-e" in modes:
            return self._exec_error_mode(cmds, silent=silent)
        return [self._exec(cmd, silent=silent) for cmd in cmds]

    def close(self) -> None:
        self._proc.stdin.close()
        self._std_out.close()
        self._std_err.close()
        self._proc.terminate()
        self._proc.wait(timeout=0.2)

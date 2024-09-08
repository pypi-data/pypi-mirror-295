from __future__ import annotations

import linecache
import os
import stat
import subprocess
import time
from dataclasses import dataclass
from getpass import getpass
from pathlib import Path
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
        env = os.environ.copy()
        _passwd = None
        self._passwd_file = None
        if passwd_strat is not None:
            if passwd_strat.ask and not passwd_strat.env:
                _passwd = getpass("Password: ")
            if passwd_strat.env:
                _passwd = os.environ.get(passwd_strat.env)
            if _passwd is not None:
                self._passwd_file = Path("./tmp_file")
                if self._passwd_file.exists():
                    self._passwd_file.unlink()
                self._passwd_file.touch()
                with self._passwd_file.open("r+") as pw_file:
                    pw_file.write(f"#!/bin/bash\necho '{_passwd}'\n")
                stats = self._passwd_file.stat()
                self._passwd_file.chmod(stats.st_mode | stat.S_IEXEC)
                env["SUDO_ASKPASS"] = self._passwd_file.as_posix()
        if not executable:
            executable = os.environ.get("SHELL", "/bin/bash")
        self._std_out = NamedTemporaryFile("rb+")
        self._std_err = NamedTemporaryFile("rb+")
        self._proc = subprocess.Popen(
            [executable],
            stdin=subprocess.PIPE,
            stdout=self._std_out,
            stderr=self._std_err,
            env=env,
        )
        self._wait_time = wait_time
        self._track_env = track_env

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

    def _reset_passwd_file(self) -> None:
        if self._passwd_file is not None:
            self._passwd_file.unlink()

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
    def _get_nth_line_in_file(file: NamedTemporaryFile, n: int) -> str:
        linecache.clearcache()
        return linecache.getline(file.name, n)

    @staticmethod
    def _get_file_line_length(file: NamedTemporaryFile) -> int:
        linecache.clearcache()
        return len(linecache.getlines(file.name))

    @staticmethod
    def _read_line(file: NamedTemporaryFile) -> str:
        return file.readline().decode("utf-8")

    def _std_out_read(self, uuid: str, *, print_out: bool = False) -> tuple[str, int]:
        self._check_file_for_uuid(self._std_out, uuid, print_out=print_out)
        self._std_out.seek(0)
        lines = []
        line = self._read_line(self._std_out)
        while True:
            if uuid in line:
                return_code = line.split(" ")[-1]
                break
            lines.append(line)
            line = self._read_line(self._std_out)
        std_out = "".join(lines)
        self._reset_std_out()
        return std_out.rstrip(), int(return_code)

    def _check_file_for_uuid(
        self, file: NamedTemporaryFile, uuid: str, *, print_out: bool = False
    ) -> None:
        if print_out:
            current_line = 0
            line = self._get_nth_line_in_file(file, current_line)
            print(line, end="")
            previous_line = line
            while uuid not in line:
                if line != previous_line:
                    print(line, end="")
                previous_line = line
                if current_line < self._get_file_line_length(file):
                    current_line += 1
                line = self._get_nth_line_in_file(file, current_line)
                time.sleep(self._wait_time)
        else:
            while uuid not in self._get_last_line_in_file(file):
                time.sleep(self._wait_time)

    def _std_err_read(self, *, print_out: bool = False) -> str:
        self._std_err.seek(0)
        std_err = "".join(line.decode("utf-8") for line in self._std_err.readlines())
        if print_out:
            print(std_err, end="")
        self._reset_std_err()
        return std_err.rstrip()

    def sudo_exec(
        self, cmd: str, modes: list[Mode] | None = None, *, print_out: bool = False
    ) -> Result:
        cmds = [cmd]
        if modes is None:
            modes = []
        print_in = "-v" not in modes
        if "-e" in modes:
            return self._exec_error_mode(cmds, print_in=print_in)[0]
        return self._exec(cmd, print_in=print_in, print_out=print_out)

    def _exec(
        self,
        cmd: str,
        *,
        print_in: bool = True,
        print_out: bool = False,
    ) -> Result:
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
        if cmd.startswith("sleep"):
            cmd = cmd.replace("sleep ", "")
            time.sleep(float(cmd))
            if print_out:
                print()
            return Result(std_in, 0, "", "", self._get_env_vars(uuid))
        if not print_in and cmd:
            print(cmd)
        if self._passwd_file is None:
            self._proc.stdin.write(f"{cmd}\necho {uuid} $?\n".encode())
        else:
            self._proc.stdin.write(f"sudo -A {cmd}\necho {uuid} $?\n".encode())
        self._proc.stdin.flush()
        std_out, return_code = self._std_out_read(uuid, print_out=print_out)
        return Result(
            std_in,
            return_code,
            std_out,
            self._std_err_read(print_out=print_out),
            self._get_env_vars(uuid),
        )

    def _get_env_vars(self, uuid: str) -> dict[str, str] | None:
        if self._track_env:
            self._proc.stdin.write(f"env\necho {uuid} $?\n".encode())
            self._proc.stdin.flush()
            env, _ = self._std_out_read(uuid)
            return {line.split("=")[0]: line.split("=")[1] for line in env.split("\n")}
        return None

    def _exec_error_mode(
        self, cmds: list[str], *, print_in: bool = True, print_out: bool = False
    ) -> list[Result]:
        results = []
        for cmd in cmds:
            result = self._exec(cmd, print_in=print_in, print_out=print_out)
            results.append(result)
            if result.return_code != 0:
                break
        return results

    def exec(
        self, *cmds: str, modes: list[Mode] | None = None, print_out: bool = False
    ) -> Result:
        return self._combine_results(
            self.exec_all(list(cmds), modes, print_out=print_out)
        )

    def exec_all(
        self,
        cmds: list[str],
        modes: list[Mode] | None = None,
        *,
        print_out: bool = False,
    ) -> list[Result]:
        try:
            if modes is None:
                modes = []
            print_in = "-v" not in modes
            if "-e" in modes:
                return self._exec_error_mode(cmds, print_in=print_in)
            return [
                self._exec(cmd, print_in=print_in, print_out=print_out) for cmd in cmds
            ]
        except Exception as err:
            print(err)
            self.close()

    def close(self) -> None:
        self._proc.stdin.close()
        self._reset_std_out()
        self._reset_std_err()
        self._std_out.close()
        self._std_err.close()
        if self._passwd_file is not None:
            self._reset_passwd_file()
        self._proc.terminate()
        self._proc.wait(timeout=0.2)

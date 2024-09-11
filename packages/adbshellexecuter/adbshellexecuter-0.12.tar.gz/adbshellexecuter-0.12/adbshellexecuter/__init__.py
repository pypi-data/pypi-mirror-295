import time
import subprocess
import ctypes
import sys
import os
from functools import cache
from exceptdrucker import errwrite
import threading
from osversionchecker import check_os
from collections import deque

subprocess._USE_VFORK = False
subprocess._USE_POSIX_SPAWN = False
adbconfig = sys.modules[__name__]
adbconfig.max_capture_stdout = 10000
adbconfig.max_capture_stderr = 10000
adbconfig.debugmode = True
os_system_points, active_os_system = check_os()
iswindows = active_os_system == "windows"
if iswindows:
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = subprocess.SW_HIDE
    creationflags = subprocess.CREATE_NO_WINDOW
    invisibledict = {
        "startupinfo": startupinfo,
        "creationflags": creationflags,
        "start_new_session": True,
    }
    from ctypes import wintypes

    windll = ctypes.LibraryLoader(ctypes.WinDLL)
    kernel32 = windll.kernel32
    GetExitCodeProcess = windll.kernel32.GetExitCodeProcess
    _GetShortPathNameW = kernel32.GetShortPathNameW
    _GetShortPathNameW.argtypes = [wintypes.LPCWSTR, wintypes.LPWSTR, wintypes.DWORD]
    _GetShortPathNameW.restype = wintypes.DWORD
else:
    invisibledict = {}
    startupinfo = None
    creationflags = None


class SubprocessWrite(subprocess.Popen):
    """
    A class to manage subprocess execution with custom stdin, stdout, and stderr handling.

    Args:
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            **{
                **kwargs,
                **{
                    "stdin": subprocess.PIPE,
                    "stdout": subprocess.PIPE,
                    "stderr": subprocess.PIPE,
                },
            },
        )
        self.extra_data_to_print_stdout = ""
        self.extra_data_to_print_stderr = ""
        self.print_stdout = True
        self.print_stderr = True
        self.stderr_results = deque(maxlen=adbconfig.max_capture_stdout)
        self.stdout_results = deque(maxlen=adbconfig.max_capture_stderr)
        self.t1 = threading.Thread(target=self._readstdout, name="stdout", daemon=True)
        self.t2 = threading.Thread(target=self._readstderr, name="stderr", daemon=True)
        self.stop_thread1 = False
        self.stop_thread2 = False
        # Start the threads to capture and print the subprocess output
        self.t1.start()
        self.t2.start()

    def stdinwrite(self, data):
        """
        Write data to the subprocess stdin.

        Args:
            data (str or bytes): The data to write to stdin.

        Returns:
            bool: True if write was successful, False otherwise.
        """
        wasok = False
        try:
            if isinstance(data, str):
                data = data.encode()
            self.stdin.write(data + b"\n")
            self.stdin.flush()
            wasok = True
        except Exception:
            if adbconfig.debugmode:
                errwrite()
        return wasok

    def _readstdout(self):
        """
        Read and print stdout of the subprocess.
        """
        try:
            for l in iter(self.stdout.readline, b""):
                if self.stop_thread1:
                    break
                self.stdout_results.append(l)
                if self.print_stdout:
                    sys.stdout.write(
                        f'{self.extra_data_to_print_stdout}{l.decode("utf-8", "backslashreplace")}'
                    )
        except Exception:
            if adbconfig.debugmode:
                errwrite()

    def _readstderr(self):
        """
        Read and print stderr of the subprocess.
        """
        try:
            for l in iter(self.stderr.readline, b""):
                if self.stop_thread2:
                    break
                self.stderr_results.append(l)
                if self.print_stderr:
                    sys.stderr.write(
                        f'{self.extra_data_to_print_stderr}{l.decode("utf-8", "backslashreplace")}'
                    )
        except Exception:
            if adbconfig.debugmode:
                errwrite()

    def kill(self, *args, **kwargs):
        """
        Kill the subprocess and stop the stdout and stderr threads.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        self.stop_thread1 = True
        self.stop_thread2 = True
        time.sleep(2)

        killthread(self.t1)
        killthread(self.t2)
        super().kill(*args, **kwargs)

    def terminate(self, *args, **kwargs):
        """
        Terminate the subprocess and stop the stdout and stderr threads.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        self.stop_thread1 = True
        self.stop_thread2 = True
        time.sleep(2)

        killthread(self.t1)
        killthread(self.t2)
        super().terminate(*args, **kwargs)


@cache
def get_short_path_name(long_name):
    """
    Get the short path name for a given long path name (Windows only).

    Args:
        long_name (str): The long path name.

    Returns:
        str: The short path name.
    """
    try:
        if not iswindows:
            return long_name
        output_buf_size = 4096
        output_buf = ctypes.create_unicode_buffer(output_buf_size)
        _ = _GetShortPathNameW(long_name, output_buf, output_buf_size)
        return output_buf.value
    except Exception:
        if adbconfig.debugmode:
            errwrite()
    return long_name


def killthread(threadobject):
    """
    Kill a thread.

    Args:
        threadobject (threading.Thread): The thread object to kill.

    Returns:
        bool: True if thread was killed, False otherwise.
    """
    if not threadobject.is_alive():
        return True
    tid = -1
    for tid1, tobj in threading._active.items():
        if tobj is threadobject:
            tid = tid1
            break
    if tid == -1:
        sys.stderr.write(f"{threadobject} not found")
        return False
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
        ctypes.c_long(tid), ctypes.py_object(SystemExit)
    )
    if res == 0:
        return False
    elif res != 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, 0)
        return False
    return True


def _inputdict_from_command(command):
    """
    Convert a command to a dictionary suitable for subprocess input.

    Args:
        command (str, list, or tuple): The command to convert.

    Returns:
        dict: The command as a dictionary.
    """
    if isinstance(command, (list, tuple)):
        if isinstance(command[0], (str)):
            command = " ".join(command)
        elif isinstance(command[0], (bytes)):
            command = b" ".join(command)
    if not isinstance(command, (bytes)):
        command = command.encode()
    return {"input": command}


class UniversalADBExecutor:
    """
    A class to execute ADB (Android Debug Bridge) commands on multiple operating systems.

    This class provides methods to run ADB commands with and without capturing stdout and stderr,
    as well as creating non-blocking processes. It handles different operating system environments
    such as Windows, Linux, macOS, and Android, providing a unified interface for ADB command execution.
    Òn Android, the "adb shell" part is completely ignored, instead a subshell (sh) is used to execute

    Args:
        adb_path (str): The path to the adb executable.
        device_serial (str): The serial number of the device.
        standard_kwargs_windows (tuple): Standard kwargs for Windows.
        standard_kwargs_linux (tuple): Standard kwargs for Linux.
        standard_kwargs_darwin (tuple): Standard kwargs for macOS.
        standard_kwargs_android (tuple): Standard kwargs for Android.
    """

    def __init__(
        self,
        adb_path=None,
        device_serial=None,
        standard_kwargs_windows=(
            ("env", os.environ),
            ("shell", False),
            ("startupinfo", startupinfo),
            (
                "creationflags",
                creationflags,
            ),
            ("start_new_session", True),
        ),
        standard_kwargs_linux=(
            ("env", os.environ),
            ("shell", True),
        ),
        standard_kwargs_darwin=(
            ("env", os.environ),
            ("shell", True),
        ),
        standard_kwargs_android=(
            ("env", os.environ),
            ("shell", True),
        ),
    ) -> None:
        self.mainshell = os.environ.get("SHELL", "")
        self.adb_path = adb_path
        if iswindows:
            self.adb_path = get_short_path_name(self.adb_path)
        self.device_serial = device_serial
        if active_os_system == "android":
            self.start_command_shell = [self.mainshell]
        else:
            self.start_command_shell = [
                self.adb_path,
                "-s",
                self.device_serial,
                "shell",
            ]
        self.standard_kwargs_windows = dict(standard_kwargs_windows)
        self.standard_kwargs_linux = dict(standard_kwargs_linux)
        self.standard_kwargs_darwin = dict(standard_kwargs_darwin)
        self.standard_kwargs_android = dict(standard_kwargs_android)
        self.capture_output_dict = {"capture_output": True}
        self.proc = None

    def shell_without_capturing_stdout_and_stderr(
        self,
        command,
        debug=True,
        ignore_exceptions=False,
        **kwargs,
    ):
        """
        Execute a shell command without capturing stdout and stderr.

        Args:
            command (str, bytes, list, or tuple): The command to execute.
            debug (bool): Whether to print debug information.
            ignore_exceptions (bool): Whether to ignore exceptions.
            **kwargs: Arbitrary keyword arguments for subprocess.run.

        Returns:
            subprocess.CompletedProcess: The result of the command execution.
        """
        try:
            inputdict = _inputdict_from_command(command)

            if active_os_system == "android":
                return subprocess.run(
                    self.start_command_shell,
                    **{**self.standard_kwargs_android, **kwargs, **inputdict},
                )
            elif active_os_system == "windows":
                return subprocess.run(
                    self.start_command_shell,
                    **{**self.standard_kwargs_windows, **kwargs, **inputdict},
                )
            elif active_os_system == "linux":
                return subprocess.run(
                    self.start_command_shell,
                    **{**self.standard_kwargs_linux, **kwargs, **inputdict},
                )
            elif active_os_system == "darwin":
                return subprocess.run(
                    self.start_command_shell,
                    **{**self.standard_kwargs_darwin, **kwargs, **inputdict},
                )
        except Exception as e:
            if debug:
                errwrite()
            if not ignore_exceptions:
                raise e

    def shell_with_capturing_import_stdout_and_stderr(
        self,
        command,
        debug=True,
        ignore_exceptions=False,
        **kwargs,
    ):
        """
        Execute a shell command with capturing stdout and stderr.

        Args:
            command (str, bytes, list, or tuple): The command to execute.
            debug (bool): Whether to print debug information.
            ignore_exceptions (bool): Whether to ignore exceptions.
            **kwargs: Arbitrary keyword arguments to pass to subprocess.run.

        Returns:
            tuple: A tuple containing stdout, stderr, and return code.
        """
        stdout, stderr, returncode = None, None, None
        inputdict = _inputdict_from_command(command)

        try:
            if active_os_system == "android":
                returndata = subprocess.run(
                    self.start_command_shell,
                    **{
                        **self.standard_kwargs_android,
                        **kwargs,
                        **self.capture_output_dict,
                        **inputdict,
                    },
                )
            elif active_os_system == "windows":
                returndata = subprocess.run(
                    self.start_command_shell,
                    **{
                        **self.standard_kwargs_windows,
                        **kwargs,
                        **self.capture_output_dict,
                        **inputdict,
                    },
                )
            elif active_os_system == "linux":
                returndata = subprocess.run(
                    self.start_command_shell,
                    **{
                        **self.standard_kwargs_linux,
                        **kwargs,
                        **self.capture_output_dict,
                        **inputdict,
                    },
                )
            elif active_os_system == "darwin":
                returndata = subprocess.run(
                    self.start_command_shell,
                    **{
                        **self.standard_kwargs_darwin,
                        **kwargs,
                        **self.capture_output_dict,
                        **inputdict,
                    },
                )
            stdout, stderr, returncode = (
                        returndata.stdout,
                        returndata.stderr,
                        returndata.returncode,
                    )
            if debug:
                try:

                    print("Returncode:", returncode)
                    stdoutput = (
                        stdout.decode("utf-8", errors="backslashreplace")
                        .strip()
                        .splitlines()
                    )
                    stderror = (
                        stderr.decode("utf-8", errors="backslashreplace")
                        .strip()
                        .splitlines()
                    )
                    for line in stdoutput:
                        print("Stdout:", line)
                    for line in stderror:
                        print("Stderr:", line)
                    return stdout, stderr, returncode
                except Exception:
                    errwrite()
        except Exception as e:
            if debug:
                errwrite()
            if not ignore_exceptions:
                raise e
        return stdout, stderr, returncode

    def create_non_blocking_proc(self, debug=True, ignore_exceptions=False, **kwargs):
        """
        Create a non-blocking subprocess.

        Args:
            debug (bool): Whether to print debug information.
            ignore_exceptions (bool): Whether to ignore exceptions.
            **kwargs: Arbitrary keyword arguments to pass to subprocess.Popen.

        Returns:
            SubprocessWrite: The created subprocess.
        """
        try:
            if active_os_system == "windows":
                self.proc = SubprocessWrite(
                    self.start_command_shell,
                    **{**self.standard_kwargs_windows, **kwargs},
                )
            elif active_os_system == "linux":
                self.proc = SubprocessWrite(
                    self.start_command_shell, **{**self.standard_kwargs_linux, **kwargs}
                )
            elif active_os_system == "darwin":
                self.proc = SubprocessWrite(
                    self.start_command_shell,
                    **{**self.standard_kwargs_darwin, **kwargs},
                )
            elif active_os_system == "android":
                self.proc = SubprocessWrite(
                    self.start_command_shell,
                    **{**self.standard_kwargs_android, **kwargs},
                )
        except Exception as e:
            if debug:
                errwrite()
            if not ignore_exceptions:
                raise e
        return self.proc

    def non_shell_adb_commands_with_s_serial(
        self, command, debug=True, ignore_exceptions=False, **kwargs
    ):
        """
        Execute non-shell ADB commands with device serial.

        Args:
            command (str, bytes, list, or tuple): The command to execute.
            debug (bool): Whether to print debug information.
            ignore_exceptions (bool): Whether to ignore exceptions.
            **kwargs: Arbitrary keyword arguments for subprocess.run.

        Returns:
            subprocess.CompletedProcess: The result of the command execution.
        """
        try:
            if not isinstance(command, (list)):
                if not isinstance(command, (tuple)):
                    command = [command]
                else:
                    command = list(command)

            if active_os_system != "android":
                fullcommand = self.start_command_shell[:-1] + command
            else:
                fullcommand = None
            if active_os_system == "windows":
                return subprocess.run(
                    fullcommand,
                    **{**self.standard_kwargs_windows, **kwargs},
                )
            elif active_os_system == "linux":
                return subprocess.run(
                    fullcommand,
                    **{**self.standard_kwargs_linux, **kwargs},
                )
            elif active_os_system == "darwin":
                return subprocess.run(
                    fullcommand,
                    **{**self.standard_kwargs_darwin, **kwargs},
                )
            elif active_os_system == "android":
                return fullcommand
        except Exception as e:
            if debug:
                errwrite()
            if not ignore_exceptions:
                raise e

    def non_shell_adb_commands_without_s_serial(
        self, command, debug=True, ignore_exceptions=False, **kwargs
    ):
        """
        Execute non-shell ADB commands without device serial.

        Args:
            command (str, bytes, list, or tuple): The command to execute.
            debug (bool): Whether to print debug information.
            ignore_exceptions (bool): Whether to ignore exceptions.
            **kwargs: Arbitrary keyword arguments for subprocess.run.

        Returns:
            subprocess.CompletedProcess: The result of the command execution.
        """
        try:
            if not isinstance(command, (list)):
                if not isinstance(command, (tuple)):
                    command = [command]
                else:
                    command = list(command)
            if active_os_system != "android":
                fullcommand = self.start_command_shell[:1] + command
            else:
                fullcommand = None
            if active_os_system == "windows":
                return subprocess.run(
                    fullcommand,
                    **{**self.standard_kwargs_windows, **kwargs},
                )
            elif active_os_system == "linux":
                return subprocess.run(
                    fullcommand,
                    **{**self.standard_kwargs_linux, **kwargs},
                )
            elif active_os_system == "darwin":
                return subprocess.run(
                    fullcommand,
                    **{**self.standard_kwargs_darwin, **kwargs},
                )
            elif active_os_system == "android":
                return fullcommand
        except Exception as e:
            if debug:
                errwrite()
            if not ignore_exceptions:
                raise e


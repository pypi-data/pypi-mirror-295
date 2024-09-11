# A class to execute ADB (Android Debug Bridge) commands on multiple operating systems.

### Tested against Windows 10/Android/Linux / Python 3.11 / Anaconda

### pip install adbshellexecuter


```PY

A class to execute ADB (Android Debug Bridge) commands on multiple operating systems.

This class provides methods to run ADB commands with and without capturing stdout and stderr,
as well as creating non-blocking subprocesses. It handles different operating system environments
such as Windows, Linux, macOS, and Android, providing a unified interface for ADB command execution.
Òn Android, the "adb shell" part is completely ignored, instead a subshell (sh) is used to execute commands

Args:
    adb_path (str): The path to the adb executable.
    device_serial (str): The serial number of the device.
    standard_kwargs_windows (tuple): Standard kwargs for Windows.
    standard_kwargs_linux (tuple): Standard kwargs for Linux.
    standard_kwargs_darwin (tuple): Standard kwargs for macOS.
    standard_kwargs_android (tuple): Standard kwargs for Android.
# Example usage
import shutil
from adbshellexecuter import UniversalADBExecutor
device_serial = "127.0.0.1:5645"
adb_path = shutil.which("adb")

adbshell = UniversalADBExecutor(
    adb_path=adb_path,
    device_serial=device_serial,
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
)

adbshell.non_shell_adb_commands_without_s_serial(
    [
        "connect",
        device_serial,
    ],
)

p1 = adbshell.shell_without_capturing_stdout_and_stderr(
    "mkdir -p '/sdcard/testfiles'", cwd="c:\\windows"
)
p2 = adbshell.shell_with_capturing_import_stdout_and_stderr("ls /sdcard", check=True)
p3 = adbshell.non_shell_adb_commands_with_s_serial(
    r'push "C:\writetext.txt" /sdcard/testfiles'
)

nonblock = adbshell.create_non_blocking_proc(
    debug=True, ignore_exceptions=False, bufsize=1
)
nonblock.extra_data_to_print_stderr = "stderr: "
nonblock.extra_data_to_print_stdout = "stdout: "
nonblock.stdinwrite("ls")
nonblock.stdinwrite("ls /sdcard/testfiles")
print(nonblock.stdout_results)
nonblock.stdinwrite("ls /sdcardbbbbbbbb/testfiles")
print(nonblock.stderr_results)
nonblock.stdinwrite("su")
commandok = nonblock.stdinwrite("ls /system")
print(f"{commandok=}")
print(nonblock.stderr_results)
commandok = nonblock.stdinwrite("ls /system")
nonblock.print_stdout = False
nonblock.print_stderr = False
print(nonblock.stderr_results)
nonblock.kill()
commandok2 = nonblock.stdinwrite("ls /system")

p4 = adbshell.shell_without_capturing_stdout_and_stderr(
    command="while true;do ls;sleep 1;done",
    debug=True,
    ignore_exceptions=True,
    timeout=10,
)
```
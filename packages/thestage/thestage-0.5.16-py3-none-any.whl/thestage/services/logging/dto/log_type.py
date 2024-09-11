from enum import Enum


class LogType(str, Enum):
    stdout = "stdout"
    stderr = "stderr"
    platform_stdout = "platform_stdout"
    platform_stderr = "platform_stderr"

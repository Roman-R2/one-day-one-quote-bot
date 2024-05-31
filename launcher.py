import concurrent.futures
import subprocess

from sys import platform

from app.services.app_logger import AppLogger
from app.services.log_assistant import LogAssistant

LOGGER = AppLogger().get_logger()


class OSPlatform:
    LINUX = ["linux", "linux2"]
    MAC_OS = ["darwin"]
    WINDOWS = ["win32"]

    LogAssistant.put_to_log(
        logger=LOGGER,
        message=f'Определена платфрма {platform}. Запускаем процессы.',
        with_print=True
    )


linux_commands = ["python3 main.py", "python3 schedule_main.py"]
windows_commands = ["python main.py", "python schedule_main.py"]


def run_commands(command):
    print(f"\t{command=}")
    subprocess.run(command, shell=True)


if platform in OSPlatform.LINUX:
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(run_commands, linux_commands)
elif platform in OSPlatform.MAC_OS:
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(run_commands, linux_commands)
elif platform in OSPlatform.WINDOWS:
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(run_commands, windows_commands)

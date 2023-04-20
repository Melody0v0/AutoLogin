
import os
import platform
import sys

import pythoncom
from win32comext.shell import shell


def add_to_startup():
    if platform.system() == 'Windows':
        # 获取当前用户的启动目录
        startup_folder = os.path.join(os.path.expanduser('~'), 'AppData', 'Roaming', 'Microsoft', 'Windows',
                                      'Start Menu', 'Programs', 'Startup')

        # 获取应用程序的当前目录
        current_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
        exe_name = os.path.basename(sys.argv[0])
        exe_path = os.path.join(current_directory, exe_name)

        # 将应用程序添加到启动目录
        shortcut_path = os.path.join(startup_folder, f'{exe_name}.lnk')
        shell_link = pythoncom.CoCreateInstance(
            shell.CLSID_ShellLink,
            None,
            pythoncom.CLSCTX_INPROC_SERVER,
            shell.IID_IShellLink
        )
        shell_link.SetPath(exe_path)
        shell_link.SetWorkingDirectory(current_directory)
        shell_link.SetDescription("My App")
        shell_link.QueryInterface(pythoncom.IID_IPersistFile).Save(shortcut_path, 0)
        print("succeed add")


def remove_from_startup():
    if platform.system() == 'Windows':
        startup_folder = os.path.join(os.path.expanduser('~'), 'AppData', 'Roaming', 'Microsoft', 'Windows',
                                      'Start Menu', 'Programs', 'Startup')

        # 获取当前正在运行的可执行文件的名称
        exe_name = os.path.basename(sys.argv[0])

        shortcut_path = os.path.join(startup_folder, f'{exe_name}.lnk')

        if os.path.exists(shortcut_path):
            os.remove(shortcut_path)
        print("succeed remove")

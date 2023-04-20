import os
import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtNetwork import QLocalSocket, QLocalServer
from PyQt5.QtWidgets import QApplication
import images_rc
from ui import LoginWindow

def main():
    app = QApplication(sys.argv)

    # 获取当前执行文件的绝对路径作为唯一名称
    unique_app_name = os.path.abspath(sys.argv[0])

    # 检查是否已经有一个实例在运行
    socket = QLocalSocket()
    socket.connectToServer(unique_app_name)
    if socket.waitForConnected(500):  # 尝试连接到已有的实例
        print("应用程序已经在运行。")
        sys.exit(1)  # 如果已有实例在运行，退出当前实例

    # 如果没有找到已运行的实例，则创建一个 QLocalServer
    local_server = QLocalServer()
    local_server.listen(unique_app_name)

    login_window = LoginWindow()
    app.setWindowIcon(QIcon(":/logo.ico"))
    login_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
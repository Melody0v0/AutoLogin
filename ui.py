
import os
import platform
import sys

from PyQt5.QtCore import QTimer, Qt, QCoreApplication
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QComboBox, QPushButton, QVBoxLayout, QHBoxLayout, QFormLayout, \
    QCheckBox, QSystemTrayIcon
from qtconsole.mainwindow import MainWindow

import images_rc

from config import add_to_startup, remove_from_startup
from network import login


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.timer_started = False
        self.credentials_file = self.get_credentials_file_path()
        self.load_credentials()
        self.load_auto_start_setting()




    def init_ui(self):
        self.setWindowTitle('登录')
        layout = QVBoxLayout()

        # self.setFixedSize(230, 190)  # 禁止调整窗口大小

        # 用户名，密码，运营商表单
        form_layout = QFormLayout()
        self.username_input = QLineEdit()
        self.username_input.textChanged.connect(self.stop_auto_login)
        form_layout.addRow('学号：', self.username_input)
        self.password_input = QLineEdit()
        self.password_input.textChanged.connect(self.stop_auto_login)
        form_layout.addRow('密码：', self.password_input)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.operator_combo = QComboBox()
        self.operator_combo.addItem('移动', 'cmcc')
        self.operator_combo.addItem('电信', 'telecom')
        form_layout.addRow('运营商：', self.operator_combo)
        layout.addLayout(form_layout)

        # 记住密码，开机自启复选框
        checkbox_layout = QHBoxLayout()

        self.remember_password_checkbox = QCheckBox("记住密码")
        checkbox_layout.addWidget(self.remember_password_checkbox)

        self.auto_start_checkbox = QCheckBox("开机自启")
        self.auto_start_checkbox.stateChanged.connect(
            self.auto_start_state_changed)
        checkbox_layout.addWidget(self.auto_start_checkbox)

        layout.addLayout(checkbox_layout)

        # 登录信息
        self.login_info_label = QLabel()
        self.login_info_label.setWordWrap(True)
        layout.addWidget(self.login_info_label)

        # 登录，最小化按钮
        button_layout = QHBoxLayout()
        self.login_btn = QPushButton('登录')
        self.login_btn.clicked.connect(self.handle_login)
        button_layout.addWidget(self.login_btn)
        self.minimize_btn = QPushButton("最小化")
        self.minimize_btn.clicked.connect(self.minimize_to_tray)
        button_layout.addWidget(self.minimize_btn)
        layout.addLayout(button_layout)

        # 版本标签
        self.version_label = QLabel("Version 1.0.0")
        layout.addWidget(self.version_label)

        # 设置托盘图标
        pixmap = QPixmap(':/logo.ico')  # 使用资源文件中的图标
        icon = QIcon(pixmap)
        self.tray_icon = QSystemTrayIcon(icon, self)
        self.tray_icon.setToolTip("登录窗口")
        self.tray_icon.activated.connect(self.tray_icon_clicked)
        self.tray_icon.show()




        self.setLayout(layout)

        # 添加定时器，每10秒执行一次登录操作
        self.timer = QTimer()
        self.timer.timeout.connect(self.handle_login)

    def stop_auto_login(self):
        if self.timer.isActive():
            self.timer.stop()

    def auto_start_state_changed(self, state):
        if state == Qt.Checked:
            add_to_startup()
            self.save_auto_start_setting(True)
        else:
            remove_from_startup()
            self.save_auto_start_setting(False)

    # 最小化到托盘的槽函数
    def minimize_to_tray(self):
        self.hide()

    # 托盘图标点击事件
    def tray_icon_clicked(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            if self.isHidden():
                self.show()
            else:
                self.hide()

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        operator = self.operator_combo.currentData()

        success, msg = login(username, password, operator)
        if success and msg == "登录成功！":
            self.login_info_label.setText(
                f'<font color="green">{msg}每隔10秒判断一次登录状态</font')
            self.login_succeed(username, password)
        elif success and msg == "已经登录......":
            self.login_info_label.setText(f'<font color="blue">{msg}</font>')
            self.login_succeed(username, password)
        elif msg == "尚未连接wifi":
            self.login_info_label.setText(f'<font color="red">{msg}</font>')
        else:
            self.login_info_label.setText(f'<font color="red">未知错误</font>')

    def login_succeed(self, username, password):
        if not self.timer_started:
            self.timer.start(10000)
            self.timer_started = True
        if self.remember_password_checkbox.isChecked():
            self.save_credentials(username, password)
        else:
            self.delete_credentials()

    def get_credentials_file_path(self):
        if platform.system() == "Windows":
            app_data_folder = os.environ["APPDATA"]
        else:
            app_data_folder = os.path.expanduser("~/.local/share")

        app_folder = os.path.join(app_data_folder, "MyApp")
        os.makedirs(app_folder, exist_ok=True)
        return os.path.join(app_folder, "AutoLoginConfig.txt")

    def get_auto_start_setting_file_path(self):
        if platform.system() == "Windows":
            app_data_folder = os.environ["APPDATA"]
        else:
            app_data_folder = os.path.expanduser("~/.local/share")

        app_folder = os.path.join(app_data_folder, "MyApp")
        os.makedirs(app_folder, exist_ok=True)
        return os.path.join(app_folder, "AutoStartSetting.txt")

    def save_credentials(self, username, password):
        with open(self.credentials_file, "w") as file:
            file.write(f"{username}\n{password}")

    def delete_credentials(self):
        try:
            os.remove(self.credentials_file)
        except FileNotFoundError:
            pass

    def save_auto_start_setting(self, auto_start):
        with open(self.get_auto_start_setting_file_path(), "w") as file:
            file.write(str(auto_start))

    def load_credentials(self):
        try:
            with open(self.credentials_file, "r") as file:
                username = file.readline().strip()
                password = file.readline().strip()
                self.username_input.setText(username)
                self.password_input.setText(password)
                self.remember_password_checkbox.setChecked(True)
                self.handle_login()
        except FileNotFoundError:
            pass
        self.load_auto_start_setting()

    def load_auto_start_setting(self):
        try:
            with open(self.get_auto_start_setting_file_path(), "r") as file:
                auto_start = file.readline().strip()
                if auto_start.lower() == "true":
                    self.auto_start_checkbox.setChecked(True)
                    add_to_startup()
                else:
                    self.auto_start_checkbox.setChecked(False)
                    remove_from_startup()
        except FileNotFoundError:
            pass

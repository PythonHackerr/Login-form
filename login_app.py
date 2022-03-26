import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox
from PyQt5.uic import loadUi
import json


class LoginManager():
    def __init__(self, userdata):
        self.userdata = userdata

    def check_if_can_login(self, nickname, email, password):
        with open(self.userdata, "r") as json_file:
            users = json.load(json_file)
            for user in users:
                # check for nickname or mail and password
                if ((nickname == user["username"] or email == user["mail"]) and password == user["pass"]):
                    return True
        return False

    def check_if_user_exists(self, nickname, email):
        with open(self.userdata, "r") as json_file:
            users = json.load(json_file)
            for user in users:
                # check for nickname
                if (nickname == user["username"]):
                    return "nickname: " + str(nickname)
                # check for mail
                if (email == user["mail"]):
                    return "mail: " + str(email)
        return ""


class Login(QDialog):
    def __init__(self, login_manager):
        super(Login, self).__init__()
        loadUi("login.ui", self)
        self.login_manager = login_manager
        self.login_bt.clicked.connect(self.login)
        self.password_tb.setEchoMode(QtWidgets.QLineEdit.Password)
        self.create_account_bt.clicked.connect(self.show_create_account)

    def show_create_account(self):
        create_account = CreateAccount(self.login_manager)
        widget.addWidget(create_account)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def show_popup(self, text, icon):
        msg = QMessageBox()
        msg.setWindowTitle("Warning!")
        msg.setIcon(icon)
        msg.setText(text)
        msg.exec_()

    def login(self):
        nickname = self.nickname_tb.text()
        email = self.email_tb.text()
        password = self.password_tb.text()
        check_login = self.login_manager.check_if_can_login(
            nickname, email, password)
        if (nickname == "" and email == ""):
            self.show_popup("Fill in nickname or email field",
                            QMessageBox.Warning)
        elif (password == ""):
            self.show_popup("Password field can't be empty!",
                            QMessageBox.Warning)
        elif (password == ""):
            self.show_popup("Password field can't be empty!",
                            QMessageBox.Warning)
        elif (check_login == True):
            self.show_popup("Successfully logged in !!!",
                            QMessageBox.Information)
        else:
            self.show_popup(
                "No user found! Try to create accout if you don't have one", QMessageBox.Warning)


class CreateAccount(QDialog):
    def __init__(self, login_manager):
        super(CreateAccount, self).__init__()
        loadUi("create_account.ui", self)
        self.login_manager = login_manager
        self.sign_up_bt.clicked.connect(self.add_user)
        self.back_bt.clicked.connect(self.return_to_login_window)
        self.password_tb.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirm_password_tb.setEchoMode(QtWidgets.QLineEdit.Password)

    def return_to_login_window(self):
        login = Login(self.login_manager)
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def add_user(self):
        email = self.email_tb.text()
        nickname = self.nickname_tb.text()
        password = self.password_tb.text()
        confirm_password = self.confirm_password_tb.text()
        login = Login(self.login_manager.userdata)
        check_user = self.login_manager.check_if_user_exists(
            nickname, email)
        if (check_user != ""):
            login.show_popup(
                f"User with the same {check_user} already exists", QMessageBox.Warning)
        elif (nickname == ""):
            self.show_popup("Nickname field can't be empty!",
                            QMessageBox.Warning)
        elif (email == ""):
            self.show_popup("Email field can't be empty!",
                            QMessageBox.Warning)
        elif (password == ""):
            self.show_popup("Password field can't be empty!",
                            QMessageBox.Warning)
        elif password != confirm_password:
            login.show_popup(
                "Can't confirm password, try again", QMessageBox.Warning)
        else:
            self.return_to_login_window()
            new_user = {
                "username": nickname,
                "mail": email,
                "pass": password
            }
            all_users = []
            with open(self.login_manager.userdata, "r") as json_file:
                all_users = json.load(json_file)
                if not all_users:
                    all_users = []
                all_users.append(new_user)

            with open(self.login_manager.userdata, 'w') as json_file:
                json.dump(all_users, json_file, indent=4)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_manager = LoginManager("userdata.json")
    mainwindow = Login(login_manager)
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(mainwindow)
    widget.setFixedWidth(540)
    widget.setFixedHeight(720)
    widget.show()
    app.exec_()

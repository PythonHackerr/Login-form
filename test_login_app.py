from login_app import LoginManager
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox

userdata = "userdata_for_testing.json"
login_manager = LoginManager(userdata)
#mainwindow = Login("userdata.json")


def test_aa():
    assert 44 == 44


def test_add_new_user():
    user_exists = login_manager.check_if_user_exists(
        "Mommy Pig!", "mommy_piggie@ukr.net")
    assert user_exists == ""


def test_add_with_same_mail():
    user_exists = login_manager.check_if_user_exists(
        "Mommy Pig!", "mishamisha@ukr.net")
    assert user_exists == "mail: mishamisha@ukr.net"


def test_add_with_same_nickname():
    user_exists = login_manager.check_if_user_exists(
        "BigBOSS23", "mommy_piggie@ukr.net")
    assert user_exists == "nickname: BigBOSS23"


def test_login_no_user_found():
    check_login = login_manager.check_if_can_login(
        "Some_user", "bla bla bla", "password")
    assert check_login == False


def test_login_by_mail():
    check_login = login_manager.check_if_can_login(
        "", "peppa@piggies.net", "Peppa123")
    assert check_login == True


def test_login_by_nickname():
    check_login = login_manager.check_if_can_login(
        "Peppa pig", "", "Peppa123")
    assert check_login == True


def test_login_with_wrong_password():
    check_login = login_manager.check_if_can_login(
        "Peppa pig", "peppa@piggies.net", "wrong password!!!")
    assert check_login == False

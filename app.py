import sqlite3
import smtplib
import sys
from datetime import datetime

from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QTableWidgetItem, QMessageBox, QPlainTextEdit
from PyQt5.uic import loadUi

import functions as funcs

DB = sqlite3.connect('database.db', check_same_thread=False)
cursor = DB.cursor()

# Email configuration
email_config = dict(
    host='smtp.gmail.com',
    port=468,
    tls=True,
    user='ezechivin12@gmail.com',
    password='asimvin123',
    from_name="Chimere's Mini Project",
    encoding='utf-8'
)


class MAIN(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        loadUi('UI/main_window.ui', self)
        self.setWindowTitle('Our Main Window')

        columns = funcs.db_sel_columns('students')
        for item in columns:
            self.cmb_columns.addItem(item)

        self.buttonHandler()

        self.show()

    def buttonHandler(self):
        self.actionExit.triggered.connect(close_app)
        self.contact_sub.clicked.connect(self.sendemail)
        self.btn_save.clicked.connect(self.addstudent)
        self.btn_refresh.clicked.connect(self.refresh_table)
        self.btn_search.clicked.connect(self.search_table)
        self.btn_clear.clicked.connect(self.clearform)
        self.btn_next.clicked.connect(self.go_next)
        self.btn_prev.clicked.connect(self.go_back)
        self.student_id.returnPressed.connect(self.disp_user)
        self.btn_del.clicked.connect(self.delete_item)

    def sendemail(self):
        print('clicked')
        name = self.txt_name.text()
        sender_email = self.txt_email.text()
        message = self.txt_msg.toPlainText()
        gmail_user = 'asimvinci231@gmail.com'
        gmail_password = 'asimvin123'
        try:
            subject = f"Feedback form {name}"
            msg = funcs.htmlmessage(name, sender_email, message)
            result = funcs.send_email(subject, msg)
            if msg == "ok":
                print("Message has been sent")
                self.txt_name.setText('')
                self.txt_email.setText('')
                self.txt_msg.setPlainText('')
            else:
                print(result)
            # server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            # server.ehlo()
            # server.login(gmail_user, gmail_password)
        except Exception as err:
            print('Something went wrong...')
            print(str(err))

    def refresh_table(self):
        self.reloadTable('students')

    def search_table(self):
        text = self.txt_search.text()
        column = self.cmb_columns.currentText()
        self.reloadTable('students', '*', f"where {column} LIKE '%{text}%'")

    def reloadTable(self, table, what='*', conditions=''):
        table = funcs.db_select(table, what, conditions)
        self.table_students.setRowCount(0)
        for rows, columns in enumerate(table):
            self.table_students.insertRow(rows)
            for rowData, columnData in enumerate(columns):
                self.table_students.setItem(rows, rowData, QTableWidgetItem(str(columnData)))

    def delete_item(self):
        ser_id = self.lbl_id.text()
        if int(ser_id) > 0:
            result = funcs.db_select('students', 'id')
            db_id = []
            for x in result:
                db_id.append(x[0])
            ser_id = int(ser_id) - 1

            reply = funcs.db_delete('students', f"WHERE id = {db_id[ser_id]}")
            if reply == "ok":
                my_msg('Operation Successful', 'Student has been deleted', QMessageBox.Information)
                self.refresh_table()
                self.clearform()
            else:
                my_msg('Operation Unsuccessful', str(reply), QMessageBox.Information)

    def go_back(self):
        ser_id = self.lbl_id.text()
        ser_id = int(ser_id) - 1
        if ser_id > 0:
            # try:
            result = funcs.db_select('students', 'id')
            db_id = []
            for x in result:
                db_id.append(x[0])
            ser_id = int(ser_id) - 1
            user = funcs.db_select('students', conditions=f"where id = {db_id[ser_id]}")
            self.setUserDetails(user[0])
            ser_id = int(ser_id) + 1
            if int(ser_id) < 10:
                self.lbl_id.setText(f"0{str(ser_id)}")
            else:
                self.lbl_id.setText(f"{str(ser_id)}")
        # except Exception as err:
        #     my_msg('User not found', str(err), QMessageBox.Information)
        else:
            my_msg('User not found', 'Beginning of list reached', QMessageBox.Information)

    def go_next(self):
        ser_id = self.lbl_id.text()
        ser_id = int(ser_id) + 1
        try:
            result = funcs.db_select('students', 'id')
            db_id = []
            for x in result:
                db_id.append(x[0])
            ser_id = int(ser_id) - 1
            user = funcs.db_select('students', conditions=f"where id = {db_id[ser_id]}")
            self.setUserDetails(user[0])
            ser_id = int(ser_id) + 1
            if int(ser_id) < 10:
                self.lbl_id.setText(f"0{str(ser_id)}")
            else:
                self.lbl_id.setText(f"{str(ser_id)}")
        except Exception as err:
            my_msg('User not found', str(err), QMessageBox.Information)

    def disp_user(self):
        value = self.student_id.text()
        msg = QMessageBox()
        if not value.isdigit():
            my_msg('Number Format Error', 'Only digits are allowed')
        else:
            result = funcs.db_select('students', 'id')
            db_id = []
            for x in result:
                db_id.append(x[0])
            ser_id = int(value) - 1
            try:
                user = funcs.db_select('students', conditions=f"where id = {db_id[ser_id]}")
                self.setUserDetails(user[0])
                if int(value) < 10:
                    self.lbl_id.setText(f"0{str(value)}")
                else:
                    self.lbl_id.setText(f"{str(value)}")

            except Exception as err:
                my_msg('User not found', str(err), QMessageBox.Information)

    def setUserDetails(self, userDetails):
        self.txt_college.setText(userDetails[3])
        self.txt_level.setText(userDetails[4])
        self.txt_matric.setText(userDetails[5])
        self.txt_name_2.setText(userDetails[1])
        self.txt_dept.setText(userDetails[6])
        self.txt_courses.setText(str(userDetails[7]))
        self.txt_age.setText(str(userDetails[2]))
        self.txt_gpa.setText(str(userDetails[8]))

    def clearform(self):
        self.txt_college.setText('')
        self.txt_level.setText('')
        self.txt_matric.setText('')
        self.txt_name_2.setText('')
        self.txt_dept.setText('')
        self.txt_courses.setText('')
        self.txt_age.setText('')
        self.txt_gpa.setText('')
        self.student_id.setText('')
        self.lbl_id.setText('00')

    def addstudent(self):
        try:
            College = self.txt_college.text().upper()
            Level = self.txt_level.text().upper()
            Matric = self.txt_matric.text().upper()
            Name = self.txt_name_2.text()
            Dept = self.txt_dept.text()
            Courses = self.txt_courses.text()
            Age = self.txt_age.text()
            GPA = self.txt_gpa.text()
            noww = datetime.now().strftime("%A %B %d, %Y %H:%M:%S")
            # College = self.txtCollege.text()
            # sentence = f"{}"
            # print(College, Level, Matric, Name, Dept, Courses, Age, GPA)
            msg = funcs.db_insert('students',
                                  "fullname, age, college, level, matric_number, department, number_of_courses, gpa, reg_date",
                                  f"'{Name}','{Age}','{College}','{Level}','{Matric}','{Dept}','{Courses}','{GPA}','{noww}'")
        except Exception as err:
            msg = str(err)
        print(msg)


class regForm(QWidget):
    def __init__(self) -> None:
        super(regForm, self).__init__()
        loadUi('UI/sign_in.ui', self)

        self.button_handler()

        self.setWindowTitle('Our Register Form')
        self.show()

    def button_handler(self):
        self.reg_button.clicked.connect(self.registration)
        self.btnlogin.clicked.connect(self.go_to_login)

    def go_to_login(self):
        print('clicked login link')
        self.frm = loginForm()
        self.frm.show()
        self.hide()

    def registration(self):
        Username = funcs.lw_inp(self.txt_user.text())
        Email = funcs.inp(self.txt_email.text())
        Fname = funcs.inp(self.txt_fname.text())
        Passwd = self.txt_pass.text()
        Confirm = self.txt_repass.text()
        noww = datetime.now().strftime("%A %B %d, %Y %H:%M:%S")
        # print(f"The Username is {Username} with an email of {Email}, fullname is {Fname} and both passwords are {Passwd} and {Confirm} the time is {noww}")
        if not Username or not Email or not Fname or not Confirm or not Passwd:
            msg = "Fill in empty Fields"
            self.lbl_reply.setStyleSheet('color: red')
        elif len(Passwd) < 6:
            msg = "Password is too short"
            self.lbl_reply.setStyleSheet('color: red')
        elif Confirm != Passwd:
            msg = "Passwords do not match"
            self.lbl_reply.setStyleSheet('color: red')
        elif not funcs.emailCheck(Email):
            msg = "Email address is not valid"
            self.lbl_reply.setStyleSheet('color: red')
        else:
            Passwd = funcs.password(Passwd)
            sql = f"INSERT INTO users (username, email, password, fullname, regdate) VALUES ('{Username}', '{Email}', '{Passwd}', '{Fname}', '{noww}') "
            cursor.execute(sql)
            DB.commit()
            DB.close()
            msg = 'User Registered'
            self.lbl_reply.setStyleSheet('color: green')
        self.lbl_reply.setText(msg)


class loginForm(QWidget):
    def __init__(self) -> None:
        super().__init__()
        loadUi('UI/login.ui', self)

        self.buttonHandle()

        self.setWindowTitle('Our Login Form')
        self.show()

    def showReg(self):
        self.frm = regForm()
        self.frm.show()
        self.hide()

    def buttonHandle(self):
        self.btnRegister.clicked.connect(self.regClicked)
        self.btn_login.clicked.connect(self.login)

    def regClicked(self):
        print('Register has been clicked')
        self.showReg()

    def login(self):
        user = self.txt_user.text()
        passwd = self.txt_pass.text()
        msg = ''

        if not user or not passwd:
            msg = "you must fill in the empty field"
            self.lbl_reply.setStyleSheet('color: red')
        else:
            sql = f"SELECT password FROM users WHERE username = '{user}'"
            result = cursor.execute(sql).fetchone()
            if result != None:
                db_password = cursor.execute(sql).fetchone()[0]
                if funcs.verify(passwd, db_password):
                    msg = 'Welcome'
                    self.lbl_reply.setStyleSheet('color: green')
                else:
                    msg = 'Password incorrect, Try again later'
                    self.lbl_reply.setStyleSheet('color: red')
            else:
                msg = "User not found"
                self.lbl_reply.setStyleSheet('color: red')
        self.lbl_reply.setText(msg)


def close_app():
    app.exit()


def pushClik():
    print('Outside function')


def my_msg(title, message, msgType=QMessageBox.Information, buttons=QMessageBox.Cancel):
    msg = QMessageBox()
    msg.setWindowTitle(title)
    msg.setIcon(msgType)
    msg.setText(message)
    msg.setStandardButtons(buttons)
    result = msg.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    firstWindow = MAIN()
    # firstWindow = loginForm()
    # firstWindow = regForm()
    sys.exit(app.exec_())

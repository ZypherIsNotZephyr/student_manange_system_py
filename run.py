import sys
import login
import stu
import sql
import tishi
import tishi2
import studentmessage
import xuanke
import kebiao
import kaoshi
from PyQt5 import QtWidgets


# 登录界面
class LOGIN(QtWidgets.QMainWindow, login.Ui_MainWindow):
    def __init__(self):
        super(LOGIN, self).__init__()
        self.setupUi(self)
        self.ts = TISHI(self)
        self.mw = MAIN(self)

    # 判断登录账号密码是否正确
    def sure(self):
        sid = int(self.lineEdit.text())
        pwd = self.lineEdit_2.text()
        # 通过数据库查询账号密码
        if sql.SqlConnect_Login(sid, pwd):
            self.mw.show()  # mainwindow主界面显示
            self.mw.sid = sid  # 传递用户账户，方便后续操作
            # print("self.mw.sid="+str(self.mw.sid))
            self.close()  # 登录成功后，关闭当前窗口
        else:
            # print("学号或密码错误\n")
            self.ts.show()


# 主界面
class MAIN(QtWidgets.QMainWindow, stu.Ui_MainWindow):
    def __init__(self, last_form):
        super(MAIN, self).__init__()
        self.setupUi(self)
        self.last_form = last_form
        self.sid = -1
        self.stumessage = StudentMessage(self)  # 个人信息界面
        self.xuanke = CHOICES(self)  # 选课界面
        self.kebiao = COURSE(self)
        self.kaoshi = EXAM(self)

    def no(self):
        self.close()

    # 显示个人信息界面
    def personal(self):
        self.stumessage.sid = self.sid
        Student_ID, Student_Name, Student_Password, Student_phone, Student_email, Student_homepage, Student_profile = sql.SqlConnect_Person(
            self.sid)
        self.stumessage.lineEdit.setText(str(Student_Name))
        self.stumessage.lineEdit_2.setText(str(Student_ID))
        self.stumessage.textEdit.setText(str(Student_homepage))
        self.stumessage.textEdit_2.setText(str(Student_profile))
        self.stumessage.lineEdit_3.setText(str(Student_phone))
        self.stumessage.lineEdit_4.setText(str(Student_email))
        self.stumessage.lineEdit_5.setText(str(Student_Password))
        self.stumessage.show()

    # 选课界面
    def choices(self):
        self.xuanke.sid = self.sid
        self.xuanke.show()

    # 查看我的课程
    def courses(self):
        self.kebiao.sid = self.sid
        self.kebiao.show()

    def exam(self):
        self.kaoshi.sid = self.sid
        self.kaoshi.show()


# 账号或密码错误界面
class TISHI(QtWidgets.QMainWindow, tishi.Ui_MainWindow):
    def __init__(self, last_form):
        super(TISHI, self).__init__()
        self.setupUi(self)
        self.last_form = last_form


# 提示选课成功界面
class TISHI2(QtWidgets.QMainWindow, tishi2.Ui_MainWindow):
    def __init__(self, last_form):
        super(TISHI2, self).__init__()
        self.setupUi(self)
        self.last_form = last_form


# 个人信息界面
class StudentMessage(QtWidgets.QMainWindow, studentmessage.Ui_MainWindow):
    def __init__(self, last_form):
        super(StudentMessage, self).__init__()
        self.setupUi(self)
        self.last_form = last_form
        self.sid = -1

        # 初始化信息
        self.lineEdit.setText('')
        self.lineEdit_2.setText('')
        self.lineEdit_5.setText('')
        self.textEdit.setText('')
        self.textEdit_2.setText('')
        self.lineEdit_3.setText('')
        self.lineEdit_4.setText('')

    def S_save(self):
        # stums = sql.SqlConnect_Person(self.sid)
        # print(stums[0],type(stums))
        Student_Name = self.lineEdit.text()
        Student_Password = self.lineEdit_5.text()
        Student_phone = self.lineEdit_3.text()
        Student_email = self.lineEdit_4.text()
        Student_homepage = self.textEdit.toPlainText()
        Student_profile = self.textEdit_2.toPlainText()
        student = (
            self.sid, Student_Name, Student_Password, Student_phone, Student_email, Student_homepage, Student_profile)
        sql.SqlConnect_Save_Student(student)
        self.close()


# 选课界面
class CHOICES(QtWidgets.QMainWindow, xuanke.Ui_MainWindow):
    def __init__(self, last_form):
        super(CHOICES, self).__init__()
        self.setupUi(self)
        self.last_form = last_form
        self.sid = -1
        self.tishi2 = TISHI2(self)

    def c_save(self):
        self.close()

    def all(self):
        Am = sql.SqlConnect_Allcourses()
        # print(type(Am[0][0]))
        for i in range(10):
            for j in range(5):
                try:
                    self.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(Am[i][j])))
                except:
                    self.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(""))

    def search(self):
        index = self.comboBox.currentIndex()
        message = self.lineEdit.text()
        Am = sql.SqlConnect_Search_Courses(index, message)
        for i in range(10):
            for j in range(5):
                try:
                    self.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(Am[i][j])))
                except:
                    self.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(""))

    def add(self):
        cid = self.lineEdit_2.text()
        tname = self.lineEdit_3.text()
        if sql.SqlConnect_Add_Course(cid, tname, self.sid):
            self.tishi2.show()

    def delete(self):
        cid = self.lineEdit_2.text()
        tname = self.lineEdit_3.text()
        if sql.SqlConnect_Del_Course(cid, tname, self.sid):
            self.tishi2.show()


# 查看课表
class COURSE(QtWidgets.QMainWindow, kebiao.Ui_MainWindow):
    def __init__(self, last_form):
        super(COURSE, self).__init__()
        self.setupUi(self)
        self.last_form = last_form
        self.sid = -1

    def see(self):
        Am = sql.SqlConnect_Seecourses(self.sid)
        for i in range(10):
            for j in range(4):
                try:
                    self.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(Am[i][j])))
                except:
                    self.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(""))


# 考试查询
class EXAM(QtWidgets.QMainWindow, kaoshi.Ui_MainWindow):
    def __init__(self, last_form):
        super(EXAM, self).__init__()
        self.setupUi(self)
        self.last_form = last_form
        self.sid = -1

    def seeexam(self):
        Am = sql.SqlConnect_Seeexam(self.sid)
        for i in range(10):
            for j in range(4):
                try:
                    self.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(Am[i][j])))
                except:
                    self.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(""))


# 开始
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui = LOGIN()
    ui.show()
    sys.exit(app.exec_())

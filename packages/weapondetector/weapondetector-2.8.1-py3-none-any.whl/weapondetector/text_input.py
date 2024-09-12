import os
import sys
from PyQt5 import QtCore, QtGui, QtWidgets

main_path = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(main_path, "assets", "logo.png")
cams_file_path = os.path.join(main_path, "assets", "cams.txt")


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(577, 877)

        Form.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        Form.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.widget = QtWidgets.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(10, 10, 560, 860))
        self.widget.setObjectName("widget")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setGeometry(QtCore.QRect(0, 0, 560, 860))
        self.label.setStyleSheet("background-color:rgba(50, 150, 225, 240);\n"
                                 "border-radius:20px;")
        self.label.setText("")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setGeometry(QtCore.QRect(180, 10, 201, 231))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap(logo_path))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setGeometry(QtCore.QRect(80, 240, 141, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.line = QtWidgets.QFrame(self.widget)
        self.line.setGeometry(QtCore.QRect(30, 230, 501, 20))
        self.line.setStyleSheet("")
        self.line.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line.setLineWidth(2)
        self.line.setMidLineWidth(0)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setObjectName("line")
        self.label_4 = QtWidgets.QLabel(self.widget)
        self.label_4.setGeometry(QtCore.QRect(340, 240, 170, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.lineEdit = QtWidgets.QLineEdit(self.widget)
        self.lineEdit.setEnabled(True)
        self.lineEdit.setGeometry(QtCore.QRect(30, 290, 240, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit.setFont(font)
        self.lineEdit.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lineEdit.setStyleSheet("background-color:rgba(0, 0, 0, 0);\n"
                                    "border:none;\n"
                                    "border-bottom:2px solid rgba(0, 0, 0, 155);\n"
                                    "color:rgba(0, 0, 0, 255);\n"
                                    "padding-bottom:5px;\n"
                                    "")
        self.lineEdit.setText("")
        self.lineEdit.setCursorPosition(0)
        self.lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_2.setEnabled(True)
        self.lineEdit_2.setGeometry(QtCore.QRect(290, 290, 240, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lineEdit_2.setStyleSheet("background-color:rgba(0, 0, 0, 0);\n"
                                      "border:none;\n"
                                      "border-bottom:2px solid rgba(0, 0, 0, 155);\n"
                                      "color:rgba(0, 0, 0, 255);\n"
                                      "padding-bottom:5px;\n"
                                      "")
        self.lineEdit_2.setText("")
        self.lineEdit_2.setCursorPosition(0)
        self.lineEdit_2.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_3.setEnabled(True)
        self.lineEdit_3.setGeometry(QtCore.QRect(30, 330, 240, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_3.setFont(font)
        self.lineEdit_3.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lineEdit_3.setStyleSheet("background-color:rgba(0, 0, 0, 0);\n"
                                      "border:none;\n"
                                      "border-bottom:2px solid rgba(0, 0, 0, 155);\n"
                                      "color:rgba(0, 0, 0, 255);\n"
                                      "padding-bottom:5px;\n"
                                      "")
        self.lineEdit_3.setText("")
        self.lineEdit_3.setCursorPosition(0)
        self.lineEdit_3.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_4 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_4.setEnabled(True)
        self.lineEdit_4.setGeometry(QtCore.QRect(290, 330, 240, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_4.setFont(font)
        self.lineEdit_4.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lineEdit_4.setStyleSheet("background-color:rgba(0, 0, 0, 0);\n"
                                      "border:none;\n"
                                      "border-bottom:2px solid rgba(0, 0, 0, 155);\n"
                                      "color:rgba(0, 0, 0, 255);\n"
                                      "padding-bottom:5px;\n"
                                      "")
        self.lineEdit_4.setText("")
        self.lineEdit_4.setCursorPosition(0)
        self.lineEdit_4.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.lineEdit_5 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_5.setEnabled(True)
        self.lineEdit_5.setGeometry(QtCore.QRect(30, 370, 240, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_5.setFont(font)
        self.lineEdit_5.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lineEdit_5.setStyleSheet("background-color:rgba(0, 0, 0, 0);\n"
                                      "border:none;\n"
                                      "border-bottom:2px solid rgba(0, 0, 0, 155);\n"
                                      "color:rgba(0, 0, 0, 255);\n"
                                      "padding-bottom:5px;\n"
                                      "")
        self.lineEdit_5.setText("")
        self.lineEdit_5.setCursorPosition(0)
        self.lineEdit_5.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.lineEdit_6 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_6.setEnabled(True)
        self.lineEdit_6.setGeometry(QtCore.QRect(290, 370, 240, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_6.setFont(font)
        self.lineEdit_6.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lineEdit_6.setStyleSheet("background-color:rgba(0, 0, 0, 0);\n"
                                      "border:none;\n"
                                      "border-bottom:2px solid rgba(0, 0, 0, 155);\n"
                                      "color:rgba(0, 0, 0, 255);\n"
                                      "padding-bottom:5px;\n"
                                      "")
        self.lineEdit_6.setText("")
        self.lineEdit_6.setCursorPosition(0)
        self.lineEdit_6.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.lineEdit_7 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_7.setEnabled(True)
        self.lineEdit_7.setGeometry(QtCore.QRect(30, 410, 240, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_7.setFont(font)
        self.lineEdit_7.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lineEdit_7.setStyleSheet("background-color:rgba(0, 0, 0, 0);\n"
                                      "border:none;\n"
                                      "border-bottom:2px solid rgba(0, 0, 0, 155);\n"
                                      "color:rgba(0, 0, 0, 255);\n"
                                      "padding-bottom:5px;\n"
                                      "")
        self.lineEdit_7.setText("")
        self.lineEdit_7.setCursorPosition(0)
        self.lineEdit_7.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_7.setObjectName("lineEdit_7")
        self.lineEdit_8 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_8.setEnabled(True)
        self.lineEdit_8.setGeometry(QtCore.QRect(290, 410, 240, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_8.setFont(font)
        self.lineEdit_8.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lineEdit_8.setStyleSheet("background-color:rgba(0, 0, 0, 0);\n"
                                      "border:none;\n"
                                      "border-bottom:2px solid rgba(0, 0, 0, 155);\n"
                                      "color:rgba(0, 0, 0, 255);\n"
                                      "padding-bottom:5px;\n"
                                      "")
        self.lineEdit_8.setText("")
        self.lineEdit_8.setCursorPosition(0)
        self.lineEdit_8.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_8.setObjectName("lineEdit_8")
        self.lineEdit_9 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_9.setEnabled(True)
        self.lineEdit_9.setGeometry(QtCore.QRect(30, 450, 240, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_9.setFont(font)
        self.lineEdit_9.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lineEdit_9.setStyleSheet("background-color:rgba(0, 0, 0, 0);\n"
                                      "border:none;\n"
                                      "border-bottom:2px solid rgba(0, 0, 0, 155);\n"
                                      "color:rgba(0, 0, 0, 255);\n"
                                      "padding-bottom:5px;\n"
                                      "")
        self.lineEdit_9.setText("")
        self.lineEdit_9.setCursorPosition(0)
        self.lineEdit_9.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_9.setObjectName("lineEdit_9")
        self.lineEdit_10 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_10.setEnabled(True)
        self.lineEdit_10.setGeometry(QtCore.QRect(290, 450, 240, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_10.setFont(font)
        self.lineEdit_10.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lineEdit_10.setStyleSheet("background-color:rgba(0, 0, 0, 0);\n"
                                       "border:none;\n"
                                       "border-bottom:2px solid rgba(0, 0, 0, 155);\n"
                                       "color:rgba(0, 0, 0, 255);\n"
                                       "padding-bottom:5px;\n"
                                       "")
        self.lineEdit_10.setText("")
        self.lineEdit_10.setCursorPosition(0)
        self.lineEdit_10.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_10.setObjectName("lineEdit_10")
        self.lineEdit_11 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_11.setEnabled(True)
        self.lineEdit_11.setGeometry(QtCore.QRect(30, 490, 240, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_11.setFont(font)
        self.lineEdit_11.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lineEdit_11.setStyleSheet("background-color:rgba(0, 0, 0, 0);\n"
                                       "border:none;\n"
                                       "border-bottom:2px solid rgba(0, 0, 0, 155);\n"
                                       "color:rgba(0, 0, 0, 255);\n"
                                       "padding-bottom:5px;\n"
                                       "")
        self.lineEdit_11.setText("")
        self.lineEdit_11.setCursorPosition(0)
        self.lineEdit_11.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_11.setObjectName("lineEdit_11")
        self.lineEdit_12 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_12.setEnabled(True)
        self.lineEdit_12.setGeometry(QtCore.QRect(290, 490, 240, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_12.setFont(font)
        self.lineEdit_12.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lineEdit_12.setStyleSheet("background-color:rgba(0, 0, 0, 0);\n"
                                       "border:none;\n"
                                       "border-bottom:2px solid rgba(0, 0, 0, 155);\n"
                                       "color:rgba(0, 0, 0, 255);\n"
                                       "padding-bottom:5px;\n"
                                       "")
        self.lineEdit_12.setText("")
        self.lineEdit_12.setCursorPosition(0)
        self.lineEdit_12.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_12.setObjectName("lineEdit_12")
        self.lineEdit_13 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_13.setEnabled(True)
        self.lineEdit_13.setGeometry(QtCore.QRect(30, 530, 240, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_13.setFont(font)
        self.lineEdit_13.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lineEdit_13.setStyleSheet("background-color:rgba(0, 0, 0, 0);\n"
                                       "border:none;\n"
                                       "border-bottom:2px solid rgba(0, 0, 0, 155);\n"
                                       "color:rgba(0, 0, 0, 255);\n"
                                       "padding-bottom:5px;\n"
                                       "")
        self.lineEdit_13.setText("")
        self.lineEdit_13.setCursorPosition(0)
        self.lineEdit_13.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_13.setObjectName("lineEdit_13")
        self.lineEdit_14 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_14.setEnabled(True)
        self.lineEdit_14.setGeometry(QtCore.QRect(290, 530, 240, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_14.setFont(font)
        self.lineEdit_14.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lineEdit_14.setStyleSheet("background-color:rgba(0, 0, 0, 0);\n"
                                       "border:none;\n"
                                       "border-bottom:2px solid rgba(0, 0, 0, 155);\n"
                                       "color:rgba(0, 0, 0, 255);\n"
                                       "padding-bottom:5px;\n"
                                       "")
        self.lineEdit_14.setText("")
        self.lineEdit_14.setCursorPosition(0)
        self.lineEdit_14.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_14.setObjectName("lineEdit_14")
        self.lineEdit_15 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_15.setEnabled(True)
        self.lineEdit_15.setGeometry(QtCore.QRect(30, 570, 240, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_15.setFont(font)
        self.lineEdit_15.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lineEdit_15.setStyleSheet("background-color:rgba(0, 0, 0, 0);\n"
                                       "border:none;\n"
                                       "border-bottom:2px solid rgba(0, 0, 0, 155);\n"
                                       "color:rgba(0, 0, 0, 255);\n"
                                       "padding-bottom:5px;\n"
                                       "")
        self.lineEdit_15.setText("")
        self.lineEdit_15.setCursorPosition(0)
        self.lineEdit_15.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_15.setObjectName("lineEdit_15")
        self.lineEdit_16 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_16.setEnabled(True)
        self.lineEdit_16.setGeometry(QtCore.QRect(290, 570, 240, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_16.setFont(font)
        self.lineEdit_16.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lineEdit_16.setStyleSheet("background-color:rgba(0, 0, 0, 0);\n"
                                       "border:none;\n"
                                       "border-bottom:2px solid rgba(0, 0, 0, 155);\n"
                                       "color:rgba(0, 0, 0, 255);\n"
                                       "padding-bottom:5px;\n"
                                       "")
        self.lineEdit_16.setText("")
        self.lineEdit_16.setCursorPosition(0)
        self.lineEdit_16.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_16.setObjectName("lineEdit_16")
        self.lineEdit_17 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_17.setEnabled(True)
        self.lineEdit_17.setGeometry(QtCore.QRect(30, 610, 240, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_17.setFont(font)
        self.lineEdit_17.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lineEdit_17.setStyleSheet("background-color:rgba(0, 0, 0, 0);\n"
                                       "border:none;\n"
                                       "border-bottom:2px solid rgba(0, 0, 0, 155);\n"
                                       "color:rgba(0, 0, 0, 255);\n"
                                       "padding-bottom:5px;\n"
                                       "")
        self.lineEdit_17.setText("")
        self.lineEdit_17.setCursorPosition(0)
        self.lineEdit_17.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_17.setObjectName("lineEdit_17")
        self.lineEdit_18 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_18.setEnabled(True)
        self.lineEdit_18.setGeometry(QtCore.QRect(290, 610, 240, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_18.setFont(font)
        self.lineEdit_18.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lineEdit_18.setStyleSheet("background-color:rgba(0, 0, 0, 0);\n"
                                       "border:none;\n"
                                       "border-bottom:2px solid rgba(0, 0, 0, 155);\n"
                                       "color:rgba(0, 0, 0, 255);\n"
                                       "padding-bottom:5px;\n"
                                       "")
        self.lineEdit_18.setText("")
        self.lineEdit_18.setCursorPosition(0)
        self.lineEdit_18.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_18.setObjectName("lineEdit_18")
        self.lineEdit_19 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_19.setEnabled(True)
        self.lineEdit_19.setGeometry(QtCore.QRect(30, 650, 240, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_19.setFont(font)
        self.lineEdit_19.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lineEdit_19.setStyleSheet("background-color:rgba(0, 0, 0, 0);\n"
                                       "border:none;\n"
                                       "border-bottom:2px solid rgba(0, 0, 0, 155);\n"
                                       "color:rgba(0, 0, 0, 255);\n"
                                       "padding-bottom:5px;\n"
                                       "")
        self.lineEdit_19.setText("")
        self.lineEdit_19.setCursorPosition(0)
        self.lineEdit_19.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_19.setObjectName("lineEdit_19")
        self.lineEdit_20 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_20.setEnabled(True)
        self.lineEdit_20.setGeometry(QtCore.QRect(290, 650, 240, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_20.setFont(font)
        self.lineEdit_20.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lineEdit_20.setStyleSheet("background-color:rgba(0, 0, 0, 0);\n"
                                       "border:none;\n"
                                       "border-bottom:2px solid rgba(0, 0, 0, 155);\n"
                                       "color:rgba(0, 0, 0, 255);\n"
                                       "padding-bottom:5px;\n"
                                       "")
        self.lineEdit_20.setText("")
        self.lineEdit_20.setCursorPosition(0)
        self.lineEdit_20.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_20.setObjectName("lineEdit_20")
        self.lineEdit_21 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_21.setEnabled(True)
        self.lineEdit_21.setGeometry(QtCore.QRect(30, 690, 240, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_21.setFont(font)
        self.lineEdit_21.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lineEdit_21.setStyleSheet("background-color:rgba(0, 0, 0, 0);\n"
                                       "border:none;\n"
                                       "border-bottom:2px solid rgba(0, 0, 0, 155);\n"
                                       "color:rgba(0, 0, 0, 255);\n"
                                       "padding-bottom:5px;\n"
                                       "")
        self.lineEdit_21.setText("")
        self.lineEdit_21.setCursorPosition(0)
        self.lineEdit_21.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_21.setObjectName("lineEdit_21")
        self.lineEdit_22 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_22.setEnabled(True)
        self.lineEdit_22.setGeometry(QtCore.QRect(290, 690, 240, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_22.setFont(font)
        self.lineEdit_22.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lineEdit_22.setStyleSheet("background-color:rgba(0, 0, 0, 0);\n"
                                       "border:none;\n"
                                       "border-bottom:2px solid rgba(0, 0, 0, 155);\n"
                                       "color:rgba(0, 0, 0, 255);\n"
                                       "padding-bottom:5px;\n"
                                       "")
        self.lineEdit_22.setText("")
        self.lineEdit_22.setCursorPosition(0)
        self.lineEdit_22.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_22.setObjectName("lineEdit_22")
        self.lineEdit_23 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_23.setEnabled(True)
        self.lineEdit_23.setGeometry(QtCore.QRect(30, 730, 240, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_23.setFont(font)
        self.lineEdit_23.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lineEdit_23.setStyleSheet("background-color:rgba(0, 0, 0, 0);\n"
                                       "border:none;\n"
                                       "border-bottom:2px solid rgba(0, 0, 0, 155);\n"
                                       "color:rgba(0, 0, 0, 255);\n"
                                       "padding-bottom:5px;\n"
                                       "")
        self.lineEdit_23.setText("")
        self.lineEdit_23.setCursorPosition(0)
        self.lineEdit_23.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_23.setObjectName("lineEdit_23")
        self.lineEdit_24 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_24.setEnabled(True)
        self.lineEdit_24.setGeometry(QtCore.QRect(290, 730, 240, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_24.setFont(font)
        self.lineEdit_24.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lineEdit_24.setStyleSheet("background-color:rgba(0, 0, 0, 0);\n"
                                       "border:none;\n"
                                       "border-bottom:2px solid rgba(0, 0, 0, 155);\n"
                                       "color:rgba(0, 0, 0, 255);\n"
                                       "padding-bottom:5px;\n"
                                       "")
        self.lineEdit_24.setText("")
        self.lineEdit_24.setCursorPosition(0)
        self.lineEdit_24.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_24.setObjectName("lineEdit_24")
        self.pushButton_2 = QtWidgets.QPushButton(self.widget)
        self.pushButton_2.setGeometry(QtCore.QRect(120, 815, 150, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setAutoFillBackground(False)
        self.pushButton_2.setStyleSheet("QPushButton#pushButton_2{    \n"
                                        "    background-color: qlineargradient(spread:pad, x1:0, y1:0.505682, x2:1, y2:0.477, stop:0 rgba(220, 47, 78, 219), stop:1 rgba(220, 98, 112, 226));\n"
                                        "    color:rgba(255, 255, 255, 210);\n"
                                        "    border-radius:5px;\n"
                                        "}\n"
                                        "QPushButton#pushButton_2:hover{    \n"
                                        "    background-color: qlineargradient(spread:pad, x1:0, y1:0.505682, x2:1, y2:0.477, stop:0 rgba(220, 67, 98, 219), stop:1 rgba(220, 118, 132, 226));\n"
                                        "}\n"
                                        "QPushButton#pushButton_2:pressed{    \n"
                                        "    padding-left:5px;\n"
                                        "    padding-top:5px;\n"
                                        "    background-color:rgba(220, 118, 132, 200);\n"
                                        "}")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setGeometry(QtCore.QRect(290, 815, 150, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setAutoFillBackground(False)
        self.pushButton.setStyleSheet("QPushButton#pushButton{    \n"
                                      "    background-color: qlineargradient(spread:pad, x1:0, y1:0.505682, x2:1, y2:0.477, stop:0 rgba(20, 210, 90, 219), stop:1 rgba(85, 250, 90, 226));\n"
                                      "    color:rgba(255, 255, 255, 210);\n"
                                      "    border-radius:5px;\n"
                                      "}\n"
                                      "QPushButton#pushButton:hover{    \n"
                                      "    background-color: qlineargradient(spread:pad, x1:0, y1:0.505682, x2:1, y2:0.477, stop:0 rgba(40, 220, 98, 219), stop:1 rgba(105, 220, 132, 226));\n"
                                      "}\n"
                                      "QPushButton#pushButton:pressed{    \n"
                                      "    padding-left:5px;\n"
                                      "    padding-top:5px;\n"
                                      "    background-color:rgba(105, 220, 132, 200);\n"
                                      "}\n"
                                      "")
        self.pushButton.setObjectName("pushButton")
        self.label_5 = QtWidgets.QLabel(self.widget)
        self.label_5.setGeometry(QtCore.QRect(80, 770, 141, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.label_5.setFont(font)
        self.label_5.setScaledContents(False)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.lineEdit_25 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_25.setEnabled(True)
        self.lineEdit_25.setGeometry(QtCore.QRect(290, 770, 240, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_25.setFont(font)
        self.lineEdit_25.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lineEdit_25.setStyleSheet("background-color:rgba(0, 0, 0, 0);\n"
                                       "border:none;\n"
                                       "border-bottom:2px solid rgba(0, 0, 0, 155);\n"
                                       "color:rgba(0, 0, 0, 255);\n"
                                       "padding-bottom:5px;\n"
                                       "")

        self.lineEdit_25.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)
        self.lineEdit_25.setText("")
        self.lineEdit_25.setCursorPosition(0)
        self.lineEdit_25.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_25.setObjectName("lineEdit_25")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        self.pushButton_2.clicked.connect(lambda: self.cancel_button_fn(Form))
        self.pushButton.clicked.connect(lambda: self.ok_button_fn(self.print_cam_urls, Form))

    def write_list_to_file(self, list_to_write, filename):
        """Writes a list to a text file, placing each item on a separate line."""
        with open(filename, 'w') as file:
            for item in list_to_write:
                file.write(item + '\n')

    def read_list_from_file(self, filename):
        """Reads a list from a text file, assuming each item is on a separate line."""
        with open(filename, 'r') as file:
            lines = file.readlines()
        return [item.replace('\n', "") for line in lines for item in line.split(' ')]

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_3.setText(_translate("Form", "Camera URLs"))
        self.label_4.setText(_translate("Form", "Camera Location"))

        if not os.path.exists(cams_file_path):
            self.lineEdit.setPlaceholderText(_translate("Form", "rtsp://"))
            self.lineEdit_2.setPlaceholderText(_translate("Form", "e.g. Main Hall"))
            self.lineEdit_3.setPlaceholderText(_translate("Form", "rtsp://"))
            self.lineEdit_4.setPlaceholderText(_translate("Form", "e.g. Main Hall"))
            self.lineEdit_5.setPlaceholderText(_translate("Form", "rtsp://"))
            self.lineEdit_6.setPlaceholderText(_translate("Form", "e.g. Main Hall"))
            self.lineEdit_7.setPlaceholderText(_translate("Form", "rtsp://"))
            self.lineEdit_8.setPlaceholderText(_translate("Form", "e.g. Main Hall"))
            self.lineEdit_9.setPlaceholderText(_translate("Form", "rtsp://"))
            self.lineEdit_10.setPlaceholderText(_translate("Form", "e.g. Main Hall"))
            self.lineEdit_11.setPlaceholderText(_translate("Form", "rtsp://"))
            self.lineEdit_12.setPlaceholderText(_translate("Form", "e.g. Main Hall"))
            self.lineEdit_13.setPlaceholderText(_translate("Form", "rtsp://"))
            self.lineEdit_14.setPlaceholderText(_translate("Form", "e.g. Main Hall"))
            self.lineEdit_15.setPlaceholderText(_translate("Form", "rtsp://"))
            self.lineEdit_16.setPlaceholderText(_translate("Form", "e.g. Main Hall"))
            self.lineEdit_17.setPlaceholderText(_translate("Form", "rtsp://"))
            self.lineEdit_18.setPlaceholderText(_translate("Form", "e.g. Main Hall"))
            self.lineEdit_19.setPlaceholderText(_translate("Form", "rtsp://"))
            self.lineEdit_20.setPlaceholderText(_translate("Form", "e.g. Main Hall"))
            self.lineEdit_21.setPlaceholderText(_translate("Form", "rtsp://"))
            self.lineEdit_22.setPlaceholderText(_translate("Form", "e.g. Main Hall"))
            self.lineEdit_23.setPlaceholderText(_translate("Form", "rtsp://"))
            self.lineEdit_24.setPlaceholderText(_translate("Form", "e.g. Main Hall"))
            self.lineEdit_25.setPlaceholderText(_translate("Form", "e.g. 0.8"))
        else:
            cams_list = self.read_list_from_file(cams_file_path)
            self.lineEdit.setText(_translate("Form", cams_list[0]))
            self.lineEdit_2.setText(_translate("Form", cams_list[1]))
            self.lineEdit_3.setText(_translate("Form", cams_list[2]))
            self.lineEdit_4.setText(_translate("Form", cams_list[3]))
            self.lineEdit_5.setText(_translate("Form", cams_list[4]))
            self.lineEdit_6.setText(_translate("Form", cams_list[5]))
            self.lineEdit_7.setText(_translate("Form", cams_list[6]))
            self.lineEdit_8.setText(_translate("Form", cams_list[7]))
            self.lineEdit_9.setText(_translate("Form", cams_list[8]))
            self.lineEdit_10.setText(_translate("Form", cams_list[9]))
            self.lineEdit_11.setText(_translate("Form", cams_list[10]))
            self.lineEdit_12.setText(_translate("Form", cams_list[11]))
            self.lineEdit_13.setText(_translate("Form", cams_list[12]))
            self.lineEdit_14.setText(_translate("Form", cams_list[13]))
            self.lineEdit_15.setText(_translate("Form", cams_list[14]))
            self.lineEdit_16.setText(_translate("Form", cams_list[15]))
            self.lineEdit_17.setText(_translate("Form", cams_list[16]))
            self.lineEdit_18.setText(_translate("Form", cams_list[17]))
            self.lineEdit_19.setText(_translate("Form", cams_list[18]))
            self.lineEdit_20.setText(_translate("Form", cams_list[19]))
            self.lineEdit_21.setText(_translate("Form", cams_list[20]))
            self.lineEdit_22.setText(_translate("Form", cams_list[21]))
            self.lineEdit_23.setText(_translate("Form", cams_list[22]))
            self.lineEdit_24.setText(_translate("Form", cams_list[23]))
            self.lineEdit_25.setText(_translate("Form", cams_list[24]))

            self.label_4.setFocus()

        self.label_5.setText(_translate("Form", "Threshold"))

        self.pushButton_2.setText(_translate("Form", "Cancel"))
        self.pushButton.setText(_translate("Form", "OK"))

    def cancel_button_fn(self, Form):
        Form.close()

    def ok_button_fn(self, callback, Form):
        self.cam_urls = []
        self.cam_urls.append(f"{self.lineEdit.text().strip().replace(' ', '_')} {self.lineEdit_2.text().strip().replace(' ', '_')}")
        self.cam_urls.append(f"{self.lineEdit_3.text().strip().replace(' ', '_')} {self.lineEdit_4.text().strip().replace(' ', '_')}")
        self.cam_urls.append(f"{self.lineEdit_5.text().strip().replace(' ', '_')} {self.lineEdit_6.text().strip().replace(' ', '_')}")
        self.cam_urls.append(f"{self.lineEdit_7.text().strip().replace(' ', '_')} {self.lineEdit_8.text().strip().replace(' ', '_')}")
        self.cam_urls.append(f"{self.lineEdit_9.text().strip().replace(' ', '_')} {self.lineEdit_10.text().strip().replace(' ', '_')}")
        self.cam_urls.append(f"{self.lineEdit_11.text().strip().replace(' ', '_')} {self.lineEdit_12.text().strip().replace(' ', '_')}")
        self.cam_urls.append(f"{self.lineEdit_13.text().strip().replace(' ', '_')} {self.lineEdit_14.text().strip().replace(' ', '_')}")
        self.cam_urls.append(f"{self.lineEdit_15.text().strip().replace(' ', '_')} {self.lineEdit_16.text().strip().replace(' ', '_')}")
        self.cam_urls.append(f"{self.lineEdit_17.text().strip().replace(' ', '_')} {self.lineEdit_18.text().strip().replace(' ', '_')}")
        self.cam_urls.append(f"{self.lineEdit_19.text().strip().replace(' ', '_')} {self.lineEdit_20.text().strip().replace(' ', '_')}")
        self.cam_urls.append(f"{self.lineEdit_21.text().strip().replace(' ', '_')} {self.lineEdit_22.text().strip().replace(' ', '_')}")
        self.cam_urls.append(f"{self.lineEdit_23.text().strip().replace(' ', '_')} {self.lineEdit_24.text().strip().replace(' ', '_')}")
        self.cam_urls.append(f"{self.lineEdit_25.text().strip()} ")

        self.write_list_to_file(self.cam_urls, cams_file_path)

        callback(self.cam_urls)
        Form.close()

    def print_cam_urls(self, cam_urls):
        pass


def get_cam_urls():

    cam_urls = []

    def print_cam_urls(urls):
        nonlocal cam_urls
        cam_urls = urls

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    ui.pushButton.clicked.connect(lambda: ui.ok_button_fn(print_cam_urls, Form))
    Form.show()
    _ = app.exec_()
    Form.close()
    return cam_urls


if __name__ == "__main__":

    urls = get_cam_urls()
    for i in urls:
        if i != " ":
            print(f"Data: {i}")
        else:
            print("Empty Data.")

    # app = QtWidgets.QApplication(sys.argv)
    # Form = QtWidgets.QWidget()
    # ui = Ui_Form()
    # ui.setupUi(Form)
    # Form.show()

    # cam_urls = None

    # def handle_ok_button():

    #     cam_urls = ui.ok_button_fn()
    #     Form.close()

    # ui.pushButton.clicked.connect(handle_ok_button)

    # sys.exit(app.exec_())
    # print(cam_urls)

    # sys.exit(app.exec_())

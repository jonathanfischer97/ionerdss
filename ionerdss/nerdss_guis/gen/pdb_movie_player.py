# Form implementation generated from reading ui file 'pdb_movie_player.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        self.labelMovie = QtWidgets.QLabel(parent=Form)
        self.labelMovie.setGeometry(QtCore.QRect(10, 10, 361, 21))
        self.labelMovie.setObjectName("labelMovie")
        self.pushButtonPause = QtWidgets.QPushButton(parent=Form)
        self.pushButtonPause.setGeometry(QtCore.QRect(150, 270, 89, 25))
        self.pushButtonPause.setObjectName("pushButtonPause")
        self.openGLWidgetMovie = QtWidgets.QWidget(parent=Form)
        self.openGLWidgetMovie.setGeometry(QtCore.QRect(10, 40, 381, 221))
        self.openGLWidgetMovie.setObjectName("openGLWidgetMovie")
        self.pushButtonPlay = QtWidgets.QPushButton(parent=Form)
        self.pushButtonPlay.setGeometry(QtCore.QRect(40, 270, 89, 25))
        self.pushButtonPlay.setObjectName("pushButtonPlay")
        self.pushButtonQuit = QtWidgets.QPushButton(parent=Form)
        self.pushButtonQuit.setGeometry(QtCore.QRect(260, 270, 89, 25))
        self.pushButtonQuit.setObjectName("pushButtonQuit")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "PDB Movie Player"))
        self.labelMovie.setText(_translate("Form", "Time: 0s"))
        self.pushButtonPause.setText(_translate("Form", "Pause"))
        self.pushButtonPlay.setText(_translate("Form", "Play"))
        self.pushButtonQuit.setText(_translate("Form", "Quit"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec())

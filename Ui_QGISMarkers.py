# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file Ui_QGISMarkers.ui
# Created with: PyQt4 UI code generator 4.4.4
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_QGISMarkers(object):
    def setupUi(self, QGISMarkers):
        QGISMarkers.setObjectName("QGISMarkers")
        QGISMarkers.resize(400, 300)
        self.buttonBox = QtGui.QDialogButtonBox(QGISMarkers)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.retranslateUi(QGISMarkers)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), QGISMarkers.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), QGISMarkers.reject)
        QtCore.QMetaObject.connectSlotsByName(QGISMarkers)

    def retranslateUi(self, QGISMarkers):
        QGISMarkers.setWindowTitle(QtGui.QApplication.translate("QGISMarkers", "QGISMarkers", None, QtGui.QApplication.UnicodeUTF8))

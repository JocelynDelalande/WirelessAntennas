# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file Ui_WirelessAntennas.ui
# Created with: PyQt4 UI code generator 4.4.4
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_WirelessAntennas(object):
    def setupUi(self, WirelessAntennas):
        WirelessAntennas.setObjectName("WirelessAntennas")
        WirelessAntennas.resize(400, 300)
        self.buttonBox = QtGui.QDialogButtonBox(WirelessAntennas)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.retranslateUi(WirelessAntennas)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), WirelessAntennas.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), WirelessAntennas.reject)
        QtCore.QMetaObject.connectSlotsByName(WirelessAntennas)

    def retranslateUi(self, WirelessAntennas):
        WirelessAntennas.setWindowTitle(QtGui.QApplication.translate("WirelessAntennas", "WirelessAntennas", None, QtGui.QApplication.UnicodeUTF8))

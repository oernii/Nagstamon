# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/oernii/src/Nagstamon/Nagstamon/QUI/dialog_downtime.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_dialog_downtime(object):
    def setupUi(self, dialog_downtime):
        dialog_downtime.setObjectName("dialog_downtime")
        dialog_downtime.resize(409, 294)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(dialog_downtime.sizePolicy().hasHeightForWidth())
        dialog_downtime.setSizePolicy(sizePolicy)
        dialog_downtime.setSizeGripEnabled(True)
        dialog_downtime.setModal(True)
        self.gridLayout = QtWidgets.QGridLayout(dialog_downtime)
        self.gridLayout.setObjectName("gridLayout")
        self.label_start_time = QtWidgets.QLabel(dialog_downtime)
        self.label_start_time.setObjectName("label_start_time")
        self.gridLayout.addWidget(self.label_start_time, 2, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 13, 2, 1, 1)
        self.input_label_description = QtWidgets.QLabel(dialog_downtime)
        self.input_label_description.setObjectName("input_label_description")
        self.gridLayout.addWidget(self.input_label_description, 0, 0, 1, 5)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.button_change_defaults_downtime = QtWidgets.QPushButton(dialog_downtime)
        self.button_change_defaults_downtime.setObjectName("button_change_defaults_downtime")
        self.horizontalLayout.addWidget(self.button_change_defaults_downtime)
        self.button_box = QtWidgets.QDialogButtonBox(dialog_downtime)
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.button_box.setObjectName("button_box")
        self.horizontalLayout.addWidget(self.button_box)
        self.gridLayout.addLayout(self.horizontalLayout, 18, 0, 2, 5)
        self.label_duration_hours = QtWidgets.QLabel(dialog_downtime)
        self.label_duration_hours.setObjectName("label_duration_hours")
        self.gridLayout.addWidget(self.label_duration_hours, 12, 2, 1, 1)
        self.input_spinbox_duration_minutes = QtWidgets.QSpinBox(dialog_downtime)
        self.input_spinbox_duration_minutes.setObjectName("input_spinbox_duration_minutes")
        self.gridLayout.addWidget(self.input_spinbox_duration_minutes, 12, 3, 1, 1)
        self.input_lineedit_comment = QtWidgets.QLineEdit(dialog_downtime)
        self.input_lineedit_comment.setObjectName("input_lineedit_comment")
        self.gridLayout.addWidget(self.input_lineedit_comment, 1, 0, 1, 5)
        self.label_duration_minutes = QtWidgets.QLabel(dialog_downtime)
        self.label_duration_minutes.setObjectName("label_duration_minutes")
        self.gridLayout.addWidget(self.label_duration_minutes, 12, 4, 1, 1)
        self.input_spinbox_duration_hours = QtWidgets.QSpinBox(dialog_downtime)
        self.input_spinbox_duration_hours.setObjectName("input_spinbox_duration_hours")
        self.gridLayout.addWidget(self.input_spinbox_duration_hours, 12, 1, 1, 1)
        self.label_duration = QtWidgets.QLabel(dialog_downtime)
        self.label_duration.setObjectName("label_duration")
        self.gridLayout.addWidget(self.label_duration, 12, 0, 1, 1)
        self.label_end_time = QtWidgets.QLabel(dialog_downtime)
        self.label_end_time.setObjectName("label_end_time")
        self.gridLayout.addWidget(self.label_end_time, 3, 0, 1, 1)
        self.input_lineedit_end_time = QtWidgets.QLineEdit(dialog_downtime)
        self.input_lineedit_end_time.setObjectName("input_lineedit_end_time")
        self.gridLayout.addWidget(self.input_lineedit_end_time, 3, 1, 1, 4)
        self.input_lineedit_start_time = QtWidgets.QLineEdit(dialog_downtime)
        self.input_lineedit_start_time.setObjectName("input_lineedit_start_time")
        self.gridLayout.addWidget(self.input_lineedit_start_time, 2, 1, 1, 4)
        self.input_radiobutton_type_flexible = QtWidgets.QRadioButton(dialog_downtime)
        self.input_radiobutton_type_flexible.setObjectName("input_radiobutton_type_flexible")
        self.gridLayout.addWidget(self.input_radiobutton_type_flexible, 6, 0, 1, 1)
        self.input_radiobutton_type_fixed = QtWidgets.QRadioButton(dialog_downtime)
        self.input_radiobutton_type_fixed.setObjectName("input_radiobutton_type_fixed")
        self.gridLayout.addWidget(self.input_radiobutton_type_fixed, 5, 0, 1, 1)

        self.retranslateUi(dialog_downtime)
        self.button_box.accepted.connect(dialog_downtime.accept)
        self.button_box.rejected.connect(dialog_downtime.reject)
        QtCore.QMetaObject.connectSlotsByName(dialog_downtime)
        dialog_downtime.setTabOrder(self.input_lineedit_comment, self.input_spinbox_duration_hours)
        dialog_downtime.setTabOrder(self.input_spinbox_duration_hours, self.input_spinbox_duration_minutes)
        dialog_downtime.setTabOrder(self.input_spinbox_duration_minutes, self.button_change_defaults_downtime)

    def retranslateUi(self, dialog_downtime):
        _translate = QtCore.QCoreApplication.translate
        dialog_downtime.setWindowTitle(_translate("dialog_downtime", "Downtime"))
        self.label_start_time.setText(_translate("dialog_downtime", "Start time:"))
        self.input_label_description.setText(_translate("dialog_downtime", "description - set by QUI.py"))
        self.button_change_defaults_downtime.setText(_translate("dialog_downtime", "Change downtime defaults..."))
        self.label_duration_hours.setText(_translate("dialog_downtime", "hours"))
        self.label_duration_minutes.setText(_translate("dialog_downtime", "minutes"))
        self.label_duration.setText(_translate("dialog_downtime", "Duration:"))
        self.label_end_time.setText(_translate("dialog_downtime", "End time:"))
        self.input_lineedit_end_time.setText(_translate("dialog_downtime", "n/a"))
        self.input_lineedit_start_time.setText(_translate("dialog_downtime", "n/a"))
        self.input_radiobutton_type_flexible.setText(_translate("dialog_downtime", "Flexible"))
        self.input_radiobutton_type_fixed.setText(_translate("dialog_downtime", "Fixed"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dialog_downtime = QtWidgets.QDialog()
    ui = Ui_dialog_downtime()
    ui.setupUi(dialog_downtime)
    dialog_downtime.show()
    sys.exit(app.exec_())


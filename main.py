from gui_3 import Ui_Barbershop
from PyQt5 import QtWidgets
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Barbershop()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
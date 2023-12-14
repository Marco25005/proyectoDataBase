from PyQt5.QtWidgets import QApplication, QMainWindow, QHeaderView, QAbstractItemView, QDialog, QMessageBox
from PyQt5 import QtCore, QtWidgets
from PyQt5.uic import loadUi
import icons_rc
import sys

class Principal(QMainWindow):
    def __init__(self):
        super(Principal, self).__init__()

        # Cargar el archivo .ui
        loadUi('new_interfaz.ui', self)

        # eliminar la barra de titulo que viene por defecto en Qt
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)

         # botones de la barra de titulo
        self.bt_cerrar.clicked.connect(lambda: self.close())
        self.bt_minimizar.clicked.connect(self.minimizar)
        self.bt_maximizar.clicked.connect(self.maximizar)
        
        # mover ventana
        self.fr_header.mouseMoveEvent=self.mover_ventana

        # determinar el tamaño del QSizeGrip
        self.size = 15
        self.grip = QtWidgets.QSizeGrip(self)
        self.grip.resize(self.size, self.size)

    def minimizar(self):
        self.showMinimized()

    def maximizar(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    # Capturar clic del mouse para recordar la posición al arrastrar
    def mousePressEvent(self, event):
        self.position = event.globalPos()
    
    def mover_ventana(self, event):
        if self.isMaximized() == False:
            if event.buttons() == QtCore.Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.position)
                self.position = event.globalPos()
                event.accept()
        if event.globalPos().y() <= 10:
            self.showMaximized()
        else:
            self.showNormal()

        

    # ubica el la opcion de redimensionar a la derecha y abajo
    def resizeEvent(self, event):
        self.grip.move(self.rect().right() - self.size, self.rect().bottom() - self.size) 
        
    # Capturar clic del mouse para recordar la posición al arrastrar
    def mousePressEvent(self, event):
        self.position = event.globalPos()



if __name__ == '__main__':
    app = QApplication([])
    ventana = Principal()
    ventana.show()
    sys.exit(app.exec_())

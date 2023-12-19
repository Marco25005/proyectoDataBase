from PyQt5.QtWidgets import QApplication, QMainWindow, QHeaderView,QAbstractItemView
from PyQt5.QtCore import QPropertyAnimation
from PyQt5 import QtCore, QtWidgets
from PyQt5.uic import loadUi
from baseDatos import *
import icons_rc
import sys

class Principal(QMainWindow):
    def __init__(self):
        super(Principal, self).__init__()

        # Cargar el archivo .ui
        loadUi('new_interfaz.ui', self)
        self.data=DataBase()
        self.bt_agregar.clicked.connect(lambda:self.seleccionarPagina(False)) #boton agregar de la pagina principal
        self.bt_editar.clicked.connect(lambda: self.seleccionarPagina(True)) #boton editar de la pagina principal
        self.bt_estadio_regresar.clicked.connect(lambda: self.stackedw.setCurrentWidget(self.page_menu)) #botones para regresar al menu princial de cada pagina
        self.bt_partido_regresar.clicked.connect(lambda: self.stackedw.setCurrentWidget(self.page_menu))
        self.bt_arbitro_regresar.clicked.connect(lambda: self.stackedw.setCurrentWidget(self.page_menu))
        self.cb_tabla.currentIndexChanged.connect(self.mostrarTablas)
        
        
        self.mostrarTablas() # mostramos la tabla inicial
        self.llenarCB() #llenamos los combo box para su primer uso
       
        # eliminar la barra de titulo que viene por defecto en Qt
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)

        # botones de la barra de titulo
        self.bt_cerrar.clicked.connect(lambda: self.close())
        self.bt_minimizar.clicked.connect(self.minimizar)
        self.bt_maximizar.clicked.connect(self.maximizar)

        # boton refrescar
        self.bt_refrescar.clicked.connect(self.refrescar_datos)
        
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
    
    def seleccionarPagina(self,tipo):
        self.tipoDeBoton=tipo #variable golobal para recordar que boton se a presionado en otras funciones
        if self.cb_tabla.currentText()=="Árbitro":
            self.stackedw.setCurrentWidget(self.page_agg_arbitro)
            self.bt_aceptar_arbitro.clicked.connect(lambda: self.agregar_editarArbitro(tipo))
        
        elif self.cb_tabla.currentText()=="Partido":
            self.stackedw.setCurrentWidget(self.page_agg_partido)
            self.bt_aceptar_partido.clicked.connect(lambda: self.agregar_editarPartido(tipo))
        else:
            self.stackedw.setCurrentWidget(self.page_agg_estadio)
            self.bt_aceptar_estadio.clicked.connect(lambda: self.agregar_editarEstadio(tipo))
        #print(self.stackedw.currentIndex()) #metodo que usare para llenar los labels en el editar  
    
    def mostrarTablas(self):
        self.filaSelecionada=[] # al mostrar la nueva tabla quitamos los elementos seleccionados anteriormente
        self.tb_container.clear() # limpiamos la tabla para volverla a llenar con lo nuevo a mostrar
        nombreTabla=self.cb_tabla.currentText() #obtenemos el texto que se refiere a cada tabla para mostrarla
        if nombreTabla=="Árbitro":
            self.tabla=self.data.mostrarArbitro()
        elif nombreTabla=="Partido":
            self.tabla=self.data.mostrarPartidos()
        else:
            self.tabla=self.data.mostrarEstadio()
        self.tb_container.setRowCount(len(self.tabla[1])) # ubicamos la cantidad de filas que tendra la tabla
        self.tb_container.setColumnCount(len(self.tabla[0])) # hacemos lo mismo con las columnas
        self.tb_container.setHorizontalHeaderLabels(self.tabla[0]) # ubicamos el encabezado en cada columna
        fila = 0
        for i in self.tabla[1]:
            for j in range(len(i)):
                self.tb_container.setItem(fila, j, QtWidgets.QTableWidgetItem(str(i[j])))
            fila += 1
        #ancho de columna ajustable
        self.tb_container.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    
    def llenarCB(self):
        self.cb_reemplazo.clear() #limpiamos el combo box
        self.cb_estadio.clear()
        self.cb_arbitro.clear()
        if len(self.data.listarArbitros()[1])!=0: #comprobamos que haya arbitros
            self.cb_reemplazo.addItems(self.data.listarArbitros()[1]) # si hay los agregamos al combo box
            self.cb_arbitro.addItems(self.data.listarArbitros()[1])
        else:
            self.cb_reemplazo.addItem("ninguno") #sino agregamos la palabra ninguno
        self.cb_estadio.addItems(self.data.listarEstadios())
    
    def agregar_editarArbitro(self,estado): #echo
        try:
            nombre=self.lineEdit_nombre.text() #tomamos el contenido de cada entry
            apellido=self.lineEdit_apellido.text()
            pais=self.lineEdit_pais.text()
            pasaporte=self.lineEdit_pasaporte.text()
            inicio=self.lineEdit_inicio.text()
            remplazo=self.data.listarArbitros()[0][self.cb_reemplazo.currentIndex()] #aqui tomamos el indice del combo box en la lista de pasaportes para obtener el pasaporte segun el nombre
            if nombre!="" and apellido!="" and pais!="" and pasaporte!="" and inicio!="": #comprobamos que todos los campos esten rellenos
                int(pasaporte), int(inicio)
                if estado: # dependiendo de la funcion que tenga puesta el boton editara o agregara si entraste a la pagina editar estado=True
                    self.data.editarArbitro(pasaporte,pais, inicio, nombre, apellido, remplazo, self.oldPasaporte)
                    self.lb_msgerror.setText("elemento editado") #mandamos un mensaje que indica que se edito el arbitro
                else:
                    self.data.agregarArbitro(pasaporte,pais, inicio, nombre, apellido, remplazo)
                    self.lb_msgerror.setText("elemento agregado")
                self.lineEdit_nombre.clear() #limpiamos todos los entrys luego de agregar o editar
                self.lineEdit_apellido.clear()
                self.lineEdit_pais.clear()
                self.lineEdit_pasaporte.clear()
                self.lineEdit_inicio.clear()
                self.llenarCB() #actualizamos el combo box por si se agrego o cambio algun elemento
            else:
                self.lb_msgerror.setText("rellene todos los campos")
        except ValueError:
            self.lb_msgerror.setText("revise los campos")
        except sqlite3.IntegrityError:
            self.lb_msgerror.setText("el elemento ya existe")

    def refrescar_datos(self):
        self.mostrarTablas()
    
    def agregar_editarEstadio(self,estado):
        try:
            nombre=self.lineEdit_nombre_ciudad.text()
            ciudad=self.lineEdit_ciudad.text()
            capacidadMax=self.spb_capacidad_max.text()
            capacidadHabitada=self.spb_capacidad_hab.text()
            seguridad=self.spb_seguridad.text()
            if nombre!="" and ciudad!="" and capacidadMax!="" and capacidadHabitada!="" and seguridad!="":
                int(capacidadMax),int(capacidadHabitada),int(seguridad)
                if estado:
                    self.data.editarEstadio(nombre,ciudad,capacidadMax,capacidadHabitada,seguridad,self.oldName)
                    self.lb_msgerror.setText("elemento editado")
                else:
                    self.data.agregarEstadio(nombre,ciudad,capacidadMax,capacidadHabitada,seguridad)
                    self.lb_msgerror.setText("elemento agregado")
                self.lineEdit_nombre_ciudad.clear()
                self.lineEdit_ciudad.clear()
                self.spb_capacidad_max.clear()
                self.spb_capacidad_hab.clear()
                self.spb_seguridad.clear()
            else:
                self.lb_msgerror.setText("rellene todos los campos")
        except ValueError:
            self.lb_msgerror.setText("revise los campos")
        except sqlite3.IntegrityError:
            self.lb_msgerror.setText("el elemento ya existe")



    def agregar_editarPartido(self,estado):
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = Principal()
    ventana.show()
    sys.exit(app.exec_())

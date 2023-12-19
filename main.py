from PyQt5.QtWidgets import QApplication, QMainWindow, QHeaderView, QAbstractItemView, QMessageBox
from PyQt5.QtCore import QPropertyAnimation
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QDate, QTime
from PyQt5.uic import loadUi
from baseDatos import *
import sys
import icons_rc

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
        self.bt_eliminar.clicked.connect(lambda: self.eliminar_fila(self.filaSelecionada)) # boton eliminar 
        self.bt_info.clicked.connect(self.acerca_de)
        self.bt_menu.clicked.connect(self.desplazarMenu)
        # Establecer el comportamiento de selección del QTableWidget como seleccionar filas
        self.tb_container.setSelectionBehavior (QAbstractItemView.SelectRows)
        # Conectar la señal de clic del QTableWidget a una función personalizada
        self.tb_container.clicked.connect (self.seleccionarFilas)
        self.cb_tabla.currentIndexChanged.connect(self.mostrarTablas)
        self.dateEdit_fecha.setDate(QDate.currentDate())
        self.mostrarTablas() # mostramos la tabla inicial
        self.llenarCB() #llenamos los combo box para su primer uso
        self.oldPasaporte=None
        self.oldID=None
        self.oldName=None
        # eliminar la barra de titulo que viene por defecto en Qt
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)

        # botones de la barra de titulo
        self.bt_cerrar.clicked.connect(lambda: self.close())
        self.bt_minimizar.clicked.connect(self.minimizar)
        self.bt_maximizar.clicked.connect(self.maximizar)

        # boton refrescar
        self.bt_refrescar.clicked.connect(self.mostrarTablas)
        
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
    
    def desplazarMenu(self): #para desplazar el frame del menu hamburguesa
        ancho=self.fr_menu.width()
        if ancho==0:
            extender=400
        else:
            extender=0
        self.animation=QPropertyAnimation(self.fr_menu,b"maximumWidth")
        self.animation.setDuration(350)
        self.animation.setStartValue(ancho)
        self.animation.setEndValue(extender)
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()     
        

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
         
    
    def mostrarTablas(self):
        self.filaSelecionada=[] # al mostrar la nueva tabla quitamos los elementos seleccionados anteriormente
        self.tb_container.clear() # limpiamos la tabla para volverla a llenar con lo nuevo a mostrar
        nombreTabla=self.cb_tabla.currentText() #obtenemos el texto que se refiere a cada tabla para mostrarla
        if nombreTabla=="Árbitro":
            self.lb_nombre_tabla.setText(nombreTabla)
            self.tabla=self.data.mostrarArbitro()
        elif nombreTabla=="Partido":
            self.lb_nombre_tabla.setText(nombreTabla)
            self.tabla=self.data.mostrarPartidos()
        else:
            self.lb_nombre_tabla.setText(nombreTabla)
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
            if self.cb_reemplazo.currentText()!="ninguno":
                remplazo=self.data.listarArbitros()[0][self.cb_reemplazo.currentIndex()] #aqui tomamos el indice del combo box en la lista de pasaportes para obtener el pasaporte segun el nombre
            else:
                remplazo=None
            if nombre!="" and apellido!="" and pais!="" and pasaporte!="" and inicio!="": #comprobamos que todos los campos esten rellenos
                int(pasaporte), int(inicio)
                if estado and self.oldPasaporte!= None: # dependiendo de la funcion que tenga puesta el boton editara o agregara si entraste a la pagina editar estado=True
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
        except sqlite3.IntegrityError as e:
            if e.args[0]=="error en remplazar":
                self.lb_msgerror.setText("el arbitro no se puede remplazar asi mismo")
            else:    
                self.lb_msgerror.setText("el elemento ya existe")

    def agregar_editarEstadio(self,estado):
        try:
            nombre=self.lineEdit_nombre_ciudad.text()
            ciudad=self.lineEdit_ciudad.text()
            capacidadMax=self.spb_capacidad_max.text()
            capacidadHabitada=self.spb_capacidad_hab.text()
            seguridad=self.spb_seguridad.text()
            if nombre!="" and ciudad!="" and capacidadMax!="" and capacidadHabitada!="" and seguridad!="":
                int(capacidadMax),int(capacidadHabitada),int(seguridad)
                if estado and self.oldName!=None:
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
        except sqlite3.IntegrityError as e:
            if e.args[0]=="CHECK constraint failed: capacidad_habitada <= capacidad_maxima":
                self.lb_msgerror.setText("capacidad habitada mayor que maxima")
            else:
                self.lb_msgerror.setText("el elemento ya existe")

    def agregar_editarPartido(self,estado):
        try:
            id = self.lineEdit_id.text()
            instancia = self.cb_instacia.currentText()
            duracion = self.spinBox_duracion.text()
            fecha = self.dateEdit_fecha.text()
            hora = self.timeEdit_hora.text()
            arbitro = self.data.listarArbitros()[0][self.cb_arbitro.currentIndex()]
            estadio = self.cb_estadio.currentText()
            
            if (id != "" and instancia != "" and duracion != "" and fecha != "" and hora != ""
                and arbitro != "" and estadio != ""):
                int(id)
                if estado and self.oldID!=None:
                    self.data.editarPartido(id, instancia, duracion, fecha, hora, arbitro, estadio,self.oldID)
                    self.lb_msgerror.setText("elemento editado")
                else:
                    self.data.agregarPartido(id, instancia, duracion, fecha, hora, arbitro, estadio)
                    self.lb_msgerror.setText("elemento agregado")
                self.lineEdit_id.clear()
                self.spinBox_duracion.clear()
                self.timeEdit_hora.setTime(QTime.fromString("00:00", "hh:mm"))
                self.llenarCB()
            else:
                self.lb_msgerror.setText("rellene todos los campos")
        except ValueError:
            self.lb_msgerror.setText("revise los campos")
        except sqlite3.IntegrityError:
            self.lb_msgerror.setText("el elemento ya existe")

    def eliminar_fila(self, row):
            if self.cb_tabla.currentText() == "Árbitro":
                if len(row) != 0:
                    try:
                        self.data.borrarArbitro(row[0])
                        self.lb_msgerror.setText("Árbitro {} eliminado".format(row[0]))
                    except sqlite3.IntegrityError:
                        self.lb_msgerror.setText("el arbitro tiene un partido")
                else:
                    self.lb_msgerror.setText("seleccione una fila")

            elif self.cb_tabla.currentText() == "Partido":
                if len(row) != 0:
                    self.data.borrarPartido(row[0])
                    self.lb_msgerror.setText("Partido {} eliminado".format(row[0]))
                else:
                    self.lb_msgerror.setText("seleccione una fila")
            
            else:
                try:
                    if len(row) != 0:
                        self.data.borrarEstadio(row[0])
                        self.lb_msgerror.setText("Estadio {} eliminado".format(row[0]))
                    else:
                        self.lb_msgerror.setText("seleccione una fila")
                except sqlite3.IntegrityError:
                    self.lb_msgerror.setText("el estadio tiene un partido")
            self.mostrarTablas() #se actualiza la tabla al final de la eliminacion
            self.llenarCB()
    
    def seleccionarFilas(self, index): #metodo para seleccionar una fila completa y guardar en una lista
        # Obtener el número de fila del índice
        self.filaSelecionada.clear()
        self.lb_msgerror.clear()
        row = index.row ()
        # Obtener los datos de la fila seleccionada
        for j in range (len(self.tabla[0])):
            self.filaSelecionada.append (self.tb_container.item (row, j).text ()) #vamos metiendo cada elemento de la fila
        self.llenarLineEdit()
    
    def llenarLineEdit(self):
        #arbitro
        if self.stackedw.currentIndex()==1 and len(self.filaSelecionada)!=0 and self.tipoDeBoton: #si se encuentra en editar arbitro
            self.lineEdit_nombre.clear() #limpiamos todos los entrys luego de agregar o editar
            self.lineEdit_apellido.clear()
            self.lineEdit_pais.clear()
            self.lineEdit_pasaporte.clear()
            self.lineEdit_inicio.clear()
            #los llenamos
            self.cb_reemplazo.setCurrentText(self.filaSelecionada[3])
            self.lineEdit_nombre.insert(self.filaSelecionada[3])
            self.lineEdit_pasaporte.insert(self.filaSelecionada[0])
            self.lineEdit_pais.insert(self.filaSelecionada[1])
            self.lineEdit_inicio.insert(self.filaSelecionada[2])
            self.lineEdit_apellido.insert(self.filaSelecionada[4])
            self.oldPasaporte=self.lineEdit_pasaporte.text()
        elif self.stackedw.currentIndex()==2 and len(self.filaSelecionada)!=0 and self.tipoDeBoton: # partido
            
            self.lineEdit_id.clear() # limpiamos el lineEdit
                #agregamos los elementos nuevos seleccionados
            self.cb_instacia.setCurrentText(self.filaSelecionada[1])
            tiempo=QTime.fromString(self.filaSelecionada[4],"h:mm AP")
            self.timeEdit_hora.setTime(tiempo)
            self.lineEdit_id.insert(self.filaSelecionada[0])
            self.spinBox_duracion.setValue(int(self.filaSelecionada[2]))
            fecha=QDate.fromString(self.filaSelecionada[3],"d/M/yyyy")
            self.dateEdit_fecha.setDate(fecha)
            self.cb_arbitro.setCurrentText(self.filaSelecionada[5])
            self.cb_estadio.setCurrentText(self.filaSelecionada[6])
            self.oldID=self.lineEdit_id.text()
        elif  self.stackedw.currentIndex()==3 and len(self.filaSelecionada)!=0 and self.tipoDeBoton:
            #limpiamos todos los lineEdit
            self.lineEdit_nombre_ciudad.clear()
            self.lineEdit_ciudad.clear()
            self.spb_capacidad_max.clear()
            self.spb_capacidad_hab.clear()
            self.spb_seguridad.clear()
            # los llenamos con la informacion seleccionada
            self.lineEdit_nombre_ciudad.insert(self.filaSelecionada[0])
            self.lineEdit_ciudad.insert(self.filaSelecionada[1])
            self.spb_capacidad_max.insert(self.filaSelecionada[2])
            self.spb_capacidad_hab.insert(self.filaSelecionada[3])
            self.spb_seguridad.insert(self.filaSelecionada[4])
            self.oldName=self.lineEdit_nombre_ciudad.text()



    def acerca_de(self):
        msg = """
        MQP-DB ("Mundial Qatar Partido")
        
        
        Esta aplicación PyQt5 proporciona una interfaz gráfica 
        intuitiva para la gestión de información relacionada con 
        Árbitros, Partidos y Estadios. Los usuarios pueden navegar 
        entre diferentes tablas, realizar operaciones CRUD (Crear, 
        Leer, Actualizar, Eliminar) y visualizar datos en tiempo
        real. Con un diseño moderno y características avanzadas, 
        nuestra herramienta ofrece una experiencia eficiente y 
        efectiva para la administración de datos deportivos.
        Versión: 1.0
        
        """
        QMessageBox.information(None, "MQP-DB", msg)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = Principal()
    ventana.show()
    sys.exit(app.exec_())
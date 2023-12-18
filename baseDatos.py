import sqlite3
class DataBase:

    def __init__(self):
        self.base_datos=sqlite3.connect("base de datos.db")
        self.base_datos.cursor().execute("PRAGMA foreign_keys=ON").close() #activamos las llaves foraneas de las tablas
    
    #mostrar
    def mostrarPartidos(self):
        con=self.base_datos.cursor()
        con.execute("SELECT * FROM Partido")
        # headers 
        headers=[] #Se crea una lista para los encabezados de las columnas de la tabla
        for header in con.description: 
            headers.append(header[0]) #extraemos cada encabezado de la consulta y llenamos la lista
        partido=con.fetchall() #obtiene los datos de la tabla
        con.close() #cerramos el cursor
        return headers, partido # devuelve una tupla con los encabezados y los partidos
    
    def mostrarEstadio(self):
        con=self.base_datos.cursor()
        con.execute("SELECT * FROM Estadio")
        headers=[]
        for header in con.description:
            headers.append(header[0])
        estadio=con.fetchall()
        con.close()
        return headers, estadio
    
    def mostrarArbitro(self):
        con=self.base_datos.cursor()
        con.execute("SELECT * FROM Arbitro")
        headers=[]
        for header in con.description:
            headers.append(header[0])
        arbitro=con.fetchall()
        con.close()
        return headers, arbitro
    
    #agregar
    def agregarPartido(self,id,instancia,duracion,fecha,hora,arbitro,estadio):
        con=self.base_datos.cursor()
        con.execute(f"INSERT INTO Partido(id, instancia, duracion, fecha, hora, arbitro, estadio) Values('{id}', '{instancia}', '{duracion}', '{fecha}', '{hora}', '{arbitro}', '{estadio}')")
        self.base_datos.commit()
        con.close()
    
    def agregarEstadio(self,nombre,ciudad,capacidad_maxima,capacidad_habitada,policias):
        con=self.base_datos.cursor()
        con.execute(f"INSERT INTO Estadio(nombre, ciudad, capacidad_maxima, capacidad_habitada, policias) Values('{nombre}', '{ciudad}', '{capacidad_maxima}', '{capacidad_habitada}', '{policias}')")
        self.base_datos.commit()
        con.close()
    
    def agregarArbitro(self,pasaporte,pais,anio_inicio,nombre,apellido,reemplaza):
        con=self.base_datos.cursor()
        con.execute(f"INSERT INTO Arbitro(pasaporte, pais, anio_inicio, nombre, apellido, reemplaza) Values('{pasaporte}', '{pais}', '{anio_inicio}', '{nombre}', '{apellido}', '{reemplaza}')")
        self.base_datos.commit()
        con.close()
    
    #editar
    def editarPartido(self,id,instancia,duracion,fecha,hora,arbitro,estadio, oldId):
        con=self.base_datos.cursor()
        con.execute(f"UPDATE Partido SET id='{id}', instancia='{instancia}', duracion='{duracion}', fecha='{fecha}', hora='{hora}', arbitro='{arbitro}', estadio='{estadio}' WHERE id='{oldId}'")
        self.base_datos.commit()
        con.close()
    
    def editarEstadio(self,nombre,ciudad,capacidad_maxima,capacidad_habitada,policias, oldName):
        con=self.base_datos.cursor()
        con.execute(f"UPDATE Estadio SET nombre='{nombre}', ciudad='{ciudad}', capacidad_maxima='{capacidad_maxima}',capacidad_habitada='{capacidad_habitada}', policias='{policias}' WHERE nombre='{oldName}'")
        self.base_datos.commit()
        con.close()
    
    def editarArbitro(self,pasaporte,pais,anio_inicio,nombre,apellido,reemplaza, oldPasaporte):
        con=self.base_datos.cursor()
        con.execute(f"UPDATE Arbitro SET pasaporte='{pasaporte}', pais='{pais}', anio_inicio='{anio_inicio}', apellido='{apellido}', reemplaza='{reemplaza}', nombre='{nombre}' WHERE pasaporte='{oldPasaporte}' ")
        self.base_datos.commit()
        con.close()
    
    def borrarPartido(self,id):
        con=self.base_datos.cursor()
        con.execute(f"DELETE FROM Partido WHERE id='{id}'")
        self.base_datos.commit()
        con.close()
    
    def borrarEstadio(self,nombre):
        con=self.base_datos.cursor()
        con.execute(f"DELETE FROM Estadio WHERE nombre='{nombre}'")
        self.base_datos.commit()
        con.close()
    
    def borrarArbitro(self,pasaporte):
        con=self.base_datos.cursor()
        con.execute(f"DELETE FROM Arbitro WHERE pasaporte='{pasaporte}'")
        self.base_datos.commit()
        con.close()
    
    def listarArbitros(self):
        con=self.base_datos.cursor()
        con.execute("SELECT pasaporte, nombre FROM Arbitro")
        lista=con.fetchall()
        listaNombre=[i[1] for i in lista] 
        pasaportes=[pasaporte[0] for pasaporte in lista]
        con.close()
        return pasaportes,listaNombre
    
    def listarEstadios(self):
        con=self.base_datos.cursor()
        con.execute("SELECT nombre FROM Estadio")
        lista=con.fetchall()
        listaNombre=[i[0] for i in lista]
        return listaNombre
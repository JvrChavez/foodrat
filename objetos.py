import tkinter as tk
import mysql.connector
from datetime import date

class Dieta:
    def __init__(self, idrat, peso, sobras, dieta, diferencia):
        self.idrat = idrat
        self.peso = peso
        self.sobras = sobras
        self.dieta = dieta
        self.diferencia = diferencia

class Rata:
    def __init__(self,idrat,name,fase):
        self.idrat=idrat
        self.name=name
        self.fase=fase

class BaseDatosRatas:
    def __init__(self, host, port,usuario, contraseña, nombre_base_datos):
        self.host = host
        self.port=port
        self.usuario = usuario
        self.contraseña = contraseña
        self.nombre_base_datos = nombre_base_datos

    def conectar(self):
        self.conexion = mysql.connector.connect(
            host=self.host,
            port=self.port,
            user=self.usuario,
            password=self.contraseña,
            database=self.nombre_base_datos
        )
        self.cursor = self.conexion.cursor()

    def desconectar(self):
        self.cursor.close()
        self.conexion.close()

    def insertar_rata(self, rata):
        consulta = "INSERT INTO rat (idrat, name, fase) VALUES (%s, %s, %s)"
        datos = (rata.id, rata.peso, rata.fecha_nacimiento, rata.estable)
        self.cursor.execute(consulta, datos)
        self.conexion.commit()

    def insertar_dieta(self, rata):
        consulta = "INSERT INTO ratas (idrat, name, fase) VALUES (%s, %s, %s, %s)"
        datos = (Dieta.idrat, rata.peso, rata.fecha_nacimiento, rata.estable)
        self.cursor.execute(consulta, datos)
        self.conexion.commit()

    def consultar_fase(self,rata):
        consulta="SELECT fase FROM rat WHERE id=%s"
        datos=(rata.id)
        return self.cursor.fetchall()


    def consultar_ratas(self):
        self.cursor.execute("SELECT * FROM ratas")
        resultados = self.cursor.fetchall()
        ratas = []
        for resultado in resultados:
            id = resultado[0]
            peso = resultado[1]
            fecha_nacimiento = resultado[2]
            estable = resultado[3]
            rata = Rata(id, peso, fecha_nacimiento, estable)
            ratas.append(rata)
        return ratas

class VentanaRatas:
    def __init__(self, base_datos):
        self.base_datos = base_datos

        self.ventana = tk.Tk()
        self.ventana.title("Registro y consulta de ratas")
        self.ventana.geometry("400x300")

        self.etiqueta_id = tk.Label(self.ventana, text="ID:")
        self.etiqueta_id.pack()
        self.entry_id = tk.Entry(self.ventana)
        self.entry_id.pack()

        self.etiqueta_peso = tk.Label(self.ventana, text="Peso")#date.today().strftime('%Y-%m-%d') PARA FECHA
        self.etiqueta_peso.pack()
        self.entry_peso = tk.Entry(self.ventana)
        self.entry_peso.pack()

        self.etiqueta_sobras = tk.Label(self.ventana, text="Sobras")#date.today().strftime('%Y-%m-%d') PARA FECHA
        self.etiqueta_sobras.pack()
        self.entry_sobras = tk.Entry(self.ventana)
        self.entry_sobras.pack()

        self.etiqueta_fecha_nacimiento = tk.Label(self.ventana, text="Fecha de nacimiento:")
        self.etiqueta_fecha_nacimiento.pack()
        self.entry_fecha_nacimiento = tk.Entry(self.ventana)
        self.entry_fecha_nacimiento.pack()

        self.etiqueta_estable = tk.Label(self.ventana, text="Estable:")
        self.etiqueta_estable.pack()
        self.entry_estable = tk.Entry(self.ventana)
        self.entry_estable.pack()

        self.boton_registrar = tk.Button(self.ventana, text="Registrar", command=self.registrar_rata)
        self.boton_registrar.pack()

        self.boton_consultar = tk.Button(self.ventana, text="Consultar", command=self.consultar_ratas)
        self.boton_consultar.pack()

        self.texto_consulta = tk.Text
        self.texto_consulta = tk.Text(self.ventana)
        self.texto_consulta.pack()

    def registrar_dieta(self):
        idrat = int(self.entry_id.get())
        peso = float(self.entry_peso.get())
        sobras = int(self.entry_sobras.get())
        dieta = bool(self.entry_estable.get())
        diferencia = 

        rata = Dieta(idrat, peso, sobras, dieta, diferencia
        self.base_datos.insertar_rata(rata)
        self.entry_id.delete(0, tk.END)
        self.entry_peso.delete(0, tk.END)
        self.entry_fecha_nacimiento.delete(0, tk.END)
        self.entry_estable.delete(0, tk.END)

    def consultar_ratas(self):
        ratas = self.base_datos.consultar_ratas()
        self.texto_consulta.delete("1.0", tk.END)
        for rata in ratas:
            texto = f"ID: {rata.id}\n"
            texto += f"Peso: {rata.peso}\n"
            texto += f"Fecha de nacimiento: {rata.fecha_nacimiento}\n"
            texto += f"Estable: {rata.estable}\n"
            texto += "----------------\n"
            self.texto_consulta.insert(tk.END, texto)

    def iniciar_aplicacion(self):
        self.base_datos.conectar()
        self.ventana.mainloop()
        self.base_datos.desconectar()

# Configuración de la base de datos
host = "localhost"
port = "3306"
usuario = "root"
contraseña = ""
nombre_base_datos = "foodrat"

# Crear objeto de base de datos y ventana
base_datos = BaseDatosRatas(host, port, usuario, contraseña, nombre_base_datos)
ventana_ratas = VentanaRatas(base_datos)

# Iniciar la aplicación
ventana_ratas.iniciar_aplicacion()

import tkinter as tk
import mysql.connector
from datetime import date
from PIL import ImageTk, Image

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

    def insertar_rata(self, idrat):
        try:
            consulta = "INSERT INTO rat (idrat, name) VALUES (%s, %s)"
            datos = (idrat, "rat"+idrat,)
            self.cursor.execute(consulta, datos)
            self.conexion.commit()
        except mysql.connector.IntegrityError as e:
            print("Error: El valor ya está duplicado en la base de datos")

    def insertar_dieta(self, idrat):
        consulta = "INSERT INTO ratas (idrat, name,) VALUES (%s, %s)"
        datos = (idrat, "rat"+idrat,)
        self.cursor.execute(consulta, datos)
        self.conexion.commit()

    def consultar_fase(self,idrat):
        consulta="SELECT fase FROM rat WHERE idrat=%s ORDER BY fase DESC LIMIT 1"#Con el order by, se obtienen los ultimos registros y el LIMIT dice cuantos seran
        datos=(idrat,)
        self.cursor.execute(consulta, datos)
        return self.cursor.fetchone()
    
    def numero_registros(self,idrat):
        consulta="SELECT peso FROM diadieta WHERE idrat=%s ORDER BY fecha DESC"
        datos=(idrat,)
        self.cursor.execute(consulta,datos)
        resultado=self.cursor.fetchall()
        return len(resultado)


    def consultar_ratas(self):
        self.cursor.execute("SELECT * FROM rat")
        resultados = self.cursor.fetchall()
        ratas = []
        for resultado in resultados:
            idrat = resultado[0]
            name = resultado[1]
            fase = resultado[2]            
            rata = Rata(idrat,name,fase)
            ratas.append(rata)
        return ratas

class VentanaRatas:
    def __init__(self, base_datos):
        self.base_datos = base_datos

        self.ventana = tk.Tk()
        self.ventana.title("Foodrat")
        self.ventana.geometry("400x300")

        self.imagen=Image.open("logo.png")
        self.imagen = self.imagen.resize((100, 100))
        self.photo = ImageTk.PhotoImage(self.imagen)
        self.label_imagen = tk.Label(self.ventana, image=self.photo)
        self.label_imagen.place(x=10,y=200)

        self.etiqueta_id = tk.Label(self.ventana, text="ID:")
        self.etiqueta_id.pack()
        self.entry_id = tk.Entry(self.ventana)
        self.entry_id.pack()

        self.etiqueta_peso = tk.Label(self.ventana, text="Peso:")#date.today().strftime('%Y-%m-%d') PARA FECHA
        self.etiqueta_peso.pack()
        self.entry_peso = tk.Entry(self.ventana)
        self.entry_peso.pack()

        self.etiqueta_sobras = tk.Label(self.ventana, text="Sobras")#date.today().strftime('%Y-%m-%d') PARA FECHA
        self.etiqueta_sobras.pack()
        self.entry_sobras = tk.Entry(self.ventana)
        self.entry_sobras.pack()

        #self.etiqueta_fecha_nacimiento = tk.Label(self.ventana, text="Fecha de nacimiento:")
        #self.etiqueta_fecha_nacimiento.pack()
        #self.entry_fecha_nacimiento = tk.Entry(self.ventana)
        #self.entry_fecha_nacimiento.pack()

        #self.etiqueta_estable = tk.Label(self.ventana, text="Estable:")
        #self.etiqueta_estable.pack()
        #self.entry_estable = tk.Entry(self.ventana)
        #self.entry_estable.pack()

        self.boton_registrar = tk.Button(self.ventana, text="Resultado",command=self.consultar_fase)
        self.boton_registrar.pack()
        self.boton_prueba = tk.Button(self.ventana, text="PRUEBA",command=self.insertar_rata)
        self.boton_prueba.pack()
        #self.boton_registrar.place(x=170,y=200)

        """self.boton_consultar = tk.Button(self.ventana, text="Reinicio de sujeto", command=self.consultar_ratas)
        self.boton_consultar.place(x=145,y=120)"""

        self.etiqueta_resultado = tk.Label(self.ventana, text="Resultado: Dieta de hoy es 15 gr")
        self.etiqueta_resultado.pack()

        self.boton_consultar = tk.Button(self.ventana, text="Limpiar",command=self.limpiar)        
        self.boton_consultar.pack()

        self.boton_consultar = tk.Button(self.ventana, text="Admin")
        self.boton_consultar.place(x=330,y=20)

        #self.texto_consulta = tk.Text
        #self.texto_consulta = tk.Text(self.ventana)
        #self.texto_consulta.pack()

    def registrar_dieta(self):
        idrat = int(self.entry_id.get())
        peso = float(self.entry_peso.get())
        sobras = int(self.entry_sobras.get())
        dieta = bool(self.entry_estable.get())
        #diferencia = 

        rata = Dieta(idrat, peso, sobras, dieta, diferencia)
        self.base_datos.insertar_rata(rata)
        self.entry_id.delete(0, tk.END)
        self.entry_peso.delete(0, tk.END)
        self.entry_fecha_nacimiento.delete(0, tk.END)
        self.entry_estable.delete(0, tk.END)

    def insertar_rata(self):#FUNCIONALIDAD de registrar una rata ya esta funcionando
        self.base_datos.insertar_rata(self.entry_id.get())

    def consultar_fase(self):
        fase=self.base_datos.consultar_fase(self.entry_id.get())
        self.etiqueta_resultado.config(text=fase)
        return fase
    
    def numero_registros(self):
        numero=self.base_datos.numero_registros(self.entry_id.get())
        self.etiqueta_resultado.config(text=numero)
        return numero

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
    
    def limpiar(self):
        self.entry_id.delete(0,tk.END)
        self.entry_peso.delete(0,tk.END)
        self.entry_sobras.delete(0,tk.END)
        self.etiqueta_resultado.config(text="")
        

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

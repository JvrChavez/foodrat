import tkinter as tk
import mysql.connector
from datetime import datetime
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

    def insertar_dieta_fase1(self, idrat,peso,sobras):
        consulta = "INSERT INTO diadieta (idrat,fecha,peso,sobras) VALUES (%s,%s,%s,%s)"
        datos = (idrat, datetime.now().strftime('%Y-%m-%d %H:%M:%S'),peso,sobras,)
        self.cursor.execute(consulta, datos)
        self.conexion.commit()

    def insertar_dieta_fase2(self, idrat,peso,sobras,dieta,diferencia):
        consulta = "INSERT INTO diadieta (idrat,fecha,peso,sobras,dieta,diferencia) VALUES (%s,%s,%s,%s,%s,%s)"
        datos = (idrat, datetime.now().strftime('%Y-%m-%d %H:%M:%S'),peso,sobras,dieta,diferencia)
        self.cursor.execute(consulta, datos)
        self.conexion.commit()

    def consultar_peso_estable(self,idrat):
        consulta="SELECT pesoestable FROM rat WHERE idrat= %s"
        datos=(idrat,)
        self.cursor.execute(consulta, datos)
        estable=self.cursor.fetchone()
        return int(estable[0])
    
    def consultar_ultima_dieta(self,idrat):
        consulta="SELECT dieta FROM diadieta WHERE idrat=%s ORDER BY fecha DESC LIMIT 1"#Con el order by, se obtienen los ultimos registros y el LIMIT dice cuantos seran
        datos=(idrat,)
        self.cursor.execute(consulta, datos)
        dieta=self.cursor.fetchone()
        return int(dieta[0])

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
    
    def cambiar_fase(self,idrat,fase,peso):
        consulta="UPDATE rat SET fase = %s, pesoestable = %s WHERE idrat = %s"
        datos=(fase,peso,idrat,)
        self.cursor.execute(consulta,datos)
        self.conexion.commit()
    
    def ultimos_registros(self,idrat):
        consulta="SELECT peso FROM diadieta WHERE idrat=%s ORDER BY fecha DESC LIMIT 8"
        datos=(idrat,)
        self.cursor.execute(consulta,datos)
        resultados = self.cursor.fetchall()
        registros=[]
        for resultado in resultados:
            registros.append(int(resultado[0]))
        return registros


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

        self.boton_registrar = tk.Button(self.ventana, text="Resultado",command=self.insertar_dieta)
        self.boton_registrar.pack()
        self.boton_prueba = tk.Button(self.ventana, text="PRUEBA",command=self)
        self.boton_prueba.pack()
        #self.boton_registrar.place(x=170,y=200)

        """self.boton_consultar = tk.Button(self.ventana, text="Reinicio de sujeto", command=self.consultar_ratas)
        self.boton_consultar.place(x=145,y=120)"""

        self.etiqueta_resultado = tk.Label(self.ventana, text="")
        self.etiqueta_resultado.pack()

        self.boton_consultar = tk.Button(self.ventana, text="Limpiar",command=self.limpiar)        
        self.boton_consultar.pack()

        self.boton_consultar = tk.Button(self.ventana, text="Admin")
        self.boton_consultar.place(x=330,y=20)

    def insertar_dieta(self):
        if self.numero_registros()>8:
            fase = self.consultar_fase()
            if fase and int(fase[0]) == 1:
                #Aqui hare el calculo para saber si ya es estable el peso de la rata creando un metodo que mande a llamar los ultimos 6 registros o hasta mas
                registros=self.base_datos.ultimos_registros(self.entry_id.get())
                print ("El resultado de estabilidad es: "+str(self.calcular_estabilidad(registros)))
                if self.calcular_estabilidad(registros):
                    print("Cambiaremos a fase 2")
                    self.base_datos.cambiar_fase(self.entry_id.get(),2,self.entry_peso.get())
                    #Arriba se hace la machaca de fase 1 a 2
                    self.base_datos.insertar_dieta_fase2(self.entry_id.get(),self.entry_peso.get(),self.entry_sobras.get(),15,0)
                    self.etiqueta_resultado.config(text="Por fin estable dale 15gr")
                else:
                    print("Fase 1 dentro del if")
                    self.base_datos.insertar_dieta_fase1(self.entry_id.get(),self.entry_peso.get(),self.entry_sobras.get())
                    self.etiqueta_resultado.config(text="Aun no es estable")
            elif fase and int(fase[0]) == 2:
                print("Estamos en la fase 2")
                pesoEstable=self.base_datos.consultar_peso_estable(self.entry_id.get())
                ultimaDieta=self.base_datos.consultar_ultima_dieta(self.entry_id.get())
                pesoActual=int(self.entry_peso.get())
                diferencia=pesoEstable-pesoActual
                if pesoActual>pesoEstable*.8:
                    if pesoActual>pesoEstable*.85:
                        print('Disminuyo la dieta')
                        dietaIdeal=ultimaDieta-((pesoActual-pesoEstable*.85)/2)#Significa debe bajar peso para estar en el margen
                    else:
                        print('Se mantuvo la dieta')
                        dietaIdeal=ultimaDieta#Significa que esta en el margen
                else:
                    print('Se subio la dieta')
                    dietaIdeal=ultimaDieta-((pesoActual-pesoEstable*.8)/2)#Significa debe subir peso para estar en el margen
                self.base_datos.insertar_dieta_fase2(self.entry_id.get(),self.entry_peso.get(),self.entry_sobras.get(),str(dietaIdeal),diferencia)
                self.etiqueta_resultado.config(text="La dieta de hoy es: "+str(dietaIdeal)+"gr")
        else:
            print("Fase 1 fuera del if")
            self.base_datos.insertar_dieta_fase1(self.entry_id.get(),self.entry_peso.get(),self.entry_sobras.get())
            self.etiqueta_resultado.config(text="Aun no es estable")

    def calcular_estabilidad(self,registros):
        primer= sum(registros[:3])/3
        segundo=sum(registros[3:6])/3
        primerError=abs(((primer-segundo)/(sum(registros[:6])/6))*100)
        print("Primer porcentaje de error "+str(primerError))
        if primerError<=.5:
            tercero=sum(registros[1:4])/3
            cuarto=sum(registros[4:7])/3
            segundoError=abs(((tercero-cuarto)/(sum(registros[1:7])/6))*100)
            print("Segundo porcentaje de error "+str(segundoError))
            if segundoError<=.5:
                quinto=sum(registros[2:5])/3
                sexto=sum(registros[5:8])/3
                tercerError=abs(((quinto-sexto)/(sum(registros[2:8])/6))*100)
                print("Tercer porcentaje de error "+str(tercerError))
                if tercerError<=.5:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False                    

    def insertar_rata(self):#FUNCIONALIDAD de registrar una rata ya esta funcionando
        self.base_datos.insertar_rata(self.entry_id.get())

    def consultar_fase(self):
        fase=self.base_datos.consultar_fase(self.entry_id.get())
        #self.etiqueta_resultado.config(text=fase)
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

import tkinter as tk
import mysql.connector
from datetime import datetime
from PIL import ImageTk, Image
from tkinter import ttk

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

    def insertar_rata_fase(self, idrat,fase,peso):
        try:
            consulta = "INSERT INTO rat (idrat, name,fase,pesoestable) VALUES (%s, %s,%s,%s)"
            datos = (idrat, "rat"+idrat,fase,peso,)
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
        datos = (idrat, datetime.now().strftime('%Y-%m-%d %H:%M:%S'),peso,sobras,dieta,diferencia,)
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
    
    def ultimos_registros_fase2(self,idrat):
        consulta="SELECT dieta FROM diadieta WHERE idrat=%s ORDER BY fecha DESC LIMIT 15"
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

        self.etiqueta_sobras = tk.Label(self.ventana, text="Sobras:")#date.today().strftime('%Y-%m-%d') PARA FECHA
        self.etiqueta_sobras.pack()
        self.entry_sobras = tk.Entry(self.ventana)
        self.entry_sobras.pack()

        self.checkbox_value=tk.BooleanVar(self.ventana)
        self.checkbox=tk.Checkbutton(self.ventana,text="Extra de fin de semana",variable=self.checkbox_value)
        self.checkbox.pack()

        self.combodieta = ttk.Combobox(
            self.ventana,
            state="readonly",
            values=["95%-90%","90%-85%","85%-80%","80%-75%","75%-70%","70%-65%"]
        )
        self.combodieta.current(2)
        self.combodieta.pack()

        self.boton_resultado = tk.Button(self.ventana, text="Resultado",command=self.insertar_dieta)
        self.boton_resultado.pack()

        self.etiqueta_resultado = tk.Label(self.ventana, text="")
        self.etiqueta_resultado.pack()

        self.boton_limpiar = tk.Button(self.ventana, text="Limpiar",command=self.limpiar)        
        self.boton_limpiar.pack()        

        self.boton_admin = tk.Button(self.ventana, text="Admin",command=lambda:self.ventanaLogin(0))
        self.boton_admin.place(x=330,y=20)

    def insertar_dieta(self):
        ##if self.numero_registros()>8:#Se pregunta si tiene mas de 8 registros
            fase = self.consultar_fase()
            dietasetup=self.combodieta.get()
            if (dietasetup)=="95%-90%":
                alto=.95
                bajo=.9
            elif("90%-85%"):
                alto=.9
                bajo=.85
            elif("85%-80%"):
                alto=.85
                bajo=.8
            elif("80%-75%"):
                alto=.8
                bajo=.75
            elif("75%-70%"):
                alto=.75
                bajo=.7
            elif("70%-65%"):
                alto=.7
                bajo=.65
            if fase and int(fase[0]) == 1:
                #Aqui hare el calculo para saber si ya es estable el peso de la rata creando un metodo que mande a llamar los ultimos 6 registros o hasta mas
                registros=self.base_datos.ultimos_registros(self.entry_id.get())
                print ("El resultado de estabilidad es: "+str(self.calcular_estabilidad(registros)))
                if self.calcular_estabilidad(registros):
                    print("Cambiaremos a fase 2")
                    self.base_datos.cambiar_fase(self.entry_id.get(),2,self.entry_peso.get())
                    #Arriba se hace la machaca de fase 1 a 2
                    self.base_datos.insertar_dieta_fase2(self.entry_id.get(),self.entry_peso.get(),self.entry_sobras.get(),15,0)
                    if self.checkbox_value.get():
                        self.etiqueta_resultado.config(text="Por fin estable dale 45gr")
                    else:                        
                        self.etiqueta_resultado.config(text="Por fin estable dale 15gr")
                else:
                    print("Fase 1 dentro del if")
                    self.base_datos.insertar_dieta_fase1(self.entry_id.get(),self.entry_peso.get(),self.entry_sobras.get())
                    self.etiqueta_resultado.config(text="Aun no es estable")
            elif fase and int(fase[0]) == 2:
                print("Estamos en la fase 2")
                if self.calcular_saludfase2(self.entry_id.get(),bajo):#Saber si sigue saludable la rata
                    registros=self.base_datos.ultimos_registros_fase2(self.entry_id.get())
                    registroAntiguo=registros[14]
                    if registroAntiguo == 15:#Se cumplio el tiempo de fase 2
                        print("Cambiaremos a fase 3")   
                        pesoEstable=self.base_datos.consultar_peso_estable(self.entry_id.get())                    
                        pesoActual=int(self.entry_peso.get())
                        diferencia=pesoEstable-pesoActual                                             
                        self.base_datos.cambiar_fase(self.entry_id.get(),3,self.entry_peso.get())
                        #Arriba se hace la machaca de fase 2 a 3
                        self.base_datos.insertar_dieta_fase2(self.entry_id.get(),self.entry_peso.get(),self.entry_sobras.get(),15,diferencia)
                        if self.checkbox_value.get():
                            self.etiqueta_resultado.config(text="Termino fase 2 dale 45gr")
                        else:                        
                            self.etiqueta_resultado.config(text="Termino fase 2 dale 15gr")
                    else:#Aun se matiene en fase 2
                        pesoEstable=self.base_datos.consultar_peso_estable(self.entry_id.get())                    
                        pesoActual=int(self.entry_peso.get())
                        diferencia=pesoEstable-pesoActual
                        self.base_datos.insertar_dieta_fase2(self.entry_id.get(),self.entry_peso.get(),self.entry_sobras.get(),15,diferencia)
                        if self.checkbox_value.get():
                            self.etiqueta_resultado.config(text="Aun en fase 2 dale 45gr")
                        else:                        
                            self.etiqueta_resultado.config(text="Aun en fase 2 dale 15gr")
                else:#en caso de que no este saludable
                    print("Esta bajando demasiado rapido, se sube la dieta y pasa a fase 3")
                    pesoEstable=self.base_datos.consultar_peso_estable(self.entry_id.get())
                    ultimaDieta=self.base_datos.consultar_ultima_dieta(self.entry_id.get())
                    pesoActual=int(self.entry_peso.get())
                    dietaIdeal=int(ultimaDieta-((pesoActual-pesoEstable*bajo)/2))#Significa debe subir peso para estar en el margen
                    self.base_datos.insertar_dieta_fase2(self.entry_id.get(),self.entry_peso.get(),self.entry_sobras.get(),str(dietaIdeal),diferencia)
                    if self.checkbox_value.get():
                        gramosFinde=dietaIdeal*3
                        self.etiqueta_resultado.config(text="La dieta de hoy es: "+str(gramosFinde)+"gr")
                    else:
                        self.etiqueta_resultado.config(text="La dieta de hoy es: "+str(dietaIdeal)+"gr")
            elif fase and int(fase[0])==3:
                print("Estamos en la fase 3")
                pesoEstable=self.base_datos.consultar_peso_estable(self.entry_id.get())
                ultimaDieta=self.base_datos.consultar_ultima_dieta(self.entry_id.get())
                pesoActual=int(self.entry_peso.get())
                diferencia=pesoEstable-pesoActual
                if pesoActual>pesoEstable*bajo:
                    if pesoActual>pesoEstable*alto:
                        print('Disminuyo la dieta')
                        dietaIdeal=int(ultimaDieta-((pesoActual-pesoEstable*alto)/2))#Significa debe bajar peso para estar en el margen
                    else:
                        print('Se mantuvo la dieta')
                        dietaIdeal=ultimaDieta#Significa que esta en el margen
                else:
                    print('Se subio la dieta')
                    dietaIdeal=int(ultimaDieta-((pesoActual-pesoEstable*bajo)/2))#Significa debe subir peso para estar en el margen
                self.base_datos.insertar_dieta_fase2(self.entry_id.get(),self.entry_peso.get(),self.entry_sobras.get(),str(dietaIdeal),diferencia)
                if self.checkbox_value.get():
                    gramosFinde=dietaIdeal*3
                    self.etiqueta_resultado.config(text="La dieta de hoy es: "+str(gramosFinde)+"gr")
                else:
                    self.etiqueta_resultado.config(text="La dieta de hoy es: "+str(dietaIdeal)+"gr")

            """else:#En caso de no tener mas de 8 registros...

                print("Fase 1 fuera del if")
                self.base_datos.insertar_dieta_fase1(self.entry_id.get(),self.entry_peso.get(),self.entry_sobras.get())
                self.etiqueta_resultado.config(text="Aun no es estable")"""

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

    def calcular_saludfase2(self,bajo):
        pesoActual=int(self.entry_peso.get())
        pesoEstable=self.base_datos.consultar_peso_estable(self.entry_id.get())
        if pesoActual < pesoEstable*bajo:
            return False
        else:
            return True

    def insertar_rata(self):#FUNCIONALIDAD de registrar una rata ya esta funcionando
        fase=self.combo.get()
        match fase:
            case "1":
                print("Registro en fase 1")
                self.base_datos.insertar_rata(self.entry_id.get())
            case "2":
                print("Registro en fase 2")
                self.base_datos.insertar_rata_fase(self.entry_id.get(),fase,self.entry_pesoEstable.get())
            case "3":
                print("Registro en fase 3")
                self.base_datos.insertar_rata_fase(self.entry_id.get(),fase,self.entry_pesoEstable.get())
                pesoActual=int(self.entry_peso.get())
                pesoEstable=int(self.entry_pesoEstable.get())
                diferencia=pesoEstable-pesoActual
                self.base_datos.insertar_dieta_fase2(self.entry_id.get(),self.entry_peso.get(),"0",self.entry_dieta.get(),diferencia)                

    def consultar_fase(self):
        fase=self.base_datos.consultar_fase(self.entry_id.get())
        #self.etiqueta_resultado.config(text=fase)
        return fase
    
    def numero_registros(self):
        numero=self.base_datos.numero_registros(self.entry_id.get())
        self.etiqueta_resultado.config(text=numero)
        return numero

    def iniciar_aplicacion(self):
        self.base_datos.conectar()
        self.ventana.mainloop()
        self.base_datos.desconectar()
    
    def ventanaNormal(self):
        #Desaparecer
        self.etiqueta_usuario.pack_forget()
        self.entry_usuario.pack_forget()
        self.etiqueta_pass.pack_forget()
        self.entry_pass.pack_forget()
        self.boton_login.pack_forget()
        self.boton_back_login.place_forget()
        #Aparecer
        self.etiqueta_id.pack()
        self.entry_id.pack()
        self.etiqueta_peso.pack()
        self.entry_peso.pack()
        self.etiqueta_sobras.pack()
        self.entry_sobras.pack()
        self.checkbox.pack()
        self.boton_resultado.pack()
        self.etiqueta_resultado.pack()
        self.boton_limpiar.pack()
        self.boton_admin.place(x=330,y=20)

    def ventanaLogin(self,donde):
        if donde==0:
            #Desaparecer normal
            self.etiqueta_id.pack_forget()
            self.entry_id.pack_forget()
            self.etiqueta_peso.pack_forget()
            self.entry_peso.pack_forget()
            self.etiqueta_sobras.pack_forget()
            self.entry_sobras.pack_forget()
            self.checkbox.pack_forget()
            self.boton_resultado.pack_forget()
            self.etiqueta_resultado.pack_forget()
            self.boton_limpiar.pack_forget()
            self.boton_admin.place_forget()
        else:
            #desaparecen los de ventana admin
            self.etiquetaAdminitrador.pack_forget()
            self.boton_ventanaRegistro.pack_forget()
            self.boton_ventanaReinicio.pack_forget()
            self.boton_back_admin.place_forget()
        #Aparecer
        self.etiqueta_usuario = tk.Label(self.ventana, text="Usuario:")
        self.etiqueta_usuario.pack()
        self.entry_usuario = tk.Entry(self.ventana)
        self.entry_usuario.pack()
        self.etiqueta_pass = tk.Label(self.ventana, text="Password:")
        self.etiqueta_pass.pack()
        self.entry_pass = tk.Entry(self.ventana,show="•")
        self.entry_pass.pack()
        self.boton_login=tk.Button(self.ventana, text="Login",command=lambda:self.ventanaAdmin(0))
        self.boton_login.pack()
        self.boton_back_login = tk.Button(self.ventana, text="Back",command=self.ventanaNormal)
        self.boton_back_login.place(x=330,y=20)

    def ventanaAdmin(self,donde):
        if donde==0:
            #Desaparecer login
            self.etiqueta_usuario.pack_forget()
            self.entry_usuario.pack_forget()
            self.etiqueta_pass.pack_forget()
            self.entry_pass.pack_forget()
            self.boton_login.pack_forget()
            self.boton_back_login.place_forget()
        elif donde==1:
            #Desaparecer Registro
            self.etiqueta_registro.pack_forget()
            self.combo.pack_forget()
            self.etiqueta_id.pack_forget()
            self.entry_id.pack_forget()
            self.etiqueta_pesoEstable.pack_forget()
            self.etiqueta_Add_fase2.pack_forget()
            self.entry_pesoEstable.pack_forget()        
            self.etiqueta_dieta.pack_forget()
            self.etiqueta_Add_fase3.pack_forget()
            self.entry_dieta.pack_forget()
            self.etiqueta_peso.pack_forget()
            self.entry_peso.pack_forget()
            self.boton_registro.pack_forget()
            self.boton_back_registro.place_forget()
        elif donde==2:
            #Desaparece Reinicio
            self.etiqueta_reinicio.pack_forget()
            self.etiqueta_id.pack_forget()
            self.entry_id.pack_forget()
            self.boton_reinicio.pack_forget()            
            self.boton_back_reinicio.place_forget()
        #Aparecer
        self.etiquetaAdminitrador=tk.Label(self.ventana,text="Administrador")
        self.etiquetaAdminitrador.pack()
        self.boton_ventanaRegistro=tk.Button(self.ventana,text="Registrar",command=self.ventanaRegistro)
        self.boton_ventanaRegistro.pack()
        self.boton_ventanaReinicio=tk.Button(self.ventana,text="Reinicio de sujeto",command=self.ventanaReinicio)
        self.boton_ventanaReinicio.pack()
        self.boton_back_admin = tk.Button(self.ventana, text="Back",command=lambda:self.ventanaLogin(1))
        self.boton_back_admin.place(x=330,y=20)

    def ventanaRegistro(self):
        #Desaparecer
        self.etiquetaAdminitrador.pack_forget()
        self.boton_ventanaRegistro.pack_forget()
        self.boton_ventanaReinicio.pack_forget()
        self.boton_back_admin.place_forget()
        #Aparecer
        self.etiqueta_registro=tk.Label(self.ventana,text="Registro de nueva rata seleccionando su fase:")
        self.etiqueta_Add_fase2=tk.Label(self.ventana,text="*Peso estable necesario de fase 2 en adelante")
        self.etiqueta_pesoEstable=tk.Label(self.ventana,text="Peso estable:")
        self.etiqueta_Add_fase3=tk.Label(self.ventana,text="*Dieta necesaria de fase 3 en adelante")
        self.etiqueta_dieta=tk.Label(self.ventana,text="Dieta:")
        self.entry_pesoEstable = tk.Entry(self.ventana)
        self.entry_dieta = tk.Entry(self.ventana)
        self.combo = ttk.Combobox(
            self.ventana,
            state="readonly",
            values=["1", "2", "3"]
        )        
        self.etiqueta_registro.pack()
        self.combo.pack()
        self.etiqueta_id.pack()
        self.entry_id.pack()        
        self.etiqueta_pesoEstable.pack()
        self.etiqueta_Add_fase2.pack()
        self.entry_pesoEstable.pack()        
        self.etiqueta_dieta.pack()
        self.etiqueta_Add_fase3.pack()
        self.entry_dieta.pack()
        self.etiqueta_peso.pack()
        self.entry_peso.pack()
        self.boton_registro=tk.Button(self.ventana,text="Registrar",command=self.insertar_rata)
        self.boton_registro.pack()
        self.boton_back_registro = tk.Button(self.ventana, text="Back",command=lambda:self.ventanaAdmin(1))
        self.boton_back_registro.place(x=330,y=20)

    def ventanaReinicio(self):
        #Desaparecer
        self.etiquetaAdminitrador.pack_forget()
        self.boton_ventanaRegistro.pack_forget()
        self.boton_ventanaReinicio.pack_forget()
        self.boton_back_admin.place_forget()
        #Aparecer
        self.etiqueta_reinicio=tk.Label(self.ventana,text="Reinicio de fase en rata")
        self.etiqueta_reinicio.pack()
        self.etiqueta_id.pack()
        self.entry_id.pack()
        self.boton_reinicio=tk.Button(self.ventana,text="Reiniciar",command=self.reiniciar_fase)
        self.boton_reinicio.pack()
        self.boton_back_reinicio = tk.Button(self.ventana, text="Back",command=lambda:self.ventanaAdmin(2))
        self.boton_back_reinicio.place(x=330,y=20)
        
    def reiniciar_fase(self):
        self.base_datos.cambiar_fase(self.entry_id.get(),1,0)

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

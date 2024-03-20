import tkinter as tk
import mysql.connector
import hashlib
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
        datos = (idrat, datetime.now().strftime('%Y-%m-%d %H:%M:%S'),peso,str(sobras),)
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
        return float(estable[0])
    
    def consultar_ultima_dieta(self,idrat):
        consulta="SELECT dieta FROM diadieta WHERE idrat=%s ORDER BY fecha DESC LIMIT 1"#Con el order by, se obtienen los ultimos registros y el LIMIT dice cuantos seran
        datos=(idrat,)
        self.cursor.execute(consulta, datos)
        dieta=self.cursor.fetchone()
        if dieta[0] is not None: #Excepcion para poder regresar tipo float aunque sea null
            return float(dieta[0])
        else:
            return 0.0
        ##return float(dieta[0])

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
            registros.append(float(resultado[0]))
        return registros
    
    def ultimos_registros_fase2(self,idrat):
        consulta="SELECT dieta FROM diadieta WHERE idrat=%s ORDER BY fecha DESC LIMIT 15"
        datos=(idrat,)
        self.cursor.execute(consulta,datos)
        resultados = self.cursor.fetchall()
        registros=[]
        for resultado in resultados:
            registros.append(resultado[0])
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
        self.ventana.resizable(width=False, height=False)

        self.imagen=Image.open("_internal/logo.png")
        self.imagen = self.imagen.resize((150, 110))
        self.photo = ImageTk.PhotoImage(self.imagen)
        self.label_imagen = tk.Label(self.ventana, image=self.photo)
        self.label_imagen.place(x=-25,y=190)

        self.etiqueta_id = tk.Label(self.ventana, text="ID:")
        self.etiqueta_id.pack()
        self.entry_id = tk.Entry(self.ventana)
        self.entry_id.pack()
        self.entry_id.bind("<Key>", self.on_key_press)
        self.entry_id.bind("<KeyRelease>", self.actualizar_estado_boton_main)

        self.etiqueta_peso = tk.Label(self.ventana, text="Peso:")#date.today().strftime('%Y-%m-%d') PARA FECHA
        self.etiqueta_peso.pack()
        self.entry_peso = tk.Entry(self.ventana)
        self.entry_peso.pack()
        self.entry_peso.bind("<Key>", self.on_key_press)
        self.entry_peso.bind("<KeyRelease>", self.actualizar_estado_boton_main)

        self.etiqueta_sobras = tk.Label(self.ventana, text="Sobras:")#date.today().strftime('%Y-%m-%d') PARA FECHA
        self.etiqueta_sobras.pack()
        self.entry_sobras = tk.Entry(self.ventana)
        self.entry_sobras.pack()
        self.entry_sobras.bind("<Key>", self.on_key_press)

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

        self.boton_resultado = tk.Button(self.ventana, text="Resultado",state="disabled",command=self.insertar_dieta)
        self.boton_resultado.pack()

        self.etiqueta_resultado = tk.Label(self.ventana, text="")
        self.etiqueta_resultado.pack()

        self.boton_limpiar = tk.Button(self.ventana, text="Limpiar",command=self.limpiar)        
        self.boton_limpiar.pack()        

        self.boton_admin = tk.Button(self.ventana, text="Admin",command=lambda:self.ventanaLogin(0))
        self.boton_admin.place(x=330,y=20)

    def insertar_dieta(self):
        if self.numero_registros()>8:#Se pregunta si tiene mas de 8 registrosx
            fase = self.consultar_fase()
            dietasetup=self.combodieta.get()
            #Quitar el combobox de la dietasetup
            if (dietasetup)=="95%-90%":
                alto=.95
                bajo=.9
            elif(dietasetup)=="90%-85%":
                alto=.9
                bajo=.85
            elif(dietasetup)=="85%-80%":
                alto=.85
                bajo=.8
            elif(dietasetup)=="80%-75%":
                alto=.8
                bajo=.75
            elif(dietasetup)=="75%-70%":
                alto=.75
                bajo=.7
            elif(dietasetup)=="70%-65%":
                alto=.7
                bajo=.65
            print("alto"+str(alto)+" bajo"+str(bajo))
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
                if self.calcular_saludfase2(bajo):#Saber si sigue saludable la rata
                    registros=self.base_datos.ultimos_registros_fase2(self.entry_id.get())
                    numeroDeArray = self.numero_registros() - 1 if self.numero_registros() < 14 else 14
                    registroAntiguo=registros[numeroDeArray]
                    if registroAntiguo == 15:#Se cumplio el tiempo de fase 2
                        print("Cambiaremos a fase 3")   
                        pesoEstable=self.base_datos.consultar_peso_estable(self.entry_id.get())                    
                        pesoActual=float(self.entry_peso.get())
                        diferencia=pesoEstable-pesoActual                                             
                        self.base_datos.cambiar_fase(self.entry_id.get(),3,pesoEstable)
                        #Arriba se hace la machaca de fase 2 a 3
                        self.base_datos.insertar_dieta_fase2(self.entry_id.get(),self.entry_peso.get(),self.entry_sobras.get(),15,diferencia)
                        if self.checkbox_value.get():
                            self.etiqueta_resultado.config(text="Termino fase 2 dale 45gr")
                        else:                        
                            self.etiqueta_resultado.config(text="Termino fase 2 dale 15gr")
                    else:#Aun se matiene en fase 2
                        pesoEstable=self.base_datos.consultar_peso_estable(self.entry_id.get())                    
                        pesoActual=float(self.entry_peso.get())
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
                    pesoActual=float(self.entry_peso.get())
                    diferencia=pesoEstable-pesoActual
                    self.base_datos.cambiar_fase(self.entry_id.get(),3,pesoEstable)
                    dietaIdeal=float(ultimaDieta-((pesoActual-pesoEstable*bajo)/2))#Significa debe subir peso para estar en el margen
                    if dietaIdeal>=20:
                        dietaIdeal=20
                    elif dietaIdeal<=8:
                        dietaIdeal=8
                    self.base_datos.insertar_dieta_fase2(self.entry_id.get(),self.entry_peso.get(),self.entry_sobras.get(),str(dietaIdeal),diferencia)
                    if self.checkbox_value.get():
                        gramosFinde=dietaIdeal*3
                        self.etiqueta_resultado.config(text="La dieta de hoy es: "+str(round(gramosFinde,1))+"gr")
                    else:
                        self.etiqueta_resultado.config(text="La dieta de hoy es: "+str(round(dietaIdeal,1))+"gr")
            elif fase and int(fase[0])==3:
                print("Estamos en la fase 3")
                pesoEstable=self.base_datos.consultar_peso_estable(self.entry_id.get())
                ultimaDieta=self.base_datos.consultar_ultima_dieta(self.entry_id.get())
                pesoActual=float(self.entry_peso.get())
                diferencia=pesoEstable-pesoActual
                if pesoActual>pesoEstable*bajo:
                    if pesoActual>pesoEstable*alto:
                        print('Disminuyo la dieta')
                        dietaIdeal=float(ultimaDieta-((pesoActual-(pesoEstable*alto))/2))#Significa debe bajar peso para estar en el margen
                    else:
                        print('Se mantuvo la dieta')
                        dietaIdeal=ultimaDieta#Significa que esta en el margen
                else:
                    print('Se subio la dieta')
                    dietaIdeal=float(ultimaDieta-((pesoActual-(pesoEstable*bajo))/2))#Significa debe subir peso para estar en el margen
                #
                #Tope maximo y minimo de dieta, minimo sera 8 y maximo 20
                #
                if dietaIdeal>=20:
                    dietaIdeal=20
                elif dietaIdeal<=8:
                    dietaIdeal=8
                #Fin de bloqueo de dieta para no llegar a extremos
                self.base_datos.insertar_dieta_fase2(self.entry_id.get(),self.entry_peso.get(),self.entry_sobras.get(),str(dietaIdeal),diferencia)
                if self.checkbox_value.get():
                    gramosFinde=dietaIdeal*3
                    self.etiqueta_resultado.config(text="La dieta de hoy es: "+str(round(gramosFinde,1))+"gr")
                else:
                    self.etiqueta_resultado.config(text="La dieta de hoy es: "+str(round(dietaIdeal,1))+"gr")
        else:#En caso de no tener mas de 8 registros...

            print("Fase 1 fuera del if")
            self.base_datos.insertar_dieta_fase1(self.entry_id.get(),self.entry_peso.get(),self.entry_sobras.get())
            self.etiqueta_resultado.config(text="Aun no es estable")

    def calcular_estabilidad(self,registros):
        primer= sum(registros[:3])/3
        segundo=sum(registros[3:6])/3
        primerError=abs(((primer-segundo)/(sum(registros[:6])/6))*100) #DA ERROR-----creo que ya no da error... 
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
        pesoActual=float(self.entry_peso.get())
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
                pesoActual=float(self.entry_peso.get())
                pesoEstable=float(self.entry_pesoEstable.get())
                diferencia=pesoEstable-pesoActual
                self.base_datos.insertar_dieta_fase2(self.entry_id.get(),self.entry_peso.get(),"0",self.entry_dieta.get(),diferencia)                

    def consultar_fase(self):
        fase=self.base_datos.consultar_fase(self.entry_id.get())
        return fase
    
    def numero_registros(self):
        numero=self.base_datos.numero_registros(self.entry_id.get())
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
        self.entry_id.bind("<KeyRelease>", self.actualizar_estado_boton_main)
        self.entry_id.pack()
        self.etiqueta_peso.pack()
        self.entry_peso.bind("<KeyRelease>", self.actualizar_estado_boton_main)
        self.entry_peso.pack()
        self.etiqueta_sobras.pack()
        self.entry_sobras.pack()
        self.checkbox.pack()
        self.combodieta.pack()
        self.combodieta.current(2)
        self.boton_resultado = tk.Button(self.ventana, text="Resultado",state="disabled",command=self.insertar_dieta)
        self.boton_resultado.pack()
        self.etiqueta_resultado.pack()
        self.boton_limpiar.pack()
        self.boton_admin.place(x=330,y=20)
        self.limpiar()

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
            self.combodieta.pack_forget()
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
        self.etiqueta_usuario.pack(pady=10)
        self.entry_usuario = tk.Entry(self.ventana)
        self.entry_usuario.pack(pady=10)
        self.etiqueta_pass = tk.Label(self.ventana, text="Password:")
        self.etiqueta_pass.pack(pady=10)
        self.entry_pass = tk.Entry(self.ventana,show="•")
        self.entry_pass.pack(pady=10)
        self.boton_login=tk.Button(self.ventana, text="Login",command=lambda:(self.login(self.entry_usuario.get(),self.entry_pass.get())))
        self.boton_login.pack(pady=10)
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
        self.etiquetaAdminitrador.pack(pady=10)
        self.boton_ventanaRegistro=tk.Button(self.ventana,text="Registrar",command=self.ventanaRegistro)
        self.boton_ventanaRegistro.pack(pady=10)
        self.boton_ventanaReinicio=tk.Button(self.ventana,text="Reinicio de sujeto",command=self.ventanaReinicio)
        self.boton_ventanaReinicio.pack(pady=10)
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
        self.combo.bind("<<ComboboxSelected>>", self.actualizar_estado_boton)
        self.etiqueta_registro.pack()
        self.combo.pack()
        self.etiqueta_id.pack()
        self.entry_id.pack()
        self.entry_id.bind("<KeyRelease>", self.actualizar_estado_boton)        
        self.etiqueta_pesoEstable.pack()
        self.etiqueta_Add_fase2.pack()
        self.entry_pesoEstable.pack()   
        self.entry_pesoEstable.bind("<Key>", self.on_key_press)
        self.entry_pesoEstable.bind("<KeyRelease>", self.actualizar_estado_boton)     
        self.etiqueta_dieta.pack()
        self.etiqueta_Add_fase3.pack()
        self.entry_dieta.pack()
        self.entry_dieta.bind("<Key>", self.on_key_press)
        self.entry_dieta.bind("<KeyRelease>", self.actualizar_estado_boton)
        self.etiqueta_peso.pack()
        self.entry_peso.pack()
        self.entry_peso.bind("<KeyRelease>", self.actualizar_estado_boton)
        self.boton_registro=tk.Button(self.ventana,text="Registrar",state="disabled",command=lambda:(self.insertar_rata(),self.ventanaAdmin(1)))
        self.boton_registro.pack()
        self.boton_back_registro = tk.Button(self.ventana, text="Back",command=lambda:self.ventanaAdmin(1))
        self.boton_back_registro.place(x=330,y=20)
        self.limpiar()

    def actualizar_estado_boton(self, event=None): #Funcion que inhabilita el boton si no tiene datos los txt
        fasecombo = self.combo.get()
        id = self.entry_id.get().strip()
        peso = self.entry_peso.get().strip()
        pesoEstable = self.entry_pesoEstable.get().strip()
        dieta = self.entry_dieta.get().strip()

        if fasecombo == "1":
            if id:
                self.boton_registro.config(state="normal")
            else:
                self.boton_registro.config(state="disabled")
        elif fasecombo == "2":
            if pesoEstable:
                self.boton_registro.config(state="normal")
            else:
                self.boton_registro.config(state="disabled")
        elif fasecombo == "3":
            if peso and dieta:
                self.boton_registro.config(state="normal")
            else:
                self.boton_registro.config(state="disabled")
    
    def actualizar_estado_boton_main(self, event=None): #Funcion que inhabilita el boton si no tiene datos los txt
        id = self.entry_id.get().strip()
        peso = self.entry_peso.get().strip()
        if id and peso:
            self.boton_resultado.config(state="normal")
        else:
            self.boton_resultado.config(state="disabled")

    
    def ventanaReinicio(self):
        #Desaparecer
        self.etiquetaAdminitrador.pack_forget()
        self.boton_ventanaRegistro.pack_forget()
        self.boton_ventanaReinicio.pack_forget()
        self.boton_back_admin.place_forget()
        #Aparecer
        self.etiqueta_reinicio=tk.Label(self.ventana,text="Reinicio de fase en rata")
        self.etiqueta_reinicio.pack(pady=10)
        self.etiqueta_id.pack(pady=10)
        self.entry_id.pack(pady=10)
        self.boton_reinicio=tk.Button(self.ventana,text="Reiniciar",command=lambda:(self.reiniciar_fase(),self.ventanaAdmin(2)))
        self.boton_reinicio.pack(pady=10)
        self.boton_back_reinicio = tk.Button(self.ventana, text="Back",command=lambda:self.ventanaAdmin(2))
        self.boton_back_reinicio.place(x=330,y=20)
        self.limpiar()
        
    def reiniciar_fase(self):
        self.base_datos.cambiar_fase(self.entry_id.get(),1,0)

    def limpiar(self):
        self.entry_id.delete(0,tk.END)
        self.entry_peso.delete(0,tk.END)
        self.entry_sobras.delete(0,tk.END)
        self.combodieta.current(2)
        self.etiqueta_resultado.config(text="")

    def limpiarLogin(self):
        self.entry_usuario.delete(0,tk.END)
        self.entry_pass.delete(0,tk.END)

    #Funcion evento que evita meter letras
    def on_key_press(self,event):
        try:
            char = event.char
            if char.isalpha():
                return "break"
        except Exception as e:
            print("Error:", e)

    #Funcion que verifica el login
    def login(self,user,password):
        bytes = user.encode('utf-8')
        hasher = hashlib.sha256()
        hasher.update(bytes)
        hash_encriptado = hasher.hexdigest()
        if hash_encriptado=="b2dcf6868bf33bf09d13ead90ff0a998883066cec333f1b9869aa86965e7cb7e":
            bytespass = password.encode('utf-8')
            hasherpass = hashlib.sha256()
            hasherpass.update(bytespass)
            hash_encriptadopass = hasherpass.hexdigest()
            if hash_encriptadopass=="a4e7c6ae4013276deabc1be4f9c65a6dc382f317e0cb81497aba26915cde5b66":
                self.ventanaAdmin(0)
        self.limpiarLogin()
        
        

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
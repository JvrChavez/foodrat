import mysql.connector as mariadb
# decodigo.com
def consultar():
    mariadb_conexion = mariadb.connect(host='localhost', port='3307',user='root', password='', database='foodrat')
    mycursor = mariadb_conexion.cursor()
    try:
        mycursor.execute("SELECT * FROM diadieta")
        for idrat, fecha, peso, sobras,dieta,diferencia  in mycursor:
            print("id: " + str(idrat))
            print("fecha: " + str(fecha))
            print("peso: " + str(peso))
            print("sobras: " + str(sobras))
            print("dieta: "+str(dieta))
            print("diferenia: "+str(diferencia)+"\n")
    except mariadb.Error as error:
        print("Error: {}".format(error))
    mariadb_conexion.close()
def ingresar():
    mariadb_conexion = mariadb.connect(host='localhost',port='3307',user='root',password='',database='foodrat')
    mycursor = mariadb_conexion.cursor()
    print("Ingresa tu id")
    id=input()
    print("Ingresa fecha")
    fecha=input()
    print("Ingresa peso")
    peso=input()
    print("Ingresa sobras")
    sobras=input()
    print("Ingresa dieta")
    dieta=input()
    print("Ingresa diferencia")
    diferencia=input()
    try: 
        query="INSERT INTO diadieta (idrat,fecha,peso,sobras,dieta,diferencia) VALUES (%s,%s,%s,%s,%s,%s)"
        values=(int(id),fecha,int(peso),int(sobras),int(dieta),int(diferencia))
        print("Resulado query,values")
        print(query,values)
        mycursor.execute(query,values)
        print(f"{mycursor.rowcount}, details inserted")
    except mariadb.Error as e:
        print(f"Error: {e}")
    mariadb_conexion.commit()
    mariadb_conexion.close()
def consultarEstabilidad(idratconsult):
    mariadb_conexion = mariadb.connect(host='localhost', port='3307',user='root', password='', database='foodrat')
    mycursor = mariadb_conexion.cursor()
    try:
        query="SELECT fase FROM rat WHERE idrat=%s"
        values=(idratconsult,)
        mycursor.execute(query,values)
        #myresult=mycursor.fetchall()
        for fase in mycursor:        
            print(f"La estabilidad de la rata con id: {idratconsult}, es {fase[0]}")
    except mariadb.Error as error:
        print("Error: {}".format(error))
    mariadb_conexion.close()

switch=input("1.- Dieta diaria\n2.- Registrar nueva rata\n3.- Consultar estabilidad\n")
match switch:
    case "1":
        print("Dieta diaria")
        ingresar()
    case "2":
        print("Registrar nueva rata")
    case "3":
        inputidRat=input("Consultar estabilidad de la rata:")
        consultarEstabilidad(inputidRat)
    case _:
        print("No escogio una opcion")
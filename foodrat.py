from tkinter import *
from tkinter import messagebox
ventana=Tk()
ventana.geometry("800x400")


def calularDieta():
    #Para subir
    #si(peso<=80%, dieta+(dif/2),dieta)
    #Para bajar
    #si(peso>=85%, dieta+(dif/2),dieta)
    #la diferencia es 80% menos el peso actual
    peso=int(inPeso.get())
    dieta=int(inDieta.get())
    estable=int(inEstable.get())
    dif8=abs(estable*.8-peso)
    dif85=abs(estable*.85-peso)
    print(estable*.8)
    print(dif8)
    print(dif85)
    if(peso<=(estable*.8)):#subir
        print("if")
        lblPorcRes["text"]=str(dieta+(dif8/2))
    elif(peso>=(estable*.85)):
        print("elif")
        lblPorcRes["text"]=str(dieta-(dif85/2))
    else:
        print("else")
        lblPorcRes["text"]=dieta
#Fase 1
headF1=Label(ventana,text="Fase 1")
lblRatF1=Label(ventana,text="Rata:")
lblPesoF1=Label(ventana,text="Peso:")
lblTempF1=Label(ventana,text="Temperatura:")
lblFoodF1=Label(ventana,text="Comida sobrante:")
inRatF1=Entry(ventana)
inPesoF1=Entry(ventana)
inTempF1=Entry(ventana)
inFoodF1=Entry(ventana)

#Fase2
head=Label(ventana,text="Fase 2")
lblRat=Label(ventana,text="Rata:")#Labels
lblPeso=Label(ventana,text="Peso *:")
lblDia=Label(ventana,text="Dia :")
lblTemp=Label(ventana,text="Temperatura :")
lblFood=Label(ventana,text="Comida :")
lblPorc=Label(ventana,text="Porcentaje :")
lblPorcRes=Label(ventana,text="hola")
inRat=Entry(ventana)#Entrys
inPeso=Entry(ventana)
inDia=Entry(ventana)
inTemp=Entry(ventana)
inFood=Entry(ventana)
btn=Button(ventana,text="Done",command=calularDieta)

def verFase1():
    borrarFase2()
    headF1.place(x=75,y=25)
    lblRatF1.place(x=50,y=50)
    inRatF1.place(x=150,y=50)
    lblPesoF1.place(x=50,y=75)
    inPesoF1.place(x=150,y=75)
    lblTempF1.place(x=50,y=100)
    inTempF1.place(x=150,y=100)
    lblFood.place(x=50,y=125)
    inFoodF1.place(x=150,y=125)    
def BorrarFase1():
    headF1.place_forget()
    lblRatF1.place_forget()
    inRatF1.place_forget()
    lblPesoF1.place_forget()
    inPesoF1.place_forget()
    lblTempF1.place_forget()
    inTempF1.place_forget()
    lblFood.place_forget()
    inFoodF1.place_forget()
def verFase2():
    BorrarFase1()
    head.place(x=75,y=25)
    lblRat.place(x=50,y=50)
    inRat.place(x=150,y=50)
    lblPeso.place(x=50,y=75)
    inPeso.place(x=150,y=75)
    lblDia.place(x=50,y=100)
    inDia.place(x=150,y=100)
    lblTemp.place(x=50,y=125)
    inTemp.place(x=150,y=125)
    lblFood.place(x=50,y=150)
    inFood.place(x=150,y=150)
    lblPorc.place(x=50,y=210)
    lblPorcRes.place(x=150,y=210)
    btn.place(x=200,y=175)
def borrarFase2():
    head.place_forget()
    lblRat.place_forget()
    inRat.place_forget()
    lblPeso.place_forget()
    inPeso.place_forget()
    lblDia.place_forget()
    inDia.place_forget()
    lblTemp.place_forget()
    inTemp.place_forget()
    lblFood.place_forget()
    inFood.place_forget()
    btn.place_forget()
    lblPorc.place_forget()
    lblPorcRes.place_forget()

btnBorrarF1=Button(ventana,text="Borrar Fase 1",command=BorrarFase1)
btnBorrarF1.place(x=150,y=300)
btnVerF1=Button(ventana,text="Ver Fase 1",command=verFase1)
btnVerF1.place(x=150,y=330)
btnBorrarF2=Button(ventana,text="Borrar Fase 2",command=borrarFase2)
btnBorrarF2.place(x=300,y=300)
btnVerF2=Button(ventana,text="Ver Fase 2",command=verFase2)
btnVerF2.place(x=300,y=330)

#Datos de la base
headBase=Label(ventana,text="Datos de la base...")
lblPesoAnt=Label(ventana,text="Peso anterior:")
lblEstable=Label(ventana,text="100% de peso:")
lblDieta=Label(ventana,text="Dieta:")
inPesoAnt=Entry(ventana)
inEstable=Entry(ventana)
inDieta=Entry(ventana)
headBase.place(x=400,y=25)#places
lblEstable.place(x=400,y=50)
inEstable.place(x=550,y=50)
lblPesoAnt.place(x=400,y=75)
inPesoAnt.place(x=550,y=75)
lblDieta.place(x=400,y=100)
inDieta.place(x=550,y=100)

ventana.mainloop()
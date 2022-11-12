import tkinter
from datetime import date
from tkinter import *
from tkinter import messagebox
from tkinter import ttk #para tener más opciones
import pandas as pd #se importa pandas y le digo que es pd

today = date.today() #Obtiene la fecha del día de hoy, gracias a una libreria DateTime
main = Tk()
main.title("Programa ABCC")

fechaAlta = date.today()
fechaBaja = today.strftime("%Y-%m-%d")

#######################FUNCIONES######################
def Alta ():
    #Este if, me ayuda a validar los controles que no esten vacios para que no me de error el sistema
    if e1.get() and e2.get() and e3.get() and e4.get() and e5.get() and e6.get() and e7.get() and e8.get() and e9.get():
        print("se lleno completamente")

        # Se cambio el AND por OR para que una vez que salga el mensaje de limites de digitos sea por que un entry no cumplio
        # con lim, en ves de que sea necesario llenar todos los entrys
        if len(e1.get()) > 6 or len(e2.get()) > 15 or len(e3.get()) > 15 or len(e4.get()) > 20 \
                or len(e8.get()) > 9 or len(e9.get()) > 9:
            messagebox.showinfo("Informacion importante",
                                "Se recomienda cumplir con el limite de los siguientes datos por favor.\n"
                                "- Sku: 6 digitos max\n"
                                "- Articulo: 15 digitos max\n"
                                "- Marca: 15 digitos max\n"
                                "- Modelo: 20 digitos max\n"
                                "- Stock: 9 digitos max \n"
                                "- Cantidad: 9 digitos max")
        else:

            if int(e9.get()) > int(e8.get()):
                messagebox.showinfo("Nope", "No se puede por que la cantidad no debe ser mayor al stock")
            else:
                # Se da de alta los datos, el read lee el fiechero para así dar uso de insertar datos con el append
                dfArticulos = pd.read_csv("JollyRancher.csv",
                                          delimiter=",")  # Se creo un dataframe, basicamente se creo una tabla proveniente de excel a python
                dfArticulos = dfArticulos.append(pd.Series(
                    [e1.get(), e2.get(), e3.get(), e4.get(), e5.get(), e6.get(), e7.get(), e9.get(), e8.get(),
                     fechaAlta, 0,
                     "1900-01-01"], index=dfArticulos.columns),
                    ignore_index=True)  # esta linea, agrega datos de columnas

                # Para borrar al momento de ingresar y dar alta los datos
                e1.delete(0, END)
                e2.delete(0, END)
                e3.delete(0, END)
                e4.delete(0, END)
                e5.set("") # me limpia la lista para que no muestre nada en los entrys y que no se queden los datos ahí flotando
                e6.set("")
                e7.set("")
                e8.delete(0, END)
                e9.delete(0, END)

                dfArticulos.to_csv('JollyRancher.csv',
                                   index=False)  # index = false lo que hace, evita que se haga espacio blanco en las celdas de excel
                print(dfArticulos.head())

                messagebox.showinfo("Datos dados de alta", "Se ha subido los datos existosamente!")
    else:
        messagebox.showinfo("Datos incompletos", "Falta campos por rellenar, por favor verifique bien los datos.")

def Baja ():
    dfArticulos = pd.read_csv("JollyRancher.csv", delimiter=",")
    resp = messagebox.askyesno("¿Estas seguro?", "¿Quieres eliminar este Sku?")
    if resp:
        print("Si vas a eliminar")
        dfArticulos = dfArticulos[dfArticulos["Sku"] != int(e1.get())] #Lo que hace, es buscar todos los valores que no son igual al Sku solicitado hacinedo que se borre

        e2.delete(0, END)
        e3.delete(0, END)
        e4.delete(0, END)
        e8.delete(0, END)
        e9.delete(0, END)

        b2["state"] = DISABLED
        b3["state"] = DISABLED

        dfArticulos.to_csv('JollyRancher.csv',index=False) #Para guardar
    else:
        messagebox.showinfo("Entendido", "Este Sku no será eliminado.")



def Cambio():
    print("cambio")
    dfArticulos = pd.read_csv("JollyRancher.csv", delimiter=",")

    #Para ingresar los nuevos datos

    #Se localiza en la tabla el sku solicitado y se cambia el articulo con el sku
    dfArticulos.loc[dfArticulos["Sku"] == int(e1.get()),"Articulo"] = e2.get()
    dfArticulos.loc[dfArticulos["Sku"] == int(e1.get()),"Marca"] = e3.get()
    dfArticulos.loc[dfArticulos["Sku"] == int(e1.get()),"Modelo"] = e4.get()
    dfArticulos.loc[dfArticulos["Sku"] == int(e1.get()),"Departamento"] = e5.get()
    dfArticulos.loc[dfArticulos["Sku"] == int(e1.get()),"Clase"] = e6.get()
    dfArticulos.loc[dfArticulos["Sku"] == int(e1.get()),"Familia"] = e7.get()
    dfArticulos.loc[dfArticulos["Sku"] == int(e1.get()),"Stock"] = e8.get()
    dfArticulos.loc[dfArticulos["Sku"] == int(e1.get()),"Cantidad"] = e9.get()
    dfArticulos.loc[dfArticulos["Sku"] == int(e1.get()),"Descontinuado"] = Checkbox.get()

    if Checkbox.get() == 1:
        dfArticulos.loc[dfArticulos["Sku"] == int(e1.get()),"Fecha Baja"] = today
    else:
        dfArticulos.loc[dfArticulos["Sku"] == int(e1.get()), "Fecha Baja"] = "1900-01-01"


    messagebox.showinfo("Cambio realizado", "Se ha hecho el cambio.")
    dfArticulos.to_csv('JollyRancher.csv', index=False) #Para guardar

    # Para limpiar los ENTRYS para así dejarlos en blancos e ingresar los nuevos datos
    e2.delete(0, END)
    e3.delete(0, END)
    e4.delete(0, END)
    e5.set("")  # me limpia la lista para que no muestre nada en los entrys y que no se queden los datos ahí flotando
    e6.set("")
    e7.set("")
    e8.delete(0, END)
    e9.delete(0, END)
    eFechaBaja.delete("1.0",END)
    eFechaAlta.delete("1.0",END)

def Consulta():
    dfArticulos = pd.read_csv("JollyRancher.csv", delimiter=",")

    if e1.get(): #Checar que se haya introducido un Sku

        # En dfArticulos, para ser más especifico en la busqueda, se le inserta [] y dentro el nombre de lo que se quiere buscar.
        if int(e1.get()) not in dfArticulos[
            "Sku"].values:  # Si no se encuentra dentro de mi DATAFRAME que viene siendo dfArticulos hara lo siguiente

            e2["state"] = NORMAL
            e3["state"] = NORMAL
            e4["state"] = NORMAL
            e5["state"] = NORMAL
            e6["state"] = DISABLED
            e7["state"] = DISABLED
            e8["state"] = NORMAL
            e9["state"] = NORMAL

            # Para borrar al momento de ingresar y dar alta los datos, el sku se queda por que se le va dar de alta
            e2.delete(0, END)
            e3.delete(0, END)
            e4.delete(0, END)
            # e5.delete(0, END)
            # e6.delete(0, END)
            # e7.delete(0, END)
            e8.delete(0, END)
            e9.delete(0, END)

            b1["state"] = NORMAL
            b2["state"] = DISABLED
            b3["state"] = DISABLED

        else:

            print(dfArticulos.loc[dfArticulos["Sku"] == int(
                e1.get())])  # Se busca en la base de datos con el dataframe por el SKU :D

            # Habilitar los entrys de cada widget
            e2["state"] = NORMAL
            e3["state"] = NORMAL
            e4["state"] = NORMAL
            e5["state"] = NORMAL
            e6["state"] = NORMAL
            e7["state"] = NORMAL
            e8["state"] = NORMAL
            e9["state"] = NORMAL
            e10["state"] = NORMAL
            eFechaBaja["state"] = NORMAL
            eFechaAlta["state"] = NORMAL

            # Hace que aparezca los datos en los entrys al verificar que el sku existe, mas que nada, los rellena con los datos ya existentes.#

            Busqueda = dfArticulos.loc[dfArticulos["Sku"] == (
                int(e1.get()))]  # lo que hace es guiarse con el sku para así encontrar los demás datos

            # Para borrar al momento de ingresar y dar alta los datos
            e2.delete(0, END)
            e3.delete(0, END)
            e4.delete(0, END)
            e8.delete(0, END)
            e9.delete(0, END)
            eFechaBaja.delete(1.0, END)
            eFechaAlta.delete(1.0, END)

            # El .loc esta buscando desde la posicion 0 el valor de la columna establecida, iloc es para buscar por posicion, es el que mejor jalo
            e2.insert(0, Busqueda.iloc[0]["Articulo"])
            e3.insert(0, Busqueda.iloc[0]["Marca"])
            e4.insert(0, Busqueda.iloc[0]["Modelo"])
            e5.set(Busqueda.iloc[0]["Departamento"])  # El set lo establece, pone el valor como dice su nombre
            e6.set(Busqueda.iloc[0]["Clase"])
            e7.set(Busqueda.iloc[0]["Familia"])
            e8.insert(0, Busqueda.iloc[0]["Stock"])
            e9.insert(0, Busqueda.iloc[0]["Cantidad"])
            ################Para activar o desactivar el checbox##############
            if Busqueda.iloc[0]['Descontinuado'] == 1:
                e10.select()
            elif Busqueda.iloc[0]['Descontinuado'] == 0:
                e10.deselect()
            ##################################################################
            eFechaBaja.insert(END, Busqueda.iloc[0]["Fecha Baja"])
            eFechaAlta.insert(END, Busqueda.iloc[0]["Fecha Alta"])

            # Habilitar los botones BAJA Y CAMBIO, DESABILITAR ALTA porque ya existe
            b1["state"] = DISABLED
            b2["state"] = NORMAL
            b3["state"] = NORMAL
    else:
        messagebox.showinfo("Sku no introducido", "Por favor introduce un Sku para hacer la consulta.")



##################Funciones para activar los botonoes de dropbox y hacer la busqueda y enlace######################
#Nombre Depa busca Numero Depa -> Numero Depa busca Nombre Clase -> Nombre Clase busca Numero Clase -> Numero Clase busca Nombre Familia
def activarClase(self):
    e6["state"] = NORMAL
    TablaClase = pd.read_csv("Clase.csv", delimiter=",") #se lee el archivo de Clase.csv
    TablaDepa = pd.read_csv("Departamentos.csv", delimiter=",")

    #Se neceista este codigo para hacer que lo que dropea de Depa, suelte las opciones de Depa.
    BusqNumDep = TablaDepa[TablaDepa["Nombre Depa"] == (e5.get())] #Se esta flitrando para buscar el numero de depa en Departamento.csv
    BusqClase = TablaClase[TablaClase["Num Depa"] == BusqNumDep.iloc[0]["Num Depa"]] #Se esta flitrando para buscar el numero de depa en Departamento.csv
    e6.config(values=list(BusqClase["Nombre Clase"])) #me va a traer el nombre de las clases asociados con el nombre de departamento


#Mismo procedimiento que la funcion de activarClase
def activarFamily(self):
    e7["state"] = NORMAL
    TablaFamily = pd.read_csv("Familia.csv", delimiter=",")
    TablaClase = pd.read_csv("Clase.csv", delimiter=",")

    BusqClase = TablaClase[TablaClase["Nombre Clase"] == (e6.get())] #Con el Nombre Clase
    BusqFam = TablaFamily[TablaFamily["Num Clase"] == BusqClase.iloc[0]["Num Clase"]] #Se busca el Num Clase

    e7.config(values=list(BusqFam["Nombre Familia"]))#se busca Nombre Familia y lo muestra.

########### WIDGETS ################

#Dimensiones: Ancho x Altura
main.geometry("550x450")

###################Creacion de menu#####################

SkuLabel = Label(text="Sku:")
e1 = Entry(main)
SkuLabel.grid(column=0,row=1, padx=20)
e1.grid(column=1,row=1, padx=20)

ArLabel = Label(text="Articulo:")
e2 = Entry(main)
ArLabel.grid(column=0,row=2, padx=20)
e2.grid(column=1,row=2,columnspan=2, sticky=W+E, padx=20)

e2["state"] = DISABLED

marcLabel = Label(text="Marca:")
e3 = Entry(main)
marcLabel.grid(column=0,row=3, padx=20)
e3.grid(column=1,row=3,columnspan=2, sticky=W+E, padx=20)

e3["state"] = DISABLED

MoLabel = Label(text="Modelo:")
e4 = Entry(main)
MoLabel.grid(column=0,row=4, padx=20)
e4.grid(column=1,row=4,columnspan=2, sticky=W+E, padx=20)

e4["state"] = DISABLED
############Para hacer que sea un dropbox################
TablaDepa = pd.read_csv("Departamentos.csv",delimiter=",")#agarrar el archivo de departamentos y hacerlo en tabla en python
TablaDepa["Nombre Depa"] #Esta buscando los nombres de los depas
options = list(TablaDepa["Nombre Depa"]) #se convierte en una lista la "TablaDepa"

click = StringVar()
click.set(options[0])

DepaLabel = Label(text="Departamento:")
e5 = ttk.Combobox(main, values=options) #el * despiegla la lista
DepaLabel.grid(column=0,row=5, padx=20)
e5.grid(column=1,row=5,columnspan=2, sticky=W+E, padx=20)

e5.bind("<<ComboboxSelected>>", activarClase) #en este pedazo, estamos ligando una funcion

e5["state"] = DISABLED

##########CLASE DROPBOX##################
ClaLabel = Label(text="Clase:")
e6 = ttk.Combobox(main, values=[" "]) #en values se le pone corchetes y ub espacio vacio para que inicie vacio
ClaLabel.grid(column=0,row=6, padx=20)
e6.grid(column=1,row=6, columnspan=2, sticky=W+E, padx=20)

e6.bind("<<ComboboxSelected>>", activarFamily)

e6["state"] = DISABLED

############FAMILIA DROPBOX#################
FamLabel = Label(text="Familia:")
e7 = ttk.Combobox(main, values=[" "])
FamLabel.grid(column=0,row=7, padx=20)
e7.grid(column=1,row=7,columnspan=2, sticky=W+E, padx=20)

e7["state"] = DISABLED
###############################################
StoLabel = Label(text="Stock:")
e8 = Entry(main)
StoLabel.grid(column=0,row=8, padx=20)
e8.grid(column=1,row=8, padx=20)

e8["state"] = DISABLED

CanLabel = Label(text="Cantidad:")
e9 = Entry(main)
CanLabel.grid(column=2,row=8)
e9.grid(column=3,row=8)

e9["state"] = DISABLED

########################Fechas################
FechaAltLabel = Label(text="Fecha Alta:")
FechaAltLabel.grid(column=0,row=9, padx=20)
eFechaAlta = Text(main, width=15,height=1)
eFechaAlta.grid(column=1,row=9,padx=20)

eFechaAlta["state"] = DISABLED

FechaBajLabel = Label(text="Fecha Baja:")
FechaBajLabel.grid(column=2, row=9, padx=20)
eFechaBaja = Text(main, width=15,height=1)
eFechaBaja.grid(column=3,row=9,padx=20)

eFechaBaja["state"] = DISABLED
#############################################
Checkbox = tkinter.IntVar()

e10 = tkinter.Checkbutton(main, text="Descontinuado", onvalue=1, offvalue=0, variable=Checkbox)
e10.grid(column=3,row=1, padx=20)
e10["state"] = DISABLED

#########################BOTONES######################
b1=Button(main,padx=15 ,text ="Alta", command=Alta)
b1.grid(column=0,row=10, sticky=E)
b1["state"] = DISABLED #para desabilitar el boton

b2=Button(main,text ="Baja", command=Baja)
b2.grid(column=1,row=10)
b2["state"] = DISABLED

b3=Button(main, text ="Guardar", command=Cambio)
b3.grid(column=2, row=10, padx=20)
b3["state"] = DISABLED

b4=Button(main, text ="Consulta", command=Consulta)
b4.grid(column=3, row=10, padx=20)
#######################################################
main.mainloop()
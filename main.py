from tkinter import *
from tkinter import ttk, messagebox
from connection import *

# funciones  
def validar():
    return len(dni.get()) > 0 and len(legajo.get()) > 0 and len(nombre.get()) > 0 and len(apellido.get()) > 0
    
def limpiar():
    dni.set("")
    legajo.set("")
    nombre.set("")
    apellido.set("")
    dni_entry.config(state="normal")
       
def seleccionar(event):
    seleccion = tabla_estud.selection()
    if seleccion:
        id_db = seleccion[0]
        values = tabla_estud.item(id_db, "values")
        if values:
            dni.set(values[1])
            legajo.set(values[2])
            nombre.set(values[3])
            apellido.set(values[4])
    
def vaciar_datos():
    #se deben recorrer las filas del treeview y borrar los datos
    filas = tabla_estud.get_children()
    for fila in filas:
        tabla_estud.delete(fila)

def cargar_datos():
    vaciar_datos()
    sql = "SELECT * FROM alumnos"
    db.cursor.execute(sql)
    filas = db.cursor.fetchall()
    for fila in filas:
        id_db = fila[0]
        tabla_estud.insert("", END, id_db, text=id_db, values=fila)
    
def eliminar():
    respuesta = messagebox.askquestion("Eliminar", message="¿Estás seguro de eliminar el registro seleccionado?")
    if respuesta == "yes":
        try:
            id_db = tabla_estud.selection()[0]
            sql = "DELETE FROM alumnos WHERE IdAlumno=" + id_db
            db.cursor.execute(sql)
            db.connection.commit()
            tabla_estud.delete(id_db)
            mensaje_label.config(text="Se ha eliminado el registro correctamente", fg="green")
            cargar_datos()
            limpiar()
        except IndexError:
            mensaje_label.config(text="Seleccione un registro para eliminar", fg="red")

def agregar():
    respuesta = messagebox.askquestion("Agregar", message="¿Estás seguro de agregar el nuevo registro?")
    if respuesta == "yes":
        if validar():
            values = (dni.get(), legajo.get(), nombre.get(), apellido.get())
            sql = "INSERT INTO alumnos (Dni, Legajo, Nombre, Apellido) VALUES (%s, %s, %s, %s)"
            db.cursor.execute(sql, values)
            db.connection.commit()
            mensaje_label.config(text="Registro añadido correctamente", fg="green")
            limpiar()         
            cargar_datos()
        else:
            mensaje_label.config(text="Los campos no deben estar vacíos", fg="red")   

def actualizar():
    respuesta = messagebox.askquestion("Actualizar", message="¿Estás seguro de actualizar el registro seleccionado?")
    if respuesta == "yes":
        if validar():  
            id_db = tabla_estud.selection()[0]
            values = (dni.get(), legajo.get(), nombre.get(), apellido.get())
            sql = "UPDATE alumnos SET Dni=%s, Legajo=%s, Nombre=%s, Apellido=%s WHERE IdAlumno=" + id_db
            db.cursor.execute(sql, values)
            db.connection.commit()
            mensaje_label.config(text="Registro actualizado correctamente", fg="green")
            limpiar()
            cargar_datos()
        else:
            mensaje_label.config(text="Los campos no deben estar vacíos", fg="red")

ventana = Tk()
ventana.title("Plataforma de CRUD")
ventana.geometry("600x500") #dimensiones anchoxalto
ventana.resizable(0, 0) #para que el usuario no pueda modificar el tamaño

#vamos a crear un frame, dentro luego los label, botones, etc
marco = LabelFrame(ventana, text="Formulario de Gestión de Estudiantes", font="Courier 10") # ledigo donde va a estar
marco.place(x=50, y=50, width=500, height=400)

#labels y entries
dni = StringVar()
legajo = StringVar()
nombre = StringVar()
apellido = StringVar()
db = Database()

dni_label = Label(marco, text="DNI", font="Courier 10").grid(column=0, row=0, padx=5, pady=5)
dni_entry = Entry(marco, textvariable=dni)
dni_entry.grid(column=1, row=0)

legajo_label = Label(marco, text="Legajo", font="Courier 10").grid(column=0, row=1, padx=5, pady=5)
legajo_entry = Entry(marco, textvariable=legajo)
legajo_entry.grid(column=1, row=1)

nombre_label = Label(marco, text="Nombre", font="Courier 10").grid(column=2, row=0, padx=10, pady=5)
nombre_entry = Entry(marco, textvariable=nombre)
nombre_entry.grid(column=3, row=0)

apellido_label = Label(marco, text="Apellido", font="Courier 10").grid(column=2, row=1, padx=10, pady=5)
apellido_entry = Entry(marco, textvariable=apellido)
apellido_entry.grid(column=3, row=1)

limpiar_btn = Button(marco, text="Limpiar", bd=3, command=lambda:limpiar())
limpiar_btn.grid(column=4, row=1, padx=10)

mensaje_label = Label(marco, text="", fg="green")
mensaje_label.grid(column=0, row=2, columnspan=4, pady=5)

# tabla de lista de estudiantes
tabla_estud = ttk.Treeview(marco)
tabla_estud.grid(column=0, row=3, columnspan=4, pady=10)
tabla_estud["columns"] = ("ID", "DNI", "LEGAJO", "NOMBRE", "APELLIDO") #que columnas va a tener
tabla_estud.column("#0", width=0, stretch=NO)
tabla_estud.column("ID", width=50, anchor=CENTER)
tabla_estud.column("DNI", width=60, anchor=CENTER) #centrado
tabla_estud.column("LEGAJO", width=50, anchor=CENTER)
tabla_estud.column("NOMBRE", width=100, anchor=CENTER)
tabla_estud.column("APELLIDO", width=100, anchor=CENTER)
tabla_estud.heading("#0", text="")
tabla_estud.heading("ID", text="ID")
tabla_estud.heading("DNI", text="DNI")
tabla_estud.heading("LEGAJO", text="LEGAJO")
tabla_estud.heading("NOMBRE", text="NOMBRE")
tabla_estud.heading("APELLIDO", text="APELLIDO")
tabla_estud.bind("<<TreeviewSelect>>", seleccionar)

# botones de acciones
agregar_btn = Button(marco, text="Agregar", bd=3, command=lambda:agregar())
agregar_btn.grid(column=1, row=4, padx=5)
modificar_btn = Button(marco, text="Actualizar", bd=3, command=lambda:actualizar())
modificar_btn.grid(column=2, row=4)
eliminar_btn = Button(marco, text="Eliminar", bd=3, command=lambda:eliminar())
eliminar_btn.grid(column=3, row=4)

cargar_datos()
ventana.mainloop()
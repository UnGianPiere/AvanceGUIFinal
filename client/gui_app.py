import tkinter as tk
from tkinter import ttk

from ModelDB.conexion_db import Conexion


def barra_menu(root):
    barra_menu = tk.Menu(root)
    menu_inicio = tk.Menu(barra_menu, tearoff=0)
    barra_menu.add_cascade(label='Personal', menu=menu_inicio)
    barra_menu.add_cascade(label='Buscar')
    barra_menu.add_cascade(label='Actualizar')
    menu_inicio.add_command(label='Crear registro')
    menu_inicio.add_command(label='Eliminar registro')
    menu_inicio.add_command(label='Salir', command=root.destroy)


class Frame(tk.Frame):
    def __init__(self, root=None):
        super().__init__(root)
        self.pack()
        self.config(bg='#A1b0cb')

        self.Opciones()

    def Opciones(self):
        img_crear = tk.PhotoImage(file="img/add.png")
        img_gestionar = tk.PhotoImage(file="img/gestionarE.png")
        img_gestionarB = tk.PhotoImage(file="img/bonificacion.png")
        self.BOTONCREAR = tk.Button(self, image=img_crear, command=ventana_Crear)
        self.BOTONCREAR.image=img_crear
        self.BOTONCREAR.config(font=('Times New Roman', 10, 'bold'), fg='white', bg='grey', activebackground='green')
        self.BOTONCREAR.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.BOTONBUSCAR = tk.Button(self, image=img_gestionar, command=ventana_buscar)
        self.BOTONBUSCAR.image = img_gestionar
        self.BOTONBUSCAR.config(font=('Times New Roman', 10, 'bold'), fg='white', bg='grey', activebackground='green')
        self.BOTONBUSCAR.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.BOTONACTUALIZAR = tk.Button(self, image=img_gestionarB)
        self.BOTONACTUALIZAR.image = img_gestionarB
        self.BOTONACTUALIZAR.config(font=('Times New Roman', 10, 'bold'), fg='white', bg='grey',
                                    activebackground='green')
        self.BOTONACTUALIZAR.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        self.BOTONSALIR = tk.Button(self, text='Salir',command=self.destroy)
        self.BOTONSALIR.config(font=('Times New Roman', 10, 'bold'), fg='#D01818', bg='#Ce8d8d',
                                    activebackground='green')
        self.BOTONSALIR.grid(row=7, column=0, padx=10, pady=(50, 10), sticky="ew")



def ventana_buscar():
    FrameBuscar1()
class FrameBuscar1(tk.Toplevel):
    def __init__(self, TopLevel=None):
        super().__init__(TopLevel)
        self.title('Buscar Empleado')
        self.geometry("600x400")
        self.contenido()

    def contenido(self):
        self.label = tk.Label(self, text="Nombre del Empleado:")
        self.label.grid(row=0, column=0, padx=10, pady=10)
        self.entry = tk.Entry(self)
        self.entry.grid(row=0, column=1, padx=10, pady=10, columnspan=2)
        self.botonBuscar = tk.Button(self, command=self.Buscar, text='Buscar Empleado')
        self.botonBuscar.config(bg='Green', fg='White')
        self.botonBuscar.grid(row=1, column=1, padx=10, pady=10)

        self.tablaB = ttk.Treeview(self, column=('Nombre', 'Cargo'))
        self.tablaB.grid(row=2, column=0, columnspan=3)
        self.tablaB.heading('#0', text='ID')
        self.tablaB.heading('#1', text='Nombre')
        self.tablaB.heading('#2', text='Cargo')

        self.botonSeleccionar = tk.Button(self, command=self.Seleccion, text='Mostrar Historial')
        self.botonSeleccionar.config(bg='grey', fg='White')
        self.botonSeleccionar.grid(row=3, column=1, padx=10, pady=10)

        self.botonSeleccionar2 = tk.Button(self, command=self.Seleccion2, text='Gestionar asistencia ')
        self.botonSeleccionar2.config(bg='grey', fg='White')
        self.botonSeleccionar2.grid(row=3, column=2, padx=10, pady=10)
    def Buscar(self):

        conexion = Conexion()
        cursor = conexion.cursor()
        nombre = self.entry.get()
        cursor.execute(f"select * from Empleado Where NombreCompleto LIKE '%{nombre}%'")
        self.lista = []
        self.Empleado = cursor.fetchall()
        self.lista = self.Empleado
        self.lista.reverse()
        self.tablaB.delete(*self.tablaB.get_children())
        for i in self.lista:
            self.tablaB.insert('', 0, text=i[0], values=(i[1], i[3]))

        cursor.close()
        conexion.close()

    def Seleccion(self):
        selected_item = self.tablaB.selection()
        if selected_item:
            selected_row = self.tablaB.item(selected_item)
            self.id = selected_row['text']  # ID en la columna 0
            self.nombre = selected_row['values'][0]  # Nombre en la columna 1
        conexion = Conexion()
        cursor = conexion.cursor()
        cursor.execute(f"select * from tblBoletaPago Where IDEmpleado LIKE {self.id}")
        lista=[]
        histo=cursor.fetchall()
        lista=histo
        lista.reverse()
        FrameHistorial=tk.Toplevel()
        FrameHistorial.title('Historial de pagos')
        FrameHistorial.geometry("600x400")
        FrameHistorial.iconbitmap('img/add.ico')
        FrameHistorial.label = tk.Label(FrameHistorial, text=f"Nombre del Empleado: {self.nombre}")
        FrameHistorial.label.grid(row=0, column=0, padx=10, pady=10)

        tablaBOL= ttk.Treeview(FrameHistorial, column=('Fecha', 'Monto'))
        tablaBOL.grid(row=2, column=0, columnspan=3)
        tablaBOL.heading('#0', text='ID de Boleta')
        tablaBOL.heading('#1', text='Fecha de pago')
        tablaBOL.heading('#2', text='Monto Total')
        for i in lista:
                tablaBOL.insert('', 0, text=i[0], values=(i[4], i[1]))

        cursor.close()
        conexion.close()

    def Seleccion2(self):
        selected_item = self.tablaB.selection()
        if selected_item:
            selected_row = self.tablaB.item(selected_item)
            self.id = selected_row['text']  # ID en la columna 0
        conexion = Conexion()
        cursor = conexion.cursor()
        FrameHistorial2 = tk.Toplevel()
        label_horas_extra = tk.Label(FrameHistorial2, text="Horas Extra:")
        label_horas_extra.grid(row=3, column=0, padx=10, pady=10)
        entry_horas_extra = tk.Entry(FrameHistorial2)
        entry_horas_extra.grid(row=3, column=1, padx=10, pady=10)

        label_minutos_falta = tk.Label(FrameHistorial2, text="Minutos de Falta:")
        label_minutos_falta.grid(row=4, column=0, padx=10, pady=10)
        entry_minutos_falta = tk.Entry(FrameHistorial2)
        entry_minutos_falta.grid(row=4, column=1, padx=10, pady=10)

        label_dias_falta = tk.Label(FrameHistorial2, text="Días de Falta:")
        label_dias_falta.grid(row=5, column=0, padx=10, pady=10)
        entry_dias_falta = tk.Entry(FrameHistorial2)
        entry_dias_falta.grid(row=5, column=1, padx=10, pady=10)
        horas = entry_horas_extra.get()
        minutos = entry_minutos_falta.get()
        dias = entry_dias_falta.get()
        botonGuarda = tk.Button(FrameHistorial2, text='Guardar',command=lambda:GuardarDATOSEMPLEDO(self.id,horas,minutos,dias))
        botonGuarda.config(bg='grey', fg='White')
        botonGuarda.grid(row=6, column=2, padx=10, pady=10)
        cursor.close()
        conexion.close()

def GuardarDATOSEMPLEDO(id,horas,minutos,dias):
    conexion = Conexion()
    cursor = conexion.cursor()
    idmes='MES011'
    print(f'{id},{horas},{minutos},{dias}')
    cursor.execute(f'Insert into tblDetalleMensualTrabajador (IDEmpleado,IDMes,detailHorasExtra,detailMinutosTardanzas,detailDiasFalta) values ( {id},{idmes},{horas},{minutos},{dias} )')
    print('se guardo correctamente los datos')
    cursor.close()
    conexion.close()

def ventana_Crear():
    Framecrear1()
class Framecrear1(tk.Toplevel):
    def __init__(self, TopLevel=None):
        super().__init__(TopLevel)
        self.title('Crear Empleado')
        self.geometry("800x600")
        self.iconbitmap('img/add.ico')
        self.contenido()
        self.deshabilitar_campos()
        self.tabla_empleado()

    def contenido(self):

        self.label_nombre = tk.Label(self, text='Nombre Completo: ')
        self.label_nombre.config(font=('Times New Roman', 14, 'bold'))
        self.label_nombre.grid(row=0, column=0, padx=10, pady=10)

        self.label_Sueldo = tk.Label(self, text='Sueldo: ')
        self.label_Sueldo.config(font=('Times New Roman', 14, 'bold'))
        self.label_Sueldo.grid(row=1, column=0, padx=10, pady=10)

        self.label_cargo = tk.Label(self, text='Cargo: ')
        self.label_cargo.config(font=('Times New Roman', 14, 'bold'))
        self.label_cargo.grid(row=2, column=0, padx=10, pady=10)

        self.nombre = tk.StringVar()
        self.entry_nombre = tk.Entry(self, textvariable=self.nombre)
        self.entry_nombre.config(width=50, font=('Times New Roman', 14))
        self.entry_nombre.grid(row=0, column=1, padx=10, pady=10, columnspan=2)

        self.sueldo = tk.StringVar()
        self.entry_Sueldo = tk.Entry(self, textvariable=self.sueldo)
        self.entry_Sueldo.config(width=50, font=('Times New Roman', 14))
        self.entry_Sueldo.grid(row=1, column=1, padx=10, pady=10, columnspan=2)

        self.cargo = tk.StringVar()
        self.entry_Cargo = tk.Entry(self, textvariable=self.cargo)
        self.entry_Cargo.config(width=50, font=('Times New Roman', 14))
        self.entry_Cargo.grid(row=2, column=1, padx=10, pady=10, columnspan=2)

        self.boton_nuevo = tk.Button(self, text='Nuevo', command=self.habilitar_campos)
        self.boton_nuevo.config(width=20, font=('Times New Roman', 14, 'bold'), fg='Red', bg='Orange',
                                activebackground='green')
        self.boton_nuevo.grid(row=4, column=0, padx=10, pady=10)

        self.boton_guardar = tk.Button(self, text='Guardar', command=self.guardar_datos)
        self.boton_guardar.config(width=20, font=('Times New Roman', 14, 'bold'), fg='Red', bg='Orange',
                                  activebackground='green')
        self.boton_guardar.grid(row=4, column=1, padx=10, pady=10)

        self.boton_cancelar = tk.Button(self, text='Cancelar', command=self.deshabilitar_campos)
        self.boton_cancelar.config(width=20, font=('Times New Roman', 14, 'bold'), fg='Red', bg='Orange',
                                   activebackground='green')
        self.boton_cancelar.grid(row=4, column=2, padx=10, pady=10)

        self.boton_Eliminar = tk.Button(self, text='Eliminar')
        self.boton_Eliminar.config(width=20, font=('Times New Roman', 14, 'bold'), fg='Yellow', bg='Red',
                                   activebackground='green')
        self.boton_Eliminar.grid(row=6, column=1, padx=10, pady=10)

        self.boton_Editar = tk.Button(self, text='Editar')
        self.boton_Editar.config(width=20, font=('Times New Roman', 14, 'bold'), fg='Yellow', bg='Green',
                                 activebackground='green')
        self.boton_Editar.grid(row=6, column=0, padx=10, pady=10)


    def deshabilitar_campos(self):
        self.entry_Cargo.config(state='disable')
        self.entry_Sueldo.config(state='disable')
        self.entry_nombre.config(state='disable')
        self.boton_guardar.config(state='disable')
        self.boton_cancelar.config(state='disable')
        self.nombre.set('')
        self.sueldo.set('')
        self.cargo.set('')

    def habilitar_campos(self):
        self.entry_Cargo.config(state='normal')
        self.entry_Sueldo.config(state='normal')
        self.entry_nombre.config(state='normal')
        self.boton_guardar.config(state='normal')
        self.boton_cancelar.config(state='normal')

    def guardar_datos(self):
        conexion = Conexion()
        nombre = self.entry_nombre.get()
        sueldo = self.sueldo.get()
        cargo = self.cargo.get()

        # Obtén el último ID
        cursor = conexion.cursor()
        cursor.execute('SELECT MAX(ID) as UltimoID FROM Empleado;')
        resultado = cursor.fetchone()

        if resultado and resultado.UltimoID is not None:
            ultimo_id = resultado.UltimoID
            nuevo_id = ultimo_id + 1
        else:
            # Si no se encontraron registros, establece el nuevo ID en 1
            nuevo_id = 1

        try:
            cursor.execute(f"INSERT INTO Empleado VALUES (?, ?, ?, ?)",
                           (nuevo_id, nombre, sueldo, cargo))
            conexion.commit()  # Realiza la confirmación para guardar los cambios
            print('Se guardó correctamente')
        except Exception as e:
            print(f'Error al guardar: {e}')

        cursor.close()
        conexion.close()

    def tabla_empleado(self):
        conexion = Conexion()
        self.tabla = ttk.Treeview(self, column=('Nombre', 'Sueldo', 'Cargo'))
        self.tabla.grid(row=5, column=0, columnspan=4)
        self.tabla.heading('#0', text='ID')
        self.tabla.heading('#1', text='Nombre')
        self.tabla.heading('#2', text='Sueldo')
        self.tabla.heading('#3', text='Cargo')

        cursor = conexion.cursor()

        cursor.execute("Select * from Empleado;")
        self.lista = []
        Empleado = cursor.fetchall()
        self.lista = Empleado
        self.lista.reverse()

        for i in self.lista:
            self.tabla.insert('', 0, text=i[0], values=(i[1], i[2], i[3]))

        for col in ('#0', '#1', '#2', '#3'):
            self.tabla.column(col, anchor='center')
        cursor.close()
        conexion.close()




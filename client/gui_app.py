import tkinter as tk
from tkinter import ttk
from ModelDB.conexion_db import Conexion


def barra_menu(root):
    barra_menu = tk.Menu(root)
    root.config(menu=barra_menu, width=380, height=300)

    menu_inicio = tk.Menu(barra_menu, tearoff=0)

    barra_menu.add_cascade(label='Personal', menu=menu_inicio)
    barra_menu.add_cascade(label='Buscar')
    barra_menu.add_cascade(label='Actualizar')

    menu_inicio.add_command(label='Crear registro')
    menu_inicio.add_command(label='Eliminar registro')
    menu_inicio.add_command(label='Salir', command=root.destroy)


class Frame(tk.Frame):
    def __init__(self, root=None):
        super().__init__(root, width=1080, height=600)
        self.root = root
        self.pack()
        self.config()
        self.campos_cliente()
        self.deshabilitar_campos()
        self.tabla_empleado()

    def campos_cliente(self):
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
                                   activebackground='green',command=ventana_actualizar)
        self.boton_Eliminar.grid(row=6, column=1, padx=10, pady=10)

        self.boton_Editar = tk.Button(self, text='Editar')
        self.boton_Editar.config(width=20, font=('Times New Roman', 14, 'bold'), fg='Yellow', bg='Green',
                                 activebackground='green',command=ventana_buscar)
        self.boton_Editar.grid(row=6, column=0, padx=10, pady=10)
        self.addClient = tk.PhotoImage()

    def habilitar_campos(self):
        self.entry_Cargo.config(state='normal')
        self.entry_Sueldo.config(state='normal')
        self.entry_nombre.config(state='normal')
        self.boton_guardar.config(state='normal')
        self.boton_cancelar.config(state='normal')

    def deshabilitar_campos(self):
        self.entry_Cargo.config(state='disable')
        self.entry_Sueldo.config(state='disable')
        self.entry_nombre.config(state='disable')
        self.boton_guardar.config(state='disable')
        self.boton_cancelar.config(state='disable')
        self.nombre.set('')
        self.sueldo.set('')
        self.cargo.set('')

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

        cursor.close()
        conexion.close()

        for i in self.lista:
            self.tabla.insert('', 0, text=i[0], values=(i[1], i[2], i[3]))

        for col in ('#0', '#1', '#2', '#3'):
            self.tabla.column(col, anchor='center')

def ventana_buscar():
    FrameBuscar = tk.Toplevel()
    FrameBuscar.title('Buscar Empleado')
    FrameBuscar()





def ventana_actualizar():
    FrameActuzalizar = tk.Toplevel()
    FrameActuzalizar.title('Actualizar Bonificaciones')

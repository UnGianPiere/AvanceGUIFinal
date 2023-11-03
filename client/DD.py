import tkinter as tk
from tkinter import ttk

def crear_empleado():
    # Lógica para la función "Crear Empleado" aquí
    pass

def gestion_empleado():
    # Lógica para la función "Gestión Empleado" aquí
    pass

def gestion_beneficios():
    # Lógica para la función "Gestión Beneficios" aquí
    pass

root = tk.Tk()
root.title("Menú Minimalista")

# Configurar el tamaño de la ventana
root.geometry("400x300")

# Crear un estilo minimalista
style = ttk.Style()
style.configure("TFrame", background="#333")
style.configure("TButton", padding=(10, 5, 10, 5), font='Helvetica 12', foreground='white', background='#333')

# Crear un marco para organizar los botones
frame = ttk.Frame(root)
frame.pack(expand=True, fill='both')

# Colocar los botones en el marco con el administrador de geometría grid
btn_crear_empleado = ttk.Button(frame, text="Crear Empleado", command=crear_empleado)
btn_gestion_empleado = ttk.Button(frame, text="Gestión Empleado", command=gestion_empleado)
btn_gestion_beneficios = ttk.Button(frame, text="Gestión Beneficios", command=gestion_beneficios)

btn_crear_empleado.grid(row=0, pady=10, sticky='ew')
btn_gestion_empleado.grid(row=1, pady=10, sticky='ew')
btn_gestion_beneficios.grid(row=2, pady=10, sticky='ew')

# Configurar el botón "Salir" fuera del marco
btn_salir = ttk.Button(root, text="Salir", command=root.quit)
btn_salir.pack(pady=10)

root.mainloop()

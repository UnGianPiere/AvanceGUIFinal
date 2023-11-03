import tkinter as tk

from client.gui_app import Frame, barra_menu


def main():

    root = tk.Tk()
    root.title('Sueldos')
    root.iconbitmap('img/icono.ico')
    root.geometry("370x600")
    barra_menu(root)
    app = Frame(root=root)
    root.configure(bg='#A1b0cb')
    app.mainloop()


if __name__ == '__main__':
    main()

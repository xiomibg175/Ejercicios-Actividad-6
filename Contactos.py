import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class Contacto:
    def __init__(self, nombres, apellidos, fecha_nacimiento, direccion, telefono, correo):
        self.nombres = nombres
        self.apellidos = apellidos
        self.fecha_nacimiento = fecha_nacimiento
        self.direccion = direccion
        self.telefono = telefono
        self.correo = correo

    def __str__(self):
       
        return f"{self.nombres}-{self.apellidos}-{self.fecha_nacimiento}-{self.direccion}-{self.telefono}-{self.correo}"

class ListaContactos:
    def __init__(self):
        self.lista = []

    def agregar_contacto(self, contacto):
        self.lista.append(contacto)

class VentanaContacto(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Detalles del contacto")
        self.geometry("600x300")
        self.resizable(False, False)
        
        self.lista_contactos = ListaContactos()
        
        self.centrar_ventana()
        self.crear_interfaz()

    def centrar_ventana(self):
        self.update_idletasks()
        ancho = self.winfo_width()
        alto = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.winfo_screenheight() // 2) - (alto // 2)
        self.geometry(f'{ancho}x{alto}+{x}+{y}')

    def crear_interfaz(self):
        
        main_frame = tk.Frame(self, highlightbackground="green", highlightcolor="green", highlightthickness=2, bd=0)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        
        main_frame.columnconfigure(1, weight=1)
        main_frame.columnconfigure(2, weight=3) 
        
        opts = {'padx': 5, 'pady': 5, 'sticky': 'w'}

        
        tk.Label(main_frame, text="Nombres:").grid(row=0, column=0, **opts)
        tk.Label(main_frame, text="Apellidos:").grid(row=1, column=0, **opts)
        tk.Label(main_frame, text="Fecha nacimiento:").grid(row=2, column=0, **opts)
        tk.Label(main_frame, text="Dirección:").grid(row=3, column=0, **opts)
        tk.Label(main_frame, text="Teléfono:").grid(row=4, column=0, **opts)
        tk.Label(main_frame, text="Correo:").grid(row=5, column=0, **opts)

       
        self.txt_nombres = tk.Entry(main_frame)
        self.txt_nombres.grid(row=0, column=1, **opts)

        self.txt_apellidos = tk.Entry(main_frame)
        self.txt_apellidos.grid(row=1, column=1, **opts)

        
        frame_fecha = tk.Frame(main_frame)
        
        frame_fecha.grid(row=2, column=1, padx=5, pady=5, sticky="we")
        
        self.txt_fecha = tk.Entry(frame_fecha)
        self.txt_fecha.pack(side="left", fill="x", expand=True)
        self.txt_fecha.insert(0, "dd/mm/aaaa") 
        
       
        lbl_cal = tk.Label(frame_fecha, text="📅", cursor="hand2")
        lbl_cal.pack(side="right", padx=2)

        self.txt_direccion = tk.Entry(main_frame)
        self.txt_direccion.grid(row=3, column=1, **opts)

        self.txt_telefono = tk.Entry(main_frame)
        self.txt_telefono.grid(row=4, column=1, **opts)

        self.txt_correo = tk.Entry(main_frame)
        self.txt_correo.grid(row=5, column=1, **opts)

        btn_agregar = tk.Button(main_frame, text="Agregar", width=15, command=self.accion_agregar)
        
        btn_agregar.grid(row=6, column=0, columnspan=2, pady=15, padx=5, sticky="w")

        
        self.lista_view = tk.Listbox(main_frame, highlightthickness=1, relief="sunken")
        self.lista_view.grid(row=0, column=2, rowspan=7, padx=10, pady=5, sticky="nsew")
        
        
        scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=self.lista_view.yview)
        scrollbar.grid(row=0, column=3, rowspan=7, sticky="ns")
        self.lista_view.config(yscrollcommand=scrollbar.set)

    def accion_agregar(self):
        nombres = self.txt_nombres.get()
        apellidos = self.txt_apellidos.get()
        fecha = self.txt_fecha.get()
        direccion = self.txt_direccion.get()
        telefono = self.txt_telefono.get()
        correo = self.txt_correo.get()

        
        if not all([nombres, apellidos, fecha, direccion, telefono, correo]) or fecha == "dd/mm/aaaa":
            messagebox.showinfo("Mensaje", "No se permiten campos vacíos\nError en ingreso de datos")
            return

        nuevo_contacto = Contacto(nombres, apellidos, fecha, direccion, telefono, correo)
        self.lista_contactos.agregar_contacto(nuevo_contacto)

        
        item_str = str(nuevo_contacto)
        self.lista_view.insert(tk.END, item_str)

        self.limpiar_campos()

    def limpiar_campos(self):
        self.txt_nombres.delete(0, tk.END)
        self.txt_apellidos.delete(0, tk.END)
        self.txt_fecha.delete(0, tk.END)
        self.txt_fecha.insert(0, "dd/mm/aaaa")
        self.txt_direccion.delete(0, tk.END)
        self.txt_telefono.delete(0, tk.END)
        self.txt_correo.delete(0, tk.END)

if __name__ == "__main__":
    app = VentanaContacto()
    app.mainloop()
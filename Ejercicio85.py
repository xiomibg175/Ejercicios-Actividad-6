import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime

class Huesped:
    def __init__(self, nombres, apellidos, documento_identidad):
        self.nombres = nombres
        self.apellidos = apellidos
        self.documento_identidad = documento_identidad
        self.fecha_ingreso = None
        self.fecha_salida = None

    def set_fecha_ingreso(self, fecha):
        self.fecha_ingreso = fecha

    def set_fecha_salida(self, fecha):
        self.fecha_salida = fecha

    def obtener_dias_alojamiento(self):
        if self.fecha_ingreso and self.fecha_salida:
            delta = self.fecha_salida - self.fecha_ingreso
            dias = delta.days
            return dias if dias > 0 else 0
        return 0

class Habitacion:
    def __init__(self, numero, disponible, precio_dia):
        self.numero_habitacion = numero
        self.disponible = disponible
        self.precio_dia = precio_dia
        self.huesped = None

    def set_huesped(self, huesped):
        self.huesped = huesped

    def set_disponible(self, disponible):
        self.disponible = disponible

class Hotel:
    def __init__(self):
        self.lista_habitaciones = []
        for i in range(1, 11):
            precio = 120000.0 if i <= 5 else 160000.0
            self.lista_habitaciones.append(Habitacion(i, True, precio))

    def buscar_fecha_ingreso_habitacion(self, numero):
        for hab in self.lista_habitaciones:
            if hab.numero_habitacion == numero and hab.huesped:
                return hab.huesped.fecha_ingreso.strftime("%Y-%m-%d")
        return ""

    def buscar_habitacion_ocupada(self, numero):
        for hab in self.lista_habitaciones:
            if hab.numero_habitacion == numero:
                return not hab.disponible
        return False

    def obtener_habitacion(self, numero):
        for hab in self.lista_habitaciones:
            if hab.numero_habitacion == numero:
                return hab
        return None

def centrar_ventana(window, w, h):
    window.update_idletasks()
    ws = window.winfo_screenwidth()
    hs = window.winfo_screenheight()
    x = int((ws/2) - (w/2))
    y = int((hs/2) - (h/2))
    window.geometry(f'{w}x{h}+{x}+{y}')

class VentanaIngreso(tk.Toplevel):
    def __init__(self, padre, hotel, num_habitacion):
        super().__init__(padre)
        self.hotel = hotel
        self.num_habitacion = num_habitacion
        self.title("Ingreso")
        self.geometry("290x250")
        self.resizable(False, False)
        centrar_ventana(self, 290, 250)
        self.crear_componentes()

    def crear_componentes(self):
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        opts = {'padx': 5, 'pady': 3, 'sticky': 'w'}

        tk.Label(self, text=f"Habitación: {self.num_habitacion}").grid(row=0, column=0, **opts)

        tk.Label(self, text="Fecha (aaaa-mm-dd):").grid(row=1, column=0, **opts)
        self.txt_fecha = tk.Entry(self)
        self.txt_fecha.grid(row=1, column=1, **opts)

        tk.Label(self, text="Huésped", font=("Arial", 9, "bold")).grid(row=2, column=0, **opts)

        tk.Label(self, text="Nombre: ").grid(row=3, column=0, **opts)
        self.txt_nombre = tk.Entry(self)
        self.txt_nombre.grid(row=3, column=1, **opts)

        tk.Label(self, text="Apellidos: ").grid(row=4, column=0, **opts)
        self.txt_apellidos = tk.Entry(self)
        self.txt_apellidos.grid(row=4, column=1, **opts)

        tk.Label(self, text="Doc. Identidad: ").grid(row=5, column=0, **opts)
        self.txt_documento = tk.Entry(self)
        self.txt_documento.grid(row=5, column=1, **opts)

        btn_frame = tk.Frame(self)
        btn_frame.grid(row=6, column=0, columnspan=2, pady=10)
        
        btn_aceptar = tk.Button(btn_frame, text="Aceptar", width=10, command=self.accion_aceptar)
        btn_aceptar.pack(side="left", padx=5)

        btn_cancelar = tk.Button(btn_frame, text="Cancelar", width=10, command=self.destroy)
        btn_cancelar.pack(side="left", padx=5)

    def accion_aceptar(self):
        try:
            fecha_str = self.txt_fecha.get()
            nombre = self.txt_nombre.get()
            apellidos = self.txt_apellidos.get()
            doc_str = self.txt_documento.get()

            if not fecha_str or not nombre or not apellidos or not doc_str:
                raise ValueError("Campos vacíos")

            fecha_ingreso = datetime.strptime(fecha_str, "%Y-%m-%d")
            doc_id = int(doc_str)

            habitacion = self.hotel.obtener_habitacion(self.num_habitacion)
            if habitacion:
                huesped = Huesped(nombre, apellidos, doc_id)
                huesped.set_fecha_ingreso(fecha_ingreso)
                habitacion.set_huesped(huesped)
                habitacion.set_disponible(False)
                messagebox.showinfo("Mensaje", "El huésped ha sido registrado", parent=self)
                self.destroy()

        except ValueError:
            messagebox.showerror("Error", "Campo nulo o error en formato de numero", parent=self)

class VentanaSalida(tk.Toplevel):
    def __init__(self, padre, hotel, num_habitacion):
        super().__init__(padre)
        self.hotel = hotel
        self.num_habitacion = num_habitacion
        self.habitacion = self.hotel.obtener_habitacion(num_habitacion)
        self.title("Salida huéspedes")
        self.geometry("260x260")
        self.resizable(False, False)
        centrar_ventana(self, 260, 260)
        self.crear_componentes()

    def crear_componentes(self):
        opts = {'padx': 5, 'pady': 3, 'sticky': 'w'}

        tk.Label(self, text=f"Habitación: {self.num_habitacion}", font=("Arial", 9, "bold")).grid(row=0, column=0, **opts)

        fecha_ingreso = self.hotel.buscar_fecha_ingreso_habitacion(self.num_habitacion)
        tk.Label(self, text=f"Fecha de ingreso: {fecha_ingreso}").grid(row=1, column=0, **opts)

        tk.Label(self, text="Fecha de salida (aaaa-mm-dd):").grid(row=2, column=0, **opts)
        
        self.txt_fecha_salida = tk.Entry(self)
        self.txt_fecha_salida.grid(row=3, column=0, padx=5, pady=3, sticky="ew")

        btn_calcular = tk.Button(self, text="Calcular", command=self.accion_calcular)
        btn_calcular.grid(row=4, column=0, pady=5)

        self.lbl_dias = tk.Label(self, text="Cantidad de días: ")
        self.lbl_dias.grid(row=5, column=0, **opts)

        self.lbl_total = tk.Label(self, text="Total: $")
        self.lbl_total.grid(row=6, column=0, **opts)

        self.btn_registrar = tk.Button(self, text="RegistrarSalida", state="disabled", command=self.accion_registrar)
        self.btn_registrar.grid(row=7, column=0, pady=10)

    def accion_calcular(self):
        try:
            fecha_str = self.txt_fecha_salida.get()
            fecha_salida = datetime.strptime(fecha_str, "%Y-%m-%d")
            
            self.habitacion.huesped.set_fecha_salida(fecha_salida)
            
            if self.habitacion.huesped.fecha_ingreso > fecha_salida:
                messagebox.showerror("Mensaje", "La fecha de salida es menor que la de ingreso", parent=self)
                return

            dias = self.habitacion.huesped.obtener_dias_alojamiento()
            total = dias * self.habitacion.precio_dia

            self.lbl_dias.config(text=f"Cantidad de días: {dias}")
            self.lbl_total.config(text=f"Total: ${total:.1f}")
            self.btn_registrar.config(state="normal")

        except ValueError:
            messagebox.showerror("Mensaje", "La fecha no está en el formato solicitado", parent=self)

    def accion_registrar(self):
        self.habitacion.set_huesped(None)
        self.habitacion.set_disponible(True)
        messagebox.showinfo("Mensaje", "Se ha registrado la salida del huésped", parent=self)
        self.destroy()

class VentanaHabitaciones(tk.Toplevel):
    def __init__(self, padre, hotel):
        super().__init__(padre)
        self.hotel = hotel
        self.title("Habitaciones")
        self.geometry("760x260")
        self.resizable(False, False)
        centrar_ventana(self, 760, 260)
        self.crear_componentes()

    def crear_componentes(self):
        for i in range(5):
            num = i + 1
            x_pos = 20 + (i * 140)
            hab = self.hotel.obtener_habitacion(num)
            
            tk.Label(self, text=f"Habitación {num}", font=("Arial", 9, "bold")).place(x=x_pos, y=30, width=130, height=23)
            estado = "Disponible" if hab.disponible else "No disponible"
            tk.Label(self, text=estado).place(x=x_pos, y=50, width=100, height=23)

        for i in range(5):
            num = i + 6
            x_pos = 20 + (i * 140)
            hab = self.hotel.obtener_habitacion(num)
            
            tk.Label(self, text=f"Habitación {num}", font=("Arial", 9, "bold")).place(x=x_pos, y=120, width=130, height=23)
            estado = "Disponible" if hab.disponible else "No disponible"
            tk.Label(self, text=estado).place(x=x_pos, y=140, width=100, height=23)

        tk.Label(self, text="Habitación a reservar:").place(x=250, y=180, width=135, height=23)
        
        self.spin_hab = tk.Spinbox(self, from_=1, to=10)
        self.spin_hab.place(x=380, y=180, width=40, height=23)
        
        btn_aceptar = tk.Button(self, text="Aceptar", command=self.accion_aceptar)
        btn_aceptar.place(x=500, y=180, width=100, height=23)

    def accion_aceptar(self):
        num = int(self.spin_hab.get())
        if self.hotel.buscar_habitacion_ocupada(num):
             messagebox.showinfo("Mensaje", "La habitación está ocupada", parent=self)
        else:
            self.destroy()
            VentanaIngreso(self.master, self.hotel, num)

class VentanaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.hotel = Hotel()
        self.title("Hotel")
        self.geometry("280x380")
        self.resizable(False, False)
        centrar_ventana(self, 280, 380)
        self.crear_menu()

    def crear_menu(self):
        barra_menu = tk.Menu(self)
        self.config(menu=barra_menu)
        
        menu_opciones = tk.Menu(barra_menu, tearoff=0)
        barra_menu.add_cascade(label="Menú", menu=menu_opciones)
        
        menu_opciones.add_command(label="Consultar habitaciones", command=self.abrir_habitaciones)
        menu_opciones.add_command(label="Salida de huéspedes", command=self.abrir_salida)

    def abrir_habitaciones(self):
        VentanaHabitaciones(self, self.hotel)

    def abrir_salida(self):
        num_str = simpledialog.askstring("Salida de huéspedes", "Ingrese número de habitación", parent=self)
        if num_str:
            try:
                num = int(num_str)
                if num < 1 or num > 10:
                    messagebox.showinfo("Mensaje", "El número de habitación debe estar entre 1 y 10")
                elif self.hotel.buscar_habitacion_ocupada(num):
                    VentanaSalida(self, self.hotel, num)
                else:
                    messagebox.showinfo("Mensaje", "La habitación ingresada no ha sido ocupada")
            except ValueError:
                messagebox.showerror("Error", "Campo nulo o error en formato de numero")

if __name__ == "__main__":
    app = VentanaPrincipal()
    app.mainloop()
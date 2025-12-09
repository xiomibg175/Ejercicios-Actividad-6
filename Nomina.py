import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os


class Empleado:
    def __init__(self, nombre, apellidos, cargo, genero, salario_dia, 
                 dias_trabajados, otros_ingresos, pagos_salud, aporte_pensiones):
        self.nombre = nombre
        self.apellidos = apellidos
        self.cargo = cargo
        self.genero = genero
        self.salario_dia = salario_dia
        self.dias_trabajados = dias_trabajados
        self.otros_ingresos = otros_ingresos
        self.pagos_salud = pagos_salud
        self.aporte_pensiones = aporte_pensiones

   
    def get_nombre(self): return self.nombre
    def get_apellidos(self): return self.apellidos
    def get_cargo(self): return self.cargo
    def get_genero(self): return self.genero
    def get_salario_dia(self): return self.salario_dia
    def get_dias_trabajados(self): return self.dias_trabajados
    def get_otros_ingresos(self): return self.otros_ingresos
    def get_pagos_salud(self): return self.pagos_salud
    def get_aporte_pensiones(self): return self.aporte_pensiones

    def calcular_nomina(self):
        
        devengado = (self.salario_dia * self.dias_trabajados) + self.otros_ingresos
        deducciones = self.pagos_salud + self.aporte_pensiones
        return devengado - deducciones

class ListaEmpleados:
    def __init__(self):
        self.lista = []
        self.total_nomina = 0.0

    def agregar_empleado(self, empleado):
        self.lista.append(empleado)

    def calcular_total_nomina(self):
        self.total_nomina = sum(e.calcular_nomina() for e in self.lista)
        return self.total_nomina

    def obtener_matriz(self):
        
        datos = []
        for e in self.lista:
            sueldo = e.calcular_nomina()
           
            datos.append((e.get_nombre(), e.get_apellidos(), f"{sueldo:.1f}"))
        self.calcular_total_nomina()
        return datos

    def convertir_texto(self):
        
        texto = ""
        for e in self.lista:
            texto += f"Nombre = {e.get_nombre()}\n"
            texto += f"Apellidos = {e.get_apellidos()}\n"
            texto += f"Cargo = {e.get_cargo()}\n"
            texto += f"Género = {e.get_genero()}\n"
            texto += f"Salario = ${e.get_salario_dia()}\n"
            texto += f"Días trabajados = {e.get_dias_trabajados()}\n"
            texto += f"Otros ingresos = ${e.get_otros_ingresos()}\n"
            texto += f"Pagos saludo = ${e.get_pagos_salud()}\n"
            texto += f"Aportes pensiones = ${e.get_aporte_pensiones()}\n"
            texto += "---------\n"
        
        texto += f"Total nómina = ${self.calcular_total_nomina():.2f}"
        return texto



def centrar_ventana(ventana, ancho, alto):
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()
    x = int((pantalla_ancho / 2) - (ancho / 2))
    y = int((pantalla_alto / 2) - (alto / 2))
    ventana.geometry(f'{ancho}x{alto}+{x}+{y}')



class VentanaAgregarEmpleado(tk.Toplevel):
    def __init__(self, padre, lista_empleados):
        super().__init__(padre)
        self.lista = lista_empleados
        self.title("Agregar Empleado")
        self.geometry("300x400")
        self.resizable(False, False)
        centrar_ventana(self, 300, 400)
        self.transient(padre)
        
        self.crear_componentes()

    def crear_componentes(self):
       
        self.var_genero = tk.StringVar(value="Masculino")
        
       
        
        tk.Label(self, text="Nombre:").place(x=20, y=20, width=135, height=23)
        self.txt_nombre = tk.Entry(self)
        self.txt_nombre.place(x=160, y=20, width=100, height=23)

        tk.Label(self, text="Apellidos:").place(x=20, y=50, width=135, height=23)
        self.txt_apellidos = tk.Entry(self)
        self.txt_apellidos.place(x=160, y=50, width=100, height=23)

        tk.Label(self, text="Cargo:").place(x=20, y=80, width=135, height=23)
        self.cbo_cargo = ttk.Combobox(self, state="readonly", values=["Directivo", "Estratégico", "Operativo"])
        self.cbo_cargo.current(0)
        self.cbo_cargo.place(x=160, y=80, width=100, height=23)

        tk.Label(self, text="Género:").place(x=20, y=110, width=100, height=30)
        tk.Radiobutton(self, text="Masculino", variable=self.var_genero, value="Masculino").place(x=160, y=110, width=100, height=30)
        tk.Radiobutton(self, text="Femenino", variable=self.var_genero, value="Femenino").place(x=160, y=140, width=100, height=30)

        tk.Label(self, text="Salario por día:").place(x=20, y=170, width=135, height=23)
        self.txt_salario = tk.Entry(self)
        self.txt_salario.place(x=160, y=170, width=100, height=23)

        tk.Label(self, text="Días trabajados al mes:").place(x=20, y=200, width=135, height=23)
        self.spin_dias = tk.Spinbox(self, from_=1, to=31)
        self.spin_dias.delete(0, "end")
        self.spin_dias.insert(0, 30)
        self.spin_dias.place(x=160, y=200, width=40, height=23)

        tk.Label(self, text="Otros ingresos:").place(x=20, y=230, width=135, height=23)
        self.txt_otros = tk.Entry(self)
        self.txt_otros.place(x=160, y=230, width=100, height=23)

        tk.Label(self, text="Pagos por salud:").place(x=20, y=260, width=135, height=23)
        self.txt_salud = tk.Entry(self)
        self.txt_salud.place(x=160, y=260, width=100, height=23)

        tk.Label(self, text="Aportes pensiones:").place(x=20, y=290, width=135, height=23)
        self.txt_pension = tk.Entry(self)
        self.txt_pension.place(x=160, y=290, width=100, height=23)

        # Botones
        self.btn_agregar = tk.Button(self, text="Agregar", command=self.accion_agregar)
        self.btn_agregar.place(x=20, y=320, width=100, height=23)

        self.btn_limpiar = tk.Button(self, text="Limpiar", command=self.accion_limpiar)
        self.btn_limpiar.place(x=160, y=320, width=80, height=23)

    def accion_limpiar(self):
        self.txt_nombre.delete(0, tk.END)
        self.txt_apellidos.delete(0, tk.END)
        self.txt_salario.delete(0, tk.END)
        self.spin_dias.delete(0, tk.END)
        self.spin_dias.insert(0, 30)
        self.txt_otros.delete(0, tk.END)
        self.txt_salud.delete(0, tk.END)
        self.txt_pension.delete(0, tk.END)

    def accion_agregar(self):
        try:
            nombre = self.txt_nombre.get()
            apellidos = self.txt_apellidos.get()
            
            if not nombre or not apellidos:
                messagebox.showerror("Error", "Campo nulo o error en formato de numero", parent=self)
                return

            
            emp = Empleado(
                nombre,
                apellidos,
                self.cbo_cargo.get(),
                self.var_genero.get(),
                float(self.txt_salario.get()),
                int(self.spin_dias.get()),
                float(self.txt_otros.get()),
                float(self.txt_salud.get()),
                float(self.txt_pension.get())
            )
            
            self.lista.agregar_empleado(emp)
            messagebox.showinfo("Mensaje", "El empleado ha sido agregado", parent=self)
            self.accion_limpiar()

        except ValueError:
            messagebox.showerror("Error", "Campo nulo o error en formato de numero", parent=self)


class VentanaNomina(tk.Toplevel):
    def __init__(self, padre, lista_empleados):
        super().__init__(padre)
        self.lista = lista_empleados
        self.title("Nómina de Empleados")
        self.geometry("350x250")
        self.resizable(False, False)
        centrar_ventana(self, 350, 250)
        self.transient(padre)
        
        self.crear_componentes()

    def crear_componentes(self):
        tk.Label(self, text="Lista de empleados:").place(x=20, y=10, width=135, height=23)

        
        cols = ("NOMBRE", "APELLIDOS", "SUELDO")
        self.tabla = ttk.Treeview(self, columns=cols, show="headings")
        
        self.tabla.heading("NOMBRE", text="NOMBRE")
        self.tabla.heading("APELLIDOS", text="APELLIDOS")
        self.tabla.heading("SUELDO", text="SUELDO")
        
        self.tabla.column("NOMBRE", width=100)
        self.tabla.column("APELLIDOS", width=100)
        self.tabla.column("SUELDO", width=100)

        
        for d in self.lista.obtener_matriz():
            self.tabla.insert("", tk.END, values=d)

        self.tabla.place(x=20, y=50, width=310, height=100)

        # Total Nómina
        total = self.lista.calcular_total_nomina()
        tk.Label(self, text=f"Total nómina mensual = $ {total:.2f}").place(x=20, y=160, width=250, height=23)


class VentanaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.empleados = ListaEmpleados()
        self.title("Nómina")
        self.geometry("280x380")
        self.resizable(False, False)
        centrar_ventana(self, 280, 380)
        
        self.crear_menu()

    def crear_menu(self):
        barra_menu = tk.Menu(self)
        self.config(menu=barra_menu)

        menu_opc = tk.Menu(barra_menu, tearoff=0)
        barra_menu.add_cascade(label="Menú", menu=menu_opc)

        menu_opc.add_command(label="Agregar empleado", command=self.abrir_agregar)
        menu_opc.add_command(label="Calcular nómina", command=self.abrir_nomina)
        menu_opc.add_separator()
        menu_opc.add_command(label="Guardar archivo", command=self.guardar_archivo)

    def abrir_agregar(self):
        VentanaAgregarEmpleado(self, self.empleados)

    def abrir_nomina(self):
        VentanaNomina(self, self.empleados)

    def guardar_archivo(self):
        # Seleccionar carpeta
        directorio = filedialog.askdirectory(title="Open")
        
        if directorio:
            try:
                ruta = os.path.join(directorio, "Nómina.txt")
                with open(ruta, "w", encoding="utf-8") as f:
                    f.write(self.empleados.convertir_texto())
                
                nombre_carpeta = os.path.basename(directorio)
                messagebox.showinfo("Mensaje", f"El archivo de la nómina Nómina.txt se ha creado en {nombre_carpeta}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Error al guardar: {e}")


if __name__ == "__main__":
    app = VentanaPrincipal()
    app.mainloop()
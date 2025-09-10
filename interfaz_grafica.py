import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk; Image.Resampling
from sistema_medico import SistemaMedico
from visualizador_graphviz import VisualizadorGraphviz
import os

class InterfazGrafica:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Turnos Médicos - Clínica")
        self.root.geometry("1000x700")
        self.root.resizable(True, True)
        self.root.configure(bg="#f0f4f8")

        self.estilo = ttk.Style()
        self.estilo.theme_use("clam")

        self.estilo.configure("TLabel", font=("Arial", 11), background="#f0f4f8")
        self.estilo.configure("TButton", font=("Arial", 11, "bold"), padding=8)
        self.estilo.configure("Titulo.TLabel", font=("Arial", 16, "bold"), foreground="#2c3e50", background="#f0f4f8")
        self.estilo.configure("Subtitulo.TLabel", font=("Arial", 12, "bold"), foreground="#34495e", background="#f0f4f8")

        self.estilo.map("TButton",
            foreground=[("active", "white")],
            background=[("pressed", "!disabled", "#2980b9"), ("active", "#3498db")]
        )

        self.sistema = SistemaMedico()
        self.visualizador = VisualizadorGraphviz("cola_turnos")

        self.crear_widgets()
        self.actualizar_lista_y_grafico()

    def crear_widgets(self):
        frame_izquierdo = tk.Frame(self.root, bg="white", padx=20, pady=20, relief="groove", bd=2)
        frame_izquierdo.pack(side=tk.LEFT, fill=tk.Y, padx=20, pady=20)

        ttk.Label(frame_izquierdo, text="Registrar Nuevo Paciente", style="Titulo.TLabel").pack(pady=(0, 20))

        ttk.Label(frame_izquierdo, text="Nombre:").pack(anchor=tk.W, pady=(5,0))
        self.entry_nombre = ttk.Entry(frame_izquierdo, width=30, font=("Arial", 11))
        self.entry_nombre.pack(pady=2, ipady=3)

        ttk.Label(frame_izquierdo, text="Edad:").pack(anchor=tk.W, pady=(10,0))
        self.entry_edad = ttk.Entry(frame_izquierdo, width=30, font=("Arial", 11))
        self.entry_edad.pack(pady=2, ipady=3)

        ttk.Label(frame_izquierdo, text="Especialidad:").pack(anchor=tk.W, pady=(10,0))
        self.combo_especialidad = ttk.Combobox(frame_izquierdo, values=[
            "Medicina General", "Pediatría", "Ginecología", "Dermatología"
        ], state="readonly", width=28, font=("Arial", 11))
        self.combo_especialidad.set("Medicina General")
        self.combo_especialidad.pack(pady=2, ipady=3)

        ttk.Button(frame_izquierdo, text="Registrar Paciente", command=self.registrar_paciente, style="TButton").pack(pady=(20,10), ipady=5, fill=tk.X)
        ttk.Button(frame_izquierdo, text="Atender Siguiente", command=self.atender_paciente, style="TButton").pack(pady=10, ipady=5, fill=tk.X)
        ttk.Button(frame_izquierdo, text="Salir", command=self.salir_aplicacion, style="TButton").pack(pady=(30,10), ipady=5, fill=tk.X)

        frame_derecho = tk.Frame(self.root, bg="#f0f4f8", padx=20, pady=20)
        frame_derecho.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(0,20), pady=20)

        ttk.Label(frame_derecho, text="Pacientes en Espera", style="Titulo.TLabel").pack(pady=(0,10))

        frame_lista = tk.Frame(frame_derecho, bg="white", relief="sunken", bd=1)
        frame_lista.pack(fill=tk.BOTH, expand=True, pady=(0,20))

        self.lista_pacientes = tk.Listbox(
            frame_lista,
            width=75,
            height=12,
            font=("Courier", 10),
            bg="white",
            fg="#2c3e50",
            selectbackground="#3498db",
            selectforeground="white",
            relief="flat"
        )
        scrollbar = ttk.Scrollbar(frame_lista, orient="vertical", command=self.lista_pacientes.yview)
        self.lista_pacientes.config(yscrollcommand=scrollbar.set)

        self.lista_pacientes.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(1,0), pady=1)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0,1), pady=1)

        ttk.Label(frame_derecho, text="Visualización de la Cola", style="Subtitulo.TLabel").pack(pady=(10,5))

        frame_imagen = tk.Frame(frame_derecho, bg="white", relief="groove", bd=2)
        frame_imagen.pack(fill=tk.BOTH, expand=True, pady=(5,0))

        self.label_imagen = tk.Label(
            frame_imagen,
            text="Bienvenido\nLa visualización aparecerá al registrar su primer paciente.",
            bg="white",
            fg="#2c3e50",
            font=("Arial", 13, "bold"),
            justify="center",
            wraplength=500,
            anchor="center"
        )
        self.label_imagen.pack(expand=True, fill="both")

    def registrar_paciente(self):
        nombre = self.entry_nombre.get().strip()
        edad_str = self.entry_edad.get().strip()
        especialidad = self.combo_especialidad.get()

        if not nombre or not edad_str or not especialidad:
            messagebox.showwarning("Advertencia", "Por favor, complete todos los campos.")
            return

        try:
            edad = int(edad_str)
            if edad < 0 or edad > 150:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "La edad debe ser un número entero válido (0-150).")
            return

        if self.sistema.registrar_paciente(nombre, edad, especialidad):
            messagebox.showinfo("Éxito", f"Paciente '{nombre}' ({edad} años) registrado correctamente.")
            self.limpiar_campos()
            self.actualizar_lista_y_grafico()
        else:
            messagebox.showerror("Error", "No se pudo registrar al paciente.")

    def limpiar_campos(self):
        self.entry_nombre.delete(0, tk.END)
        self.entry_edad.delete(0, tk.END)
        self.combo_especialidad.set("Medicina General")

    def atender_paciente(self):
        resultado = self.sistema.atender_siguiente()
        if "error" in resultado:
            messagebox.showinfo("ℹInformación", resultado["error"])
        else:
            paciente = resultado["paciente"]
            tiempo_espera = 0
            tiempo_atencion = paciente.obtener_tiempo_atencion()
            tiempo_total = tiempo_espera + tiempo_atencion

            mensaje = (
                f"¡ATENCIÓN!\n\n"
                f"Nombre: {paciente.nombre}\n"
                f"Edad: {paciente.edad} años\n"
                f"Especialidad: {paciente.especialidad}\n"
                f"Tiempo de atención: {tiempo_atencion} min\n"
                f"Tiempo en cola: {tiempo_espera} min\n"
                f"Tiempo total: {tiempo_total} min"
            )
            messagebox.showinfo("Paciente Atendido", mensaje)
            self.actualizar_lista_y_grafico()

    def actualizar_lista_y_grafico(self):
        self.lista_pacientes.delete(0, tk.END)
        tamano = self.sistema.obtener_tamano_cola()

        for i in range(tamano):
            paciente = self.sistema.obtener_paciente_en_posicion(i)
            if paciente:
                tiempo_espera = self.sistema.obtener_tiempo_espera_paciente(i)
                tiempo_atencion = paciente.obtener_tiempo_atencion()
                tiempo_total = tiempo_espera + tiempo_atencion
                self.lista_pacientes.insert(
                    tk.END,
                    f"{i+1}. {paciente.nombre} ({paciente.edad} años) - {paciente.especialidad} | Atención: {tiempo_atencion} min | Espera: {tiempo_espera} min | Total: {tiempo_total} min"
                )

        frente = self.sistema.obtener_frente_cola()
        self.visualizador.generar_grafo(frente)

        self.root.after(50, self.mostrar_imagen_grafico)

    def mostrar_imagen_grafico(self):
        ruta_imagen = self.visualizador.obtener_ruta_imagen()
        if os.path.exists(ruta_imagen):
            try:
                self.label_imagen.update_idletasks()

                container_width = self.label_imagen.winfo_width()
                container_height = self.label_imagen.winfo_height()

                if container_width <= 1: container_width = 800
                if container_height <= 1: container_height = 400

                imagen = Image.open(ruta_imagen)
                original_width, original_height = imagen.size

                scale_x = container_width / original_width
                scale_y = container_height / original_height
                scale = min(scale_x, scale_y)

                new_width = int(original_width * scale)
                new_height = int(original_height * scale)

                imagen = imagen.resize((new_width, new_height), Image.Resampling.LANCZOS)

                foto = ImageTk.PhotoImage(imagen)

                self.label_imagen.config(
                    image=foto,
                    text="",
                    bg="white",
                    anchor="center"
                )
                self.label_imagen.image = foto
                self.label_imagen.update()

            except Exception as e:
                print(f"ERROR AL CARGAR IMAGEN: {e}")
                self.label_imagen.config(
                    text=f"Error al cargar gráfico.\n{str(e)}",
                    image="",
                    bg="white",
                    fg="red",
                    font=("Arial", 12),
                    anchor="center",
                    justify="center"
                )
        else:
            self.label_imagen.config(
                text="Bienvenido\nRegistre su primer paciente para ver la visualización.",
                image="",
                bg="white",
                fg="#2c3e50",
                font=("Arial", 13, "bold"),
                justify="center",
                anchor="center",
                wraplength=500
            )

    def salir_aplicacion(self):
        confirmar = messagebox.askyesno("Salir", "¿Está seguro que desea salir de la aplicación?")
        if confirmar:
            self.root.destroy()
import tkinter as tk
from tkinter import ttk, messagebox
import datetime as dt
import calendar
import re


# -------------------------------
#  DatePicker simple (sin extras)
# -------------------------------
class DatePicker(tk.Toplevel):
    """
    Selector de fecha básico hecho con Tkinter puro.
    - Permite navegar entre meses y escoger un día.
    - Devuelve la fecha seleccionada en formato dt.date.
    Uso:
        picker = DatePicker(parent, initial_date=dt.date.today())
        parent.wait_window(picker)              # bloquea hasta cerrar
        fecha = picker.selected_date            # dt.date o None
    """
    def __init__(self, master, initial_date=None):
        super().__init__(master)
        self.title("Seleccionar fecha")
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()  # Modal

        # Configurar variables de estado
        today = dt.date.today()
        initial = initial_date or today
        self.year = initial.year
        self.month = initial.month
        self.selected_date = None

        # Estilos
        self.configure(padx=8, pady=8)

        # Encabezado (mes/año + navegación)
        header = ttk.Frame(self)
        header.grid(row=0, column=0, sticky="ew", pady=(0, 6))
        header.columnconfigure(1, weight=1)

        self.btn_prev = ttk.Button(header, text="◀", width=3, command=self.prev_month)
        self.btn_prev.grid(row=0, column=0, padx=(0, 6))

        self.lbl_title = ttk.Label(header, text="", font=("", 11, "bold"))
        self.lbl_title.grid(row=0, column=1, sticky="ew")

        self.btn_next = ttk.Button(header, text="▶", width=3, command=self.next_month)
        self.btn_next.grid(row=0, column=2, padx=(6, 0))

        # Días de la semana
        self.grid_days = ttk.Frame(self)
        self.grid_days.grid(row=1, column=0)

        # Botones inferiores
        footer = ttk.Frame(self)
        footer.grid(row=2, column=0, sticky="ew", pady=(8, 0))
        ttk.Button(footer, text="Hoy", command=self.set_today).grid(row=0, column=0, padx=(0, 6))
        ttk.Button(footer, text="Cancelar", command=self.destroy).grid(row=0, column=1)

        self.draw_calendar()

        # Centrar sobre la ventana padre
        self.update_idletasks()
        self.center_over_parent(master)

    def center_over_parent(self, master):
        """Centra el Toplevel sobre su padre."""
        if master is None:
            return
        px = master.winfo_rootx()
        py = master.winfo_rooty()
        pw = master.winfo_width()
        ph = master.winfo_height()
        sw = self.winfo_width()
        sh = self.winfo_height()
        x = px + (pw - sw) // 2
        y = py + (ph - sh) // 2
        self.geometry(f"+{x}+{y}")

    def prev_month(self):
        """Navega al mes anterior."""
        if self.month == 1:
            self.month = 12
            self.year -= 1
        else:
            self.month -= 1
        self.draw_calendar()

    def next_month(self):
        """Navega al mes siguiente."""
        if self.month == 12:
            self.month = 1
            self.year += 1
        else:
            self.month += 1
        self.draw_calendar()

    def set_today(self):
        """Selecciona la fecha de hoy y cierra."""
        self.selected_date = dt.date.today()
        self.destroy()

    def choose_day(self, day):
        """Selecciona un día del mes actual y cierra."""
        self.selected_date = dt.date(self.year, self.month, day)
        self.destroy()

    def draw_calendar(self):
        """Dibuja el calendario del mes actual."""
        # Limpiar contenido de la grilla de días
        for child in self.grid_days.winfo_children():
            child.destroy()

        # Título Mes/Año
        month_name = calendar.month_name[self.month].capitalize()
        self.lbl_title.config(text=f"{month_name} {self.year}")

        # Encabezado de días (L a D)
        days_header = ["L", "M", "X", "J", "V", "S", "D"]
        for col, name in enumerate(days_header):
            ttk.Label(self.grid_days, text=name, anchor="center").grid(row=0, column=col, padx=4, pady=2)

        # Matriz del calendario: semanas x días
        cal = calendar.Calendar(firstweekday=0)  # 0 = lunes
        # Ajuste para mostrar L-D (si tu región considera lunes=0; si no, adapta)
        # NOTE: Python usa 0=lunes por calendar.setfirstweekday(0) en algunas versiones
        # Para forzar:
        calendar.setfirstweekday(calendar.MONDAY)
        weeks = calendar.monthcalendar(self.year, self.month)

        # Crear botones de días
        for r, week in enumerate(weeks, start=1):
            for c, day in enumerate(week):
                if day == 0:
                    # Día vacío (relleno de la cuadricula)
                    ttk.Label(self.grid_days, text=" ").grid(row=r, column=c, padx=2, pady=2)
                else:
                    btn = ttk.Button(self.grid_days, text=str(day), width=3,
                                     command=lambda d=day: self.choose_day(d))
                    btn.grid(row=r, column=c, padx=2, pady=2)


# -------------------------------
#   Aplicación principal
# -------------------------------
class AgendaApp(tk.Tk):
    """Aplicación de Agenda Personal con Tkinter + ttk."""
    TIME_REGEX = re.compile(r"^(?:[01]\d|2[0-3]):[0-5]\d$")  # HH:MM formato 24h

    def __init__(self):
        super().__init__()
        self.title("Agenda Personal - Tkinter")
        self.geometry("760x480")
        self.minsize(720, 420)

        # Contenedor raíz con padding
        root = ttk.Frame(self, padding=10)
        root.pack(fill="both", expand=True)

        # ------------------ Frames (organización lógica) ------------------
        # Frame lista (Treeview con scrollbar)
        self.frame_lista = ttk.LabelFrame(root, text="Eventos programados")
        self.frame_lista.pack(side="top", fill="both", expand=True)

        # Frame formulario (fecha/hora/descripcion)
        self.frame_form = ttk.LabelFrame(root, text="Nuevo evento")
        self.frame_form.pack(side="top", fill="x", pady=(10, 0))

        # Frame acciones (botones)
        self.frame_acciones = ttk.Frame(root)
        self.frame_acciones.pack(side="top", fill="x", pady=(10, 0))

        # ------------------ Treeview ------------------
        columns = ("fecha", "hora", "descripcion")
        self.tree = ttk.Treeview(self.frame_lista, columns=columns, show="headings", height=10)
        self.tree.heading("fecha", text="Fecha (dd/mm/aaaa)")
        self.tree.heading("hora", text="Hora (HH:MM)")
        self.tree.heading("descripcion", text="Descripción")

        self.tree.column("fecha", width=150, anchor="center")
        self.tree.column("hora", width=120, anchor="center")
        self.tree.column("descripcion", width=420, anchor="w")

        scroll_y = ttk.Scrollbar(self.frame_lista, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll_y.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scroll_y.pack(side="right", fill="y")

        # ------------------ Formulario ------------------
        # Etiquetas
        ttk.Label(self.frame_form, text="Fecha:").grid(row=0, column=0, sticky="w", padx=(8, 6), pady=8)
        ttk.Label(self.frame_form, text="Hora (24h):").grid(row=0, column=2, sticky="w", padx=(8, 6), pady=8)
        ttk.Label(self.frame_form, text="Descripción:").grid(row=1, column=0, sticky="w", padx=(8, 6), pady=(0, 10))

        # Fecha: Entry + botón DatePicker
        self.var_fecha = tk.StringVar()
        self.entry_fecha = ttk.Entry(self.frame_form, textvariable=self.var_fecha, width=16, state="readonly")
        self.entry_fecha.grid(row=0, column=1, sticky="w", padx=(0, 6), pady=8)

        self.btn_cal = ttk.Button(self.frame_form, text="📅", width=3, command=self.abrir_datepicker)
        self.btn_cal.grid(row=0, column=1, sticky="e", padx=(0, 0), pady=8)

        # Hora: Entry con placeholder HH:MM
        self.var_hora = tk.StringVar()
        self.entry_hora = ttk.Entry(self.frame_form, textvariable=self.var_hora, width=10)
        self.entry_hora.grid(row=0, column=3, sticky="w", padx=(0, 6), pady=8)
        self.entry_hora.insert(0, "08:00")  # valor por defecto

        # Descripción: Entry ancho
        self.var_desc = tk.StringVar()
        self.entry_desc = ttk.Entry(self.frame_form, textvariable=self.var_desc, width=70)
        self.entry_desc.grid(row=1, column=1, columnspan=3, sticky="ew", padx=(0, 8), pady=(0, 10))

        # Ajuste de columnas del frame_form
        self.frame_form.columnconfigure(1, weight=1)
        self.frame_form.columnconfigure(3, weight=0)

        # ------------------ Botones de acción ------------------
        self.btn_agregar = ttk.Button(self.frame_acciones, text="Agregar evento", command=self.agregar_evento)
        self.btn_eliminar = ttk.Button(self.frame_acciones, text="Eliminar seleccionado", command=self.eliminar_seleccion)
        self.btn_salir = ttk.Button(self.frame_acciones, text="Salir", command=self.destroy)

        self.btn_agregar.pack(side="left", padx=5)
        self.btn_eliminar.pack(side="left", padx=5)
        self.btn_salir.pack(side="right", padx=5)

        # Lista interna de eventos (para ordenar/validar si lo necesitas)
        # Estructura: [(date_obj, "HH:MM", "Descripción"), ...]
        self.eventos = []

        # Fecha por defecto: hoy
        self.set_fecha(dt.date.today())

    # ------------------ Helpers UI ------------------
    def abrir_datepicker(self):
        """Abre el selector de fecha (DatePicker) y setea el Entry si el usuario selecciona."""
        # Intentar parsear lo que haya, si existe
        initial = None
        if self.var_fecha.get():
            try:
                initial = dt.datetime.strptime(self.var_fecha.get(), "%d/%m/%Y").date()
            except ValueError:
                initial = None

        picker = DatePicker(self, initial_date=initial)
        self.wait_window(picker)
        if picker.selected_date:
            self.set_fecha(picker.selected_date)

    def set_fecha(self, date_obj: dt.date):
        """Establece la fecha en el Entry en formato dd/mm/yyyy."""
        self.var_fecha.set(date_obj.strftime("%d/%m/%Y"))

    # ------------------ Validaciones ------------------
    def validar_fecha(self, texto_fecha: str) -> dt.date | None:
        """Valida 'dd/mm/yyyy' y devuelve dt.date o None."""
        try:
            return dt.datetime.strptime(texto_fecha, "%d/%m/%Y").date()
        except ValueError:
            return None

    def validar_hora(self, texto_hora: str) -> bool:
        """Valida formato 24h HH:MM."""
        return bool(self.TIME_REGEX.match(texto_hora.strip()))

    # ------------------ Operaciones ------------------
    def agregar_evento(self):
        """Lee los campos, valida y agrega a la tabla (Treeview)."""
        fecha_txt = self.var_fecha.get().strip()
        hora_txt = self.var_hora.get().strip()
        desc_txt = self.var_desc.get().strip()

        # Validar campos obligatorios
        if not fecha_txt or not hora_txt or not desc_txt:
            messagebox.showwarning("Campos incompletos", "Por favor, completa fecha, hora y descripción.")
            return

        # Validar fecha y hora
        fecha_obj = self.validar_fecha(fecha_txt)
        if not fecha_obj:
            messagebox.showerror("Fecha inválida", "La fecha debe tener el formato dd/mm/aaaa.")
            return

        if not self.validar_hora(hora_txt):
            messagebox.showerror("Hora inválida", "La hora debe tener el formato 24h HH:MM (ej. 08:30, 14:05).")
            return

        # Agregar a la lista interna
        self.eventos.append((fecha_obj, hora_txt, desc_txt))
        # Ordenar por fecha y hora para que la vista quede organizada
        self.eventos.sort(key=lambda e: (e[0], e[1]))

        # Repintar Treeview (simple y claro para esta escala)
        self.refrescar_tree()

        # Limpiar únicamente la descripción para acelerar el ingreso de varios eventos
        self.var_desc.set("")
        self.entry_desc.focus()

    def eliminar_seleccion(self):
        """Elimina el evento seleccionado en el Treeview (con confirmación)."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Sin selección", "Selecciona un evento en la lista para eliminar.")
            return

        if not messagebox.askyesno("Confirmar eliminación", "¿Deseas eliminar el evento seleccionado?"):
            return

        # Recuperar valores del Treeview
        item_id = selected[0]
        valores = self.tree.item(item_id, "values")  # (fecha_txt, hora_txt, desc)
        fecha_txt, hora_txt, desc_txt = valores

        # Convertir fecha de texto a date para comparar con la lista interna
        try:
            fecha_obj = dt.datetime.strptime(fecha_txt, "%d/%m/%Y").date()
        except ValueError:
            fecha_obj = None

        # Quitar de la lista interna (primer match)
        for i, (f, h, d) in enumerate(self.eventos):
            if f == fecha_obj and h == hora_txt and d == desc_txt:
                del self.eventos[i]
                break

        # Quitar del Treeview
        self.tree.delete(item_id)

    def refrescar_tree(self):
        """Limpia y vuelve a cargar los datos del Treeview en el orden actual."""
        for row in self.tree.get_children():
            self.tree.delete(row)

        for f, h, d in self.eventos:
            self.tree.insert("", "end", values=(f.strftime("%d/%m/%Y"), h, d))


# -------------------------------
#  Punto de entrada
# -------------------------------
if __name__ == "__main__":
    app = AgendaApp()
    app.mainloop()

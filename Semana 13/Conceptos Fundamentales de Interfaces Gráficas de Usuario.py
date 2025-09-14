import tkinter as tk
from tkinter import ttk, messagebox


APP_TITLE = "Gestor de Ítems — GUI Básica (Tkinter)"
PAD = 10
MIN_WIDTH = 520
MIN_HEIGHT = 380


class App(ttk.Frame):
    """Contenedor principal de la aplicación."""

    def __init__(self, master: tk.Tk | tk.Toplevel):
        super().__init__(master, padding=PAD)
        self.master: tk.Tk = master

        # Estado
        self.items_var = tk.StringVar(value=[])  # fuente de datos para el Listbox
        self.input_var = tk.StringVar()          # texto del Entry
        self.status_var = tk.StringVar(value="Listo. Ingrese un texto y presione Agregar o Enter.")

        # Configuración raíz
        self.master.title(APP_TITLE)
        self.master.minsize(MIN_WIDTH, MIN_HEIGHT)
        self.master.bind("<Escape>", self._on_escape)

        # Crear y colocar widgets
        self._build_widgets()
        self._configure_layout()

    # ---------- Construcción de UI ----------
    def _build_widgets(self) -> None:
        # Título / encabezado
        self.lbl_title = ttk.Label(self, text="Gestión simple de datos", font=("Segoe UI", 14, "bold"))
        self.lbl_sub = ttk.Label(self, text="Agrega textos a la lista. Usa Enter para agregar más rápido.")

        # Campo de texto con etiqueta
        self.lbl_input = ttk.Label(self, text="Nuevo ítem:")
        self.entry_input = ttk.Entry(self, textvariable=self.input_var, width=40)
        self.entry_input.bind("<Return>", self._on_add)  # Enter agrega

        # Botones
        self.btn_add = ttk.Button(self, text="Agregar", command=self._on_add)
        self.btn_clear_selected = ttk.Button(self, text="Limpiar selección", command=self._on_clear_selected)
        self.btn_clear_all = ttk.Button(self, text="Limpiar todo", command=self._on_clear_all)

        # Lista + Scrollbar
        self.listbox = tk.Listbox(self, listvariable=self.items_var, height=10, activestyle="dotbox")
        self.listbox.bind("<<ListboxSelect>>", self._on_select_change)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.listbox.yview)
        self.listbox.config(yscrollcommand=self.scrollbar.set)

        # Barra de estado
        self.status = ttk.Label(self, textvariable=self.status_var, relief="sunken", anchor="w")

        # Agregar todo al frame principal
        self.lbl_title.grid(row=0, column=0, columnspan=4, sticky="w")
        self.lbl_sub.grid(row=1, column=0, columnspan=4, sticky="w", pady=(0, PAD))

        self.lbl_input.grid(row=2, column=0, sticky="e", padx=(0, 5))
        self.entry_input.grid(row=2, column=1, columnspan=2, sticky="we")

        self.btn_add.grid(row=2, column=3, sticky="we", padx=(5, 0))
        self.btn_clear_selected.grid(row=3, column=2, sticky="we", pady=(5, 0))
        self.btn_clear_all.grid(row=3, column=3, sticky="we", pady=(5, 0))

        self.listbox.grid(row=4, column=0, columnspan=3, sticky="nsew", pady=(PAD, 0))
        self.scrollbar.grid(row=4, column=3, sticky="nsw", pady=(PAD, 0))

        self.status.grid(row=5, column=0, columnspan=4, sticky="we", pady=(PAD, 0))

    def _configure_layout(self) -> None:
        self.grid(sticky="nsew")
        # Expandir filas/columnas
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)

        for col in range(4):
            self.columnconfigure(col, weight=1 if col in (1, 2, 3) else 0)
        self.rowconfigure(4, weight=1)  # la fila de la listbox crece

    # ---------- Lógica de eventos ----------
    def _normalize_text(self, text: str) -> str:
        """Limpia espacios sobrantes; retorna el texto preparado para agregar."""
        return text.strip()

    def _on_add(self, event=None) -> None:
        text = self._normalize_text(self.input_var.get())
        if not text:
            self._flash_entry_error("El campo está vacío. Escriba un texto para agregar.")
            return
        # Validación: evitar duplicados exactos (opcional, se puede quitar)
        current = list(self.items_var.get())
        if text in current:
            self.status_var.set("El ítem ya existe en la lista.")
            return
        current.append(text)
        self.items_var.set(current)
        self.input_var.set("")  # limpiar campo
        self.entry_input.focus_set()
        self.status_var.set(f"Agregado: “{text}”. Total: {len(current)}")

    def _on_clear_selected(self) -> None:
        selection = list(self.listbox.curselection())
        if not selection:
            self.status_var.set("No hay selección para limpiar.")
            return
        # Eliminar desde el final para no desplazar índices
        for idx in reversed(selection):
            self.listbox.delete(idx)
        # Sincronizar el listvariable con el contenido actual
        remaining = list(self.listbox.get(0, tk.END))
        self.items_var.set(remaining)
        self.status_var.set(f"Ítems eliminados: {len(selection)}. Total: {len(remaining)}")

    def _on_clear_all(self) -> None:
        if not self.listbox.size():
            self.status_var.set("La lista ya está vacía.")
            return
        if messagebox.askyesno("Confirmación", "¿Desea eliminar todos los ítems?"):
            self.listbox.delete(0, tk.END)
            self.items_var.set([])
            self.status_var.set("Lista vaciada.")

    def _on_select_change(self, event=None) -> None:
        sel = self.listbox.curselection()
        if sel:
            count = len(sel)
            self.status_var.set(f"Selección: {count} ítem(s).")
        else:
            self.status_var.set("Sin selección.")

    def _on_escape(self, event=None) -> None:
        # Atajo: ESC limpia el Entry si hay texto; si está vacío, pregunta para salir
        if self.input_var.get():
            self.input_var.set("")
            self.status_var.set("Entrada limpiada (ESC).")
        else:
            self._confirm_exit()

    # ---------- Utilidades de UI ----------
    def _confirm_exit(self) -> None:
        if messagebox.askokcancel("Salir", "¿Desea salir de la aplicación?"):
            self.master.destroy()

    def _flash_entry_error(self, msg: str) -> None:
        """Resalta temporalmente el Entry para indicar error y muestra mensaje en status."""
        self.status_var.set(msg)
        orig = self.entry_input.cget("foreground")
        self.entry_input.config(foreground="red")
        # Después de 300 ms, restaurar
        self.after(300, lambda: self.entry_input.config(foreground=orig))


def main() -> None:
    root = tk.Tk()
    # Estilo nativo con ttk
    try:
        ttk.Style().theme_use("clam")
    except tk.TclError:
        pass
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()

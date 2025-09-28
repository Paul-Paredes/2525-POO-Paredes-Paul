import tkinter as tk
from tkinter import messagebox


# -------------------------
# Clase principal de la aplicación
# -------------------------
class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lista de Tareas")
        self.root.geometry("400x400")

        # Lista para almacenar las tareas (texto y estado)
        self.tasks = []

        # -------------------------
        # Widgets de la interfaz
        # -------------------------

        # Campo de entrada de texto
        self.entry = tk.Entry(root, width=40)
        self.entry.pack(pady=10)
        self.entry.bind("<Return>", self.add_task)  # Permite añadir tarea con Enter

        # Botones de acción
        self.btn_add = tk.Button(root, text="Añadir Tarea", command=self.add_task)
        self.btn_add.pack(pady=5)

        self.btn_complete = tk.Button(root, text="Marcar como Completada", command=self.complete_task)
        self.btn_complete.pack(pady=5)

        self.btn_delete = tk.Button(root, text="Eliminar Tarea", command=self.delete_task)
        self.btn_delete.pack(pady=5)

        # Listbox para mostrar tareas
        self.listbox = tk.Listbox(root, width=50, height=15, selectmode=tk.SINGLE)
        self.listbox.pack(pady=10)
        self.listbox.bind("<Double-1>", self.complete_task)  # Doble clic = completar tarea

    # -------------------------
    # Funcionalidades principales
    # -------------------------

    def add_task(self, event=None):
        """Añade una tarea desde el campo de entrada"""
        task_text = self.entry.get().strip()
        if task_text:
            self.tasks.append({"text": task_text, "completed": False})
            self.update_listbox()
            self.entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Advertencia", "No puedes añadir una tarea vacía.")

    def complete_task(self, event=None):
        """Marca la tarea seleccionada como completada"""
        try:
            index = self.listbox.curselection()[0]
            self.tasks[index]["completed"] = not self.tasks[index]["completed"]
            self.update_listbox()
        except IndexError:
            messagebox.showwarning("Advertencia", "Selecciona una tarea para marcarla.")

    def delete_task(self):
        """Elimina la tarea seleccionada"""
        try:
            index = self.listbox.curselection()[0]
            del self.tasks[index]
            self.update_listbox()
        except IndexError:
            messagebox.showwarning("Advertencia", "Selecciona una tarea para eliminarla.")

    def update_listbox(self):
        """Actualiza la visualización de la lista de tareas"""
        self.listbox.delete(0, tk.END)
        for task in self.tasks:
            if task["completed"]:
                self.listbox.insert(tk.END, f"✔ {task['text']}")
            else:
                self.listbox.insert(tk.END, task["text"])


# -------------------------
# Inicializar la aplicación
# -------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()

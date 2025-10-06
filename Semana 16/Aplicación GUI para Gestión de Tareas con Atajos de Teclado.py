import tkinter as tk
from tkinter import messagebox

class GestorTareas:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Tareas")
        self.root.geometry("400x400")
        self.root.resizable(False, False)

        # Campo de entrada
        self.entry_tarea = tk.Entry(root, width=40)
        self.entry_tarea.pack(pady=10)
        self.entry_tarea.focus()

        # Lista de tareas
        self.lista_tareas = tk.Listbox(root, width=50, height=15, selectmode=tk.SINGLE)
        self.lista_tareas.pack(pady=10)

        # Botones
        frame_botones = tk.Frame(root)
        frame_botones.pack()

        btn_agregar = tk.Button(frame_botones, text="Agregar", width=12, command=self.agregar_tarea)
        btn_agregar.grid(row=0, column=0, padx=5)

        btn_completar = tk.Button(frame_botones, text="Completar", width=12, command=self.completar_tarea)
        btn_completar.grid(row=0, column=1, padx=5)

        btn_eliminar = tk.Button(frame_botones, text="Eliminar", width=12, command=self.eliminar_tarea)
        btn_eliminar.grid(row=0, column=2, padx=5)

        # Atajos de teclado
        self.root.bind("<Return>", lambda event: self.agregar_tarea())
        self.root.bind("<c>", lambda event: self.completar_tarea())
        self.root.bind("<C>", lambda event: self.completar_tarea())
        self.root.bind("<Delete>", lambda event: self.eliminar_tarea())
        self.root.bind("<d>", lambda event: self.eliminar_tarea())
        self.root.bind("<D>", lambda event: self.eliminar_tarea())
        self.root.bind("<Escape>", lambda event: self.cerrar_aplicacion())

        # Lista para manejar el estado de tareas
        self.tareas = []

    def agregar_tarea(self):
        tarea = self.entry_tarea.get().strip()
        if tarea:
            self.tareas.append({"texto": tarea, "completada": False})
            self.lista_tareas.insert(tk.END, tarea)
            self.entry_tarea.delete(0, tk.END)
        else:
            messagebox.showwarning("Advertencia", "Escribe una tarea antes de agregarla.")

    def completar_tarea(self):
        seleccion = self.lista_tareas.curselection()
        if seleccion:
            index = seleccion[0]
            tarea = self.tareas[index]
            if not tarea["completada"]:
                tarea["completada"] = True
                self.lista_tareas.delete(index)
                self.lista_tareas.insert(index, f"✔ {tarea['texto']}")
                self.lista_tareas.itemconfig(index, fg="green")
            else:
                tarea["completada"] = False
                self.lista_tareas.delete(index)
                self.lista_tareas.insert(index, tarea["texto"])
                self.lista_tareas.itemconfig(index, fg="black")
        else:
            messagebox.showinfo("Info", "Selecciona una tarea para marcarla como completada.")

    def eliminar_tarea(self):
        seleccion = self.lista_tareas.curselection()
        if seleccion:
            index = seleccion[0]
            self.lista_tareas.delete(index)
            del self.tareas[index]
        else:
            messagebox.showinfo("Info", "Selecciona una tarea para eliminarla.")

    def cerrar_aplicacion(self):
        if messagebox.askokcancel("Salir", "¿Deseas cerrar la aplicación?"):
            self.root.destroy()

# Ejecutar aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = GestorTareas(root)
    root.mainloop()

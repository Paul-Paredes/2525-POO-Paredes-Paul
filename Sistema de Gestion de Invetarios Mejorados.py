# inventario.py
# Sistema de Inventario con archivo y excepciones (versión compacta, sin warnings)

from __future__ import annotations
import json
import os
from typing import Dict, Optional

ARCHIVO = "inventario.txt"


class Producto:
    def __init__(self, id_producto: str, nombre: str, cantidad: int, precio: float) -> None:
        if not isinstance(id_producto, str) or not id_producto.strip():
            raise ValueError("El ID debe ser texto no vacío.")
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre debe ser texto no vacío.")
        if not isinstance(cantidad, int) or cantidad < 0:
            raise ValueError("La cantidad debe ser entero >= 0.")
        if not isinstance(precio, (int, float)) or precio < 0:
            raise ValueError("El precio debe ser número >= 0.")
        self.id_producto = id_producto.strip()
        self.nombre = nombre.strip()
        self.cantidad = int(cantidad)
        self.precio = float(precio)

    def __str__(self) -> str:
        return (
            f"{self.id_producto} | {self.nombre} | Cantidad: {self.cantidad} | "
            f"Precio: ${self.precio:.2f} | Total: ${self.cantidad * self.precio:.2f}"
        )

    def a_dict(self) -> Dict[str, object]:
        return {
            "id": self.id_producto,
            "nombre": self.nombre,
            "cantidad": self.cantidad,
            "precio": self.precio,
        }

    @staticmethod
    def desde_dict(data: Dict[str, object]) -> "Producto":
        return Producto(
            id_producto=str(data["id"]),
            nombre=str(data["nombre"]),
            cantidad=int(data["cantidad"]),
            precio=float(data["precio"]),
        )


class Inventario:
    def __init__(self, ruta: str = ARCHIVO) -> None:
        self._ruta = ruta
        self.productos: Dict[str, Producto] = {}
        self.cargar()

    # ---------- Persistencia ----------
    def cargar(self) -> None:
        if not os.path.exists(self._ruta):
            self.guardar()  # crea archivo vacío
            print("Archivo de inventario no existía. Se creó vacío.")
            return
        try:
            self.productos.clear()
            with open(self._ruta, "r", encoding="utf-8") as f:
                ok, corruptas = 0, 0
                for linea in f:
                    linea = linea.strip()
                    if not linea:
                        continue
                    try:
                        p = Producto.desde_dict(json.loads(linea))
                        self.productos[p.id_producto] = p
                        ok += 1
                    except (json.JSONDecodeError, KeyError, ValueError, TypeError):
                        corruptas += 1
            msg = f"Carga inicial: {ok} producto(s) válido(s)."
            if corruptas:
                msg += f"  {corruptas} línea(s) corrupta(s) ignoradas."
            print(msg)
        except PermissionError:
            print("Permiso denegado al leer el archivo de inventario.")
        except OSError as e:
            print(f"Error de E/S al leer el archivo: {e}")

    def guardar(self) -> None:
        try:
            with open(self._ruta, "w", encoding="utf-8") as f:
                for p in self.productos.values():
                    f.write(json.dumps(p.a_dict(), ensure_ascii=False) + "\n")
        except PermissionError:
            print("Permiso denegado al escribir el archivo de inventario.")
        except OSError as e:
            print(f"Error de E/S al guardar: {e}")

    # ---------- Operaciones ----------
    def agregar(self, p: Producto) -> None:
        if p.id_producto in self.productos:
            print("Error: Producto ya existe.")
            return
        self.productos[p.id_producto] = p
        self.guardar()
        print("Producto agregado y guardado en el archivo.")

    def eliminar(self, id_producto: str) -> None:
        if id_producto not in self.productos:
            print("Error: Producto no encontrado.")
            return
        del self.productos[id_producto]
        self.guardar()
        print("Producto eliminado y archivo actualizado.")

    def actualizar(
        self,
        id_producto: str,
        cantidad: Optional[int] = None,
        precio: Optional[float] = None,
    ) -> None:
        prod = self.productos.get(id_producto)
        if not prod:
            print("Error: Producto no encontrado.")
            return

        cambios = 0
        if cantidad is not None:
            if isinstance(cantidad, int) and cantidad >= 0:
                prod.cantidad = cantidad
                cambios += 1
            else:
                print("Error: La cantidad debe ser un entero >= 0.")
        if precio is not None:
            if isinstance(precio, (int, float)) and precio >= 0:
                prod.precio = float(precio)
                cambios += 1
            else:
                print("Error: El precio debe ser un número >= 0.")

        if cambios:
            self.guardar()
            print("Producto actualizado y cambios guardados en el archivo.")
        else:
            print("No se realizaron cambios.")

    def buscar(self, nombre: str) -> None:
        patron = nombre.strip().lower()
        encontrados = [p for p in self.productos.values() if patron in p.nombre.lower()]
        if encontrados:
            for p in encontrados:
                print(p)
        else:
            print("No se encontraron productos con ese nombre.")

    def mostrar(self) -> None:
        if not self.productos:
            print("(Inventario vacío)")
            return
        print("\nID | Nombre | Cantidad | Precio | Total")
        print("-" * 60)
        for p in sorted(self.productos.values(), key=lambda x: x.id_producto):
            print(p)


# ---------- Utilidades de entrada ----------
def leer_entero(mensaje: str) -> int:
    while True:
        dato = input(mensaje).strip()
        try:
            return int(dato)
        except ValueError:
            print("Entrada inválida: debe ser un entero.")


def leer_flotante(mensaje: str) -> float:
    while True:
        dato = input(mensaje).strip().replace(",", ".")
        try:
            return float(dato)
        except ValueError:
            print("Entrada inválida: debe ser un número.")


def leer_texto_no_vacio(mensaje: str) -> str:
    while True:
        dato = input(mensaje).strip()
        if dato:
            return dato
        print("Entrada inválida: no puede estar vacía.")


# ---------- Menú ----------
def menu() -> None:
    inv = Inventario()
    try:
        while True:
            print("\n===== MENÚ INVENTARIO =====")
            print("1. Agregar Producto")
            print("2. Eliminar Producto")
            print("3. Actualizar Producto")
            print("4. Buscar Producto por nombre")
            print("5. Mostrar Inventario")
            print("6. Salir")
            opcion = input("Seleccione una opción: ").strip()

            if opcion == "6":
                print("Saliendo... Hasta luego.")
                break
            elif opcion == "1":
                print("\n[Agregar Producto]")
                try:
                    idp = leer_texto_no_vacio("ID único: ")
                    nombre = leer_texto_no_vacio("Nombre: ")
                    cantidad = leer_entero("Cantidad (entero >= 0): ")
                    precio = leer_flotante("Precio (>= 0): ")
                    inv.agregar(Producto(idp, nombre, cantidad, precio))
                except ValueError as e:
                    print(f"Error: {e}")
            elif opcion == "2":
                print("\n[Eliminar Producto]")
                inv.eliminar(leer_texto_no_vacio("ID a eliminar: "))
            elif opcion == "3":
                print("\n[Actualizar Producto]")
                idp = leer_texto_no_vacio("ID a actualizar: ")
                cambiar_cantidad = input("¿Cambiar cantidad? (s/n): ").strip().lower() == "s"
                nueva_cantidad = leer_entero("Nueva cantidad: ") if cambiar_cantidad else None
                cambiar_precio = input("¿Cambiar precio? (s/n): ").strip().lower() == "s"
                nuevo_precio = leer_flotante("Nuevo precio: ") if cambiar_precio else None
                inv.actualizar(idp, cantidad=nueva_cantidad, precio=nuevo_precio)
            elif opcion == "4":
                print("\n[Buscar Producto por nombre]")
                inv.buscar(leer_texto_no_vacio("Texto a buscar: "))
            elif opcion == "5":
                print("\n[Mostrar Inventario]")
                inv.mostrar()
            else:
                print("Opción inválida. Intente de nuevo.")
    except (KeyboardInterrupt, EOFError):
        print("\nInterrupción detectada. Saliendo del programa.")


if __name__ == "__main__":
    menu()
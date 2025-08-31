from __future__ import annotations
import json
from dataclasses import dataclass, asdict
from typing import Dict, List, Tuple, Optional


# -----------------------------
# Modelo de dominio
# -----------------------------
@dataclass
class Producto:
    """
    Representa un ítem del inventario.
    - id: identificador único (str)
    - nombre: nombre del producto (str)
    - cantidad: unidades disponibles (int >= 0)
    - precio: precio unitario (float >= 0)
    """
    id: str
    nombre: str
    cantidad: int
    precio: float

    # Getters/Setters explícitos (además de dataclass) para la rúbrica de POO:
    def get_id(self) -> str:
        return self.id

    def set_id(self, nuevo_id: str) -> None:
        if not nuevo_id or not isinstance(nuevo_id, str):
            raise ValueError("El ID debe ser un texto no vacío.")
        self.id = nuevo_id

    def get_nombre(self) -> str:
        return self.nombre

    def set_nombre(self, nuevo_nombre: str) -> None:
        if not nuevo_nombre or not isinstance(nuevo_nombre, str):
            raise ValueError("El nombre debe ser un texto no vacío.")
        self.nombre = nuevo_nombre

    def get_cantidad(self) -> int:
        return self.cantidad

    def set_cantidad(self, nueva_cantidad: int) -> None:
        if not isinstance(nueva_cantidad, int) or nueva_cantidad < 0:
            raise ValueError("La cantidad debe ser un entero >= 0.")
        self.cantidad = nueva_cantidad

    def get_precio(self) -> float:
        return self.precio

    def set_precio(self, nuevo_precio: float) -> None:
        if not isinstance(nuevo_precio, (int, float)) or nuevo_precio < 0:
            raise ValueError("El precio debe ser un número >= 0.")
        self.precio = float(nuevo_precio)


# -----------------------------
# Repositorio / Colecciones
# -----------------------------
class Inventario:
    """
    Gestiona un conjunto de productos utilizando colecciones:
    - dict[str, Producto] para acceso y actualización O(1) por ID
    - list[Producto] para listados/ordenamientos puntuales
    - set[str] para asegurar unicidad de IDs ya cargados (integridad)
    - tuple para claves de ordenamiento (nombre, precio, etc.)
    """
    def __init__(self) -> None:
        self._productos: Dict[str, Producto] = {}
        self._ids: set[str] = set()  # refuerza unicidad

    # --------- CRUD ----------
    def agregar(self, producto: Producto) -> None:
        if producto.id in self._productos or producto.id in self._ids:
            raise KeyError(f"Ya existe un producto con ID '{producto.id}'.")
        self._productos[producto.id] = producto
        self._ids.add(producto.id)

    def eliminar(self, product_id: str) -> bool:
        if product_id in self._productos:
            del self._productos[product_id]
            self._ids.discard(product_id)
            return True
        return False

    def actualizar_cantidad(self, product_id: str, nueva_cantidad: int) -> None:
        prod = self._obtener(product_id)
        prod.set_cantidad(nueva_cantidad)

    def actualizar_precio(self, product_id: str, nuevo_precio: float) -> None:
        prod = self._obtener(product_id)
        prod.set_precio(nuevo_precio)

    def _obtener(self, product_id: str) -> Producto:
        if product_id not in self._productos:
            raise KeyError(f"No existe producto con ID '{product_id}'.")
        return self._productos[product_id]

    # --------- Consultas ----------
    def buscar_por_nombre(self, texto: str) -> List[Producto]:
        """
        Búsqueda case-insensitive. Devuelve una lista (puede estar vacía).
        """
        t = texto.strip().lower()
        return [p for p in self._productos.values() if t in p.nombre.lower()]

    def todos(self, ordenar_por: str = "id") -> List[Producto]:
        """
        Devuelve todos los productos como lista, ordenados por:
        - "id", "nombre", "cantidad", "precio"
        """
        items: List[Producto] = list(self._productos.values())

        # tuple como clave de ordenamiento opcional
        if ordenar_por == "id":
            keyf = lambda p: (p.id,)
        elif ordenar_por == "nombre":
            keyf = lambda p: (p.nombre.lower(), p.id)
        elif ordenar_por == "cantidad":
            keyf = lambda p: (p.cantidad, p.id)
        elif ordenar_por == "precio":
            keyf = lambda p: (p.precio, p.id)
        else:
            keyf = lambda p: (p.id,)

        return sorted(items, key=keyf)

    # --------- Persistencia ----------
    def guardar_en_archivo(self, ruta: str) -> None:
        """
        Serializa el inventario a JSON.
        """
        data = [asdict(p) for p in self._productos.values()]
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def cargar_desde_archivo(self, ruta: str) -> None:
        """
        Deserializa desde JSON. Si el archivo no existe o está vacío, deja el inventario en blanco.
        """
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                data = json.load(f)
            # reconstrucción segura
            self._productos.clear()
            self._ids.clear()
            for item in data:
                p = Producto(
                    id=str(item["id"]),
                    nombre=str(item["nombre"]),
                    cantidad=int(item["cantidad"]),
                    precio=float(item["precio"]),
                )
                self.agregar(p)
        except FileNotFoundError:
            # Primer uso: sin archivo, inventario vacío
            self._productos.clear()
            self._ids.clear()
        except json.JSONDecodeError:
            # Archivo corrupto: preferimos no sobrescribir el estado en memoria
            raise ValueError("El archivo de inventario está corrupto o mal formado.")


# -----------------------------
# Utilidades de UI
# -----------------------------
def imprimir_producto(p: Producto) -> None:
    print(f"{p.id} | {p.nombre} | cant={p.cantidad} | ${p.precio:.2f}")

def leer_entero(msg: str, minimo: Optional[int] = None) -> int:
    while True:
        try:
            val = int(input(msg).strip())
            if minimo is not None and val < minimo:
                print(f"Debe ser >= {minimo}.")
                continue
            return val
        except ValueError:
            print("Ingrese un número entero válido.")

def leer_flotante(msg: str, minimo: Optional[float] = None) -> float:
    while True:
        try:
            val = float(input(msg).strip())
            if minimo is not None and val < minimo:
                print(f"Debe ser >= {minimo}.")
                continue
            return val
        except ValueError:
            print("Ingrese un número válido (puede usar decimales).")

def pausar():
    input("\nPresione ENTER para continuar...")


# -----------------------------
# Menú de consola
# -----------------------------
def menu() -> None:
    RUTA_ARCHIVO = "inventario.json"
    inv = Inventario()

    # Cargar datos previos (si existen)
    try:
        inv.cargar_desde_archivo(RUTA_ARCHIVO)
    except ValueError as e:
        print(f"Advertencia: {e}")
        print("Se continuará con inventario en memoria sin cargar el archivo.")

    while True:
        print("\n=== SISTEMA AVANZADO DE GESTIÓN DE INVENTARIO ===")
        print("1) Añadir producto")
        print("2) Eliminar producto por ID")
        print("3) Actualizar cantidad de un producto")
        print("4) Actualizar precio de un producto")
        print("5) Buscar productos por nombre")
        print("6) Mostrar todos los productos")
        print("7) Guardar inventario en archivo")
        print("0) Salir")

        opcion = input("Elige una opción: ").strip()
        if opcion == "1":
            try:
                pid = input("ID único: ").strip()
                nombre = input("Nombre: ").strip()
                cantidad = leer_entero("Cantidad (>=0): ", minimo=0)
                precio = leer_flotante("Precio (>=0): ", minimo=0.0)
                inv.agregar(Producto(pid, nombre, cantidad, precio))
                inv.guardar_en_archivo(RUTA_ARCHIVO)  # guardado inmediato para persistencia
                print("Producto añadido correctamente.")
            except (ValueError, KeyError) as e:
                print(f"Error: {e}")
            pausar()

        elif opcion == "2":
            pid = input("ID a eliminar: ").strip()
            if inv.eliminar(pid):
                inv.guardar_en_archivo(RUTA_ARCHIVO)
                print("Producto eliminado.")
            else:
                print("No se encontró un producto con ese ID.")
            pausar()

        elif opcion == "3":
            try:
                pid = input("ID a actualizar cantidad: ").strip()
                nueva = leer_entero("Nueva cantidad (>=0): ", minimo=0)
                inv.actualizar_cantidad(pid, nueva)
                inv.guardar_en_archivo(RUTA_ARCHIVO)
                print("Cantidad actualizada.")
            except (ValueError, KeyError) as e:
                print(f"Error: {e}")
            pausar()

        elif opcion == "4":
            try:
                pid = input("ID a actualizar precio: ").strip()
                nuevo = leer_flotante("Nuevo precio (>=0): ", minimo=0.0)
                inv.actualizar_precio(pid, nuevo)
                inv.guardar_en_archivo(RUTA_ARCHIVO)
                print("Precio actualizado.")
            except (ValueError, KeyError) as e:
                print(f"Error: {e}")
            pausar()

        elif opcion == "5":
            texto = input("Texto a buscar en el nombre: ").strip()
            resultados = inv.buscar_por_nombre(texto)
            if resultados:
                print("\nResultados:")
                # Ejemplo de ordenamiento por tupla (nombre, precio)
                for p in sorted(resultados, key=lambda x: (x.nombre.lower(), x.precio)):
                    imprimir_producto(p)
            else:
                print("No se encontraron coincidencias.")
            pausar()

        elif opcion == "6":
            criterio = input("Ordenar por [id/nombre/cantidad/precio] (enter = id): ").strip().lower() or "id"
            print("\nProductos en inventario:")
            for p in inv.todos(ordenar_por=criterio):
                imprimir_producto(p)
            pausar()

        elif opcion == "7":
            try:
                inv.guardar_en_archivo(RUTA_ARCHIVO)
                print(f"Inventario guardado en '{RUTA_ARCHIVO}'.")
            except Exception as e:
                print(f"No se pudo guardar: {e}")
            pausar()

        elif opcion == "0":
            # Guardado final antes de salir
            try:
                inv.guardar_en_archivo(RUTA_ARCHIVO)
            except Exception as e:
                print(f"Aviso: no se pudo guardar al salir: {e}")
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Intente de nuevo.")
# Punto de entrada del programa
if __name__ == "__main__":
    menu()
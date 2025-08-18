class Producto:
    def __init__(self, id_producto, nombre, cantidad, precio):
        # Validaciones básicas para evitar errores en tiempo de ejecución
        if not isinstance(id_producto, str) or not id_producto.strip():
            raise ValueError("El ID debe ser un texto no vacío.")
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre debe ser un texto no vacío.")
        if not isinstance(cantidad, int) or cantidad < 0:
            raise ValueError("La cantidad debe ser un entero >= 0.")
        if not isinstance(precio, (int, float)) or precio < 0:
            raise ValueError("El precio debe ser un número >= 0.")

        self.id_producto = id_producto.strip()
        self.nombre = nombre.strip()
        self.cantidad = int(cantidad)
        self.precio = float(precio)

    def __str__(self):
        total = self.cantidad * self.precio
        return f"{self.id_producto} | {self.nombre} | Cantidad: {self.cantidad} | Precio: ${self.precio:.2f} | Total: ${total:.2f}"


class Inventario:
    def __init__(self):
        # Estructura: {id: Producto}
        self.productos = {}

    def agregar_producto(self, producto):
        if producto.id_producto in self.productos:
            print("Error: Producto ya existe.")
            return
        self.productos[producto.id_producto] = producto
        print("Producto agregado correctamente.")

    def eliminar_producto(self, id_producto):
        if id_producto in self.productos:
            del self.productos[id_producto]
            print("Producto eliminado.")
        else:
            print("Error: Producto no encontrado.")

    def actualizar_producto(self, id_producto, cantidad=None, precio=None):
        prod = self.productos.get(id_producto)
        if not prod:
            print("Error: Producto no encontrado.")
            return

        hubo_cambios = False
        if cantidad is not None:
            if not isinstance(cantidad, int) or cantidad < 0:
                print("Error: La cantidad debe ser un entero >= 0.")
            else:
                prod.cantidad = cantidad
                hubo_cambios = True
        if precio is not None:
            if not isinstance(precio, (int, float)) or precio < 0:
                print("Error: El precio debe ser un número >= 0.")
            else:
                prod.precio = float(precio)
                hubo_cambios = True

        print("Producto actualizado." if hubo_cambios else "No se realizaron cambios.")

    def buscar_producto(self, nombre):
        nombre = nombre.strip().lower()
        encontrados = [p for p in self.productos.values() if nombre in p.nombre.lower()]
        if encontrados:
            for p in encontrados:
                print(p)
        else:
            print("No se encontraron productos con ese nombre.")

    def mostrar_inventario(self):
        if not self.productos:
            print("(Inventario vacío)")
            return
        print("\nID | Nombre | Cantidad | Precio | Total")
        print("-" * 60)
        for p in sorted(self.productos.values(), key=lambda x: x.id_producto):
            print(p)


# --------- Utilidades de entrada robustas ---------
def leer_entero(mensaje):
    while True:
        dato = input(mensaje).strip()
        try:
            return int(dato)
        except ValueError:
            print("Entrada inválida: debe ser un entero.")


def leer_flotante(mensaje):
    while True:
        dato = input(mensaje).strip().replace(",", ".")  # Acepta comas decimales
        try:
            return float(dato)
        except ValueError:
            print("Entrada inválida: debe ser un número (puede tener decimales).")


def leer_texto_no_vacio(mensaje):
    while True:
        dato = input(mensaje).strip()
        if dato:
            return dato
        print("Entrada inválida: no puede estar vacía.")


# --------- Menú CLI ---------
def menu():
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
                print("Saliendo... ¡Hasta luego!")
                break

            elif opcion == "1":
                print("\n[Agregar Producto]")
                try:
                    idp = leer_texto_no_vacio("ID único: ")
                    nombre = leer_texto_no_vacio("Nombre: ")
                    cantidad = leer_entero("Cantidad (entero >= 0): ")
                    if cantidad < 0:
                        print("Error: cantidad negativa.")
                        continue
                    precio = leer_flotante("Precio (>= 0): ")
                    if precio < 0:
                        print("Error: precio negativo.")
                        continue
                    inv.agregar_producto(Producto(idp, nombre, cantidad, precio))
                except ValueError as e:
                    print(f"Error: {e}")

            elif opcion == "2":
                print("\n[Eliminar Producto]")
                idp = leer_texto_no_vacio("ID a eliminar: ")
                inv.eliminar_producto(idp)

            elif opcion == "3":
                print("\n[Actualizar Producto]")
                idp = leer_texto_no_vacio("ID a actualizar: ")
                # Selecciones opcionales
                cambiar_cantidad = input("¿Cambiar cantidad? (s/n): ").strip().lower() == "s"
                nueva_cantidad = None
                if cambiar_cantidad:
                    nueva_cantidad = leer_entero("Nueva cantidad: ")

                cambiar_precio = input("¿Cambiar precio? (s/n): ").strip().lower() == "s"
                nuevo_precio = None
                if cambiar_precio:
                    nuevo_precio = leer_flotante("Nuevo precio: ")

                inv.actualizar_producto(idp, cantidad=nueva_cantidad, precio=nuevo_precio)

            elif opcion == "4":
                print("\n[Buscar Producto por nombre]")
                patron = leer_texto_no_vacio("Texto a buscar: ")
                inv.buscar_producto(patron)

            elif opcion == "5":
                print("\n[Mostrar Inventario]")
                inv.mostrar_inventario()

            else:
                print("Opción inválida. Intente de nuevo.")
    except (KeyboardInterrupt, EOFError):
        print("\nInterrupción detectada. Saliendo del programa.")


if __name__ == "__main__":
    menu()
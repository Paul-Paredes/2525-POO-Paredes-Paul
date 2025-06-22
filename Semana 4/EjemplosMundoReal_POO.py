"""
Simulación de una tienda de libros.
Demuestra Programación Orientada a Objetos con clases, atributos, métodos,
interacción entre objetos y validación de stock.

"""


class Libro:
    """Representa un libro disponible para la venta."""

    def __init__(self, isbn, titulo, autor, precio, stock):
        self.isbn = isbn
        self.titulo = titulo
        self.autor = autor
        self.precio = precio
        self.stock = stock

    def actualizar_stock(self, cantidad):
        """Actualiza el stock del libro."""
        if cantidad < 0 and abs(cantidad) > self.stock:
            raise ValueError("No hay suficiente stock para este libro.")
        self.stock += cantidad

    def __str__(self):
        return f"'{self.titulo}' de {self.autor} - ${self.precio:.2f} (Stock: {self.stock})"


class Cliente:
    """Representa un cliente con historial de compras."""

    def __init__(self, cedula, nombre):
        self.cedula = cedula
        self.nombre = nombre
        self.historial = []

    def registrar_compra(self, compra):
        """Agrega una compra al historial del cliente."""
        self.historial.append(compra)


class Carrito:
    """Carrito de compras que contiene libros seleccionados por el cliente."""

    def __init__(self, cliente):
        self.cliente = cliente
        self.items = []  # lista de tuplas: (libro, cantidad)

    def agregar_libro(self, libro, cantidad):
        if libro.stock < cantidad:
            raise ValueError("Stock insuficiente del libro.")
        libro.actualizar_stock(-cantidad)
        self.items.append((libro, cantidad))

    def calcular_total(self):
        return sum(libro.precio * cantidad for libro, cantidad in self.items)

    def finalizar_compra(self):
        """Finaliza la compra, vacía el carrito y guarda el historial del cliente."""
        total = self.calcular_total()
        detalle = {
            "items": [(libro.titulo, cantidad) for libro, cantidad in self.items],
            "total": total
        }
        self.cliente.registrar_compra(detalle)
        self.items.clear()
        return detalle


class TiendaLibros:
    """Contiene los libros disponibles y permite buscarlos."""

    def __init__(self):
        self.catalogo = []

    def agregar_libro(self, libro):
        self.catalogo.append(libro)

    def mostrar_catalogo(self):
        for libro in self.catalogo:
            print(libro)

    def buscar_por_titulo(self, titulo):
        return [libro for libro in self.catalogo if titulo.lower() in libro.titulo.lower()]


# Código de prueba
if __name__ == "__main__":
    # Crear tienda y libros
    tienda = TiendaLibros()
    tienda.agregar_libro(Libro("9780140449266", "El Principito", "Antoine de Saint-Exupéry", 12.00, 10))
    tienda.agregar_libro(Libro("9788498387087", "Cien años de soledad", "Gabriel García Márquez", 18.50, 5))
    tienda.agregar_libro(Libro("9788420469280", "1984", "George Orwell", 14.75, 7))

    # Mostrar catálogo
    print(" Catálogo de Libros:")
    tienda.mostrar_catalogo()

    # Crear cliente y carrito
    cliente = Cliente("0912345678", "Paul Paredes")
    carrito = Carrito(cliente)

    # Agregar libros al carrito
    carrito.agregar_libro(tienda.catalogo[0], 2)  # El Principito
    carrito.agregar_libro(tienda.catalogo[2], 1)  # 1984

    # Finalizar compra
    compra = carrito.finalizar_compra()
    print(f"\n Compra finalizada por {cliente.nombre}")
    print(f"Libros comprados: {compra['items']}")
    print(f"Total pagado: ${compra['total']:.2f}")
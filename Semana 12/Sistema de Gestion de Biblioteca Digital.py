from __future__ import annotations
from typing import Dict, List, Set, Iterable, Optional


class Libro:
    """
    Representa un libro en la biblioteca.

    Requisitos clave:
    - (título, autor) se almacenan en una TUPLA inmutable.
    - isbn y categoría se guardan como strings.
    """
    __slots__ = ("_titulo_autor", "categoria", "isbn")

    def __init__(self, titulo: str, autor: str, categoria: str, isbn: str) -> None:
        if not titulo or not autor:
            raise ValueError("Título y autor no pueden estar vacíos.")
        if not categoria:
            raise ValueError("La categoría no puede estar vacía.")
        if not isbn:
            raise ValueError("El ISBN no puede estar vacío.")

        # Tupla inmutable con (titulo, autor)
        self._titulo_autor: tuple[str, str] = (titulo.strip(), autor.strip())
        self.categoria: str = categoria.strip()
        self.isbn: str = str(isbn).strip()

    @property
    def titulo(self) -> str:
        return self._titulo_autor[0]

    @property
    def autor(self) -> str:
        return self._titulo_autor[1]

    def __repr__(self) -> str:
        return f"Libro(titulo='{self.titulo}', autor='{self.autor}', cat='{self.categoria}', isbn='{self.isbn}')"


class Usuario:
    """
    Representa a un usuario de la biblioteca.

    - user_id debe ser único (la Biblioteca lo garantiza con un conjunto).
    - libros_prestados almacena una LISTA de ISBNs prestados actualmente.
    """
    __slots__ = ("nombre", "user_id", "libros_prestados")

    def __init__(self, nombre: str, user_id: str) -> None:
        if not nombre:
            raise ValueError("El nombre no puede estar vacío.")
        if not user_id:
            raise ValueError("El ID de usuario no puede estar vacío.")

        self.nombre: str = nombre.strip()
        self.user_id: str = str(user_id).strip()
        self.libros_prestados: List[str] = []  # lista de ISBNs

    def tomar_prestado(self, isbn: str) -> None:
        if isbn in self.libros_prestados:
            # Protección adicional aunque la Biblioteca ya valida.
            raise ValueError(f"El usuario ya tiene prestado el ISBN {isbn}.")
        self.libros_prestados.append(isbn)

    def devolver(self, isbn: str) -> None:
        try:
            self.libros_prestados.remove(isbn)
        except ValueError:
            raise ValueError(f"El usuario no tiene prestado el ISBN {isbn}.")

    def __repr__(self) -> str:
        return f"Usuario(nombre='{self.nombre}', user_id='{self.user_id}', prestados={len(self.libros_prestados)})"


class Biblioteca:
    """
    Gestiona:
    - Diccionario de libros por ISBN: {isbn: Libro}
    - Diccionario de usuarios por ID: {user_id: Usuario}
    - Conjunto de IDs únicos: set(user_id)
    - Diccionario de préstamos: {isbn: user_id}

    Reglas de negocio:
    - No se puede prestar un libro inexistente o ya prestado.
    - No se puede quitar un libro si está prestado.
    - No se puede dar de baja a un usuario con préstamos activos.
    """
    def __init__(self) -> None:
        self.catalogo_por_isbn: Dict[str, Libro] = {}
        self.usuarios_por_id: Dict[str, Usuario] = {}
        self.ids_usuarios: Set[str] = set()
        self.prestamos: Dict[str, str] = {}  # isbn -> user_id

    # ------------------------
    # Gestión de libros
    # ------------------------
    def anadir_libro(self, libro: Libro) -> None:
        if libro.isbn in self.catalogo_por_isbn:
            raise ValueError(f"Ya existe un libro con ISBN {libro.isbn}.")
        self.catalogo_por_isbn[libro.isbn] = libro

    def quitar_libro(self, isbn: str) -> None:
        if isbn not in self.catalogo_por_isbn:
            raise KeyError(f"No existe el libro con ISBN {isbn}.")
        if isbn in self.prestamos:
            raise ValueError("No se puede quitar un libro que está prestado.")
        del self.catalogo_por_isbn[isbn]

    # ------------------------
    # Gestión de usuarios
    # ------------------------
    def registrar_usuario(self, nombre: str, user_id: str) -> Usuario:
        user_id = str(user_id).strip()
        if user_id in self.ids_usuarios:
            raise ValueError(f"El ID de usuario '{user_id}' ya está registrado.")
        usuario = Usuario(nombre, user_id)
        self.usuarios_por_id[user_id] = usuario
        self.ids_usuarios.add(user_id)
        return usuario

    def baja_usuario(self, user_id: str) -> None:
        if user_id not in self.usuarios_por_id:
            raise KeyError(f"No existe el usuario con ID '{user_id}'.")
        usuario = self.usuarios_por_id[user_id]
        if usuario.libros_prestados:
            raise ValueError("El usuario tiene préstamos activos. Debe devolverlos antes de la baja.")
        del self.usuarios_por_id[user_id]
        self.ids_usuarios.remove(user_id)

    # ------------------------
    # Préstamos
    # ------------------------
    def prestar_libro(self, isbn: str, user_id: str) -> None:
        if isbn not in self.catalogo_por_isbn:
            raise KeyError(f"No existe el libro con ISBN {isbn}.")
        if user_id not in self.usuarios_por_id:
            raise KeyError(f"No existe el usuario con ID '{user_id}'.")
        if isbn in self.prestamos:
            raise ValueError(f"El libro {isbn} ya está prestado al usuario '{self.prestamos[isbn]}'.")

        usuario = self.usuarios_por_id[user_id]
        usuario.tomar_prestado(isbn)
        self.prestamos[isbn] = user_id

    def devolver_libro(self, isbn: str, user_id: Optional[str] = None) -> None:
        if isbn not in self.prestamos:
            raise ValueError(f"El libro {isbn} no está registrado como prestado.")

        actual_uid = self.prestamos[isbn]
        if user_id is not None and user_id != actual_uid:
            raise ValueError(f"El libro {isbn} está registrado a nombre de '{actual_uid}', no de '{user_id}'.")

        usuario = self.usuarios_por_id[actual_uid]
        usuario.devolver(isbn)
        del self.prestamos[isbn]

    # ------------------------
    # Búsquedas
    # ------------------------
    def buscar_por_titulo(self, texto: str) -> List[Libro]:
        texto = texto.strip().lower()
        return [l for l in self.catalogo_por_isbn.values() if texto in l.titulo.lower()]

    def buscar_por_autor(self, texto: str) -> List[Libro]:
        texto = texto.strip().lower()
        return [l for l in self.catalogo_por_isbn.values() if texto in l.autor.lower()]

    def buscar_por_categoria(self, categoria: str) -> List[Libro]:
        categoria = categoria.strip().lower()
        return [l for l in self.catalogo_por_isbn.values() if l.categoria.lower() == categoria]

    # ------------------------
    # Listados
    # ------------------------
    def listar_libros_prestados_de_usuario(self, user_id: str) -> List[Libro]:
        if user_id not in self.usuarios_por_id:
            raise KeyError(f"No existe el usuario con ID '{user_id}'.")
        usuario = self.usuarios_por_id[user_id]
        return [self.catalogo_por_isbn[isbn] for isbn in usuario.libros_prestados]

    def listar_disponibles(self) -> Iterable[Libro]:
        """Devuelve un iterable de libros que NO están prestados."""
        for isbn, libro in self.catalogo_por_isbn.items():
            if isbn not in self.prestamos:
                yield libro

    def esta_disponible(self, isbn: str) -> bool:
        return (isbn in self.catalogo_por_isbn) and (isbn not in self.prestamos)


# ------------------------------------------------------------
# Pruebas rápidas (ejecutar este archivo directamente)
# ------------------------------------------------------------
if __name__ == "__main__":
    # 1) Crear biblioteca
    biblio = Biblioteca()

    # 2) Registrar usuarios (IDs únicos)
    u1 = biblio.registrar_usuario("Paul Paredes", "U001")
    u2 = biblio.registrar_usuario("Ana López", "U002")

    # 3) Añadir libros (ISBN como clave)
    l1 = Libro("Clean Code", "Robert C. Martin", "Programación", "9780132350884")
    l2 = Libro("Design Patterns", "Erich Gamma", "Programación", "9780201633610")
    l3 = Libro("Cien años de soledad", "Gabriel García Márquez", "Novela", "9780307474728")

    biblio.anadir_libro(l1)
    biblio.anadir_libro(l2)
    biblio.anadir_libro(l3)

    # 4) Buscar
    print("Buscar por título 'clean':", biblio.buscar_por_titulo("clean"))
    print("Buscar por autor 'gamma':", biblio.buscar_por_autor("gamma"))
    print("Buscar por categoría 'programación':", biblio.buscar_por_categoria("programación"))

    # 5) Prestar libros
    biblio.prestar_libro("9780132350884", "U001")  # Clean Code a Paul
    biblio.prestar_libro("9780201633610", "U002")  # Design Patterns a Ana

    print("Prestados de U001:", biblio.listar_libros_prestados_de_usuario("U001"))
    print("Prestados de U002:", biblio.listar_libros_prestados_de_usuario("U002"))
    print("Disponibles:", list(biblio.listar_disponibles()))

    # 6) Devolver libro
    biblio.devolver_libro("9780201633610")  # Ana devuelve
    print("Disponibles tras devolución:", list(biblio.listar_disponibles()))

    # 7) Intentar baja de usuario con libros
    try:
        biblio.baja_usuario("U001")  # Paul aún tiene un libro -> error esperado
    except Exception as e:
        print("Baja U001 falló (esperado):", e)

    # 8) Devolver y dar de baja
    biblio.devolver_libro("9780132350884")
    biblio.baja_usuario("U001")
    print("Usuarios actuales:", list(biblio.usuarios_por_id.keys()))

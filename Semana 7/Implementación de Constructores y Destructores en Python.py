# Sistema de Reserva - Hilary Resort Spa
# Autor:  Paul Paredes
# Objetivo: Demostrar uso de constructores (_init) y destructores (del_) en Python

class Cliente:
    def __init__(self, nombre, cedula, email, telefono):
        self.nombre = nombre
        self.cedula = cedula
        self.email = email
        self.telefono = telefono
        print(f"Cliente creado: {self.nombre} (Cédula: {self.cedula})")

    def __del__(self):
        print(f"Gracias por su visita, {self.nombre}. Esperamos verlo pronto en Hilary Resort Spa.")


class Habitacion:
    def __init__(self, numero, tipo, precio):
        self.numero = numero
        self.tipo = tipo
        self.precio = precio
        self.disponible = True
        print(f"Habitación {self.numero} ({self.tipo}) registrada - ${self.precio}/noche")

    def __del__(self):
        print(f"La habitación {self.numero} ha sido liberada y está lista para nuevos huéspedes.")


class Reserva:
    def __init__(self, cliente, habitacion, fecha_entrada, fecha_salida):
        self.cliente = cliente
        self.habitacion = habitacion
        self.fecha_entrada = fecha_entrada
        self.fecha_salida = fecha_salida

        if self.habitacion.disponible:
            self.habitacion.disponible = False
            print(f"Reserva confirmada para {self.cliente.nombre} en la habitación {self.habitacion.numero} del {self.fecha_entrada} al {self.fecha_salida}")
        else:
            print(f"La habitación {self.habitacion.numero} no está disponible.")

    def __del__(self):
        self.habitacion.disponible = True
        print(f"La reserva de {self.cliente.nombre} ha finalizado. Gracias por elegir Hilary Resort Spa.")


# -------- PRUEBAS --------
if __name__ == "__main__":
    # Crear clientes
    cliente1 = Cliente("Ana Torres", "0923456789", "atorres@gmail.com", "0987001122")
    cliente2 = Cliente("Luis Mendoza", "0945671234", "lmendoza@gmail.com", "0987993344")

    # Crear habitaciones
    habitacion1 = Habitacion(101, "Suite Vista a la Piscina", 120)
    habitacion2 = Habitacion(202, "Habitación Doble", 80)

    # Crear reservas
    reserva1 = Reserva(cliente1, habitacion1, "2025-07-15", "2025-07-18")
    reserva2 = Reserva(cliente2, habitacion2, "2025-07-16", "2025-07-19")

    # Simular fin del programa para activar destructores
    print("\nFin del programa. Limpieza de objetos...\n")
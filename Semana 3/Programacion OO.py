# Programación Orientada a Objetos (POO)
# Ejemplo: Simulación de uso de un teléfono móvil

class Smartphone:
    def __init__(self, battery_level=100):
        self._battery_level = battery_level
        self._usage_minutes = 0

    def use_phone(self, minutes):
        battery_consumption = minutes * 0.5
        if battery_consumption <= self._battery_level:
            self._battery_level -= battery_consumption
            self._usage_minutes += minutes
            print(f"Usando el teléfono por {minutes} minutos.")
        else:
            print("Batería insuficiente para ese tiempo de uso.")

    def charge_phone(self, amount):
        if amount <= 0:
            print("Ingrese un valor positivo para cargar.")
            return
        self._battery_level = min(100, self._battery_level + amount)
        print(f"Cargando batería: +{amount}%")

    def get_status(self):
        print("Estado del teléfono:")
        print(f"- Minutos de uso total: {self._usage_minutes}")
        print(f"- Batería restante: {self._battery_level:.2f}%")


# Bloque principal del programa
if __name__ == "__main__":
    my_phone = Smartphone()

    my_phone.use_phone(60)
    my_phone.charge_phone(20)
    my_phone.use_phone(100)

    my_phone.get_status()
# Programación Tradicional
# Ejemplo: Uso de un teléfono móvil

# Variables globales
battery_level = 100
usage_minutes = 0

# Función para usar el teléfono
def use_phone(minutes):
    global battery_level, usage_minutes
    battery_consumption = minutes * 0.5  # cada minuto consume 0.5% de batería
    if battery_consumption <= battery_level:
        battery_level -= battery_consumption
        usage_minutes += minutes
        print(f"Usando el teléfono por {minutes} minutos.")
    else:
        print("Batería insuficiente para ese tiempo de uso.")

# Función para cargar el teléfono
def charge_phone(amount):
    global battery_level
    battery_level = min(100, battery_level + amount)
    print(f"Cargando batería: +{amount}%")

# Simulación de uso
use_phone(60)
charge_phone(20)
use_phone(100)

# Mostrar resultados finales
print("Minutos de uso total:", usage_minutes)
print("Nivel de batería restante:", battery_level, "%")
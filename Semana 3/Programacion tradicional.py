# Programa tradicional para calcular el promedio semanal del clima

def ingresar_temperaturas():
    """Función para ingresar temperaturas de lunes a domingo"""
    temperaturas = []
    dias = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
    for dia in dias:
        while True:
            try:
                temp = float(input(f"Ingrese la temperatura del día {dia}: "))
                temperaturas.append(temp)
                break
            except ValueError:
                print("Por favor ingrese un número válido.")
    return temperaturas


def calcular_promedio(temperaturas):
    """Función para calcular el promedio de una lista de temperaturas"""
    return sum(temperaturas) / len(temperaturas)


# Programa principal
def main():
    temperaturas = ingresar_temperaturas()
    promedio = calcular_promedio(temperaturas)
    print(f"\nEl promedio semanal de temperatura es: {promedio:.2f}°C")


if __name__ == "__main__":
    main()
# Programa con Programación Orientada a Objetos para calcular el promedio semanal del clima

class ClimaSemanal:
    def __init__(self):
        self.__temperaturas = {}  # Encapsulamiento de los datos
        self.dias = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]

    def ingresar_datos(self):
        """Método para ingresar temperaturas diarias"""
        for dia in self.dias:
            while True:
                try:
                    temp = float(input(f"Ingrese la temperatura del día {dia}: "))
                    self.__temperaturas[dia] = temp
                    break
                except ValueError:
                    print("Por favor ingrese un número válido.")

    def calcular_promedio(self):
        """Método para calcular el promedio de temperatura semanal"""
        total = sum(self.__temperaturas.values())
        return total / len(self.__temperaturas)

    def mostrar_promedio(self):
        promedio = self.calcular_promedio()
        print(f"\nEl promedio semanal de temperatura es: {promedio:.2f}°C")


# Programa principal
def main():
    semana = ClimaSemanal()
    semana.ingresar_datos()
    semana.mostrar_promedio()


if __name__ == "__main__":
    main()
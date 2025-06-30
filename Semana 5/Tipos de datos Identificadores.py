import math

class TrianguloEquilatero:
    # Corrección: Usamos __init__ con doble guion bajo al inicio y al final
    def __init__(self, lado):
        self.lado = lado

    def calcular_area_triangulo(self):
        # Fórmula del área: (lado^2 * sqrt(3)) / 4
        return (self.lado ** 2 * math.sqrt(3)) / 4

    def calcular_perimetro_triangulo(self):
        # Fórmula del perímetro: 3 * lado
        return 3 * self.lado

# Uso
lado = 6  # La longitud de un lado del triángulo

# Crear el objeto
mi_triangulo = TrianguloEquilatero(lado)

area_del_triangulo = mi_triangulo.calcular_area_triangulo()
perimetro_del_triangulo = mi_triangulo.calcular_perimetro_triangulo()

print(f"El área de un triángulo equilátero es: {area_del_triangulo}")
print(f"El perímetro de un triángulo equilátero es: {perimetro_del_triangulo}")
# Ejemplo POO: Gestión de un gimnasio

class Cliente:
    """
    Clase base que representa a un cliente general del gimnasio.
    """

    def __init__(self, nombre, edad):
        self.nombre = nombre
        self.edad = edad

    def descripcion(self):
        print(f"Cliente: {self.nombre}, Edad: {self.edad}")


class ClientePremium(Cliente):
    """
    Clase derivada que hereda de Cliente, para clientes premium.
    Incluye atributos encapsulados y polimorfismo.
    """

    def __init__(self, nombre, edad, plan):
        super().__init__(nombre, edad)
        self.__plan = plan  # atributo privado -> encapsulación

    def descripcion(self):
        # Sobrescribiendo descripción -> polimorfismo
        print(f"Cliente Premium: {self.nombre}, Edad: {self.edad}, Plan: {self.__plan}")

    def actualizar_plan(self, nuevo_plan):
        print(f"Actualizando plan de {self.nombre} de {self.__plan} a {nuevo_plan}")
        self.__plan = nuevo_plan

    def mostrar_plan(self):
        print(f"{self.nombre} tiene el plan: {self.__plan}")


if __name__ == "__main__":
    # Cliente normal
    cliente1 = Cliente("Paul", 19)
    cliente1.descripcion()

    # Cliente premium
    cliente2 = ClientePremium("Paul", 19, "Musculación Full")
    cliente2.descripcion()  # polimorfismo: método sobreescrito
    cliente2.mostrar_plan()  # muestra el plan actual
    cliente2.actualizar_plan("Crossfit")  # cambia el plan
    cliente2.mostrar_plan()
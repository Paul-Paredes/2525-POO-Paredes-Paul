# ----------------------------
# ABSTRACCIÓN
# ----------------------------
class LamparaSimple:
    def encender(self):
        print("La lámpara está encendida.")



    def cambiar_nombre(self, nuevo_nombre):
        self.__nombre = nuevo_nombre

# ----------------------------
# HERENCIA
# ----------------------------
class PersonaBase:
    def presentarse(self):
        print("Hola, soy una persona.")

class EstudianteNuevo(PersonaBase):
    def estudiar(self):
        print("Estoy estudiando para el examen.")

# ----------------------------
# POLIMORFISMO
# ----------------------------
class PerroNuevo:
    def hablar(self):
        print("Guau!")

class RobotNuevo:
    def hablar(self):
        print("Beep boop...")

# ----------------------------
# EJECUCIÓN DEL CÓDIGO
# ----------------------------

print("=== Abstracción ===")
lampara = LamparaSimple()
lampara.encender()



print("\n=== Herencia ===")
persona = EstudianteNuevo()
persona.presentarse()
persona.estudiar()

print("\n=== Polimorfismo ===")
seres = [PerroNuevo(), RobotNuevo()]
for ser in seres:
    ser.hablar()
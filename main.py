#Importamos las funciones que vamos a utilizar de los otros modulos
from cliente import menu_cliente
from instructores import menu_instructor
from vehiculos import menu_vehiculos
from citas import menu_citas


def menu_principal():
    while True:
        print("\n==== SISTEMA DE CITAS ====")
        print("1. Módulo cliente")
        print("2. Módulo instructores")
        print("3. Módulo vehículos")
        print("4. Módulo citas")
        print("5. Salir")

        opcion_texto = input("Ingrese su opción: ").strip()
        opcion = int(opcion_texto) if opcion_texto.isdigit() else 0

        match opcion:
            case 1:
                menu_cliente()
            case 2:
                menu_instructor()
            case 3:
                menu_vehiculos()
            case 4:
                menu_citas()
            case 5:
                print("Hasta luego")
                break
            case _:
                print("Opcion no valida solo del 1-5")


if __name__ == "__main__":
    print("---- BIENVENIDO AL SISTEMA ----")
    menu_principal()
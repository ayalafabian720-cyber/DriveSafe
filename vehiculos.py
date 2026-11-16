#Importamos las funciones para manejar los json y validar la placa
from funciones import leer_json, guardar_json, validar_placa, validar_placa_registrada

#Definimos ruta del json de los vehiculos
RUTA_VEHICULOS= "data/vehiculos.json"

#Creamos la funcion para listar vehiculos
def listar_vehiculos ():
    #creamos la lista de vehiculos
    vehiculos= leer_json(RUTA_VEHICULOS)
    print(f"{'Placa':>5}{'Modelo':>20}{'Tipo':20}")
    print("-"*50)
    for i in vehiculos:
        print(f"{i['placa']:>5}{i['modelo']:>20}{i['vehiculo']:>20}")

#Creamos la funcion para registrar un vehiculo 
def registrar_vehiculo():
    #creamos la lista de vehiculos
    vehiculos= leer_json(RUTA_VEHICULOS)

    print("---- REGISTRAR VEHICULO ----")
    placa=input("Ingrese la placa del vehiculo : ").upper()
    #Validar placa
    placa= validar_placa(RUTA_VEHICULOS,placa)

    modelo=input("Ingrese el modelo del vehiculo: ")
    print("---- TIPO DE VEHICULO ----")
    opcion=int(input("Ingrese 1. si es -carro- o 2. si es -moto- :"))
    #Validar que la opcion sea 1 o 2
    while opcion < 1 or opcion > 2: 
        print("!INGRESO UNA OPCION INVALIDA")
        opcion=int(input("Ingrese 1. si es -carro- o 2. si es -moto- :"))
    if opcion == 1:
        tipo="carro"
    else:
        tipo="moto"

    vehiculos.append ({
        "placa": placa,
        "modelo": modelo,
        "vehiculo": tipo
    })
    guardar_json(RUTA_VEHICULOS, vehiculos)

#Creamos la funcion para actualizar un vehiculo

def editar_vehiculo ():
    #Creamos la lista con los vehiculos
    vehiculos= leer_json(RUTA_VEHICULOS)
    #Listamos los vehiculos
    listar_vehiculos()
    #Ingresamos y validamo la placa
    placa= input("Ingrese el numero de placa del vehiculo que desea actualizar: ").upper()
    placa= validar_placa_registrada(RUTA_VEHICULOS,placa)
    #Recorremos la lista de los vehiculos para encontrar la informacion 
    for i in vehiculos: 
        if i["placa"]== placa:
            #Pedimos el ingreso de los datos
            print(f"--- Datos del vehiculo: {i['modelo']}, con la placa: {i['placa']} ---")
            #Ingresamos y validamos la placa
            placa=input(f"Placa actual: ({i['placa']}), presione enter para dejar igual: ").upper()
            if placa and placa != i["placa"]:
                placa = validar_placa(RUTA_VEHICULOS, placa)
            modelo= input(f"Modelo actual: ({i['modelo']}), precione enter para dejar igual: ")
            print(f"Tipo de vehiculo actual:{i['vehiculo']}")
            print("--- Ingrese la opcion de actualizacion ---")
            opcion=int(input("1.Carro || 2. Moto || 3. Dejar igual: "))
            while opcion <1 or opcion >3 :
                print("Ingreso una opcion no valida: ")
                print("--- Ingrese la opcion de actualizacion ---")
                opcion=int(input("1.Carro || 2. Moto || 3. Dejar igual: "))
            if opcion == 1 :
                vehiculo="carro"
            elif opcion ==2: 
                vehiculo= "moto"
            elif opcion == 3: 
                vehiculo=i["vehiculo"]
            #Agragamos los cambios a lista
            i["placa"]=placa if placa else i["placa"]
            i["modelo"]=modelo if modelo else i["modelo"]
            i["vehiculo"]= vehiculo if vehiculo else i["vehiculo"]
            #Guardamos y cargamos los datos en el json
            guardar_json(RUTA_VEHICULOS,vehiculos)
            print("DATOS ACTUALIZADOS CORRECTAMENTE")

#Defiminos la funcion para eliminar vehiculo      
def eliminar_vehiculo():
    #Creamos la lista de los vehiculos
    vehiculos=leer_json(RUTA_VEHICULOS)
    #Lisramos los vehiculos
    listar_vehiculos()
    #Pedimos y validamos la placa
    placa=input("Ingrese la placa del vehiculo que desea eliminar: ").upper()
    placa=validar_placa_registrada(RUTA_VEHICULOS,placa)
    #Filtramos la lista solo por la placa
    placas_filtradas= [i for i in vehiculos if i["placa"] !=placa ]
    #Guardamos la informacion en json
    guardar_json(RUTA_VEHICULOS, placas_filtradas)
    print("--- VEHICULO ELIMINADO CORRECTAMENTE ---")

#Creamos la funcion para el menu de vehiculos
def menu_vehiculos():
    while True:
            print("---- MODULO VEHICULOS ----")
            print("--- INGRESE LA OPCION QUE DESEA REALIZAR ---")
            print("1. Listar vehiculos.")
            print("2. Registrar vehiculo.")
            print("3. Actualizar vehiculo.")
            print("4. Eliminar vehiculo.")
            print("5. Salir")
            op= int(input("Ingrese su opcion: "))
    
            match(int(op)):
    
                case 1 :
                    listar_vehiculos()
                case 2:
                    registrar_vehiculo()
                case 3:
                    editar_vehiculo()
                case 4:
                    eliminar_vehiculo()
                case 5:
                    break
                case _:
                    print("Ingreso una Opcion no valida")
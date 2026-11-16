#necesito importar las funciones para los json y para validar el documento

from funciones import leer_json, guardar_json, validar_documento
from funciones import validar_documento_registrado
#se definio la ruta de json cliente
RUTA_CLIENTE="Data/cliente.json"

#funcion para guardar los clientes
def guardar_cliente():
    datos_cliente=leer_json(RUTA_CLIENTE)

    print("===DATOS CLIENTE===")
    documento=int(input("Por favor ingrese su documento: "))
    documento=int(validar_documento(RUTA_CLIENTE, documento))
    nombre=str(input("Por favor ingrese su nombre: "))
    print("Para el tipo de vehiculo ingrese")
    op=int(input("1. carro / 2. moto: "))

    while op < 1 or op >2 :
        print("Ingreso una opcion no valida")
        op=int(input("1. carro / 2. moto: "))
    if op ==1:

        tipo="carro"
    else:
        tipo="moto"
    
    datos_cliente.append ({
        "documento": documento,
        "nombre": nombre,
        "vehiculo": tipo
    })

    guardar_json(RUTA_CLIENTE, datos_cliente)

#Esta funcion es para pedir la lista en la cual vamos atrabajar y luego devolversela segun se haya modificado

def listar_cliente():
    clientes=leer_json(RUTA_CLIENTE)
    if not clientes:
        print("No hay clientes registrados")
    print(f"\n {'documento' :<20}{'nombre' :<20}{'vehiculo' :<8}")
    print("-"*50)

    for i in clientes:
        print(f"{i['documento']:<20}{i['nombre']:<20}{i['vehiculo']:<8}")


 

def actualizar_cliente():
   lista_cliente=leer_json(RUTA_CLIENTE)
   listar_cliente()

   print("===Por favor ingrese los datos del cliente que desea actualizar===")
   documento=int(input("Por favor ingrese el documento: "))
   validar_documento_registrado(RUTA_CLIENTE, documento)
   for i in lista_cliente:
       if i['documento']==documento:
           print("Por favor ingrese los datos que vas a actualizar")
           documento=input(f"Su actual documento es: ({i['documento']}), o enter para dejar igual: ")
           documento=validar_documento(RUTA_CLIENTE, documento)
           nombre=input(f"Su actual nombre es: ({i['nombre']}), o enter para dejar igual: ")
           tipo=int(input("Ingrese 1. si es carro 2. si es moto"))
           while tipo <1 or tipo >2:
               print("¡EY estas ingresando un numero no valido")
               print("Vuelva a ingresar un dato correcto 1 / 2 :")
               tipo=int(input("Ingrese otra vez el tipo de vehiculo: "))
           if tipo==1:
             vehiculo="carro"
           else:
              vehiculo="moto"
        
           i["documento"]=documento if documento else i["documento"]
           i["nombre"]=nombre if nombre else i["nombre"]
           i["vehiculo"]=vehiculo if vehiculo else i["vehiculo"]

           guardar_json(RUTA_CLIENTE, lista_cliente)
           print("===¡HA SIDO ACTUALIZADO CORRECTAMENTE!===")

def eliminar_cliente():
    lista_cliente=leer_json(RUTA_CLIENTE)
    listar_cliente()
    documento=int(input("Por favor ingrese el documento del cliente que desea eliminar: "))
    documento=validar_documento_registrado(RUTA_CLIENTE, documento)
    #aqui van a estar todos los usuarios excepto al que voy a eliminar
    lista_filtrada=[i for i in lista_cliente if i["documento"] != documento]
    guardar_json(RUTA_CLIENTE, lista_filtrada)
    print("¡Cliente eliminado exitosamente!")


def menu_cliente():
    while True:
        print("===Ingrese la opción segun lo que deseas realizar===")
        print("1. Listar cliente")
        print("2. Guardar cliente")
        print("3. Actualizar cliente")
        print("4. Eliminar cliente")
        print("5. salir")
        op=int(input("Por favor ingrese su opcion: "))

        match op:
            case 1:
                listar_cliente()
            case 2:
                guardar_cliente()
            case 3:
                actualizar_cliente()
            case 4: 
                eliminar_cliente()
            case 5:
                print("Gracias por usar el sistema...saliendo")
                break
                
            case _:
                print("Has ingresado una aopcion no valida")
                op=int(input("Por favor ingrese una opción valida (1-5)"))




                    


           

            

        
           
           
           
                 



  



          



    

    

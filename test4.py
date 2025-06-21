from time import sleep

class CiudadanoError(Exception):

    def __init__(self, mensaje):
        super().__init__(mensaje)

    def __str__(self):
        return super().__str__()
    
class Ciudadano:    

    def __init__(self, nombre : str, edad : int, ingreso_mensual: float):

        if not "".join(nombre.split()).isalpha():
            raise CiudadanoError("Formato de nombre inválido. Solo letras y espacios son permitidos.")
        
        self.nombre = nombre

        if edad <= 0:
            raise CiudadanoError("La edad tiene que ser mayor que 0.")
        
        if edad > 120:
            raise CiudadanoError("Demasiada edad.")
        
        self.edad = edad
        
        if ingreso_mensual < 0:
            raise CiudadanoError("El ingreso debe ser mayor o igual a 0.")

        self.__ingreso_mensual = ingreso_mensual

    def __es_mayor_edad(self):
        return self.edad >= 18
    
    def __ingreso_mayor_2000(self):
        return self.__ingreso_mensual > 2000
    
    def __ingreso_menor_500(self):
        return self.__ingreso_mensual < 500

    def __es_apto_tributar(self):
        return self.__es_mayor_edad() and self.__ingreso_mayor_2000()
    
    def __es_apto_exencion(self):
        return self.__es_mayor_edad() and self.__ingreso_menor_500()

    def obligacion_tributaria(self):

        if self.__es_apto_tributar():
            print(f"\nEstimado usuario: {self.nombre}, ud. debe tributar.")
        elif self.__es_apto_exencion():
            print(f"\nEstimado usuario: {self.nombre}, ud. NO debe pagar impuestos.")
        else:
            if not self.__es_mayor_edad():
                print(f"\nEstimado usuario: {self.nombre}, ud. no es apto para tributar, "
                      f"ya que solo tienes {self.edad} años.")
            else:
                print(f"\nEstimado usuario: {self.nombre}, ud. no es apto para tributar, " 
                      "ya que solo posees entre 500 y 2000 USD.")

    def consultar_ciudadano(self):
        return {'Nombre': self.nombre, 
                'Edad': self.edad,
                'Ingreso': self.__ingreso_mensual,
                'Mayor': self.__es_mayor_edad(),
                'Condición': 0 if self.__es_apto_tributar() else \
                             1 if self.__es_apto_exencion() else \
                             2}
    
        # La llave de 'Condición' tiene los valores: 0, 1 o 2
        # El 0 representa a un ciudadano apto para tributar
        # El 1 representa a un ciudadano en exención
        # El 2 representa a un ciudadano NO apto para tributar

    def __str__(self):
        return f"\nNombre: {self.nombre}\nEdad: {self.edad}\nIngreso mensual: {self.__ingreso_mensual} USD" + \
               f"\nEs mayor de edad: {"Si" if self.__es_mayor_edad() else "No"}" + \
               f"\nCondición de obligación: {"Apto para tributar" if self.__es_apto_tributar() else \
                                             "En exención" if self.__es_apto_exencion() else \
                                             "NO apto para tributar"}"
    
class Control:

    ciudadanos = []

    def menu():

        while True:

            print("\n\t Software de Tributación SRI\t\n\n".upper())

            print("1. Agregar ciudadano")
            print("2. Consultar ciudadanos")
            print("3. Consultar obligaciones")
            print("4. Salir")

            opcion = input("\nIngrese una opción: ")

            if opcion == "1":
                
                while True:

                    try:

                        Control.__agregar_ciudadano()

                    except CiudadanoError as ce:

                        print(f"\nERROR. {ce}")

                    except ValueError:

                        print("\nERROR. Formato inválido en la edad o en el ingreso mensual.")

                    except Exception as e:

                        print(f"\nERROR. {e}")

                    else:

                        print("\nCIUDADANO AGREGADO")
                        
                        break
                    
                    finally:

                        sleep(1)

            elif opcion == "2" or opcion == "3":
                
                if opcion == "2":
                    Control.__consultar_ciudadanos()
                else:
                    Control.__consultar_obligaciones()

                input("\nPresione Enter para seguir.")

            elif opcion == "4":
                
                print("\nSISTEMA FINALIZADO\n")
                break

            else:
                print("\nOPCIÓN INVÁLIDA.")

                sleep(1)

    def __agregar_ciudadano():

        nombre = input("\nIngrese el nombre de usuario: ")

        assert nombre, "Rellene el nombre de usuario. No lo deje vacío."

        edad = int(input("Ingrese la edad: "))

        ingreso_mensual = float(input("Ingrese el ingreso mensual en USD: "))

        ciudadano = Ciudadano(nombre, edad, ingreso_mensual)

        ciudadano.obligacion_tributaria()

        sleep(2)

        Control.ciudadanos.append(ciudadano)

    def __consultar_ciudadanos():
        
        if any(Control.ciudadanos):
            print("\n\nCIUDADANOS REGISTRADOS")

            print(f"\nNúmero de ciudadanos: {len(Control.ciudadanos)}")

            for ciudadano in Control.ciudadanos:
                print(f"\n{ciudadano}")
        else:
            print("\nNo hay ciudadanos para consultar.")

    def __consultar_obligaciones():
        
        if any(Control.ciudadanos):

            print("\n\nOBLIGACIONES")

            ciudadanos_aptos_tributar = list(filter(lambda ciu: ciu.consultar_ciudadano()['Condición'] == 0, 
                                                    Control.ciudadanos))
            
            ciudadanos_en_exencion = list(filter(lambda ciu: ciu.consultar_ciudadano()['Condición'] == 1, 
                                                 Control.ciudadanos))
            
            ciudadanos_no_aptos_tributar = list(filter(lambda ciu: ciu.consultar_ciudadano()['Condición'] == 2, 
                                                        Control.ciudadanos))

            print(f"\nAptos para tributar: {len(ciudadanos_aptos_tributar)}")
            print(f"\nEn exención: {len(ciudadanos_en_exencion)}")
            print(f"\nNO aptos para tributar: {len(ciudadanos_no_aptos_tributar)}")

            if any(ciudadanos_aptos_tributar):
                print("\nCiudadanos aptos para tributar: ")

                for ciudadano_apto in ciudadanos_aptos_tributar:
                    print(f"\n{str(ciudadano_apto).split("Condición de obligación")[0]}")

            if any(ciudadanos_en_exencion):
                print("\nCiudadanos en exención: ")

                for ciudadano_en_exencion in ciudadanos_en_exencion:
                    print(f"\n{str(ciudadano_en_exencion).split("Condición de obligación")[0]}")

            if any(ciudadanos_no_aptos_tributar):
                print("\nCiudadanos NO aptos para tributar: ")

                for ciudadano_no_apto in ciudadanos_no_aptos_tributar:
                    print(f"\n{str(ciudadano_no_apto).split("Condición de obligación")[0]}")

        else:
            print("\nNo hay ciudadanos para consultar sus obligaciones.")

if __name__ == '__main__':
    Control.menu()
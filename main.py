import functions as fun

filename = input("Nombre del programa: ") + ".txt"
fileContent = []

try:
    with open(filename, 'r') as file:
        fileContent = file.readlines()
        print("\n Exito en lectura de archivo")
        file.close()

        state = 0 # Estado
        spc = False # Espacio
        err = False # Error
        pCnt = 0 # Parentesis Cuenta

        for line in fileContent:
            for char in line:
                print("'" + char + "'")
            # ----- Switch -----
    
            # Inicio
            if state == 0: state = 0
            # Inicio Variable
            elif state == 1: state = 1
            # Variable
            elif state == 2: state = 2
            # Asignacion
            elif state == 3: state = 3
            # Entero
            elif state == 4: state = 4
            # Negativo
            elif state == 5: state = 5
            # Parentesis Apertura
            elif state == 6: state = 6
            # Parentesis Cierre
            elif state == 7: state = 7
            # Comentario Linea
            elif state == 8: state = 8
            # 
            elif state == 9: state = 9
            # 
            elif state == 10: state = 10
            # 
            elif state == 11: state = 11
            # 
            elif state == 12: state = 12
            # 
            elif state ==13 : state = 13
            # 
            elif state == 14: state = 14
            # 
            elif state == 15: state = 15
            # 
            elif state == 16: state = 16
            # 
            elif state == 17: state = 17
            # 
            elif state == 18: state = 18
            # 
            elif state == 19: state = 19
            # 
            elif state == 20: state = 20
            # 
            elif state == 21: state = 21
            # 
            elif state == 22: state = 22
            # 
            elif state == 23: state = 23
            # 
            elif state == 24: state = 24
            # 
            elif state == 25: state = 25 

except FileNotFoundError:
    print ("\nEl archivo no fue encontrado")
except IOError:
    print ("\nError al abrir el archivo")
except Exception as e:
    print("\nError: " + e)


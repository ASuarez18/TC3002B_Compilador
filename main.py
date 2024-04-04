filename = input("Nombre del programa: ") + ".txt"
fileContent = []

try:
    with open(filename, 'r') as file:
        fileContent = file.readlines()
        print("\n Exito en lectura de archivo")
        file.close()
        for line in fileContent:
            print(line.strip())

except FileNotFoundError:
    print ("\nEl archivo no fue encontrado")
except IOError:
    print ("\nError al abrir el archivo")
except Exception as e:
    print("\nError: " + e)


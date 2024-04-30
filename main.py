import pandas as pd
import numpy as np
import functions as fun

#filename = input("Nombre del programa: ") + ".txt"
filename = "var.txt"
fileContent = []
operators = [ '+', '-', '*', '/', '%', '^', '[', ']', '(', ')', ';', '{', '}', ',']
reset = [' ', '\n']
history = []
word = ""

def checkState(state, char, word, blocked):
    newState = -1
    if char.isdigit() and not blocked and state != 1:
        newState = 2

    elif (char.isalnum() or char == '_') and not blocked:
        newState = 1

    elif char in operators and not blocked:
        newState = 3

    elif char == '<' and not blocked and state != 8:
        newState = 8

    elif char == '>' and not blocked and state in [0,19]:
        newState = 14

    elif char == '=' and not blocked and state in [0,19]:
        newState = 15

    elif char == '!' and not blocked and state in [0,19]:
        newState = 16

    elif char == '|' and not blocked and state in [0,19]:
        newState = 17

    elif char == '&' and not blocked and state in [0,19]:
        newState = 18

    elif char in reset and not blocked:
        newState = 19
    
    elif char == '#' and not blocked and state != 8:
        newState = 4
        #history.append("line_comment")

    elif char == '#' and not blocked and state == 8:
        newState = 5
        #history.append("multi_comment")

    elif char == '\'' and not blocked:
        newState = 6
        history.append("character")

    elif char == '"' and not blocked:
        newState = 7
        history.append("string")

    elif char == '=' and not blocked and state == 8:
        newState = 20
        history.append("lesser_equal_op")
    
    elif char == '=' and not blocked and state == 14:
        newState = 20
        history.append("greater_equal_op")

    elif char == '=' and not blocked and state == 15:
        newState = 20
        history.append("equal_equal_op")

    elif char == '=' and not blocked and state == 16:
        newState = 20
        history.append("not_equal_op")

    elif char == '|' and not blocked and state == 17:
        newState = 20
        history.append("or_op")

    elif char == '&' and not blocked and state == 18:
        newState = 20
        history.append("and_op")

    elif char == '\n' and blocked and state == 4:
        newState = 0

    elif char == '\'' and blocked and state == 6:
        newState = 0

    elif char == '"' and blocked and state == 7:
        newState = 0

    elif char == '>' and blocked and state == 9:
        newState = 0

    elif char != '>' and blocked and state == 9:
        newState = 5

    elif char == '#' and blocked and state == 5:
        newState = 9

    elif state == 6 and char == '\\':
        newState = 10

    elif state == 7 and char == '\\':
        newState = 11

    elif state == 10:
        newState = 6

    elif state == 11:
        newState = 7

    elif not blocked:
        newState = 404
        history.append("Error")

    if state == 8 and newState != 5 and newState != 20 and not blocked:
        history.append("lesser_op")

    if state == 14 and newState != 20 and not blocked:
        history.append("greater_op")

    if state == 15 and newState != 20 and not blocked:
        history.append("equal_op")

    if state == 16 and newState != 20 and not blocked:
        history.append("not_op")

    if state in [17,18] and newState != 20 and not blocked:
        newState = 404
        history.append("Error")

    if state in [8, 14, 15, 16, 17, 18] and newState == 20 and not blocked:
        newState = 0

    if newState != -1 and newState != state:
        if state == 1 or state == 2:
            token = fun.changeState(state, word)
            history.append(token)
        return newState
    else:
        return state

try:
    blocked = False
    with open(filename, 'r') as file:
        fileContent = file.readlines()
        print("\n Exito en lectura de archivo")
        file.close()

        state = 0 # Estado
        err = False # Error

        for line in fileContent:
            for char in line:
                state = checkState(state, char, word, blocked)
                if state != 1:
                    word = ""
                
                match state:
                    # Init Restart state
                    case 0: 
                        blocked = False
                    # Alpha state
                    case 1: 
                        word += char
                    case 3: 
                        token = fun.operator(char)
                        history.append(token)
                    case 4: 
                        blocked = True
                    case 5: 
                        blocked = True
                    case 6: 
                        blocked = True
                    case 7: 
                        blocked = True

            if state == 1 or state == 2:
                token = fun.changeState(state, word)
                history.append(token)
            
            if state == 8:
                history.append("lesser_op")

                    

except FileNotFoundError:
    print ("\nEl archivo no fue encontrado")
except IOError:
    print ("\nError al abrir el archivo")


print(history)

def load_slr_matrix(file_path):
    try:
        slr_matrix = pd.read_excel(file_path)
        return slr_matrix
    except Exception as e:
        print("Error al cargar la matriz SLR:", e)
        return None

def load_grammar_rules(file_path):
    try:
        with open(file_path, 'r') as file:
            rules = [line.strip() for line in file.readlines()]
        return rules
    except Exception as e:
        print("Error al cargar las reglas gramaticales:", e)
        return None

#matrix_path = input("Nombre de la matriz: ") + ".xlsx"
matrix_path = "Transitions.xlsx"
slr_matrix = load_slr_matrix(matrix_path)
if slr_matrix is not None:
    print("Matriz SLR cargada exitosamente:")
    print(slr_matrix)

slr_matrix_matrixed = slr_matrix.to_numpy()
column_names = slr_matrix.columns.tolist()
#slr_matrix_matrixed_ = np.vstack([column_names, slr_matrix_matrixed])

#rules_path = input("Nombre de las reglas: ") + ".txt"
rules_path = "Rules.txt"
rules = load_grammar_rules(rules_path)
if rules is not None:
    print("Reglas gramaticales cargadas exitosamente:")
    for rule in rules:
        print(rule)

column_tokens = {column_name: i for i, column_name in enumerate(column_names)}
slr_matrix_numeric = slr_matrix.replace(column_tokens)
history_numeric = [column_tokens[token] for token in history]

print(history_numeric)

estado_inicial = 0
pila = [estado_inicial]


def obtener_accion(estado, token):
    return slr_matrix_matrixed[estado][token]

def aplicar_reduccion(regla):
    return rules[regla]

print (slr_matrix_matrixed[0][0])

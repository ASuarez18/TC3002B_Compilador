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

column_tokens = {column_name: i for i, column_name in enumerate(column_names)}
slr_matrix_numeric = slr_matrix.replace(column_tokens)
history_numeric = [column_tokens[token] for token in history]

print(history_numeric)

grammar_original = {
    0: ("P'", ["PROGRAM"]),
    1: ("PROGRAM", ["DEF_LIST"]),
    2: ("DEF_LIST", ["DEF_LIST", "DEF"]),
    3: ("DEF_LIST", []),
    4: ("DEF", ["VAR_DEF"]),
    5: ("DEF", ["FUN_DEF"]),
    6: ("VAR_DEF", ["var_kwd", "VAR_LIST", "limit_op"]),
    7: ("VAR_LIST", ["ID_LIST"]),
    8: ("ID_LIST", ["ID", "ID_LIST_CONT"]),
    9: ("ID_LIST_CONT", ["coma_op", "ID", "ID_LIST_CONT"]),
    10: ("ID_LIST_CONT", []),
    11: ("FUN_DEF", ["ID", "bracket1_op", "PARAM_LIST", "bracket2_op", "curly1_op", "VAR_DEF_LIST", "STMT_LIST", "curly2_op"]),
    12: ("PARAM_LIST", ["ID_LIST"]),
    13: ("PARAM_LIST", []),
    14: ("VAR_DEF_LIST", ["VAR_DEF_LIST", "VAR_DEF"]),
    15: ("VAR_DEF_LIST", []),
    16: ("STMT_LIST", ["STMT_LIST", "STMT"]),
    17: ("STMT_LIST", []),
    18: ("STMT", ["STMT_ASSIGN"]),
    19: ("STMT", ["STMT_INCR"]),
    20: ("STMT", ["STMT_DECR"]),
    21: ("STMT", ["STMT_FUN_CALL"]),
    22: ("STMT", ["STMT_IF"]),
    23: ("STMT", ["STMT_WHILE"]),
    24: ("STMT", ["STMT_DO_WHILE"]),
    25: ("STMT", ["STMT_BREAK"]),
    26: ("STMT", ["STMT_RETURN"]),
    27: ("STMT", ["STMT_EMPTY"]),
    28: ("STMT_ASSIGN", ["ID", "equal_op", "EXPR", "limit_op"]),
    29: ("STMT_INCR", ["inc_kwd", "ID", "limit_op"]),
    30: ("STMT_DECR", ["dec_kwd", "ID", "limit_op"]),
    31: ("STMT_FUN_CALL", ["FUN_CALL", "limit_op"]),
    32: ("FUN_CALL", ["ID", "bracket1_op", "EXPR_LIST", "bracket2_op"]),
    33: ("EXPR_LIST", ["EXPR", "EXPR_LIST_CONT"]),
    34: ("EXPR_LIST", []),
    35: ("EXPR_LIST_CONT", ["coma_op", "EXPR", "EXPR_LIST_CONT"]),
    36: ("EXPR_LIST_CONT", []),
    37: ("STMT_IF", ["if_kwd", "bracket1_op", "EXPR", "bracket2_op", "curly1_op", "STMT_LIST", "curly2_op", "ELSE_IF_LIST", "ELSE"]),
    38: ("ELSE_IF_LIST", ["ELSE_IF_LIST", "elseif_kwd", "bracket1_op", "EXPR", "bracket2_op", "curly1_op", "STMT_LIST", "curly2_op"]),
    39: ("ELSE_IF_LIST", []),
    40: ("ELSE_IF", ["elseif_kwd", "bracket1_op", "EXPR", "bracket2_op", "curly1_op", "STMT_LIST", "curly2_op"]),
    41: ("ELSE", ["else_kwd", "curly1_op", "STMT_LIST", "curly2_op"]),
    42: ("ELSE", []),
    43: ("STMT_WHILE", ["while_kwd", "bracket1_op", "EXPR", "bracket2_op", "curly1_op", "STMT_LIST", "curly2_op"]),
    44: ("STMT_DO_WHILE", ["do_kwd", "curly1_op", "STMT_LIST", "curly2_op", "while_kwd", "bracket1_op", "EXPR", "bracket2_op", "limit_op"]),
    45: ("STMT_BREAK", ["break_kwd", "limit_op"]),
    46: ("STMT_RETURN", ["return_kwd", "EXPR", "limit_op"]),
    47: ("STMT_EMPTY", ["limit_op"]),
    48: ("EXPR", ["EXPR_OR"]),
    49: ("EXPR_OR", ["EXPR_OR", "OP_OR", "EXPR_AND"]),
    50: ("OP_OR", ["or_op"]),
    51: ("OP_OR", ["xor_op"]),
    52: ("EXPR_OR", ["EXPR_AND"]),
    53: ("EXPR_AND", ["EXPR_AND", "and_op", "EXPR_COMP"]),
    54: ("EXPR_AND", ["EXPR_COMP"]),
    55: ("EXPR_COMP", ["EXPR_COMP", "OP_COMP", "EXPR_REL"]),
    56: ("EXPR_COMP", ["EXPR_REL"]),
    57: ("OP_COMP", ["equal_equal_op"]),
    58: ("OP_COMP", ["not_equal_op"]),
    59: ("EXPR_REL", ["EXPR_REL", "OP_REL", "EXPR_ADD"]),
    60: ("EXPR_REL", ["EXPR_ADD"]),
    61: ("OP_REL", ["lesser_op"]),
    62: ("OP_REL", ["lesser_equal_op"]),
    63: ("OP_REL", ["greater_op"]),
    64: ("OP_REL", ["greater_eq_op"]),
    65: ("EXPR_ADD", ["EXPR_ADD", "OP_ADD", "EXPR_MUL"]),
    66: ("EXPR_ADD", ["EXPR_MUL"]),
    67: ("OP_ADD", ["plus_op"]),
    68: ("OP_ADD", ["minus_op"]),
    69: ("EXPR_MUL", ["EXPR_MUL", "OP_MUL", "EXPR_UNARY"]),
    70: ("EXPR_MUL", ["EXPR_UNARY"]),
    71: ("OP_MUL", ["multi_op"]),
    72: ("OP_MUL", ["div_op"]),
    73: ("OP_MUL", ["reminder_op"]),
    74: ("EXPR_UNARY", ["OP_UNARY", "EXPR_UNARY"]),
    75: ("EXPR_UNARY", ["EXPR_PRIMARY"]),
    76: ("OP_UNARY", ["plus_op"]),
    77: ("OP_UNARY", ["minus_op"]),
    78: ("OP_UNARY", ["not_op"]),
    79: ("EXPR_PRIMARY", ["ID"]),
    80: ("EXPR_PRIMARY", ["FUN_CALL"]),
    81: ("EXPR_PRIMARY", ["ARRAY"]),
    82: ("EXPR_PRIMARY", ["LIT"]),
    83: ("EXPR_PRIMARY", ["bracket1_op", "EXPR", "bracket2_op"]),
    84: ("ARRAY", ["sqrbracket1_op", "EXPR_LIST", "sqrbracket2_op"]),
    85: ("LIT", ["bool_kwd"]),
    86: ("LIT", ["number"]),
    87: ("LIT", ["character"]),
    88: ("LIT", ["string"]),
}


estado_inicial = 0
pila = [estado_inicial]

def error():
    print("Error");
    quit()

def obtener_accion(estado, token):
    return slr_matrix_matrixed[estado][token]

def obtener_reduccion(regla):
    return grammar_original[regla]

def aplicar_reduccion(red, stack):
    journey = len(red[1])
    print(journey)
    for i in range(journey):
        print(stack[-2])
        print(red[1][-1])
        if stack[-2] == red[1][-1]:
            stack.pop(-1)
            stack.pop(-1)
            red[1].pop(-1)
        else:
            error()
    stack.append(red[0])
    print(stack)

listTemp = ['0', 'DEF_LIST', '2', 'ID', '7', 'bracket1_op', '11', 'ID', '10', 'coma_op', '14', 'ID', '17', 'ID_LIST_CONT', '19']

aplicar_reduccion(obtener_reduccion(9),listTemp)

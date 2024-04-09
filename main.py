import functions as fun

filename = input("Nombre del programa: ") + ".txt"
fileContent = []
operators = [ '+', '-', '*', '/', '%', '!', '&', '|', '^', '>', '=', '[', ']', '(', ')', ';', '{', '}', ',']
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

    elif char == '<' and not blocked:
        newState = 8

    elif char in reset and not blocked:
        newState = 0
    
    elif char == '#' and not blocked and state != 8:
        newState = 4
        history.append("line_comment")

    elif char == '#' and not blocked and state == 8:
        newState = 5
        history.append("multi_comment")

    elif char == '\'' and not blocked:
        newState = 6
        history.append("character")

    elif char == '"' and not blocked:
        newState = 7
        history.append("string")

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

    if state == 8 and newState != 5 and not blocked:
        history.append("lesser_op")

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

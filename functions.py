def changeState(prevState, word):
    match prevState:
        case 1: 
            match word:
                # Keywords basicas
                case "if": return "if_kwd"
                case "else": return "else_kwd"
                case "elseif": return "elseif_kwd"
                case "true": return "bool_kwd"
                case "false": return "bool_kwd"
                case "while": return "while_kwd"
                case "do": return "do_kwd"
                case "return": return "return_kwd"
                case "break": return "break_kwd"
                case "dec": return "dec_kwd"
                case "inc": return "inc_kwd"
                case "var": return "var_kwd"
                # Keywords API I/O Operations
                # case "printi": return "printi_kwd_api"
                # case "printc": return "printc_kwd_api"
                # case "prints": return "prints_kwd_api"
                # case "println": return "println_kwd_api"
                # case "readi": return "readi_kwd_api"
                # case "reads": return "reads_kwd_api"
                # Keywords API Array Operations
                # case "new": return "new_kwd_api"
                # case "add": return "add_kwd_api"
                # case "get": return "get_kwd_api"
                # case "set": return "set_kwd_api"
                case _: return "ID"
        case 2:
            return "number"
    return None


def operator(char):
    match char:
        case '+': return "plus_op"
        case '-': return "minus_op"
        case '*': return "multi_op"
        case '/': return "div_op"
        case '%': return "reminder_op"
        case '^': return "xor_op"
        case '[': return "sqrbracket1_op"
        case ']': return "sqrbracket2_op"
        case '(': return "bracket1_op"
        case ')': return "bracket2_op"
        case ';': return "limit_op"
        case '{': return "curly1_op"
        case '}': return "curly2_op"
        case ',': return "comma_op"
        


    

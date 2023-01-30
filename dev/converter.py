import re

def main():
    global var_declaration_pattern
    global enum_declaration_pattern
    global print_statement_pattern
    # global operator_pattern
    # global comparator_pattern
    global if_statement_pattern
    global for_statement_pattern
    global output_file
    global print_all

    print_all = ""
    var_declaration_pattern = re.compile(r"(\w+) (\w+) = (.*?);") 
    enum_declaration_pattern = re.compile(r"enum (\w+) {(.*?)};")
    print_statement_pattern = re.compile(r"cout(.*?);")
    # operator_pattern = re.compile(r"([+\-*/%=<>!&|^]+|&&|\|\|)")
    # comparator_pattern = re.compile(r"(==|!=|<=|>=|<|>|)")
    if_statement_pattern = re.compile(r"if \((.*?)\) {(.*?)}")
    for_statement_pattern = re.compile(r"for\s*\((.*?);(.*?);(.*?)\)\s*{(.*?)}", re.DOTALL)


    # Read the input file
    with open("dev/basis.h", "r") as input_file:
        input_lines = input_file.readlines()

    # Open the output file
    with open("dev/basis.fs", "w") as output_file:
        for line in input_lines:
            # oldPatternSearch(line)
            output_file.write(patternSearch(line))
            

def oldPatternSearch(line):
    var_match = var_declaration_pattern.search(line)               # var_match is a Match object
    enum_match = enum_declaration_pattern.search(line)             # enum_match is a Match object
    print_match = print_statement_pattern.search(line)             # print_match is a Match object
    # operator = operator_pattern.sub(lambda match: match.group(0), line)
    # comparator = comparator_pattern.sub(lambda match: match.group(0), line)
    if_match = if_statement_pattern.search(line)
    for_match = for_statement_pattern.search(line) # for
    if for_match:
        init_statement = for_match.group(1)
        condition = for_match.group(2)
        increment = for_match.group(3)
        body = for_match.group(4)

        # Translate the initialization statement
        init_statement = init_statement.replace("int ", "")

        # Translate the increment statement
        increment = increment.replace("+", "..")
        increment = increment.replace("=", "")
        increment = increment.replace(";", " do")

        # Write the F# for loop to the output file
        output_file.write(f"for {init_statement} {condition} {increment}\n")

        # Translate the body of the loop
        body = body.replace("cout <<", "printfn")
        body = body.replace("<<", "")
        body = body.replace(";", "")
        output_file.write(f"{body}\n")
    elif var_match:                                                  # if var_match is not None
        type_name = var_match.group(1)                             # type_name is a string who represents the type of the variable
        var_name = var_match.group(2)                              # var_name is a string who represents the variable name
        var_value = var_match.group(3)                             # var_value is a string who represents the variable value
        # if type_name == 'int': 
        #     type_name = 'int'                                      # we set the type_name to 'int' for the output F# file
        # elif type_name == 'float':
        #     type_name = 'float'                                    # we set the type_name to 'float' for the output F# file
        # elif type_name == 'double':
        #     type_name = 'double'                                   # we set the type_name to 'double' for the output F# file
        if type_name == 'char':
            type_name = 'string'                                   # we set the type_name to 'string' for the output F# file
            var_value = str.replace(var_value, "'", '"') 
        # elif type_name == 'bool':
        #     type_name = 'bool'                                     # we set the type_name to 'bool' for the output F# file
        # elif type_name == 'string':
        #     type_name = 'string'
        output_file.write(f"let {var_name} : {type_name} = {var_value}\n")
    elif enum_match:
        enum_name = enum_match.group(1)
        enum_values = enum_match.group(2).split(',')
        output_file.write(f"type {enum_name} =\n")
        for value in enum_values:
            output_file.write(f"   | {value.strip()} = {value.strip()}\n")
    elif print_match:
        print_content = print_match.group(1)
        print_content = str.replace(print_content, "endl", "")
        print_content = str.replace(print_content, "<<", "")
        if print_content.startswith("  ") & print_content.endswith("  "):
            print_content = print_content[2:]
            print_content = print_content[:-2]
        output_file.write(f"printfn {print_content}\n")
    # elif operator:
    #     output_file.write(operator)
    # elif comparator:
    #     output_file.write(comparator)
    elif if_match:
        condition = if_match.group(1)
        code = if_match.group(2)
        output_file.write(f"if {condition} then\n{code}\n")

def TestFor():
    for_statement_pattern = re.compile(r"for \((.*?); (.*?); (.*?)\) {(.*?)}")

    with open("dev/basis.h", "r") as input_file:
        input_lines = input_file.readlines()
        for line in input_lines:
            for_match = for_statement_pattern.search(line)
            if for_match:
                initialization = for_match.group(1)
                condition = for_match.group(2)
                increment = for_match.group(3)
                code = for_match.group(4)
        print(f"for {initialization} {condition} {increment} do\n{code}\n")


'''
# TODO
 patternSearch : recursive function ?
 While we detect patterns : (Add priority like for/if statements before +/- operators) 
 We search pattern in EVERY element of the previous pattern
 If we don't have more pattern in an element we return the pattern transformed in F#
 We go back (thanks to the recursive function) and we apply the previous pattern
 We repeat until all patterns are treated
 Return variable with every pattern

 Order : For > If > Enum > Print > Var > Operator > Comparator
'''
# In progress (problem with global variable print_all)
def patternSearch(line):
    global print_all
    var_match = var_declaration_pattern.search(line)               # var_match is a Match object
    enum_match = enum_declaration_pattern.search(line)             # enum_match is a Match object
    print_match = print_statement_pattern.search(line)             # print_match is a Match object
    # operator = operator_pattern.sub(lambda match: match.group(0), line)
    # comparator = comparator_pattern.sub(lambda match: match.group(0), line)
    if_match = if_statement_pattern.search(line)
    for_match = for_statement_pattern.search(line) # for
    if for_match: # TODO
        init_statement = for_match.group(1)
        condition = for_match.group(2)
        increment = for_match.group(3)
        body = for_match.group(4)
    
        init_statement = init_statement.replace("int ", "")
        increment = increment.replace("+", "..")
        increment = increment.replace("=", "")
        increment = increment.replace(";", " do")
    
        print_all = print_all + f"for {init_statement} {condition} {increment}\n"
        # output_file.write(f"for {init_statement} {condition} {increment}\n")
        body = body.replace("cout <<", "printfn")
        body = body.replace("<<", "")
        body = body.replace(";", "")
        print_all = print_all + f"{body}\n" + "\n"
        # output_file.write(f"{body}\n")
        # output_file.write("\n")
    elif if_match:
        condition = if_match.group(1)
        condition_fsharp = patternSearch(condition)
        code = if_match.group(2)
        code_fsharp = patternSearch(code)
        print_all = print_all + f"if {condition_fsharp} then\n{code_fsharp}\n"
        # output_file.write(f"if {condition_fsharp} then\n{code_fsharp}\n")
    elif enum_match: # not implemented yet
        enum_name = enum_match.group(1)
        enum_values = enum_match.group(2).split(',')
        print_all += f"type {enum_name} =\n"
        for value in enum_values:
            print_all = print_all + f"   | {value.strip()} = {value.strip()}\n"
    elif print_match:
        print_content = print_match.group(1)
        print_content = str.replace(print_content, "endl", "")
        print_content = str.replace(print_content, "<<", "")
        print_content_fsharp = patternSearch(print_content)
        if print_content_fsharp.startswith("  ") & print_content_fsharp.endswith("  "):
            print_content_fsharp = print_content_fsharp[2:]
            print_content_fsharp = print_content_fsharp[:-2]
        print_all = print_all + f"printfn {print_content_fsharp}\n"
        # output_file.write(f"printfn {print_content_fsharp}\n")
    elif var_match:                                                  # if var_match is not None
        type_name = var_match.group(1)
        type_name_fsharp = patternSearch(type_name)                             # type_name is a string who represents the type of the variable
        var_name = var_match.group(2) 
        var_name_fsharp = patternSearch(var_name)                              # var_name is a string who represents the variable name
        var_value = var_match.group(3) 
        var_value_fsharp = patternSearch(var_value)                             # var_value is a string who represents the variable value                                # we set the type_name to 'double' for the output F# file
        if type_name_fsharp == 'char':
            type_name_fsharp = 'string'                                   # we set the type_name to 'string' for the output F# file
            var_value_fsharp = str.replace(var_value_fsharp, "'", '"') 
        print_all = print_all + f"let {var_name_fsharp} : {type_name_fsharp} = {var_value_fsharp}\n"
        # output_file.write(f"let {var_name_fsharp} : {type_name_fsharp} = {var_value_fsharp}\n")
    return print_all
    
        

def countVariables():
    # Patterns
    var_declaration_pattern = re.compile(r"(\w+) (\w+) = (.*?);") 
    enum_declaration_pattern = re.compile(r"enum (\w+) {(.*?)}") 

    # Iteration 
    int_iteration = 0
    float_iteration = 0
    double_iteration = 0
    char_iteration = 0
    bool_iteration = 0
    string_iteration = 0
    enum_iteration = 0
    


    switcher = {
        0: "int",
        1: "float",
        2: "double",
        3: "char",
        4: "bool",
        5: "string"
    }

    line_number = 0

    # Read the input file
    with open("dev/basis.h", "r") as input_file:
        input_lines = input_file.readlines()
        for line in input_lines:
            line_number += 1
            var_match = var_declaration_pattern.search(line)
            if var_match:
                type_name = var_match.group(1)
                if type_name == switcher.get(0):
                    int_iteration += 1
                    print("int found at line ", line_number)
                elif type_name == switcher.get(1):
                    float_iteration += 1
                    print("float found at line ", line_number)
                elif type_name == switcher.get(2):
                    double_iteration += 1
                    print("double found at line ", line_number)
                elif type_name == switcher.get(3):
                    char_iteration += 1
                    print("char found at line ", line_number)
                elif type_name == switcher.get(4):
                    bool_iteration += 1
                    print("bool found at line ", line_number)
                elif type_name == switcher.get(5):
                    string_iteration += 1
                    print("string found at line ", line_number)
    print("int : ", int_iteration)
    print("float : ", float_iteration)
    print("double : ", double_iteration)
    print("char : ", char_iteration)
    print("bool : ", bool_iteration)
    print("string : ", string_iteration)
    


    with open("dev/basis.h", "r") as input_file:
        input_lines = input_file.readlines()
        for line in input_lines:
            line_number += 1
            enum_match = enum_declaration_pattern.search(line)
            if enum_match:
                enum_iteration += 1
                print(f"enum found on line {line_number}")
    print("enum : ", enum_iteration)
    
    # print("total : ", int_iteration + float_iteration + double_iteration + char_iteration + bool_iteration + string_iteration + enum_iteration)

def countFunction():
    #! TODO: count the functions present in the file NOT FINISHED
    function_pattern = re.compile(r"(\w+) (\w+)\((.*?)\)")
    function_iteration = 0
    line_number = 0

    with open("dev/basis.h", "r") as input_file:
        input_lines = input_file.readlines()
        for line in input_lines:
            line_number += 1
            function_match = function_pattern.search(line)
            if function_match:
                function_iteration += 1
                print(f"function found on line {line_number}")
        print("function : ", function_iteration)

def countIf():
    if_pattern = re.compile(r"if\((.*?)\)(.*?)")
    if_iteration = 0
    line_number = 0

    with open("dev/basis.h", "r") as input_file:
        input_lines = input_file.readlines()
        for line in input_lines:
            line_number += 1
            if_match = if_pattern.search(line)
            if if_match:
                if_iteration += 1
                print(f"if statement found on line {line_number}")
        print("if : ", if_iteration)

def countFor():
    for_pattern = re.compile(r"for\((.*?)\)(.*?)")
    for_iteration = 0
    line_number = 0

    with open("dev/basis.h", "r") as input_file:
        input_lines = input_file.readlines()
        for line in input_lines:
            line_number += 1
            for_match = for_pattern.search(line)
            if for_match:
                for_iteration += 1
                print(f"for statement found on line {line_number}")
        print("for : ", for_iteration)


def TotalCount(): 
    return countVariables(), countFunction(), countIf(), countFor()


TotalCount()
main()
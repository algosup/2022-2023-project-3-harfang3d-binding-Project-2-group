import re

var_declaration_pattern = re.compile(r"(\w+) (\w+) = (.*?);")
enum_declaration_pattern = re.compile(r"enum (\w+) {(.*?)};")
print_statement_pattern = re.compile(r"cout(.*?);")
operator_pattern = re.compile(r"([+\-*/%=<>!&|^]+|&&|\|\|)")
comparator_pattern = re.compile(r"(==|!=|<=|>=|<|>)")

# Read the input file
with open("Test/basis.h", "r") as input_file:
    input_lines = input_file.readlines()

# Open the output file
with open("Test/basis.fs", "w") as output_file:
    for line in input_lines:
        var_match = var_declaration_pattern.search(line)
        enum_match = enum_declaration_pattern.search(line)
        print_match = print_statement_pattern.search(line)
        operator = operator_pattern.sub(lambda match: match.group(0).replace("&&", "&&&").replace("||", "|||"), line)
        comparator = comparator_pattern.sub(lambda match: match.group(0).replace("==", "=").replace("!=", "<>"), line)        
        if var_match:
            type_name = var_match.group(1)
            var_name = var_match.group(2)
            var_value = var_match.group(3)
            if type_name == 'int':
                type_name = 'int'
            elif type_name == 'float':
                type_name = 'single'
            elif type_name == 'double':
                type_name = 'double'
            elif type_name == 'char':
                type_name = 'char'
                var_value = "'"+var_value+"'"
            elif type_name == 'bool':
                type_name = 'bool'
            elif type_name == 'string':
                type_name = 'string'    
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
        elif operator:
            output_file.write(operator)
        elif comparator:
            output_file.write(comparator)

import re

var_declaration_pattern = re.compile(r"(\w+) (\w+) = (.*?);")
enum_declaration_pattern = re.compile(r"enum (\w+) {(.*?)};")

# Read the input file
with open("Test/basis.h", "r") as input_file:
    input_lines = input_file.readlines()

# Open the output file
with open("Test/basis.fs", "w") as output_file:
    for line in input_lines:
        var_match = var_declaration_pattern.search(line)
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
        else:
            enum_match = enum_declaration_pattern.search(line)
            if enum_match:
                enum_name = enum_match.group(1)
                enum_values = enum_match.group(2).split(',')
                output_file.write(f"type {enum_name} =\n")
                for value in enum_values:
                    output_file.write(f"   | {value.strip()} = {value.strip()}\n")

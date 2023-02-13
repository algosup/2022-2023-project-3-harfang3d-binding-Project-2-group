# FABGen - The FABulous binding Generator for F#

import lang.fsharp


def bind_stl(gen):
    gen.add_include('vector', True)
    gen.add_include('string', True)
    
    class FSharpStringConverter(lang.fsharp.FSharpTypeConverterCommon):
        def __init__(self, type, to_c_storage_type=None, bound_name=None, from_c_storage_type=None, needs_c_storage_class=False):
            super().__init__(type, to_c_storage_type, bound_name, from_c_storage_type, needs_c_storage_class)
            self.fsharp_to_c_type = "string"
            self.fsharp_type = "string"
            
        def get_type_glue(self, gen, module_name):
            return ''

        def get_type_api(self, module_name):
            return ''

        def to_c_call(self, in_var, out_var_p, is_pointer=False):
            if is_pointer:
                out = f"{out_var_p.replace('&', '_')} = &{in_var}\n"
            else:
                out = f"{out_var_p} = {in_var}\n"
            return out

        def from_c_call(self, out_var, expr, ownership):
            return out_var

    gen.bind_type(FSharpStringConverter("System.String"))


def bind_function_T(gen, type, bound_name=None):
    class FSharpStdFunctionConverter(lang.fsharp.FSharpTypeConverterCommon):
        def get_type_glue(self, gen, module_name):
            return ""

    return gen.bind_type(FSharpStdFunctionConverter(type))


class FSharpListToStdVectorConverter(lang.fsharp.FSharpTypeConverterCommon):
    def __init__(self, type, T_conv):
        native_type = f"List<{T_conv.ctype}>"
        super().__init__(type, native_type, None, native_type)
        self.T_conv = T_conv

    def get_type_glue(self, gen, module_name):
        return ''
        
    def to_c_call(self, in_var, out_var_p, is_pointer):
        return ""

    def from_c_call(self, out_var, expr, ownership):
        return ""

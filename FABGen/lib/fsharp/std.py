import lang.fsharp

def bind_std(gen):
    class FSharpConstCharPtrConverter(lang.fsharp.FSharpTypeConverterCommon):
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
                out = f"{out_var_p.replace('&', '_')} := Marshal.StringToHGlobalAnsi(*{in_var})\n"
            else:
                out = f"{out_var_p.replace('&', '_')} := Marshal.StringToHGlobalAnsi({in_var})\n"
            return out

        def from_c_call(self, out_var, expr, ownership):
            return f"Marshal.PtrToStringAnsi({out_var})"
# FABGen - The FABulous binding Generator for F#

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
        
    gen.bind_type(FSharpConstCharPtrConverter("const char *"))

    class FSharpBasicTypeConverter(lang.fsharp.FSharpTypeConverterCommon):
        def __init__(self, type, c_type, fsharp_type, to_c_storage_type=None, bound_name=None, from_c_storage_type=None, needs_c_storage_class=False):
            super().__init__(type, to_c_storage_type, bound_name, from_c_storage_type, needs_c_storage_class)
            self.fsharp_to_c_type = c_type
            self.fsharp_type = fsharp_type

        def get_type_glue(self, gen, module_name):
            return ''

        def get_type_api(self, module_name):
            return ''

        def to_c_call(self, in_var, out_var_p, is_pointer):
            if is_pointer:
                out = f"let {out_var_p.replace('&', '_')} = (*{self.fsharp_to_c_type})(System.IntPtr({in_var}))\n"
            else:
                out = f"let {out_var_p.replace('&', '_')} = {self.fsharp_to_c_type}({in_var})\n"
            return out

        def from_c_call(self, out_var, expr, ownership):
            return f"{self.fsharp_type}({out_var})"


    # gen.bind_type(FSharpBasicTypeConverter("sbyte", "sbyte", "int8"))
    # gen.bind_type(FSharpBasicTypeConverter("byte", "byte", "uint8"))
    # gen.bind_type(FSharpBasicTypeConverter("uint8", "byte", "uint8"))

    # gen.bind_type(FSharpBasicTypeConverter("int16", "int16", "int16"))
    # gen.bind_type(FSharpBasicTypeConverter("short", "int16", "int16"))
    # gen.bind_type(FSharpBasicTypeConverter("char16", "int16", "int16"))

    # gen.bind_type(FSharpBasicTypeConverter("uint16", "uint16", "uint16"))
    # gen.bind_type(FSharpBasicTypeConverter("ushort", "uint16", "uint16"))

    # gen.bind_type(FSharpBasicTypeConverter("int", "int", "int32"))
    # gen.bind_type(FSharpBasicTypeConverter("int32", "int32", "int32"))
    # gen.bind_type(FSharpBasicTypeConverter("char32", "int32", "int32"))
    # gen.bind_type(FSharpBasicTypeConverter("nint", "int", "int32"))

    # gen.bind_type(FSharpBasicTypeConverter("uint", "uint", "uint32"))
    # gen.bind_type(FSharpBasicTypeConverter("uint32", "uint32", "uint32"))
    # gen.bind_type(FSharpBasicTypeConverter("unsigned int", "uint32", "uint32"))

    # gen.bind_type(FSharpBasicTypeConverter("long", "int64", "int64"))
    # gen.bind_type(FSharpBasicTypeConverter("int64", "int64", "int64"))

    # gen.bind_type(FSharpBasicTypeConverter("float32", "float", "float32"))
    # gen.bind_type(FSharpBasicTypeConverter("single", "float", "float32"))

    # gen.bind_type(FSharpBasicTypeConverter("nuint", "uintptr", "uintptr"))
    # gen.bind_type(FSharpBasicTypeConverter("UIntPtr", "uintptr", "uintptr"))

    # gen.bind_type(FSharpBasicTypeConverter("ulong", "ulong", "uint64"))
    # gen.bind_type(FSharpBasicTypeConverter("uint64", "ulong", "uint64"))
    # gen.bind_type(FSharpBasicTypeConverter("double", "double", "float64"))

    gen.bind_type(FSharpBasicTypeConverter("byte", "unsigned char", "byte"))
    gen.bind_type(FSharpBasicTypeConverter("sbyte", "signed char", "sbyte"))
    gen.bind_type(FSharpBasicTypeConverter("int16", "short", "int16"))
    gen.bind_type(FSharpBasicTypeConverter("uint16", "unsigned short", "uint16"))
    gen.bind_type(FSharpBasicTypeConverter("int", "int", "int32"))
    gen.bind_type(FSharpBasicTypeConverter("uint", "uint", "uint32"))
    gen.bind_type(FSharpBasicTypeConverter("int64", "int64_t", "int64"))
    gen.bind_type(FSharpBasicTypeConverter("uint64", "uint64_t", "uint64"))
    gen.bind_type(FSharpBasicTypeConverter("nativeint", "intptr_t", "intPtr"))
    gen.bind_type(FSharpBasicTypeConverter("unativeint", "uintptr_t", "uintPtr"))
    gen.bind_type(FSharpBasicTypeConverter("decimal", "double", "decimal"))
    gen.bind_type(FSharpBasicTypeConverter("float", "double", "double"))
    gen.bind_type(FSharpBasicTypeConverter("double", "double", "double"))
    gen.bind_type(FSharpBasicTypeConverter("float32", "float", "single"))
    gen.bind_type(FSharpBasicTypeConverter("single", "float", "single"))
    

    class FSharpBoolConverter(lang.fsharp.FSharpTypeConverterCommon):
        def init(self, type, to_c_storage_type=None, bound_name=None, from_c_storage_type=None, needs_c_storage_class=False):
            super().init(type, to_c_storage_type, bound_name, from_c_storage_type, needs_c_storage_class)
            self.fsharp_to_c_type = "C.bool"

        def get_type_glue(self, gen, module_name):
            return ''

        def get_type_api(self, module_name):
            return ''

        def to_c_call(self, in_var, out_var_p, is_pointer):
            if is_pointer:
                out = f"{out_var_p.replace('&', '_')} := (*C.bool)(unsafe.Pointer({in_var}))\n"
            else:
                out = f"{out_var_p.replace('&', '_')} := C.bool({in_var})\n"
            return out

        def from_c_call(self, out_var, expr, ownership):
            return "bool(%s)" % (out_var)

    gen.bind_type(FSharpBoolConverter('bool')).nobind = True
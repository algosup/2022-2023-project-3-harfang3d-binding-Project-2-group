
import lang.fsharp


def bind_std(gen):
	class FsharpConstCharPtrConverter(lang.fsharp.FsharpTypeConverterCommon):
		def __init__(self, type, to_c_storage_type=None, bound_name=None, from_c_storage_type=None, needs_c_storage_class=False):
			super().__init__(type, to_c_storage_type, bound_name, from_c_storage_type, needs_c_storage_class)
			self.go_to_c_type = "*char"
			self.go_type = "string"
			
		def get_type_glue(self, gen, module_name):
			return ''

		def get_type_api(self, module_name):
			return ''

		def to_c_call(self, in_var, out_var_p, is_pointer=False):
			if is_pointer:
				out = f"{out_var_p.replace('&', '_')}1 := CString(*{in_var})\n"
				out += f"{out_var_p.replace('&', '_')} := &{out_var_p.replace('&', '_')}1\n"
			else:
				out = f"{out_var_p.replace('&', '_')}, idFin{out_var_p.replace('&', '_')} := wrapString({in_var})\n"
				out += f"defer idFin{out_var_p.replace('&', '_')}()\n"
			return out

		def from_c_call(self, out_var, expr, ownership):
			return "Fsharpstring(%s)" % (out_var)

	gen.bind_type(FsharpConstCharPtrConverter("const char *"))

	class FsharpBasicTypeConverter(lang.fsharp.FsharpTypeConverterCommon):
		def __init__(self, type, c_type, go_type, to_c_storage_type=None, bound_name=None, from_c_storage_type=None, needs_c_storage_class=False):
			super().__init__(type, to_c_storage_type, bound_name, from_c_storage_type, needs_c_storage_class)
			self.go_to_c_type = c_type
			self.go_type = go_type

		def get_type_glue(self, gen, module_name):
			return ''

		def get_type_api(self, module_name):
			return ''

		def to_c_call(self, in_var, out_var_p, is_pointer):
			if is_pointer:
				out = f"{out_var_p.replace('&', '_')} := (*{self.go_to_c_type})(unsafe.Pointer({in_var}))\n"
			else:
				out = f"{out_var_p.replace('&', '_')} := {self.go_to_c_type}({in_var})\n"
			return out

		def from_c_call(self, out_var, expr, ownership):
			return f"{self.go_type}({out_var})"

	gen.bind_type(FsharpBasicTypeConverter("char", "char", "int8"))

	gen.bind_type(FsharpBasicTypeConverter("unsigned char", "uchar", "uint8"))
	gen.bind_type(FsharpBasicTypeConverter("uint8_t", "uchar", "uint8"))

	gen.bind_type(FsharpBasicTypeConverter("short", "short", "int16"))
	gen.bind_type(FsharpBasicTypeConverter("int16_t", "short", "int16"))
	gen.bind_type(FsharpBasicTypeConverter("char16_t", "short", "int16"))

	gen.bind_type(FsharpBasicTypeConverter("uint16_t", "ushort", "uint16"))
	gen.bind_type(FsharpBasicTypeConverter("unsigned short", "ushort ", "uint16"))
	
	gen.bind_type(FsharpBasicTypeConverter("int32", "int32_t", "int32"))
	gen.bind_type(FsharpBasicTypeConverter("int", "int32_t", "int32"))
	gen.bind_type(FsharpBasicTypeConverter("int32_t", "int32_t", "int32"))
	gen.bind_type(FsharpBasicTypeConverter("char32_t", "int32_t", "int32"))
	gen.bind_type(FsharpBasicTypeConverter("size_t", "size_t", "int32"))

	gen.bind_type(FsharpBasicTypeConverter("uint32_t", "uint32_t", "uint32"))
	gen.bind_type(FsharpBasicTypeConverter("unsigned int32_t", "uint32_t", "uint32"))
	gen.bind_type(FsharpBasicTypeConverter("unsigned int", "uint32_t", "uint32"))

	gen.bind_type(FsharpBasicTypeConverter("int64_t", "int64_t", "int64"))
	gen.bind_type(FsharpBasicTypeConverter("long", "int64_t", "int64"))

	gen.bind_type(FsharpBasicTypeConverter("float32", "float", "float32"))
	gen.bind_type(FsharpBasicTypeConverter("float", "float", "float32"))
	
	gen.bind_type(FsharpBasicTypeConverter("intptr_t", "intptr_t", "uintptr"))

	gen.bind_type(FsharpBasicTypeConverter("unsigned long", "uint64_t", "uint64"))
	gen.bind_type(FsharpBasicTypeConverter("uint64_t", "uint64_t ", "uint64"))
	gen.bind_type(FsharpBasicTypeConverter("double", "double", "float64"))
	
	class FsharpBoolConverter(lang.fsharp.FsharpTypeConverterCommon):
		def __init__(self, type, to_c_storage_type=None, bound_name=None, from_c_storage_type=None, needs_c_storage_class=False):
			super().__init__(type, to_c_storage_type, bound_name, from_c_storage_type, needs_c_storage_class)
			self.go_to_c_type = "bool"
		def get_type_glue(self, gen, module_name):
			return ''

		def get_type_api(self, module_name):
			return ''

		def to_c_call(self, in_var, out_var_p, is_pointer):
			if is_pointer:
				out = f"{out_var_p.replace('&', '_')} := (*bool)(unsafe.Pointer({in_var}))\n"
			else:
				out = f"{out_var_p.replace('&', '_')} := bool({in_var})\n"
			return out

		def from_c_call(self, out_var, expr, ownership):
			return "bool(%s)" % (out_var)

	gen.bind_type(FsharpBoolConverter('bool')).nobind = True

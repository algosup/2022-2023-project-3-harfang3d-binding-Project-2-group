# Harfang - The Fabulous binding Generator for CPython and Go
# 	Copyright (C) 2020 Thomas Simonnet

import os
from os import stat_result
from pypeg2 import parse
import json
import re
import sys
import time
import importlib

import argparse

import gen
import lib

# add name to the go package 
def route_lambda(name):
	return lambda args: "%s(%s);" % (name, ", ".join(args))


def clean_name(name):
	new_name = str(name).strip().replace("_", "").replace(":", "")
	# if new_name isn't in list of reserved word in go then return new_name else return new_name + "Go"
	if new_name in ["break", "default", "func", "interface", "select", "case", "defer", "go", "map", "struct", "chan", "else", "goto", "package", "switch", "const", "fallthrough", "if", "range", "type", "continue", "for", "import", "return", "var" ]:
		return new_name + "Go"
	return new_name
	# allows you to separate go-compatible functions from others 

def clean_name_with_title(name):
	new_name = ""
	if "_" in name:
		# redo a special string.title()
		next_is_forced_uppercase = True
		for c in name:
			if c in ["*", "&"]: # don't capitalize the first letter after a pointer
				new_name += c
			elif c in ["_", "-"]: # force the next letter to be uppercase
				next_is_forced_uppercase = True
			else: # normal letter
				if next_is_forced_uppercase: # force the next letter to be uppercase
					next_is_forced_uppercase = False
					new_name += c.capitalize()
				else: # normal letter
					new_name += c
	else:
		# make sur the first letter is capitalize
		first_letter_checked = False
		for c in name: # normal letter
			if c in ["*", "&"] or first_letter_checked: # don't capitalize the first letter after a pointer
				new_name += c
			elif not first_letter_checked: # force the next letter to be uppercase
				first_letter_checked = True
				new_name += c.capitalize()
	return new_name.strip().replace("_", "").replace(":", "") # remplace "_" and ":" by " "


class GoTypeConverterCommon(gen.TypeConverter): # common class for all the go type converter
	def __init__(self, type, to_c_storage_type=None, bound_name=None, from_c_storage_type=None, needs_c_storage_class=False): # init the class
		super().__init__(type, to_c_storage_type, bound_name, from_c_storage_type, needs_c_storage_class) # init the parent class
		self.base_type = type # add the base type
		self.go_to_c_type = None # add the go to c type
		self.go_type = None # add the go type
	
	# get the go type of the variable in C type 
	def get_type_api(self, module_name): # return the go type of the variable in C type
		out = "// type API for %s\n" % self.ctype # add the comment for the type API
		if self.c_storage_class: # if the c_storage_class is not empty
			out += "struct %s;\n" % self.c_storage_class # add the struct in the c_storage_class
		if self.c_storage_class:  # if the c_storage_class is not empty
			out += "void %s(int idx, void *obj, %s &storage);\n" % (self.to_c_func, self.c_storage_class) # add the function in the c_storage_class
		else: # if not 
			out += "void %s(int idx, void *obj);\n" % self.to_c_func # add the function in the c_storage_class
		out += "int %s(void *obj, OwnershipPolicy);\n" % self.from_c_func # add the function in the c_storage_class
		out += "\n"
		return out # return the out

	def to_c_call(self, in_var, out_var_p, is_pointer): # return the go variable in C variable
		return "" # return  ""

	# add the go variable in C variable
	def from_c_call(self, out_var, expr, ownership): # return the C variable in go variable
		return "%s((void *)%s, %s);\n" % (self.from_c_func, expr, ownership) # return  ""


class DummyTypeConverter(gen.TypeConverter): # class for the dummy type converter
	def __init__(self, type, to_c_storage_type=None, bound_name=None, from_c_storage_type=None, needs_c_storage_class=False): # init the class
		super().__init__(type, to_c_storage_type, bound_name, from_c_storage_type, needs_c_storage_class) # init the parent class

	def get_type_api(self, module_name): # return  ""
		return ""

	def to_c_call(self, in_var, out_var_p, is_pointer): # return  ""
		return ""

	def from_c_call(self, out_var, expr, ownership): # return  ""
		return ""

	def check_call(self, in_var): # return  ""
		return ""

	def get_type_glue(self, gen, module_name): # return  ""
		return ""


class GoPtrTypeConverter(gen.TypeConverter): # class for the pointer type converter
	def __init__(self, type, to_c_storage_type=None, bound_name=None, from_c_storage_type=None, needs_c_storage_class=False): # init the class
		super().__init__(type, to_c_storage_type, bound_name, from_c_storage_type, needs_c_storage_class) # init the parent class

	def get_type_api(self, module_name): # return  ""
		return ""

	def to_c_call(self, in_var, out_var_p, is_pointer): # return  ""
		return ""

	def from_c_call(self, out_var, expr, ownership): # return  ""
		return ""

	def check_call(self, in_var): # return  ""
		return ""

	def get_type_glue(self, gen, module_name): # return  ""
		return ""

class GoClassTypeDefaultConverter(GoTypeConverterCommon): # default class type converter
	def __init__(self, type, to_c_storage_type=None, bound_name=None, from_c_storage_type=None, needs_c_storage_class=False): # init the class
		super().__init__(type, to_c_storage_type, bound_name, from_c_storage_type, needs_c_storage_class) # call the parent class

	def is_type_class(self): # return  ""
		return True # is a class

	def get_type_api(self, module_name): # return the go type of the variable in C type
		return "" # no type api

	def to_c_call(self, in_var, out_var_p, is_pointer): # add the go variable in C variable
		out = f"{out_var_p.replace('&', '_')} := {in_var}.h\n" # get the C pointer
		return out # no to c call

	def from_c_call(self, out_var, expr, ownership): # add the go variable in C variable
		return "" # no from c call

	def check_call(self, in_var): # check if the variable is a class
		return "" # no check

	def get_type_glue(self, gen, module_name): # get the type glue
		return "" # no type glue

class GoExternTypeConverter(GoTypeConverterCommon): # converter for extern type
	def __init__(self, type, to_c_storage_type, bound_name, module): # module is the module where the type is defined
		super().__init__(type, to_c_storage_type, bound_name) # to_c_storage_type is the type of the variable in C
		self.module = module # module is the module where the type is defined

	def get_type_api(self, module_name): # get the type API
		return '' # no type API
	
	def to_c_call(self, in_var, out_var_p): # add the go variable in C variable
		out = '' # out is the string that will be returned
		if self.c_storage_class: # if the type has a storage class
			c_storage_var = 'storage_%s' % out_var_p.replace('&', '_') # c_storage_var is the name of the variable in C
			out += '%s %s;\n' % (self.c_storage_class, c_storage_var) # add the variable in C
			out += '(*%s)(%s, (void *)%s, %s);\n' % (self.to_c_func, in_var, out_var_p, c_storage_var) # add the function pointer
		else: # if the type has no storage class
			out += '(*%s)(%s, (void *)%s);\n' % (self.to_c_func, in_var, out_var_p) # add the function pointer
		return out # return the string

	def from_c_call(self, out_var, expr, ownership): # add the C variable in go variable
		return "%s = (*%s)((void *)%s, %s);\n" % (out_var, self.from_c_func, expr, ownership) # return the function pointer

	def check_call(self, in_var): # check if the type is correct
		return "(*%s)(%s)" % (self.check_func, in_var) # return the function pointer

	def get_type_glue(self, gen, module_name): # create
		out = '// extern type API for %s\n' % self.ctype # add a comment
		if self.c_storage_class: # if the type has a storage class
			out += 'struct %s;\n' % self.c_storage_class # add a struct
		out += 'bool (*%s)(void *o) = nullptr;\n' % self.check_func # add a function pointer
		if self.c_storage_class: # if the type has a storage class
			out += 'void (*%s)(void *o, void *obj, %s &storage) = nullptr;\n' % (self.to_c_func, self.c_storage_class) # add a function pointer
		else: # if the type has no storage class
			out += 'void (*%s)(void *o, void *obj) = nullptr;\n' % self.to_c_func # add a function pointer
		out += 'int (*%s)(void *obj, OwnershipPolicy) = nullptr;\n' % self.from_c_func # add a function pointer
		out += '\n' # add a new line
		return out # return the output

class GoGenerator(gen.FABGen): # create a new generator class
	default_ptr_converter = GoPtrTypeConverter  # set the default pointer converter
	default_class_converter = GoClassTypeDefaultConverter # set the default class converter
	default_extern_converter = GoExternTypeConverter  # set the default extern converter
	
	def __init__(self): # constructor
		super().__init__() # call the base class constructor
		self.check_self_type_in_ops = True # check the self type in operations
		self.go = "" # the Go source code
		self.cgo_directives = "" # the cgo directives

	def get_language(self): 
		return "Go" # return the language name

	def output_includes(self): # output the includes
		pass # we don't need any includes

	def start(self, module_name): # start the generator
		super().start(module_name) # call the base class
		

		self._source += self.get_binding_api_declaration() # add the binding API declaration

	def set_compilation_directives(self, directives): # set the compilation directives
		self.cgo_directives = directives # store the directives

	#* kill a bunch of functions we don't care about
	def set_error(self, type, reason):
		return ""

	def get_self(self, ctx):
		return ""

	def get_var(self, i, ctx):
		return ""

	def open_proxy(self, name, max_arg_count, ctx):
		return ""

	def _proto_call(self, self_conv, proto, expr_eval, ctx, fixed_arg_count=None):
		return ""

	def _bind_proxy(self, name, self_conv, protos, desc, expr_eval, ctx, fixed_arg_count=None):
		return ""

	def close_proxy(self, ctx):
		return ""

	def proxy_call_error(self, msg, ctx):
		return ""

	def return_void_from_c(self):
		return ""

	def rval_from_nullptr(self, out_var):
		return ""

	def rval_from_c_ptr(self, conv, out_var, expr, ownership):
		return ""

	def commit_from_c_vars(self, rvals, ctx="default"):
		return ""

	def rbind_function(self, name, rval, args, internal=False):
		return ""

	# biding API 
	def get_binding_api_declaration(self): # add a struct to store type info
		type_info_name = gen.apply_api_prefix("type_info") # add a function to get the type info from a type tag

		out = '''\
struct %s {
	uint32_t type_tag;
	const char *c_type;
	const char *bound_name;

	bool (*check)(void* p);
	void (*to_c)(void *p, void *out);
	int (*from_c)(void *obj, OwnershipPolicy policy);
};\n
''' % type_info_name
	# add a function to get the type info from a type tag
		out += "// return a type info from its type tag\n" # add a function to get the type info from a type tag
		out += "%s *%s(uint32_t type_tag);\n" % (type_info_name, gen.apply_api_prefix("get_bound_type_info")) # add a function to get the type info from a type tag

		out += "// return a type info from its type name\n" # add a function to get the type info from a type name
		out += "%s *%s(const char *type);\n" % (type_info_name, gen.apply_api_prefix("get_c_type_info")) # add a function to get the type tag from a type name

		out += "// returns the typetag of a userdata object, nullptr if not a Fabgen object\n"
		out += "uint32_t %s(void* p);\n\n" % gen.apply_api_prefix("get_wrapped_object_type_tag")

		return out
	

	def output_binding_api(self): # output the binding API
		type_info_name = gen.apply_api_prefix("type_info") # the type info struct
		self._source += """\
%s *%s(uint32_t type_tag) {
	return nullptr;
}\n\n""" % (
			type_info_name, # the type info struct
			gen.apply_api_prefix("get_bound_type_info"), # get a type info from its type tag
		)
		#* return a type info from its type name
		self._source += """
%s *%s(const char *type) {
	return nullptr;
}\n\n""" % (
			type_info_name, # the type info struct
			gen.apply_api_prefix("get_c_type_info"), # get a type info from its type name
		)
		#* returns the typetag of a userdata object, nullptr if not a Fabgen object
		self._source += """\
uint32_t %s(void* p) {
	return 0;
	//auto o = cast_to_wrapped_Object_safe(L, idx);
	//return o ? o->type_tag : 0;
}\n\n""" % gen.apply_api_prefix("get_wrapped_object_type_tag") # get the type tag of a wrapped object

	#* output the binding api
	def get_output(self): # get the output
		return {"wrapper.cpp": self.go_c, "wrapper.h": self.go_h, "bind.go": self.go_bind, "translate_file.json": self.go_translate_file} # return the output
	# get the type of name
	def _get_type(self, name): # get the type from the name
		for type in self._bound_types: # loop through the bound types
			if type: # if the type exists
				return type # return the type
		return None # return none
	# 
	def _get_conv(self, conv_name): # get the type converter from the name
		if conv_name in self._FABGen__type_convs: # if the type converter is in the type converters
			return self.get_conv(conv_name) # return the type converter
		return None # return none

	def _get_conv_from_bound_name(self, bound_name): # get the type converter from the bound name
		for name, conv in self._FABGen__type_convs.items(): # loop through the type converters
			if conv.bound_name == bound_name: # if the bound name matches
				return conv # return the type converter
		return None # return none

	def __get_is_type_class_or_pointer_with_class(self, conv): # check if the type is a class or a pointer to a class
		if conv.is_type_class() or \
			(isinstance(conv, GoPtrTypeConverter) and self._get_conv(str(conv.ctype.scoped_typename)) is None): # if the type is a class or a pointer to a class
			return True # return true
		return False # return false

	def __get_stars(self, val, start_stars=0, add_start_for_ref=True): # get the stars for a type
		stars = "*" * start_stars # add the start stars
		if "carg" in val and hasattr(val["carg"].ctype, "ref"): # if the type has a carg and a ref
			stars += "*" * (len(val["carg"].ctype.ref) if add_start_for_ref else val["carg"].ctype.ref.count('*')) # add the ref stars
		elif "storage_ctype" in val and hasattr(val["storage_ctype"], "ref"): # if the type has a storage_ctype and a ref
			stars += "*" * (len(val["storage_ctype"].ref) if add_start_for_ref else val["storage_ctype"].ref.count('*')) # add the ref stars
		elif hasattr(val["conv"].ctype, "ref"): # if the type has a hasattr and a ref
			stars += "*" * (len(val["conv"].ctype.ref) if add_start_for_ref else val["conv"].ctype.ref.count('*')) # add the ref stars
		return stars # return the stars

	def __arg_from_cpp_to_c(self, val, retval_name, just_copy): # just_copy is used for return values
		src = "" # source code
		#* type class, not a pointer
		if val['conv'] is not None and val['conv'].is_type_class() and \
			not val['conv'].ctype.is_pointer() and ('storage_ctype' not in val or not hasattr(val['storage_ctype'], 'ref') or not any(s in val['storage_ctype'].ref for s in ["&", "*"])): # not a pointer
				#* special shared ptr
				if 'proxy' in val['conv']._features: # if the type has a proxy
					src += f"	if(!{retval_name})\n" \
						"		return nullptr;\n" # if the return value is null, return null

					src += "	auto " + val['conv']._features['proxy'].wrap("ret", "retPointer") # wrap the return value
				#* special std::future 
				elif val["conv"] is not None and "std::future" in str(val["conv"].ctype): # if the type is a future
					src += f"	auto retPointer = new std::future<int>(std::move({retval_name}));\n" # move the return value
				else: # else
					#* class, not pointer, but static
					if just_copy: # if just copy
						src += f"	auto retPointer = {retval_name};\n" # copy the return value
					else: # else
						src += f"	auto retPointer = new {val['conv'].ctype}({retval_name});\n" # copy the return value
				retval_name = f"({clean_name_with_title(self._name)}{clean_name_with_title(val['conv'].bound_name)})(retPointer)" # set the return value name
		else: # else
			#* special std::string (convert to const char*)
			if val["conv"] is not None and "std::string" in str(val["conv"].ctype): # if the type is a string
				stars = self.__get_stars(val) # get the stars
				if len(stars) > 0:#* rarely use but just in case
					retval_name = f"new const char*(&(*{retval_name}->begin()))" # set the return value name
				else: # else
					retval_name = f"{retval_name}.c_str()" # set the return value name
			else: # else
				retval_name = f"{retval_name}" # set the return value name

		#* cast it
		#* if it's an enum
		if val["conv"].bound_name in self._enums.keys(): # if it's an enum
			enum_conv = self._get_conv_from_bound_name(val['conv'].bound_name) # get enum converter
			if enum_conv is not None and hasattr(enum_conv, "base_type") and enum_conv.base_type is not None: # if it has a base type
				arg_bound_name = str(enum_conv.base_type) # get base type
			else: # if it doesn't have a base type
				arg_bound_name = "int" # set it to int
			retval_name = f"({arg_bound_name}){retval_name}" # cast it
		#* cast it, if it's a const
		elif 'storage_ctype' in val and val["storage_ctype"].const or \
			'carg' in val and val["carg"].ctype.const: #* if it's a const 
			arg_bound_name = self.__get_arg_bound_name_to_c(val) # get bound name
			retval_name = f"({arg_bound_name}){retval_name}" if arg_bound_name is not None else retval_name # cast it

		return src, retval_name # return source and retval_name

		#===========================/\Audrey/\------------\/Salah\/===========================
		# Convert argument of C to C++
	def __arg_from_c_to_cpp(self, val, retval_name, add_star=True):
		src = ""
		# check if there is special slice to convert
		if isinstance(val["conv"], lib.go.stl.GoSliceToStdVectorConverter):
			# special if string or const char*
			
			# check if GoStringConverter is in converted string
			if "GoStringConverter" in str(val["conv"].T_conv): # or \
				# "GoConstCharPtrConverter" in str(val["conv"].T_conv):
				# add in src vector of converted type and add string
				src += f"std::vector<{val['conv'].T_conv.ctype}> {retval_name};\n"\
					f"for(int i_counter_c=0; i_counter_c < {retval_name}ToCSize; ++i_counter_c)\n"\
					f"	{retval_name}.push_back(std::string({retval_name}ToCBuf[i_counter_c]));\n"
			#* slice from class
			# get a type, class or pointer with class it self
			elif self.__get_is_type_class_or_pointer_with_class(val["conv"].T_conv):
				# add in src vector of converted type and add it
				src += f"std::vector<{val['conv'].T_conv.ctype}> {retval_name};\n"\
					f"for(int i_counter_c=0; i_counter_c < {retval_name}ToCSize; ++i_counter_c)\n"\
					f"	{retval_name}.push_back(*(({val['conv'].T_conv.ctype}**){retval_name}ToCBuf)[i_counter_c]);\n"
			else:
				# add in src vector of converted type 
				src += f"std::vector<{val['conv'].T_conv.ctype}> {retval_name}(({val['conv'].T_conv.ctype}*){retval_name}ToCBuf, ({val['conv'].T_conv.ctype}*){retval_name}ToCBuf + {retval_name}ToCSize);\n"

		retval = ""
		#* very special case, std::string &
		# check if GoStringConverter is in converted string and Cargo in argument val and Cargo the attribute of the object and any x 
		if "GoStringConverter" in str(val["conv"]) and \
			"carg" in val and hasattr(val["carg"].ctype, "ref") and any(s in val["carg"].ctype.ref for s in ["&"]) and \
			not val["carg"].ctype.const:
			src += f"std::string {retval_name}_cpp(*{retval_name});\n"
			retval += f"{retval_name}_cpp"
		#* std::function
		
		elif "GoStdFunctionConverter" in str(val["conv"]):
			func_name = val["conv"].base_type.replace("std::function<", "")[:-1]
			first_parenthesis = func_name.find("(")
			retval += f"({func_name[:first_parenthesis]}(*){func_name[first_parenthesis:]}){retval_name}"
		#* classe or pointer on class
		else:
			# get a type, class or pointer with class it self
			if self.__get_is_type_class_or_pointer_with_class(val["conv"]):
				stars = self.__get_stars(val, add_start_for_ref=False)
				#* for type pointer, there is a * in the ctype, so remove one
				if isinstance(val['conv'], GoPtrTypeConverter):
					stars = stars[1:]
				
				#* if it's not a pointer, add a star anyway because we use pointer to use in go
				if (not val["conv"].ctype.is_pointer() and ("carg" not in val or ("carg" in val and not val["carg"].ctype.is_pointer()))):
					stars += "*"
					if add_star:
						retval += "*"

				retval += f"({val['conv'].ctype}{stars}){retval_name}"

			elif "carg" in val and hasattr(val["carg"].ctype, "ref") and any(s in val["carg"].ctype.ref for s in ["&"]) and not val["carg"].ctype.const:
				#* add cast and *
				retval = f"({val['carg'].ctype})(*{retval_name})"
			#* cast, if it's an enum
			elif val["conv"].bound_name in self._enums.keys():
				retval = f"({val['conv'].ctype}){retval_name}"
			else:
				retval = retval_name
			# get src
		return src, retval
		
		# Convert argument of C to Go
	def __arg_from_c_to_go(self, val, retval_name, non_owning=False):
		
		rval_ownership = self._FABGen__ctype_to_ownership_policy(val["conv"].ctype)

		src = ""
		#* check if pointer 
		if ('carg' in val and (val['carg'].ctype.is_pointer() or (hasattr(val['carg'].ctype, 'ref') and any(s in val['carg'].ctype.ref for s in ["&", "*"])))) or \
			('carg' not in val and 'storage_ctype' in val and (val['storage_ctype'].is_pointer() or (hasattr(val['storage_ctype'], 'ref') and any(s in val['storage_ctype'].ref for s in ["&", "*"])))) or \
			('carg' not in val and 'storage_ctype' not in val and (val['conv']._is_pointer or val['conv'].ctype.is_pointer())):
			is_pointer = True
		else:
			is_pointer = False

		#* check if ref 
		if ('carg' in val and (hasattr(val['carg'].ctype, 'ref') and any(s in val['carg'].ctype.ref for s in ["&"]))) or \
			('carg' not in val and 'storage_ctype' in val and ((hasattr(val['storage_ctype'], 'ref') and any(s in val['storage_ctype'].ref for s in ["&"])))):
			is_ref = True
		else:
			is_ref = False

		#* check if need convert from c
		#* if not a pointer
		if not is_pointer:
			if val['conv'].bound_name in self._enums.keys():#* if it's an enum
				retval_name = f"{val['conv'].bound_name}({retval_name})"
			else:
				conversion_ret = val['conv'].from_c_call(retval_name, "", "") 
				if conversion_ret != "":
					retval_name = conversion_ret

				#* if it's a class, not a pointer, only out, create the class special
				if val["conv"].is_type_class():
					retval_boundname = val["conv"].bound_name
					retval_boundname = clean_name_with_title(retval_boundname)

					src += f"	{retval_name}GO := &{retval_boundname}{{h:{retval_name}}}\n"

					#* check if owning to have the right to destroy it
					if rval_ownership != "NonOwning" and not is_ref and not non_owning:
						src += f"	runtime.SetFinalizer({retval_name}GO, func(cleanval *{retval_boundname}) {{\n" \
								f"		C.{clean_name_with_title(self._name)}{retval_boundname}Free(cleanval.h)\n" \
								f"	}})\n"
					retval_name = f"{retval_name}GO"

		#* if pointer or ref
		elif is_pointer:
			#* special const char * and string
			if "GoConstCharPtrConverter" in str(val["conv"]) or \
				"GoStringConverter" in str(val["conv"]):
				stars = self.__get_stars(val)

				retval_name_from_c = "*"*len(stars) + retval_name
				if "GoConstCharPtrConverter" in str(val["conv"]):
					retval_name_from_c = "*"*(len(stars) -1) + retval_name

				conversion_ret = val['conv'].from_c_call(retval_name_from_c, "", "")
				# if it contains a star * pointer
				if len(stars) > 0:
					prefix = "&" * len(stars)
					if "GoConstCharPtrConverter" in str(val["conv"]):
						prefix = "&" * (len(stars)-1)

					src+= f"{retval_name}GO := string({conversion_ret})\n"
					retval_name = prefix + retval_name + "GO"
				else:
					conversion_ret = retval_name

			#* if it's a class, a pointer, only out, create the class special
			elif self.__get_is_type_class_or_pointer_with_class(val["conv"]):
				retval_boundname = val['conv'].bound_name
				retval_boundname = clean_name_with_title(retval_boundname)
				src += f"var {retval_name}GO *{retval_boundname}\n" \
						f"if {retval_name} != nil {{\n" \
						f"	{retval_name}GO = &{retval_boundname}{{h:{retval_name}}}\n"

				#* check if owning to have the right to destroy it
				if rval_ownership != "NonOwning" and not is_ref and not non_owning:
					src += f"	runtime.SetFinalizer({retval_name}GO, func(cleanval *{retval_boundname}) {{\n" \
							f"		C.{clean_name_with_title(self._name)}{retval_boundname}Free(cleanval.h)\n"\
							f"	}})\n"
				src += "}\n"
				retval_name = f"{retval_name}GO"
			else:
				retval_name = f"({self.__get_arg_bound_name_to_go(val)})(unsafe.Pointer({retval_name}))\n"
		 #get a src
		return src, retval_name
			#  Convert argument of Go to C
	def __arg_from_go_to_c(self, val, arg_name):
		def convert_got_to_c(val, arg_name, arg_out_name, start_stars=0):
			stars = self.__get_stars(val, start_stars)
				# if convert values is type class
			if val["conv"].is_type_class():
				c_call = f"{clean_name(arg_out_name).replace('&', '_')} := ({stars}C.{clean_name_with_title(self._name)}{clean_name_with_title(val['conv'].bound_name)})(unsafe.Pointer({clean_name(arg_name)}))\n"
			else:
				#* get base conv (without pointer)
				base_conv = self._get_conv(str(val["conv"].ctype.scoped_typename))
				
				if base_conv is None:
					if isinstance(val["conv"], GoPtrTypeConverter):
						c_call = f"{clean_name(arg_out_name).replace('&', '_')} := ({stars[1:]}C.{clean_name_with_title(self._name)}{clean_name_with_title(val['conv'].bound_name)})(unsafe.Pointer({clean_name(arg_name)}))\n"
					else:
						c_call = f"{clean_name(arg_out_name).replace('&', '_')} := ({stars}{str(val['conv'].bound_name)})(unsafe.Pointer({clean_name(arg_name)}))\n"
				elif hasattr(base_conv, "go_to_c_type") and base_conv.go_to_c_type is not None:
					c_call = f"{clean_name(arg_out_name).replace('&', '_')} := ({stars}{base_conv.go_to_c_type})(unsafe.Pointer({clean_name(arg_name)}))\n"
				else:
					c_call = f"{clean_name(arg_out_name).replace('&', '_')} := ({stars}{base_conv.bound_name})(unsafe.Pointer({clean_name(arg_name)}))\n"
			return c_call
		
		c_call = ""
		#* if it's a pointer on something
		if isinstance(val["conv"], GoPtrTypeConverter):
			base_conv = self._get_conv(str(val["conv"].ctype.scoped_typename))
			if base_conv is None or base_conv.is_type_class():
				c_call = f"{clean_name(arg_name)}ToC := {clean_name(arg_name)}.h\n"
			else:
				c_call = convert_got_to_c(val, arg_name, f"{arg_name}ToC")
		#* if it's a class
		elif val["conv"].is_type_class():
			stars = self.__get_stars(val)
			c_call = f"{clean_name(arg_name)}ToC := {stars[1:]}{clean_name(arg_name)}.h\n"
		#* if it's an enum
		elif val["conv"].bound_name in self._enums.keys():
			enum_conv = self._get_conv_from_bound_name(val["conv"].bound_name)
			#*if it's a ref to an enum
			if len(self.__get_stars(val)) > 0:
				c_call = convert_got_to_c(val, arg_name, f"{arg_name}ToC")
			else:
				if enum_conv is not None and hasattr(enum_conv, "go_to_c_type") and enum_conv.go_to_c_type is not None:
					arg_bound_name = enum_conv.go_to_c_type
				else:
					arg_bound_name = "C.int"
					
				c_call = f"{clean_name(arg_name)}ToC := {arg_bound_name}({clean_name(arg_name)})\n"
		#* special Slice
		elif isinstance(val["conv"], lib.go.stl.GoSliceToStdVectorConverter):
			c_call = ""
			slice_name = clean_name(arg_name)
			#* special if string or const char*
			if "GoConstCharPtrConverter" in str(val["conv"].T_conv) or \
				"GoStringConverter" in str(val["conv"].T_conv):
				c_call += f"var {slice_name}SpecialString []*C.char\n"
				c_call += f"for _, s := range {slice_name} {{\n"
				c_call += f"	{slice_name}SpecialString = append({slice_name}SpecialString, C.CString(s))\n"
				c_call += f"}}\n"
				slice_name = f"{slice_name}SpecialString"

			#* if it's a class, get a list of pointer to c class
			elif self.__get_is_type_class_or_pointer_with_class(val["conv"].T_conv):
				c_call += f"var {slice_name}Pointer  []C.{clean_name_with_title(self._name)}{clean_name_with_title(val['conv'].T_conv.bound_name)}\n"
				c_call += f"for _, s := range {slice_name} {{\n"
				c_call += f"	{slice_name}Pointer = append({slice_name}Pointer, s.h)\n"
				c_call += f"}}\n"
				slice_name = f"{slice_name}Pointer"

			c_call += f"{slice_name}ToC := (*reflect.SliceHeader)(unsafe.Pointer(&{slice_name}))\n"
			c_call += f"{slice_name}ToCSize := C.size_t({slice_name}ToC.Len)\n"

			c_call += convert_got_to_c({"conv": val["conv"].T_conv}, f"{slice_name}ToC.Data", f"{slice_name}ToCBuf", 1)
		#* std function
		# create an std function if GoStdFunctionConverter is in converted string 
		elif "GoStdFunctionConverter" in str(val["conv"]):
			c_call += f"{clean_name(arg_name)}ToC := (C.{clean_name_with_title(self._name)}{clean_name_with_title(val['conv'].bound_name)})({clean_name(arg_name)})\n"
		else:
			how_many_stars = 0
			#* compute how many stars (to handle specifically the const char *)
			if "carg" in val: # is it's a Cargo value
				if hasattr(val["carg"].ctype, "ref") and any(s in val["carg"].ctype.ref for s in ["&", "*"]) and not val["carg"].ctype.const:
					how_many_stars = len(val["carg"].ctype.ref)
				elif val["carg"].ctype.is_pointer():
					# add a star for get a pointer
					how_many_stars = 1
			else:
				if hasattr(val["conv"].ctype, "ref") and any(s in val["conv"].ctype.ref for s in ["&", "*"]) and not val["carg"].ctype.const:
					how_many_stars = len(val["conv"].ctype.ref)
				elif val["conv"].ctype.is_pointer() :
					how_many_stars = 1
			
			is_pointer = True
			# if it don't containe pointer or has a pointer with GoConstCharPtrConverter in converted string
			if how_many_stars == 0 or \
				(how_many_stars == 1 and "GoConstCharPtrConverter" in str(val["conv"])):
				is_pointer = False
			c_call = val["conv"].to_c_call(clean_name(arg_name), f"{clean_name(arg_name)}ToC", is_pointer)
			# C was called and convert in Go
		return c_call
		# get a bounding name argument to Go
	def __get_arg_bound_name_to_go(self, val):
		# if the values is type class
		if val["conv"].is_type_class():
			arg_bound_name = val["conv"].bound_name
		else:
			#* check the convert from the base (in case of ptr) or a string
			if ('carg' in val and (val['carg'].ctype.is_pointer() or (hasattr(val['carg'].ctype, 'ref') and any(s in val['carg'].ctype.ref for s in ["&", "*"])))) or \
				('storage_ctype' in val and (val['storage_ctype'].is_pointer() or (hasattr(val['storage_ctype'], 'ref') and any(s in val['storage_ctype'].ref for s in ["&", "*"])))) or \
				isinstance(val['conv'], GoPtrTypeConverter):
				# get bounding name argument if the values  has Go type 
				if hasattr(val["conv"], "go_type") and val["conv"].go_type is not None:
					arg_bound_name = str(val["conv"].go_type)
				else:
					base_conv = self._get_conv(str(val['conv'].ctype.scoped_typename))
					if base_conv is None:
						arg_bound_name = str(val["conv"].bound_name)
					else:
						# 
						if hasattr(base_conv, "go_type") and base_conv.go_type is not None:
							arg_bound_name = base_conv.go_type
						else:
							arg_bound_name = base_conv.bound_name
			else:
				if val['conv'].bound_name in self._enums.keys():#* if it's an enum
					arg_bound_name = f"{val['conv'].bound_name}"
				elif hasattr(val["conv"], "go_type") and val["conv"].go_type is not None:
					arg_bound_name = val["conv"].go_type
				else:
					arg_bound_name = val["conv"].bound_name

		if arg_bound_name.endswith("_nobind") and val["conv"].nobind:
			arg_bound_name = arg_bound_name[:-len("_nobind")]

		#* if it's a pointer and not a string not a const
		if (('carg' in val and (not val["carg"].ctype.const and(val['carg'].ctype.is_pointer() or (hasattr(val['carg'].ctype, 'ref') and any(s in val['carg'].ctype.ref for s in ["&", "*"]))))) or \
			('storage_ctype' in val and (val['storage_ctype'].is_pointer() or (hasattr(val['storage_ctype'], 'ref') and any(s in val['storage_ctype'].ref for s in ["&", "*"])))) or \
			isinstance(val['conv'], GoPtrTypeConverter)):
			#* find how many * we need to add
			stars = "*"
			if "carg" in val and hasattr(val["carg"].ctype, "ref"):
				stars += "*" * (len(val["carg"].ctype.ref) - 1)
			if "storage_ctype" in val and hasattr(val["storage_ctype"], "ref"):
				stars += "*" * (len(val["storage_ctype"].ref) - 1)

			#* special const char *
			if "GoConstCharPtrConverter" in str(val["conv"]):
				stars = stars[1:]

			#* Harfang class doesn't need to be a pointer in go (because it's a struct containing a wrap pointer C)
			if not self.__get_is_type_class_or_pointer_with_class(val["conv"]):
				arg_bound_name = stars + arg_bound_name

		#* std function
		if "GoStdFunctionConverter" in str(val["conv"]):
			# used std unsafe Pointer function
			arg_bound_name = "unsafe.Pointer"

		#* class or slice, clean the name with title
		if self.__get_is_type_class_or_pointer_with_class(val["conv"]) or \
			isinstance(val['conv'], lib.go.stl.GoSliceToStdVectorConverter):
			arg_bound_name = clean_name_with_title(arg_bound_name)

		#* if it's a class, it's a pointer
		if self.__get_is_type_class_or_pointer_with_class(val["conv"]):
			# add star to make a pointer
			arg_bound_name = "*" + arg_bound_name
			
		return arg_bound_name
			# get bonding name argument to c
	def __get_arg_bound_name_to_c(self, val):
		arg_bound_name = ""
		# bonding name argument

		#* check to add const
		if 'storage_ctype' in val and val["storage_ctype"].const or \
			'carg' in val and val["carg"].ctype.const:
			# add const on argument
			arg_bound_name += "const "
		
		#* if class or pointer with class
		if self.__get_is_type_class_or_pointer_with_class(val["conv"]) or \
			"GoStdFunctionConverter" in str(val["conv"]):
			# clear the name and the converted value
			arg_bound_name += f"{clean_name_with_title(self._name)}{clean_name_with_title(val['conv'].bound_name)} "
		else:
			#* check the convert from the base (in case of ptr)
			if  ('carg' in val and (val['carg'].ctype.is_pointer() or (hasattr(val['carg'].ctype, 'ref') and any(s in val['carg'].ctype.ref for s in ["&", "*"])))) or \
				('storage_ctype' in val and (val['storage_ctype'].is_pointer() or (hasattr(val['storage_ctype'], 'ref') and any(s in val['storage_ctype'].ref for s in ["&", "*"])))) or \
				isinstance(val['conv'], GoPtrTypeConverter):
				#* check if it's an enum
				if val['conv'].bound_name in self._enums.keys():
					# converted enum for bounding name
					enum_conv = self._get_conv_from_bound_name(val['conv'].bound_name)
						# if enum don't contain any base type 
					if enum_conv is not None and hasattr(enum_conv, "base_type") and enum_conv.base_type is not None:
						# get base type of enum
						arg_bound_name = str(enum_conv.base_type)
					else:
						# get int on the argument
						arg_bound_name = "int"
				else:
					#* sometimes typedef is weird and don't give valid value, so check it
					base_conv = self._get_conv(str(val['conv'].bound_name))
					if base_conv is None:
						#* check with typedef
						if hasattr(val['conv'], "base_type") and val['conv'].base_type is not None:
							# get bas type on converted value
							arg_bound_name = str(val['conv'].base_type)
						else:
							# storage ctype is in the value
							if 'storage_ctype' in val:
								# add storage ctype
								arg_bound_name += f"{val['storage_ctype']} "
							else:
								# add converted type
								arg_bound_name += f"{val['conv'].ctype} "
					
						#* if it's a ptr type, remove a star
						if isinstance(val['conv'], GoPtrTypeConverter):
							# renplace * and & by empty slot (regular type)
							arg_bound_name = arg_bound_name.replace("*", "").replace("&", "")
					else:
         					# add converted type
						arg_bound_name += f"{val['conv'].bound_name} "

				#* add a star (only if it's not a const char * SPECIAL CASE)
				if "GoConstCharPtrConverter" not in str(val["conv"]) and ("carg" not in val or not val["carg"].ctype.const):
					arg_bound_name += "*"
					# cargo value contain a reference and don't contain any const values
				if "carg" in val and hasattr(val["carg"].ctype, "ref") and not val["carg"].ctype.const:
					# add star to get pointer
					arg_bound_name += "*" * (len(val["carg"].ctype.ref) - 1)
					# storage ctype contain a reference
				if "storage_ctype" in val and hasattr(val["storage_ctype"], "ref"):
					# add star to get pointer
					arg_bound_name += "*" * (len(val["storage_ctype"].ref) - 1)
			else:
				#* check if it's an enum
				if val['conv'].bound_name in self._enums.keys():
					# get converted value for enum conversion
					enum_conv = self._get_conv_from_bound_name(val['conv'].bound_name)
					# if enum don't contain any base type 
					if enum_conv is not None and hasattr(enum_conv, "base_type") and enum_conv.base_type is not None:
							# get base type of enum
						arg_bound_name = str(enum_conv.base_type)
					else:
						# get int on the argument
						arg_bound_name = "int"
				else:
					#* sometimes typedef is weird and don't give valid value, so check it
					base_conv = self._get_conv(str(val['conv'].bound_name))
						# untype converted
					if base_conv is None:
						# converted value has a type
						if hasattr(val['conv'], "base_type") and val['conv'].base_type is not None:
							 # get converted base type on argument
							arg_bound_name = str(val['conv'].base_type)
						else:
							# value has storage ctype
							if 'storage_ctype' in val:
								# add storage ctype on argument
								arg_bound_name += f"{val['storage_ctype']} "
							else:
								# add converted type on argument
								arg_bound_name += f"{val['conv'].ctype} "
					else:
							# add converted bounding name on argument
						arg_bound_name += f"{val['conv'].bound_name} "
			# get bounding name argument
		return arg_bound_name

	def __extract_sequence_go(self, conv):
		go = ""

		classname = clean_name_with_title(conv.bound_name)

		internal_conv = conv._features["sequence"].wrapped_conv

		arg_bound_name = self.__get_arg_bound_name_to_go({"conv": internal_conv})

		#* GET
		go += f"// Get ...\n" \
				f"func (pointer *{classname}) Get(id int) {arg_bound_name} {{\n"
		go += f"v := C.{clean_name_with_title(self._name)}{classname}GetOperator(pointer.h, C.int(id))\n"

		src, retval_go = self.__arg_from_c_to_go({"conv": internal_conv}, "v")
		go += src
		go += f"return {retval_go}\n"
		go += "}\n"

		#* SET
		go += f"// Set ...\n" \
				f"func (pointer *{classname}) Set(id int, v {arg_bound_name}) {{\n"
		#* convert to c
		c_call = self.__arg_from_go_to_c({"conv": internal_conv}, "v")
		if c_call != "":
			go += c_call
		else:
			go += "vToC := v\n"

		go += f"	C.{clean_name_with_title(self._name)}{classname}SetOperator(pointer.h, C.int(id), vToC)\n"
		go += "}\n"

		#* Len
		go += f"// Len ...\n" \
				f"func (pointer *{classname}) Len() int32 {{\n"
		go += f"return int32(C.{clean_name_with_title(self._name)}{classname}LenOperator(pointer.h))\n"
		go += "}\n"

		return go

		#===========================/\Salah/\------------\/Florent\/===========================

	# this function is used to get the sequence in GO and convert it to C (not sure actually)
	def __extract_sequence(self, conv, is_in_header=False): 
		go = ""

		cleanClassname = clean_name_with_title(conv.bound_name)

		# This function get the go sequence from the parameter of the function
		internal_conv = conv._features["sequence"].wrapped_conv

		#* special std::string (convert to const char*)
		arg_bound_name = self.__get_arg_bound_name_to_c({"conv": internal_conv})
		c_arg_bound_name = arg_bound_name.replace("std::string", "const char*")
		c_arg_bound_name = c_arg_bound_name.replace("const const", "const")

		#* GET
		# We are checking if we are in the header of the file If it is, 
		# it appends the string "extern" to the variable "go", 
		# then it appends the string "c_arg_bound_name" followed by the cleaned name of the class and the "GetOperator" method with the class instance and an integer variable "id" as its arguments. 
		# Finally, it appends a newline character to "go".
		if is_in_header:
			go += "extern "
			go += f"{c_arg_bound_name} {clean_name_with_title(self._name)}{cleanClassname}GetOperator({clean_name_with_title(self._name)}{cleanClassname} h, int id)"
			go += ";\n"
		else:
		# This code is appending a block of code to the "go" variable. 
		# The block of code is a function that gets an item of a sequence using the "get_item" method of the "sequence" feature, 
		# passing the class instance, the "id" integer variable, the "v" variable and a boolean "error" variable. 
		# Then it converts the value from C++ to C using the "arg_from_cpp_to_c" method and returns the value
			go += f"{{\n" \
				"	bool error;\n" \
				f"	{internal_conv.ctype} v;\n	"
			go += conv._features['sequence'].get_item(f"(({conv.ctype}*)h)", "id", "v", "error")

			src, retval_c = self.__arg_from_cpp_to_c({"conv": internal_conv}, "v", False)
			go += src
			go += f"	return {retval_c};\n}}\n"

		#* SET
		# This code is appending a C function declaration to the "go" variable. 
		# The function is called "SetOperator" and takes 3 arguments: the class instance "h", an integer "id" and a variable "v" of type "c_arg_bound_name". 
		# The function is prefixed with "extern" keyword, indicating that the function is implemented in another file, 
		# The function is also declared as "void" meaning it doesn't return any value
		if is_in_header:
			go += "extern "
			go += f"void {clean_name_with_title(self._name)}{cleanClassname}SetOperator({clean_name_with_title(self._name)}{cleanClassname} h, int id, {c_arg_bound_name} v)"
			go += ";\n"
		else:
		# This part of the code is a function that sets an item of a sequence using the "set_item" method of the "sequence" feature,
		# passing the class instance, the "id" integer variable, and a variable "inval" which is the converted value of v from C to C++.
		# It also uses a boolean variable "error" to check for any errors.
		# Then it converts the value from C to C++ using the "arg_from_c_to_cpp" method
			go += f"{{\n" \
				"	bool error;\n"

			src, inval = self.__arg_from_c_to_cpp({"conv": internal_conv}, "v", False)
			go += src

			go += conv._features['sequence'].set_item(f"(({conv.ctype}*)h)", "id", inval, "error")
			go += f"\n}}\n"

		#* LEN
		# First, it appends the string "extern" to the variable "go", 
		# then it appends the string "int" followed by the cleaned name of the class and the "LenOperator" method with the class instance as its argument
		if is_in_header:
			go += "extern "
			go += f"int {clean_name_with_title(self._name)}{cleanClassname}LenOperator({clean_name_with_title(self._name)}{cleanClassname} h)"
			go += ";\n"
		else:
		# it's a function that gets the size of a sequence using the "get_size" method of the "sequence" feature, 
		# passing the class instance and a integer variable "size". 
		# The function declares a variable named size and then calls the "get_size" method passing the class instance and the variable "size" as argument. 
		# Then it return the value of size which is the size of the sequence
			go += f"{{\n" \
				"	int size;\n	"
			go += conv._features['sequence'].get_size(f"(({conv.ctype}*)h)", "size")
			go += f"	return size;\n}}\n"

		return go
	# This function extract go code for getting and setting a member of a class with a specific name, 
	# conversion type and optional static, global and implicit cast options, and return it as a string
	def __extract_get_set_member_go(self, classname, member, static=False, name=None, bound_name=None, is_global=False, implicit_cast=None):
		go = ""
		# Select the type of converter, here we have a ctype converter
		conv = self.select_ctype_conv(member["ctype"])
		# We are checking if bound_name is in member
		if "bound_name" in member:
		# If he is in member, we take it and stringify it into the bound_name variable
			bound_name = str(member["bound_name"])
		elif bound_name is None:
		# If there are no bound_name in member, we stringify the name instead into the bound_name variable
			bound_name = str(member["name"])
		# We also check if there is a name link to it, if not we put the bound_name 
		if name is None:
			name = bound_name
		# We are cleaning the name 
		name = name.replace(":", "")
		name = clean_name_with_title(name)
		# it's calling a private method __get_arg_bound_name_to_go which takes a dictionary as an argument that contains key "conv" and its value is the variable conv.
		# It will return a C type name 
		arg_bound_name = self.__get_arg_bound_name_to_go({"conv": conv})

		# This function is checking if the member is global and its C type is constant, 
		# then it appends a string to the "go" variable with the name of the member 
		# and the appropriate conversion of the member to Go using the C function that get the member. 
		# If it's not global it will create a Go function that will call the C function that gets the member and convert the returned value to Go and returns it.
		def create_get_set(do_static):
			#* GET
			go = ""

			#* if it's a const, just write it once
			# This code is checking if the variable "is_global" is true and if the "ctype" property of the member variable is set to "const". 
			# If both conditions are true,it appends a comment line to the "go" variable with the name of the member variable.
			if is_global and member["ctype"].const:
				go += f"// {name} ...\n"
				# Then it checks if the type of the member is a class or pointer to a class using the private method __get_is_type_class_or_pointer_with_class.
				# If it is, it appends a variable declaration to the "go" variable,
				# the variable is named with the cleaned name of the member variable, 
				# and it is assigned the result of calling a C function to get the member and it is passed the classname and the member name, and it is casted to the appropriate Go type.
				if self.__get_is_type_class_or_pointer_with_class(conv):
					go += f"var {clean_name(name)} = {arg_bound_name.replace('*', '')}{{h:C.{clean_name_with_title(self._name)}{clean_name_with_title(classname)}Get{name}()}}\n"
				# If the implicit_cast variable is not None, it appends a variable declaration to the "go" variable, 
				# the variable is named with the cleaned name of the member variable, 
				# and it is assigned the result of calling a C function to get the member and it is passed the classname and the member name, 
				# and it is casted to the implicit_cast variable.
				elif implicit_cast is not None:
					go += f"var {clean_name(name)} = {implicit_cast}(C.{clean_name_with_title(self._name)}{clean_name_with_title(classname)}Get{name}())\n"
				else:
				#If the type is not a class or pointer to a class and implicit_cast variable is None, 
				# it appends a variable declaration to the "go" variable, 
				# the variable is named with the cleaned name of the member variable, 
				# and it is assigned the result of calling a C function to get the member and it is passed the classname and the member name,
				# and it is casted to the appropriate Go type.
					go += f"var {clean_name(name)} = {arg_bound_name}(C.{clean_name_with_title(self._name)}{clean_name_with_title(classname)}Get{name}())\n"
			else:
				go += "// "
				# If the "do_static" variable is true, the function is declared as a static function of the class, 
				# otherwise it takes a pointer to an instance of the class as its argument.
				#  The function returns the member variable in the appropriate Go type.
				if do_static:
					go += f"{clean_name_with_title(classname)}"
				go += f"Get{name} ...\n"
				go += f"func "
				if do_static:
					go += f"{clean_name_with_title(classname)}"
				else:
					go += f"(pointer *{clean_name_with_title(classname)}) "

				go += f"Get{name}() {arg_bound_name} {{\n"
				go += f"v := C.{clean_name_with_title(self._name)}{clean_name_with_title(classname)}Get{name}("
				if not static and not is_global:
					go += "pointer.h"
				go += ")\n"

				#* check if need convert from c
				# The body of the function calls the corresponding C function to get the member,
				# passing the class instance if the function is not static and not global. 
				# The returned value is stored in a variable "v" 
				# and it is then converted from C to Go using the private method __arg_from_c_to_go.
				src, retval_go = self.__arg_from_c_to_go({"conv": conv}, "v", True)
				go += src
				go += f"return {retval_go}\n"

				go += "}\n"

			#* SET
			#* add set only if the member is not const
			# This code is checking if the member is not constant, it appends a comment line to the "go" variable with the name of the member variable, 
			# followed by a Go function declaration. The function is named "Set" followed by the name of the member variable.
			if not member["ctype"].const:
				go += f"// "
				if do_static:
					go += f"{clean_name_with_title(classname)}"
				go += f"Set{name} ...\n" \
						f"func "
				# If the "do_static" variable is true, the function is declared as a static function of the class, 
				# otherwise it takes a pointer to an instance of the class as its argument 
				# and also takes a variable "v" of type arg_bound_name as parameter
				if do_static:
					go += f"{clean_name_with_title(classname)}"
				else:
					go += f"(pointer *{clean_name_with_title(classname)}) "

				go += f"Set{name}(v {arg_bound_name}) {{\n"

				#* convert to c
				# This code is converting the "v" variable from Go to C type using the private method __arg_from_go_to_c 
				# and passing the conversion type and the variable "v" as arguments.
				c_call = self.__arg_from_go_to_c({"conv": conv}, "v")
				# If the returned value of __arg_from_go_to_c is not an empty string, 
				# it appends the returned value to the "go" variable as it is the code for the conversion.
				if c_call != "":
					go += c_call
				# Otherwise, it declares a new variable "vToC" and assigns "v" to it. 
				# Then it appends a call to the C function that sets the member,
				#  passing the class instance and the "vToC" variable as arguments.
				#  Finally, it appends a closing curly brace to the "go" variable, and the function returns the "go" variable.
				else:
					go += "vToC := v\n"
				go += f"	C.{clean_name_with_title(self._name)}{clean_name_with_title(classname)}Set{name}("
				if not static and not is_global:
					go += "pointer.h, "
				go += "vToC)\n"
				go += "}\n"
			return go

		#* create twice, with and without static, to use it with the class and standalone
		if not is_global:
			go += create_get_set(False)
		if static or is_global:
			go += create_get_set(True)

		return go

	def __extract_get_set_member(self, classname, convClass, member, static=False, name=None, bound_name=None, is_global=False, is_in_header=False):
		go = ""
		# Select the type of converter, here we have a ctype converter
		conv = self.select_ctype_conv(member["ctype"])

		# If he is in member, we take it and stringify it into the bound_name variable
		if "bound_name" in member:
			bound_name = str(member["bound_name"])
		# If there are no bound_name in member, we stringify the name instead into the bound_name variable
		elif bound_name is None:
			bound_name = str(member["name"])
		# We also check if there is a name link to it, if not we put the bound_name 
		if name is None:
			name = bound_name
			
		# We are cleaning the name 
		name = clean_name_with_title(name)

		c_name = str(member["name"])

		cleanClassname = clean_name_with_title(classname)

		#* special Slice
		if isinstance(conv, lib.go.stl.GoSliceToStdVectorConverter):
			arg_bound_name = self.__get_arg_bound_name_to_c({"conv": conv.T_conv})
		else:
			arg_bound_name = self.__get_arg_bound_name_to_c({"conv": conv})
		
		#* special std::string (convert to const char*)
		c_arg_bound_name = arg_bound_name.replace("std::string", "const char*")
		c_arg_bound_name = c_arg_bound_name.replace("const const", "const")

		#* GET
		# This code is checking if the "is_in_header" variable is true, and if it is, 
		# it appends the text "extern " to the "go" variable.
		if is_in_header:
			go += "extern "
		# Then it appends a C function declaration to the "go" variable. The function is named with the cleaned name of the class,
		# followed by "Get" and the cleaned name of the member variable, and returns the member variable in the appropriate C type.
		go += f"{c_arg_bound_name} {clean_name_with_title(self._name)}{cleanClassname}Get{name.replace(':', '')}("
		# If the "static" variable is not true and the "is_global" variable is not true,
		# it takes as argument a variable "h" of type "clean_name_with_title(self._name) + cleanClassname" representing the class instance 
		# we add this into the go variable
		if not static and not is_global:
			go += f"{clean_name_with_title(self._name)}{cleanClassname} h"
		go += ")"
		
		# This code is checking if the "is_in_header" variable is true, and if it is,
		# it appends the text ";\n" to the "go" variable
		if is_in_header:
			go += ";\n"
		else:
		# Otherwise, it appends an opening curly brace to the "go" variable
			go += "{"
			#* check if the value is a ref
			# It then declares a variable "prefix" and assigns an empty string to it, 
			# which will be used to prefix the return statement with the appropriate reference operator.
			prefix = ""
			# It checks if the value is a reference or a class type and assigns the appropriate reference operator to the prefix variable.
			if (hasattr(conv.ctype, "ref") and conv.ctype.ref in ["&", "*&"]) or \
				conv.is_type_class():
				prefix = "&"
			# It then checks if the "static" variable or the "is_global" variable is true, and if it is, 
			# it appends a line to the "go" variable to retrieve the value of the member variable using the "prefix" variable,
			# the class name and the member variable name.
			if static or is_global:
				if convClass is not None:
					go += f"	auto ret = {prefix}{convClass.ctype}::{c_name};\n"
				else:
					go += f"	auto ret = {prefix}{classname}::{c_name};\n"
			else:
				# Otherwise, it checks if the class has a "proxy" feature and if it does, 
				# it performs a type cast and retrieves the value of the member variable using the "prefix" variable, 
				# the class name and the member variable name.
				if convClass is not None and "proxy" in convClass._features:
					go += f"\n	auto v = _type_tag_cast(h, {convClass.type_tag}, {convClass._features['proxy'].wrapped_conv.type_tag});\n"
					go += f"	auto ret = {prefix}(({convClass._features['proxy'].wrapped_conv.ctype}*)v)->{c_name};\n"
				# Otherwise, it retrieves the value of the member variable using the "prefix" variable, the class name and the member variable name.
				else:
					go += f"	auto ret = {prefix}(({convClass.ctype}*)h)->{c_name};\n"
			# It then converts the value from C++ to C using the private method __arg_from_cpp_to_c and passing the conversion type and the variable "ret" as arguments. 
			# And it appends the returned value to the "go" variable as the code for the conversion
			src, retval_c = self.__arg_from_cpp_to_c({"conv": conv}, "ret", True)
			go += src
			go += f"return {retval_c};\n}}\n"

		#* SET
		#* add set only if the member is not const
		# We check that member is a constant and conv is non copyable
		if not(member["ctype"].const or conv._non_copyable):
			# We append "extern" to the go variable
			if is_in_header:
				go += "extern "
			# We are cleanning the name and putting it in the go variable
			go += f"void {clean_name_with_title(self._name)}{cleanClassname}Set{name.replace(':', '')}("
			# We check that it's neither static or global 
			if not static and not is_global:
				# We add the name to the go variable
				go += f"{clean_name_with_title(self._name)}{cleanClassname} h, "
			go += f"{c_arg_bound_name} v)"

			if is_in_header:
				go += ";\n"
			else:
				# It then converts the value from C++ to C using the private method __arg_from_cpp_to_c and passing the conversion type and the variable "ret" as arguments. 
				# And it appends the returned value to the "go" variable as the code for the conversion
				src, inval = self.__arg_from_c_to_cpp({"conv": conv}, "v")
				go += src

				#f the variable is a static variable or is a global variable, 
				# the function sets the value of the variable directly
				if static or is_global:
					if convClass is not None:
						go += f"{{ {convClass.ctype}::{c_name} = {inval};\n}}\n"
					else:
						go += f"{{ {classname}::{c_name} = {inval};\n}}\n"
				else:
					# If the variable is not static or global, it sets the value of the variable via the class instance passed in as a parameter. If the class has a "proxy" feature,
					# it uses the _type_tag_cast method to convert the instance to the correct type before setting the value of the variable.
					if convClass is not None and "proxy" in convClass._features:
						go += f"{{\n	auto w = _type_tag_cast(h, {convClass.type_tag}, {convClass._features['proxy'].wrapped_conv.type_tag});\n"
						go += f"	(({convClass._features['proxy'].wrapped_conv.bound_name}*)w)->{c_name} = {inval};\n}}\n"
					else:
						go += f"{{ (({convClass.ctype}*)h)->{c_name} = {inval};}}\n"
		return go

	def __extract_method_go(self, classname, convClass, method, static=False, name=None, bound_name=None, is_global=False, is_constructor=False):
		go = ""
		# If the value of bound_name is None, we apply the method bound_name to it
		if bound_name is None:
			bound_name = method["bound_name"]
		# If there are no name , we take the bound_name as a name
		if name is None:
			name = bound_name
		#! this function is useless
		if bound_name == "OpenVRStateToViewState":
			bound_name = bound_name

		name_go = name
		# We check if there is a constructor
		if is_constructor:
			# we add "new_" to the name
			name_go = "new_" + name_go
		# Don't get this line ?
		uid = classname + bound_name if classname else bound_name

		protos = self._build_protos(method["protos"])
		for id_proto, proto in enumerate(protos):
			retval = ""

			if proto["rval"]["conv"]:
				retval = proto["rval"]["conv"].bound_name

			go += "// " + clean_name_with_title(name_go)
			#* add bounding_name to the overload function
			if "bound_name" in proto["features"]:
				go += proto["features"]["bound_name"]
			#* if automatic suffix generated
			elif "suggested_suffix" in proto:
				go += proto["suggested_suffix"]

			#* get doc
			# if classname is empty and there are a constructor
			if classname == "" or is_constructor:
				# We add the symbol bound_name to doc
				doc = self.get_symbol_doc(bound_name)
			else:
				# else we the symbol classname + bound_name 
				doc = self.get_symbol_doc(classname + "_" + bound_name)

			if doc == "":
				go += " ...\n"
			else:
				# The re.sub() function is used to perform a search-and-replace operation on a string, 
				# replacing all occurrences of a specified pattern with a specified replacement string. 
				# In this case, the pattern being searched for is "(\[)(.*?)(\])", and the replacement string is "\1harfang.\2\3". 
				go += " " + re.sub(r'(\[)(.*?)(\])', r'\1harfang.\2\3', doc) + "\n"

			go += "func "
			# If the function is not global
			if not is_global:
				# We add a pointer representing the name classname to the go variable
				go += f"(pointer *{clean_name_with_title(classname)}) "
			go += f"{clean_name_with_title(name_go)}"

			#* add bounding_name to the overload function
			if "bound_name" in proto["features"]:
				go += proto["features"]["bound_name"]
			#* if automatic suffix generated
			elif "suggested_suffix" in proto:
				go += proto["suggested_suffix"]

			#* add input(s) declaration
			go += "("
			if len(proto["args"]):
				has_previous_arg = False
				for argin in proto["argsin"]:
					if has_previous_arg:
						go += " ,"

					#* check if the input is in feature constant group, overrite the type
					if "features" in proto and "constants_group" in proto["features"] and str(argin["carg"].name) in proto["features"]["constants_group"]:
						go += f"{clean_name(argin['carg'].name)} {proto['features']['constants_group'][str(argin['carg'].name)]}"
					else:
						go += f"{clean_name(argin['carg'].name)} {self.__get_arg_bound_name_to_go(argin)}"
					has_previous_arg = True

			go += ")"

			#* add output(s) declaration
			go += "("
			has_previous_ret_arg = False
			if proto["rval"]["conv"]:
				go += self.__get_arg_bound_name_to_go(proto["rval"])
				has_previous_ret_arg = True
			
			#* only add arg output, NOT ARG IN OUT (pass them by pointer, not return them)
			if len(proto['args']):
				for arg in proto['args']:
					if 'arg_out' in proto['features'] and str(arg['carg'].name) in proto['features']['arg_out']:
						if has_previous_ret_arg:
							go += " ,"

						go += self.__get_arg_bound_name_to_go(arg)
						has_previous_ret_arg = True
			go += ")"

			#* begin function declaration
			go += "{\n"

			#* convert arg in to c
			if len(proto["args"]):
				for arg in proto["args"]:
					#* if arg out only, declare this value
					if "arg_out" in proto["features"] and str(arg["carg"].name) in proto["features"]["arg_out"]:
						arg_bound_name = self.__get_arg_bound_name_to_go(arg)

						if arg["carg"].ctype.is_pointer() or (hasattr(arg["carg"].ctype, "ref") and arg["carg"].ctype.ref == "&"):
							#* if it's a arg out and a class
							if self.__get_is_type_class_or_pointer_with_class(arg["conv"]):
								arg_bound_name = clean_name_with_title(f"new_{arg_bound_name.replace('*', '')}")
								#* find the constructor without arg
								for arg_conv in self._bound_types:
									if str(arg_conv.ctype) == str(arg["conv"].ctype) and hasattr(arg_conv, "constructor") and arg_conv.constructor is not None:
										proto_args = self._build_protos(arg_conv.constructor["protos"])
										break
								else:
									proto_args = None
								
								id_proto_without_arg = ""
								if proto_args is not None and len(proto_args) > 1:
									for id_proto_arg, proto_arg in enumerate(proto_args):
										if len(proto_arg['args']) <= 0:
											#* add bounding_name to the overload function
											if "bound_name" in proto_arg["features"]:
												id_proto_without_arg = proto_arg["features"]["bound_name"]
											#* if automatic suffix generated
											elif "suggested_suffix" in proto_arg:
												id_proto_without_arg = proto_arg["suggested_suffix"]
											break

								go += f"{clean_name(arg['carg'].name)} := {arg_bound_name}{id_proto_without_arg}()\n"
							else:
								#* not a class, remove the * and make a new
								go += f"{clean_name(arg['carg'].name)} := new({arg_bound_name.replace('*', '')})\n"
						else:
							go += f"var {clean_name(arg['carg'].name)} {arg_bound_name}\n"

					c_call = ""
					# checking the value of the 'conv' key in the arg dictionary and adding some text to the variable 'go' based on that value.
					if arg["conv"]:
						c_call = self.__arg_from_go_to_c(arg, arg['carg'].name)
					# The function then return some value which is stored in c_call variable. Then it checks if c_call is not an empty string,
					# if true it appends the c_call to the go variable.
					if c_call != "":
						go += c_call
					else:
						go += f"{clean_name(arg['carg'].name)}ToC := {clean_name(arg['carg'].name)}\n"
						
		#===========================/\Florent/\------------\/Alexandre\/===========================
			
			#* declare arg out
			if retval != "": # if there is a return value
				go += "retval := " # declare the return value

			if is_constructor: # if it's a constructor
				go += f"C.{clean_name_with_title(self._name)}Constructor{clean_name_with_title(name)}" # call the constructor
			else: # if it's a function
				go += f"C.{clean_name_with_title(self._name)}{clean_name_with_title(name)}" # call the function

			#* Is global, add the Name of the class to be sure to avoid double name function name
			if not is_global: # if it's not a global function
				go += f"{clean_name_with_title(convClass.bound_name)}" # add the name of the class

			#* Add bounding_name to the overload function
			if "bound_name" in proto["features"]: # if there is a bounding name
				go += proto["features"]["bound_name"] # add the bounding name
			#* If automatic suffix generated
			elif "suggested_suffix" in proto: # if there is a suggested suffix
				go += proto["suggested_suffix"] # add the suggested suffix

			go += "(" # open the parenthesis
			#* check if the function is global or constructor
			if not is_global and not is_constructor: # if it's not a global function and not a constructor
				#* if not, add the pointer to the C struct as the first argument
				go += "pointer.h, " # add the pointer to the C struct as the first argument

			if len(proto["args"]): # if there is at least one argument
				has_previous_arg = False # set the previous argument to false
				for arg in proto["args"]: # for each argument
					if has_previous_arg: # if there is a previous argument
						go += " ," # add a comma after the previous argument

					# special case for Slice
					if isinstance(arg["conv"], lib.go.stl.GoSliceToStdVectorConverter): # if it's a slice
						slice_name = clean_name(arg['carg'].name) # get the name of the slice
						if "GoConstCharPtrConverter" in str(arg["conv"].T_conv) or \
							"GoStringConverter" in str(arg["conv"].T_conv):	# if it's a string
							slice_name = f"{slice_name}SpecialString" # add special string to the name of the slice
						#* if it's a class, get a list of pointer to c class
						elif self.__get_is_type_class_or_pointer_with_class(arg["conv"].T_conv): # if it's a class
							slice_name = f"{slice_name}Pointer" # add pointer to the name of the slice
						go += f"{slice_name}ToCSize, {slice_name}ToCBuf" # add the size and the buffer of the slice
					else:
						# if (arg['carg'].ctype.is_pointer() or (hasattr(arg['carg'].ctype, 'ref') and arg['carg'].ctype.ref == "&")) and \
						# 	arg['conv'].bound_name != "string" and not arg['conv'].is_type_class():
						# 	go += "&"
						go += f"{clean_name(arg['carg'].name)}ToC" # add the name of the argument

					has_previous_arg = True # set the previous argument to true
			go += ")\n" # close the parenthesis
			ret_args = [] # create a list of return arguments
			if retval != "": # if there is a return value
				src, retval_go = self.__arg_from_c_to_go(proto["rval"], "retval") # convert the C return value to a Go return value
				go += src # add the source code to convert the C return value to a Go return value
				
				ret_args.append(retval_go) # Add the Go return value to the list of return arguments

			#* return arg out
			#* only add arg output, NOT ARG IN OUT (pass them by pointer, not return them)
			if "arg_out" in proto["features"]: # if there is a list of arg out
				for arg in proto['args']: # for each argument
					# check if arg is flagged as arg_out in the feature
					if 'arg_out' in proto['features'] and str(arg['carg'].name) in proto['features']['arg_out']: # if it's an arg out
						# add name
						retval_go = clean_name(str(arg["carg"].name)) # get the name of the argument
						#* if it's a arg out and a class, don't convert because it was already done upper
						if not self.__get_is_type_class_or_pointer_with_class(arg["conv"]): # if it's not a class
							retval_go = clean_name(str(arg["carg"].name)) + "ToC" # get the name of the argument
							src, retval_go = self.__arg_from_c_to_go(arg, retval_go) # convert the C return value to a Go return value
							go += src # add the source code to convert the C return value to a Go return value
							
						ret_args.append(retval_go) # Add the Go return value to the list of return arguments

			if len(ret_args) > 0: # Check if there are return arguments
				go += "return " # Add the return keyword
			has_previous_arg = False # Flag to check whether a return argument has been added before
			for retarg in ret_args: # Loop through the return arguments
				if has_previous_arg: # Check if a return argument has been added before
					# Check and remove "\n" just in case
					if go[-1] == "\n": # Check if the last character is a newline
						go = go[:-1] # Remove the last newline
					go += ", " # Separate the return arguments with commas
				has_previous_arg = True # Set the flag to True
				go += retarg # Add the return argument
				
			# Check and remove "\n" just in case
			if go[-1] == "\n": # Check if the last character is a newline
				go = go[:-1] # Remove the last newline
			go += "\n}\n" # Close the function definition
			# Check if the last character is a newline and remove it if so
			# Close the function definition

		return go

	def __extract_method(self, classname, convClass, method, static=False, name=None, bound_name=None, is_global=False, is_in_header=False, is_constructor=False, overload_op=None): # Extract a method
		go = "" # The Go code

		if bound_name is None: # Check if a bound name is specified
			bound_name = method["bound_name"] # If no bound name is specified, use the bound name from the method
		if name is None: # Check if a name is specified
			name = bound_name # If no name is specified, use the bound name
		wrap_name = bound_name # The name of the wrapper function

		cpp_function_name = name # The name of the C++ function
		if "name" in method: # Check if the method has a name
			cpp_function_name = method["name"] # If the method has a name, use that instead

		uid = classname + bound_name if classname else bound_name # The unique ID of the method

		protos = self._build_protos(method["protos"]) # Build the prototypes
		for id_proto, proto in enumerate(protos): # Iterate over the prototypes
			retval = "void" # The return value of the function

			if str(proto["rval"]["storage_ctype"]) != "void": # Check if the return value is not void
				retval = self.__get_arg_bound_name_to_c(proto["rval"]) # Get the return value

				#* special std::string (convert to const char*)
				retval = retval.replace("std::string", "const char*") # Replace std::string with const char*
				retval = retval.replace("const const", "const") # Replace const const with const

			if is_in_header: # Check if the method is in the header
				go += "extern " # Add the extern keyword
			go += f"{retval} {clean_name_with_title(self._name)}{clean_name_with_title(wrap_name)}" # Add the return value and the name of the wrapper function

			#* not global, add the Name of the class to be sure to avoid double name function name
			if not is_global or (not is_constructor and is_global and convClass is not None): # Check if the method is not global
				go += f"{clean_name_with_title(convClass.bound_name)}" # Add the name of the class

			#* add bounding_name to the overload function
			if "bound_name" in proto["features"]: # Check if the prototype has a bound name
				go += proto["features"]["bound_name"] # Add the bound name
			#* if automatic suffix generated
			elif "suggested_suffix" in proto: # Check if the prototype has a suggested suffix
				go += proto["suggested_suffix"] # Add the suggested suffix

			go += "(" # Open the function definition

			has_previous_arg = False # Flag to check whether an argument has been added before
			#* not global, member class, include the "this" pointer first
			if not is_global or (not is_constructor and is_global and convClass is not None): # Check if the method is not global
				has_previous_arg = True # Set the flag to True
				go += f"{clean_name_with_title(self._name)}{clean_name_with_title(convClass.bound_name)} this_" # Add the "this" pointer

			if len(proto["args"]): # Check if there are arguments
				for argin in proto["args"]: # Iterate over the arguments
					if has_previous_arg: # Check if an argument has been added before
						go += " ," # Separate the arguments with commas

					#* get arg name
					#* special Slice
					if isinstance(argin["conv"], lib.go.stl.GoSliceToStdVectorConverter): # Check if the argument is a slice
						arg_bound_name = self.__get_arg_bound_name_to_c({"conv": argin["conv"].T_conv}) # Get the argument bound name
					else: # If the argument is not a slice
						arg_bound_name = self.__get_arg_bound_name_to_c(argin) # Get the argument bound name

					#* special std::string (convert to const char*)
					arg_bound_name = arg_bound_name.replace("std::string", "const char*") # Replace std::string with const char*
					arg_bound_name = arg_bound_name.replace("const const", "const") # Replace const const with const

					#* special Slice
					if isinstance(argin["conv"], lib.go.stl.GoSliceToStdVectorConverter): # Check if the argument is a slice
						go += f"size_t {clean_name(argin['carg'].name)}ToCSize, {arg_bound_name} *{clean_name(argin['carg'].name)}ToCBuf" # Add the argument
					else: # If the argument is not a slice
						#* normal argument
						go += f"{arg_bound_name} {argin['carg'].name}" # Add the argument
					has_previous_arg = True # Set the flag to True

			go += ")" # Close the function definition

			if is_in_header: # Check if the method is in the header
				go += ";\n" # Add a semicolon and a new line
			else: # If the method is not in the header
				go += "{\n" # Open the function body

				args = [] 
				#* if another route is set
				if "route" in proto["features"] and convClass is not None and not is_constructor: # Check if the prototype has a route and the class is not None and the method is not a constructor
					args.append(f"({convClass.ctype}*)this_") # Add the "this" pointer

				#* convert arg to cpp
				if len(proto["args"]): # Check if there are arguments
					#* if the function is global but have a convclass,
					#* special case, which include the class has arg in first arg
					if  not is_constructor and is_global and convClass is not None: # Check if the method is not a constructor and is global and the class is not None
						src, retval_c = self.__arg_from_c_to_cpp({"conv":convClass}, "this_") # Convert the argument from C to C++
						go += src # Add the source code
						args.append(retval_c) # Add the converted argument

					#* other normal args
					for argin in proto["args"]: # Iterate over the arguments
						#* special Slice
						if isinstance(argin["conv"], lib.go.stl.GoSliceToStdVectorConverter): # Check if the argument is a slice
							src, retval_c = self.__arg_from_c_to_cpp(argin, clean_name(str(argin["carg"].name))) # Convert the argument from C to C++
						else: # If the argument is not a slice
							src, retval_c = self.__arg_from_c_to_cpp(argin, str(argin["carg"].name)) # Convert the argument from C to C++
						go += src # Add the source code
						args.append(retval_c) # Add the converted argument

				if is_constructor: # Check if the method is a constructor
					#* constructor, make our own return
					retval = "void" # Set the return value to void
					#* if another route is set
					if "route" in proto["features"]: # Check if the prototype has a route
						go += f"	return (void*){proto['features']['route'](args)}\n" # Add the source code
					elif "proxy" in convClass._features: # Check if the class has a proxy
						go += "	auto " + convClass._features["proxy"].wrap(f"new {convClass._features['proxy'].wrapped_conv.bound_name}({','.join(args)})", "v") # Add the source code
						go += "	return v;\n" # Add the source code
					else: # If the class does not have a proxy
						go += f"	return (void*)(new {convClass.ctype}({','.join(args)}));\n" # Add the source code
				else: # If the method is not a constructor
					#* if there is return value
					if retval != "void": # Check if the return value is not void
						go += "	auto ret = " # Add the source code

					#* special comparison
					if overload_op is not None: # Check if the method is a comparison
							go += f"(*({convClass.ctype}*)this_)" # Add the source code
							go += overload_op # Add the source code
							go += f"({args[0]});\n" # Add the source code
					#* classic call to function
					else: # If the method is not a comparison
						#* transform & to *
						if hasattr(proto["rval"]["storage_ctype"], "ref") and any(s in proto["rval"]["storage_ctype"].ref for s in ["&"]): # Check if the return value has a reference
							go += "&" # Add the source code

						#* if another route is set
						if "route" in proto["features"]: # Check if the prototype has a route
							go += proto["features"]["route"](args) + "\n" # Add the source code
						else: # If the prototype does not have a route
							#* not global, member class, include the "this" pointer first
							if not is_global: # Check if the method is not global
								go += f"(*({convClass.ctype}*)this_)" # Add the source code
								if convClass.ctype.is_pointer(): # Check if the class is a pointer
									go += "->" # Add the source code
								else: # If the class is not a pointer
									go += "." # Add the source code

							#* cpp function name
							go += cpp_function_name # Add the source code

							#* add function's arguments
							go += f"({','.join(args)});\n" # Add the source code

						#* return arg out
						if "arg_out" in proto["features"] or "arg_in_out" in proto["features"]: # Check if the prototype has an argument out
							for arg in proto['args']: # Iterate over the arguments
								if ('arg_out' in proto['features'] and str(arg['carg'].name) in proto['features']['arg_out']) or \
									('arg_in_out' in proto['features'] and str(arg['carg'].name) in proto['features']['arg_in_out']): # Check if the argument is an argument out
									#* FOR NOW ONLY FOR THE STD::STRING
									if "GoStringConverter" in str(arg["conv"]) and \
										"carg" in arg and hasattr(arg["carg"].ctype, "ref") and any(s in arg["carg"].ctype.ref for s in ["&"]): # Check if the argument is a string
										#* it's a pointer (or there is a bug)
										retval_cpp = f"(&({str(arg['carg'].name)}_cpp))" # Set the return value to the argument
										src, retval_cpp = self.__arg_from_cpp_to_c(arg, retval_cpp, static) # Get the source code and the return value
										go += src # Add the source code
										go += f"	{str(arg['carg'].name)} = {retval_cpp};\n" # Add the source code

				if retval != "void": # Check if the return value is not void
					src, retval_c = self.__arg_from_cpp_to_c(proto["rval"], "ret", static) # Get the source code and the return value
					go += src # Add the source code
					go += f"return {retval_c};\n" # Add the source code
				go += "}\n" # Add the source code

		return go # Return the source code

	#* VERY SPECIAL
	#* check in every methods, 
	#* if one arg is only out and if it's a class, if there is a constructor with no arg
	def _check_arg_out_add_constructor_if_needed(self, method): # Check if the argument out needs a constructor
		def check_if_val_have_constructor(val): # Check if the value has a constructor
			#* if it's a arg out and a class
			if self.__get_is_type_class_or_pointer_with_class(val["conv"]): # Check if the value is a class
				#* find the constructor without arg
				type_conv = None # Set the type converter to None
				for arg_conv in self._bound_types: # Iterate over the bound types
					if str(arg_conv.ctype) == str(val["conv"].ctype): # Check if the type converter is the same as the value
						type_conv = arg_conv # Set the type converter
						if hasattr(arg_conv, "constructor") and arg_conv.constructor is not None: # Check if the type converter has a constructor
							proto_args = self._build_protos(arg_conv.constructor["protos"]) # Get the prototypes
							break # Break the loop
				else: # If the loop did not break
					proto_args = None # Set the prototypes to None
				
				#* if no proto constructor with no args, add one
				if proto_args is None and type_conv is not None: # Check if the prototypes are None and the type converter is not None
					self.bind_constructor(type_conv, []) # Bind the constructor

		#* check all protos
		protos = self._build_protos(method["protos"]) # Get the prototypes
		for proto in protos: # Iterate over the prototypes
			#* convert arg in to c 
			if len(proto["args"]): # Check if the prototype has arguments
				for arg in proto["args"]: # Iterate over the arguments
					#* if arg out only, declare this value
					if "arg_out" in proto["features"] and str(arg["carg"].name) in proto["features"]["arg_out"]: # Check if the argument is an argument out
						if arg["carg"].ctype.is_pointer() or (hasattr(arg["carg"].ctype, "ref") and arg["carg"].ctype.ref == "&"): # Check if the argument is a pointer
							check_if_val_have_constructor(arg) # Check if the value has a constructor

	def finalize(self): # Finalize the bindings

		#* add class global
		for conv in self._bound_types: # Iterate over the bound types
			if conv.nobind: # Check if the type converter is not bound
				continue # Continue the loop

			if conv.is_type_class(): # Check if the type converter is a class
				#* add equal of deep copy
				if conv._supports_deep_compare: 
					go = ""
					if "proxy" in conv._features:
						go += f"bool _{conv.bound_name}_Equal({conv.ctype} *a, {conv.ctype} *b){{\n" # Add the source code
						go += f"	auto cast_a = _type_tag_cast(a, {conv.type_tag}, {conv._features['proxy'].wrapped_conv.type_tag});\n" # Add the source code
						go += f"	auto cast_b = _type_tag_cast(b, {conv.type_tag}, {conv._features['proxy'].wrapped_conv.type_tag});\n" 

						wrapped_conv = conv._features["proxy"].wrapped_conv # Get the wrapped converter
						if wrapped_conv.is_type_class(): # Check if the wrapped converter is a class
							go += f"	return ({wrapped_conv.bound_name}*)cast_a == ({wrapped_conv.bound_name}*)cast_b;\n" # Add the source code
						else: # If the wrapped converter is not a class
							#* check the convert from the base (in case of ptr) 
							if wrapped_conv.ctype.is_pointer() or (hasattr(wrapped_conv.ctype, "ref") and any(s in wrapped_conv.ctype.ref for s in ["&", "*"])): # Check if the wrapped converter is a pointer
								base_conv = self._get_conv(str(wrapped_conv.ctype.scoped_typename)) # Get the base converter
								if base_conv is None: # Check if the base converter is None
									type_bound_name = str(wrapped_conv.bound_name) # Set the type bound name
								else: # If the base converter is not None
									type_bound_name = str(base_conv.ctype) # Set the type bound name
							else: # If the wrapped converter is not a pointer
								type_bound_name = str(wrapped_conv.ctype) # Set the type bound name
							go += f"	return ({type_bound_name}*)cast_a == ({type_bound_name}*)cast_b;\n" # Add the source code
					else: # If the type converter is not a proxy
						go += f"bool _{conv.bound_name}_Equal({conv.bound_name} *a, {conv.bound_name} *b){{\n" # Add the source code
						go += f"	return *a == *b;\n" # Add the source code
					go += "}\n" # Add the source code

					self.insert_code(go) # Insert the source code
					if "proxy" in conv._features: # Check if the type converter is a proxy
						self.bind_method(conv, "Equal", "bool", [f"{conv.ctype} *b"], {"route": route_lambda(f"_{conv.bound_name}_Equal")}) # Bind the method
					else: # If the type converter is not a proxy
						self.bind_method(conv, "Equal", "bool", [f"{conv.bound_name} *b"], {"route": route_lambda(f"_{conv.bound_name}_Equal")}) # Bind the method

				#* VERY SPECIAL
				#* check in every methods, 
				#* if one arg is only out and if it's a class, if there is a constructor with no arg
				for method in conv.static_methods+conv.methods:	# Check in every methods
					self._check_arg_out_add_constructor_if_needed(method) # Check if the argument is an argument out and add the constructor if needed

			#* add down cast
			for base in conv._bases: # Iterate over the bases
				self.add_cast(base, conv, lambda in_var, out_var: "%s = (%s *)((%s *)%s);\n" % (out_var, conv.ctype, base.ctype, in_var)) # Add the cast

		#* VERY SPECIAL
		#* check in every methods, 
		#* if one arg is only out and if it's a class, if there is a constructor with no arg
		for func in self._FABGen__function_declarations.values(): # Iterate over the function declarations
			self._check_arg_out_add_constructor_if_needed(func) # Check if the argument is an argument out and add the constructor if needed

		super().finalize() # Call the super finalize

		self.output_binding_api() # Output the binding API

		#* helper to add from itself and from parent class
		def extract_conv_and_bases(convs_to_extract, extract_func, bases_convs_to_extract): # Extract the converter and the bases converters
			go = "" # Set the go to an empty string
			saved_names = [] # Set the saved names to an empty list
			for conv_to_extract in convs_to_extract: # Iterate over the converters to extract
				if "name" in conv_to_extract: # Check if the name is in the converters to extract
					saved_names.append(conv_to_extract["name"]) # Append the name to the saved names
				elif "op" in conv_to_extract: # Check if the op is in the converters to extract
					saved_names.append(conv_to_extract["op"]) # Append the op to the saved names
				go += extract_func(conv_to_extract) # Add the extract function

			#* add static member get set for base class
			for base_convs_to_extract in bases_convs_to_extract: # Iterate over the base converters to extract
				for conv_to_extract in base_convs_to_extract: # Iterate over the converters to extract
					#* add only if it's not already in the current class
					n = "" # Set the name to an empty string
					if "name" in conv_to_extract: # Check if the name is in the converters to extract
						n = conv_to_extract["name"] # Set the name
					elif "op" in conv_to_extract: # Check if the op is in the converters to extract
						n = conv_to_extract["op"] # Set the op
					if n not in saved_names: # Check if the name is not in the saved names
						saved_names.append(n) # Append the name to the saved names
						go += extract_func(conv_to_extract) # Add the extract function
			return go # Return the go

		#* .h
		go_h = '#pragma once\n' \
				'#ifdef __cplusplus\n'\
				'extern "C" {\n'\
				'#endif\n' # Set the go h to the source code

		go_h += '#include <stdint.h>\n' \
			'#include <stdbool.h>\n' \
			'#include <stddef.h>\n' \
			'#include <memory.h>\n' \
			'#include <string.h>\n' \
			'#include <stdlib.h>\n' \
			'#include "fabgen.h"\n\n' # Add the includes
		
		#===========================/\Alexandre/\------------\/Pierre\/===========================

		#* enum
		for bound_name, enum in self._enums.items(): # for each enum in the list
			enum_conv = self._get_conv_from_bound_name(bound_name) # get the enum conv
			if enum_conv is not None and hasattr(enum_conv, "base_type") and enum_conv.base_type is not None: # if the enum has a base type and it's not None
				arg_bound_name = str(enum_conv.base_type) # get the base type
			else:
				arg_bound_name = "int" # else set the base type to int
				
			go_h += f"extern {arg_bound_name} Get{bound_name}(const int id);\n" 

		#* write all typedef first
		for conv in self._bound_types:
			if conv.nobind:
				continue

			cleanBoundName = clean_name_with_title(conv.bound_name) # clean the bound name
			if self.__get_is_type_class_or_pointer_with_class(conv) : # if the type is a class or a pointer to a class 
				go_h += f"typedef void* {clean_name_with_title(self._name)}{cleanBoundName};\n" # add the typedef to the .h file with the name of the class 

			if "GoStdFunctionConverter" in str(conv): # if the type is a std::function
				func_name = conv.base_type.replace("std::function<", "").replace("&", "*")[:-1] #* [:-1] to remove the > of std::function
				first_parenthesis = func_name.find("(") # check location of the first parenthesis
				#* get all args boundname in c
				args = func_name[first_parenthesis+1:-1].split(",")
				args_boundname = [] # list of all args boundname
				for arg in args: # for each argument in the arguments list
					if len(arg): # if the argument is not empty
						ctype = parse(arg, gen._CType) 

						conv = self.select_ctype_conv(ctype)  # get the converter
						args_boundname.append(self.__get_arg_bound_name_to_c({"conv": conv, "carg": type('carg', (object,), {'ctype':ctype})()})) # add the argument bound name to the list

				go_h += f"typedef {func_name[:first_parenthesis]} (*{clean_name_with_title(self._name)}{cleanBoundName})({','.join(args_boundname)});\n" # add the typedef to the .h file with the name of the class

		#* write the rest of the classes
		for conv in self._bound_types: # for each converter in the list
			if conv.nobind: # if the converter is not bind
				continue

			cleanBoundName = clean_name_with_title(conv.bound_name) # clean the bound name 

			if "sequence" in conv._features: # if the converter is a sequence
				go_h += self.__extract_sequence(conv, is_in_header=True) # extract the sequence to the .h file 

			#* static members
			go_h += extract_conv_and_bases(conv.static_members, \
									lambda member: self.__extract_get_set_member(conv.bound_name, conv, member, static=True, is_in_header=True), \
									[base_class.static_members for base_class in conv._bases]) # extract the static members to the .h file 

			#* members
			go_h += extract_conv_and_bases(conv.members, \
									lambda member: self.__extract_get_set_member(conv.bound_name, conv, member, is_in_header=True), \
									[base_class.members for base_class in conv._bases]) # extract the non-static members to the .h file

			#* constructors
			if conv.constructor: # if the converter has a constructor
				go_h += self.__extract_method(cleanBoundName, conv, conv.constructor, bound_name=f"constructor_{conv.bound_name}", is_in_header=True, is_global=True, is_constructor=True) # extract the constructor to the .h file 

			#* destructor for all type class
			if self.__get_is_type_class_or_pointer_with_class(conv) : # if the type is a class or a pointer to a class 
				go_h += f"extern void {clean_name_with_title(self._name)}{cleanBoundName}Free({clean_name_with_title(self._name)}{cleanBoundName});\n" # add the destructor to the .h file with the name of the class

			#* arithmetic operators
			go_h += extract_conv_and_bases(conv.arithmetic_ops, \
									lambda arithmetic: self.__extract_method(conv.bound_name, conv, arithmetic, is_in_header=True, name=arithmetic['op'], bound_name=gen.get_clean_symbol_name(arithmetic['op'])), \
									[base_class.arithmetic_ops for base_class in conv._bases]) # extract the arithmetic operators to the .h file

			#* comparison_ops
			go_h += extract_conv_and_bases(conv.comparison_ops, \
									lambda comparison: self.__extract_method(conv.bound_name, conv, comparison, is_in_header=True, name=comparison['op'], bound_name=gen.get_clean_symbol_name(comparison['op'])), \
									[base_class.comparison_ops for base_class in conv._bases]) # extract the comparison operators to the .h file

			#* static methods
			go_h += extract_conv_and_bases(conv.static_methods, \
									lambda method: self.__extract_method(conv.bound_name, conv, method, static=True, is_in_header=True), \
									[base_class.static_methods for base_class in conv._bases]) # extract the static methods to the .h file
			#* methods
			go_h += extract_conv_and_bases(conv.methods, \
									lambda method: self.__extract_method(conv.bound_name, conv, method, is_in_header=True), \
									[base_class.methods for base_class in conv._bases]) # extract the non-static methods to the .h file
				
			
		#* functions
		for func in self._bound_functions: # for each function in the list 
			go_h += self.__extract_method("", None, func, name=func["name"], is_global=True, is_in_header=True) # extract to the .h file, the function with the name of the function

		#* global variables
		for var in self._bound_variables: # for each variable in the list
			go_h += self.__extract_get_set_member("", None, var, is_global=True, is_in_header=True) # extract to the .h file, the variable with the name of the variable

		go_h += '#ifdef __cplusplus\n' \
				'}\n' \
				'#endif\n' 
		self.go_h = go_h # add the .h file to the list of files to be generated


		#* cpp
		go_c = '// go wrapper c\n' \
				'#include \"wrapper.h\"\n' \
				'#include <memory>\n'
				
		if len(self._FABGen__system_includes) > 0: # if there are system includes 
			go_c += "".join(['#include "%s"\n\n' % path for path in self._FABGen__system_includes]) # add the system includes to the .c file 
		if len(self._FABGen__user_includes) > 0: # if there are user includes
			go_c += "".join(['#include "%s"\n\n' % path for path in self._FABGen__user_includes]) # add the user includes to the .c file

		go_c += self._source # add the source code to the .c file

		# enum
		for bound_name, enum in self._enums.items(): # for each enum in the list
			enum_conv = self._get_conv_from_bound_name(bound_name) # get the converter of the enum
			if enum_conv is not None and hasattr(enum_conv, "base_type") and enum_conv.base_type is not None: # if the converter has a base type
				arg_bound_name = str(enum_conv.base_type) # get the base type
			else: # if the converter has no base type
				arg_bound_name = "int" # set the base type to int

			enum_vars = []
			for name, value in enum.items(): # for each name and value in the enum 
				enum_vars.append(f"({arg_bound_name}){value}") # add the value to the list of enum variables
			go_c += f"static const {arg_bound_name} {clean_name_with_title(self._name)}{bound_name} [] = {{ {', '.join(enum_vars)} }};\n" # add the enum to the .c file
			go_c += f"{arg_bound_name} Get{bound_name}(const int id) {{ return {clean_name_with_title(self._name)}{bound_name}[id];}}\n" # add the get function to the .c file

		#  classes
		for conv in self._bound_types: # for each converter in the list 
			if conv.nobind: # if the converter is not to be bound 
				continue # skip the converter

			cleanBoundName = clean_name_with_title(conv.bound_name) # get the clean name of the converter 
			
			if conv.is_type_class(): # if the converter is a class 
				go_c += f"// bind {clean_name_with_title(self._name)}{cleanBoundName} methods\n" # add a comment to the .c file 

			if "sequence" in conv._features: # if the converter is a sequence 
				go_c += self.__extract_sequence(conv) # extract the sequence to the .c file
			
			# static members
			go_c += extract_conv_and_bases(conv.static_members, \
									lambda member: self.__extract_get_set_member(conv.bound_name, conv, member, static=True), \
									[base_class.static_members for base_class in conv._bases]) # extract the static members to the .c file 

			# members
			go_c += extract_conv_and_bases(conv.members, \
									lambda member: self.__extract_get_set_member(conv.bound_name, conv, member), \
									[base_class.members for base_class in conv._bases]) # extract the members to the .c file

			# constructors
			if conv.constructor:
				go_c += self.__extract_method(conv.bound_name, conv, conv.constructor, bound_name=f"constructor_{conv.bound_name}", is_global=True, is_constructor=True) # extract the constructor to the .c file
				
			#* destructor for all type class
			if self.__get_is_type_class_or_pointer_with_class(conv) :  # if the converter is a class or a pointer to a class
				#* delete
				go_c += f"void {clean_name_with_title(self._name)}{cleanBoundName}Free({clean_name_with_title(self._name)}{cleanBoundName} h){{" \
						f"delete ({conv.ctype}*)h;" \
						f"}}\n" # extract the destructor to the .c file

			#* arithmetic operators
			go_c += extract_conv_and_bases(conv.arithmetic_ops, \
									lambda arithmetic: self.__extract_method(conv.bound_name, conv, arithmetic, name=arithmetic['op'], bound_name=gen.get_clean_symbol_name(arithmetic['op']), overload_op=arithmetic["op"]), \
									[base_class.arithmetic_ops for base_class in conv._bases]) # extract the arithmetic operators to the .c file

			#* comparison_ops
			go_c += extract_conv_and_bases(conv.comparison_ops, \
									lambda comparison: self.__extract_method(conv.bound_name, conv, comparison, name=comparison["op"], bound_name=gen.get_clean_symbol_name(comparison["op"]), overload_op=comparison["op"]), \
									[base_class.comparison_ops for base_class in conv._bases]) # extract the comparison operators to the .c file

			#* static methods
			go_c += extract_conv_and_bases(conv.static_methods, \
									lambda method: self.__extract_method(conv.bound_name, conv, method, static=True), \
									[base_class.static_methods for base_class in conv._bases]) # extract the static methods to the .c file
			#* methods
			go_c += extract_conv_and_bases(conv.methods, \
									lambda method: self.__extract_method(conv.bound_name, conv, method), \
									[base_class.methods for base_class in conv._bases]) # extract the methods to the .c file

		#* functions
		for func in self._bound_functions: # for each function in the list 
			go_c += self.__extract_method("", None, func, name=func["name"], is_global=True) # extract the function to the .c file

		#* global variables
		for var in self._bound_variables: # for each variable in the list
			go_c += self.__extract_get_set_member("", None, var, is_global=True, static=True) # extract the variable to the .c file

		self.go_c = go_c

		#* .go
		go_bind = f"package {clean_name_with_title(self._name)}\n" \
				'// #include "wrapper.h"\n' \
				'// #cgo CFLAGS: -I . -Wall -Wno-unused-variable -Wno-unused-function -O3\n' \
				'// #cgo CXXFLAGS: -std=c++14 -O3\n' # add c++14 flag for cgo to compile c++14 code 
		go_bind += self.cgo_directives # add cgo directives
		go_bind += f"// #cgo LDFLAGS: -lstdc++ -L. -l{self._name}\n" \
				'import "C"\n\n' \
				'import (\n' # add import directives 
		#* check if reflect package is needed
		for conv in self._FABGen__type_convs.values(): # for each converter
			# special Slice
			if isinstance(conv, lib.go.stl.GoSliceToStdVectorConverter): # if the converter is a slice converter 
				go_bind += '	"reflect"\n' # add reflect package to the import directives
				break
		#* add runtime package if we have class
		for conv in self._FABGen__type_convs.values(): # for each converter 
			if self.__get_is_type_class_or_pointer_with_class(conv): # if the converter is a class or a pointer to a class
				go_bind += '	"runtime"\n' # add runtime package to the import directives
				break

		go_bind += '	"unsafe"\n' \
				')\n' # add unsafe package to the import directives

		with open("lib/go/WrapperConverter.go", "r") as file: # open the WrapperConverter.go file 
			lines = file.readlines() # read the lines of the file 
			go_bind += "".join(lines) # add the lines to the go_bind string
			go_bind += "\n" # add a new line to the go_bind string

		# // #cgo CFLAGS: -Iyour-include-path
		# // #cgo LDFLAGS: -Lyour-library-path -lyour-library-name-minus-the-lib-part

		for conv in self._bound_types: # for each converter in the list
			if conv.nobind: # if the converter is not to be bound
				continue 

			cleanBoundName = clean_name_with_title(conv.bound_name) # get the clean name of the converter 

			#* special Slice
			if isinstance(conv, lib.go.stl.GoSliceToStdVectorConverter): # if the converter is a slice converter 
				arg_boung_name = self.__get_arg_bound_name_to_go({"conv":conv.T_conv}) # get the bound name of the slice converter 
				go_bind += f"// {clean_name_with_title(conv.bound_name)} ...\n" \
							f"type {clean_name_with_title(conv.bound_name)} []{arg_boung_name}\n\n" # add the slice converter to the go_bind string

			#* it's class
			if self.__get_is_type_class_or_pointer_with_class(conv): # if the converter is a class or a pointer to a class
				doc = self.get_symbol_doc(conv.bound_name) # get the doc of the converter 
				if doc == "": # if the doc is empty
					doc = " ..." # add ... to the doc
				else: # if the doc is not empty 
					doc = " " + re.sub(r'(\[)(.*?)(\])', r'\1harfang.\2\3', doc) #! J'ai pas compris ce que ça fait 

				go_bind += f"// {cleanBoundName} {doc}\n" \
							f"type {cleanBoundName} struct{{\n" \
							f"	h C.{clean_name_with_title(self._name)}{cleanBoundName}\n" \
							"}\n\n" \
							f"// New{cleanBoundName}FromCPointer ...\n" \
							f"func New{cleanBoundName}FromCPointer(p unsafe.Pointer) *{cleanBoundName} {{\n" \
							f"	retvalGO := &{cleanBoundName}{{h: (C.{clean_name_with_title(self._name)}{cleanBoundName})(p)}}\n" \
							f"	return retvalGO\n" \
							"}\n" # add the class converter to the go_bind string
			
			#* it's a sequence
			if "sequence" in conv._features: # if the converter is a sequence 
				go_bind += self.__extract_sequence_go(conv) # add the sequence converter to the go_bind string 

			#* static members
			go_bind += extract_conv_and_bases(conv.static_members, \
									lambda member: self.__extract_get_set_member_go(conv.bound_name, member, static=True), \
									[base_class.static_members for base_class in conv._bases]) # add the static members of the converter to the go_bind string

			#* members
			go_bind += extract_conv_and_bases(conv.members, \
									lambda member: self.__extract_get_set_member_go(conv.bound_name, member, static=False), \
									[base_class.members for base_class in conv._bases]) # add the non-static members of the converter to the go_bind string

			#* constructors
			if conv.constructor: # if the converter has a constructor 
				go_bind += self.__extract_method_go(conv.bound_name, conv, conv.constructor, bound_name=f"{conv.bound_name}", is_global=True, is_constructor=True) # add the constructor of the converter to the go_bind string

			#* destructor for all type class
			if self.__get_is_type_class_or_pointer_with_class(conv) : # if the converter is a class or a pointer to a class 
				go_bind += f"// Free ...\n" \
				f"func (pointer *{cleanBoundName}) Free(){{\n" \
				f"	C.{clean_name_with_title(self._name)}{cleanBoundName}Free(pointer.h)\n" \
				f"}}\n" # add the destructor of the converter to the go_bind string 
				
				go_bind += f"// IsNil ...\n" \
				f"func (pointer *{cleanBoundName}) IsNil() bool{{\n" \
				f"	return pointer.h == C.{clean_name_with_title(self._name)}{cleanBoundName}(nil)\n" \
				f"}}\n" # and add the IsNil function of the converter to the go_bind string 

				#* runtime.SetFinalizer(funcret, func(ctx *Ret) { C.free(ctx.bufptr) })

			#* arithmetic operators
			go_bind += extract_conv_and_bases(conv.arithmetic_ops, \
									lambda arithmetic: self.__extract_method_go(conv.bound_name, conv, arithmetic, bound_name=gen.get_clean_symbol_name(arithmetic['op'])), \
									[base_class.arithmetic_ops for base_class in conv._bases]) # add the arithmetic operators of the converter to the go_bind string
			#* comparison_ops
			go_bind += extract_conv_and_bases(conv.comparison_ops, \
									lambda comparison: self.__extract_method_go(conv.bound_name, conv, comparison, bound_name=gen.get_clean_symbol_name(comparison['op'])), \
									[base_class.comparison_ops for base_class in conv._bases]) # add the comparison operators of the converter to the go_bind string

			#* static methods
			go_bind += extract_conv_and_bases(conv.static_methods, \
									lambda method: self.__extract_method_go(conv.bound_name, conv, method, static=True), \
									[base_class.static_methods for base_class in conv._bases]) # add the static methods of the converter to the go_bind string
			#* methods
			go_bind += extract_conv_and_bases(conv.methods, \
									lambda method: self.__extract_method_go(conv.bound_name, conv, method), \
									[base_class.methods for base_class in conv._bases]) # add the non-static methods of the converter to the go_bind string

		#* enum
		for bound_name, enum in self._enums.items(): # for each enum in the enums dictionary 
			go_bind += f"// {bound_name} ...\n" # add the enum to the go_bind string 
			enum_conv = self._get_conv_from_bound_name(bound_name) # get the converter of the enum 
			if enum_conv is not None and hasattr(enum_conv, "go_type") and enum_conv.go_type is not None: # if the converter has a go_type attribute
				go_bind += f"type {bound_name} {enum_conv.go_type}\n" # add the go_type to the go_bind string 
			else: # if the converter doesn't have a go_type attribute
				go_bind += f"type {bound_name} int\n" # add the default go_type to the go_bind string
			go_bind += "var (\n" # add the enum values to the go_bind string
			for id, name in enumerate(enum.keys()): # for each value in the enum 
				go_bind += f"	// {clean_name(name)} ...\n" # add the value to the go_bind string 
				go_bind += f"	{clean_name(name)} =  {bound_name}(C.Get{bound_name}({id}))\n" # add the value to the go_bind string 
			go_bind += ")\n" # add the enum values to the go_bind string 

		#* functions
		for func in self._bound_functions: # for each function in the bound functions list 
			go_bind += self.__extract_method_go("", None, func, is_global=True) # add the function to the go_bind string 

		#* global variables
		#* sort by group if needed
		bound_variables_groups = {}
		for var in self._bound_variables: # for each variable in the bound variables list
			if "group" in var and var["group"] is not None: # if the variable has a group attribute and it's not None 
				group_name = clean_name_with_title(var["group"]) # get the group name 
				if group_name not in bound_variables_groups: # if the group name is not in the bound variables groups dictionary 
					bound_variables_groups[group_name] = [] # add the group name to the bound variables groups dictionary 
				bound_variables_groups[group_name].append(var) # add the variable to the bound variables groups dictionary 

		#* add bound variables groups
		for group_name, var_group in bound_variables_groups.items(): # for each group in the bound variables groups dictionary 
			go_bind += f"// {group_name} ...\n" # add the group to the go_bind string 
			var_conv = self.select_ctype_conv(var_group[0]["ctype"]) # get the converter of the group 
			if var_conv is not None and hasattr(var_conv, "go_type") and var_conv.go_type is not None: # if the converter has a go_type attribute and it's not None
				go_bind += f"type {group_name} {var_conv.go_type}\n" # add the go_type to the go_bind string 
			else: # if the converter doesn't have a go_type attribute
				go_bind += f"type {group_name} int\n" # add the default go_type to the go_bind string

			for id, var in enumerate(var_group): # for each variable in the group 
				go_bind += self.__extract_get_set_member_go("", var, is_global=True, implicit_cast=group_name) # add the variable to the go_bind string 

		#* add bound variables without group
		for var in self._bound_variables: # for each variable in the bound variables list 
			if "group" not in var or var["group"] is None: # if the variable doesn't have a group attribute or it's None 
				go_bind += self.__extract_get_set_member_go("", var, is_global=True) # add the variable to the go_bind string 

		self.go_bind = go_bind # set the go_bind string to the go_bind attribute 

		#* Create Translate file c++ to go name
		go_translate_file = {}

		def bind_method_translate(classname, convClass, method, static=False, name=None, bound_name=None, is_global=False, is_constructor=False): # function to bind a method 
			if bound_name is None: # if the bound name is None
				bound_name = method["bound_name"] # get the bound name
			if name is None: # if the name is None 
				name = bound_name # get the name 

			name_go = name # set the name to the name_go variable 
			if is_constructor: # if the method is a constructor
				name_go = "new_" + name_go # add new_ to the name_go variable

			protos = self._build_protos(method["protos"]) # get the protos of the method
			return_protos_name = []
			for id_proto, proto in enumerate(protos): # for each proto in the protos list
				method_name_go = f"{clean_name_with_title(name_go)}" # set the name to the method_name_go variable

				#* add bounding_name to the overload function
				if "bound_name" in proto["features"]: # if the proto has a bound_name attribute 
					method_name_go += proto["features"]["bound_name"] # add the bound_name to the method_name_go variable
				#* if automatic suffix generated
				elif "suggested_suffix" in proto: # if the proto has a suggested_suffix attribute 
					method_name_go += proto["suggested_suffix"] # add the suggested_suffix to the method_name_go variable 
			
				return_protos_name.append(method_name_go) # add the method_name_go to the return_protos_name list 
			return name, return_protos_name # return the name and the return_protos_name list 

		for conv in self._bound_types: # for each converter in the bound types list 
			if conv.nobind: # if the converter is nobind 
				continue

			go_translate_file[conv.bound_name] = {"name": clean_name_with_title(conv.bound_name)}  # add the bound name to the go translate file dictionary 

			#* members
			members = {} 
			for member in conv.static_members + conv.members: # for each member of the class (static and not static)
				bound_name = None 
				if "bound_name" in member: # if the member has a bound name
					bound_name = str(member["bound_name"]) # get the bound name
				elif bound_name is None: # if the member has no bound name
					bound_name = str(member["name"]) # get the name

				name = bound_name.replace(":", "")
				name = clean_name_with_title(name)
				members[bound_name] = [f"Get{name}", f"Set{name}"]

			if len(members): # if the class has members
				go_translate_file[conv.bound_name]["members"] = members # add the members to the class in the go translate file
				
			# functions
			functions = {}

			# constructors
			if conv.constructor: # if the class has a constructor
				name, protos_name = bind_method_translate(conv.bound_name, conv, conv.constructor, bound_name=f"{conv.bound_name}", is_global=True, is_constructor=True)
				functions[name] = protos_name # add the constructor to the functions list

			for method in conv.static_methods + conv.methods: # for each method in the methods list
				name, protos_name = bind_method_translate(conv.bound_name, conv, method) 
				functions[name] = protos_name # add the method to the functions list
				
			for arithmetic in conv.arithmetic_ops: # for each arithmetic operation in the arithmetic_ops list
				name, protos_name = bind_method_translate(conv.bound_name, conv, arithmetic, bound_name=gen.get_clean_symbol_name(arithmetic['op']))
				functions[name] = protos_name # add the arithmetic operation to the functions list
			for comparison in conv.comparison_ops: # for each comparison operation in the comparison_ops list
				name, protos_name = bind_method_translate(conv.bound_name, conv, comparison, bound_name=gen.get_clean_symbol_name(comparison['op'])) 
				functions[name] = protos_name # add the comparison operation to the functions list
				
			if len(functions): # if the functions list is not empty
				go_translate_file[conv.bound_name]["functions"] = functions # add the functions to the go_translate_file list

		# enum
		for bound_name, enum in self._enums.items(): # for each enum in the enums list
			go_translate_file[bound_name] = bound_name # add the enum to the go_translate_file list
			go_bind += "var (\n" 
			for id, name in enumerate(enum.keys()): # for each name in the enum keys
				go_translate_file[name] = clean_name(name) # add the enum to the go_translate_file list
		
		# functions
		for func in self._bound_functions: # for each functions in the bound_functions list 
			name, protos_name = bind_method_translate("", None, func, is_global=True) # get the name and the protos_name
			go_translate_file[name] = protos_name # add the name and the protos_name to the go_translate_file list

		# global variables
		for member in self._bound_variables: # for each member in the bound_variables list
			bound_name = None # set the bound_name variable to None
			if "bound_name" in member: # if the member have the bound_name attribute
				bound_name = str(member["bound_name"]) # get the bound_name attribute
				
			elif bound_name is None: # if the bound_name attribute is not present
				bound_name = str(member["name"]) # get the name attribute

			name = bound_name.replace(":", "") # remove the ":" character
			name = clean_name_with_title(name) # clean the name
			go_translate_file[bound_name] = [f"Get{name}", f"Set{name}"] 

		self.go_translate_file = json.dumps(go_translate_file, indent=4, sort_keys=True) # This code is used to generate the go_translate_file.json file, 
		
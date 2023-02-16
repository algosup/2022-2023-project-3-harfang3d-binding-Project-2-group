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

# add name to the Fsharp package 
def route_lambda(name):
	return lambda args: "%s(%s);" % (name, ", ".join(args))


def clean_name(name):
	new_name = str(name).strip().replace("_", "").replace(":", "")
	# if new_name isn't in list of reserved word in go then return new_name else return new_name + "Go"
	if new_name in ["break", "default", "func", "interface", "select", "case", "defer", "go", "map", "struct", "chan", "else", "goto", "package", "switch", "const", "fallthrough", "if", "range", "type", "continue", "for", "import", "return", "var" ]:
		return new_name + "Fsharp"
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


class FsharpPtrTypeConverter(gen.TypeConverter): # class for the pointer type converter
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

class FsharpTypeConverterCommon(gen.TypeConverter): # common class for all the go type converter
	def __init__(self, type, to_c_storage_type=None, bound_name=None, from_c_storage_type=None, needs_c_storage_class=False): # init the class
		super().__init__(type, to_c_storage_type, bound_name, from_c_storage_type, needs_c_storage_class) # init the parent class
		self.base_type = type # add the base type
		self.go_to_c_type = None # add the go to c type
		self.go_type = None # add the go type
	
	# get the go type of the variable in C type 
	def get_type_api(self, module_name): # return the go type of the variable in C type
		out = ""
		return out # return the out

	def to_c_call(self, in_var, out_var_p, is_pointer): # return the go variable in C variable
		return "" # return  ""

	# add the go variable in C variable
	def from_c_call(self, out_var, expr, ownership): # return the C variable in go variable
		return "%s((void *)%s, %s);\n" % (self.from_c_func, expr, ownership) # return  ""



class FsharpClassTypeDefaultConverter(FsharpTypeConverterCommon): # default class type converter
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

class FsharpExternTypeConverter(FsharpTypeConverterCommon): # converter for extern type
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

class FsharpGenerator(gen.FABGen): # create a new generator class
	default_ptr_converter = FsharpPtrTypeConverter  # set the default pointer converter
	default_class_converter = FsharpClassTypeDefaultConverter # set the default class converter
	default_extern_converter = FsharpExternTypeConverter  # set the default extern converter
	
	def __init__(self): # constructor
		super().__init__() # call the base class constructor
		self.check_self_type_in_ops = True # check the self type in operations
		self.go = "" # the Go source code
		self.cgo_directives = "" # the cgo directives

	def get_language(self): 
		return "Fsharp" # return the language name

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



	

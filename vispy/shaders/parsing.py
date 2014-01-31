# -*- coding: utf-8 -*-
# Copyright (c) 2014, Vispy Development Team.
# Distributed under the (new) BSD License. See LICENSE.txt for more info.

from __future__ import print_function, division, absolute_import

import re

# regular expressions for parsing GLSL
re_type = r'(void|int|float|vec2|vec3|vec4|mat2|mat3|mat4)'
re_identifier = r'([a-zA-Z_][\w_]*)'

# type and identifier like "vec4 var_name"
re_declaration = "(?:" + re_type + "\s+" + re_identifier + ")"

# list of variable declarations like "vec4 var_name, float other_var_name"
re_arg_list = "(" + re_declaration + "(?:,\s*" + re_declaration + ")*)?"

# function declaration like "vec4 function_name(float x, float y)"
re_func_decl = re_type + "\s+" + re_identifier + "\((void|" + re_arg_list + ")\)"

# anonymous variable declarations may or may not include a name:
#  "vec4" or "vec4 var_name"
re_anon_decl = "(?:" + re_type + "(?:\s+" + re_identifier + ")?)"

# list of anonymous declarations 
re_anon_arg_list = "(" + re_anon_decl + "(?:,\s*" + re_anon_decl + ")*)?"

# function prototype declaration like
#    "vec4 function_name(float, float);"
re_func_prot = re_type + "\s+" + re_identifier + "\((void|" + re_anon_arg_list + ")\)\s*;"

def parse_function_signature(code):
    """ 
    Return the name, arguments, and return type of the first function 
    definition found in *code*. Arguments are returned as [(type, name), ...].
    """
    m = re.search("^\s*" + re_func_decl + "\s*{", code, re.M)
    if m is None:
        print(code)
        raise Exception("Failed to parse function signature. Full code is printed above.")
    rtype, name, args = m.groups()[:3]
    if args == 'void' or args.strip() == '':
        args = []
    else:
        args = [tuple(arg.strip().split(' ')) for arg in args.split(',')]
    return name, args, rtype

def find_prototypes(code):
    """
    Return a list of signatures for each function prototype declared in *code*.
    Format is [(name, [args], rtype), ...].
    """
    
    prots = []
    lines = code.split('\n')
    for line in lines:
        m = re.match("\s*" + re_func_prot, line)
        if m is not None:
            rtype, name, args = m.groups()[:3]
            if args == 'void' or args.strip() == '':
                args = []
            else:
                args = [tuple(arg.strip().split(' ')) for arg in args.split(',')]
            prots.append((name, args, rtype))
    
    return prots
    

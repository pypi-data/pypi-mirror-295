import copy
import warnings
from lark import Lark, Tree, Token, Transformer, v_args
import sys
from pathlib import Path
from collections import defaultdict
from .import_start import StronglyTypedDict, string, char, number
from lark.exceptions import UnexpectedInput

MEMBER_TYPES_RESTRICTED = True

# for now variables is only used to prevent undeclared variables of being used.
keywords = ["type", "var", "const",
            "start", "end", "print", "input", "len",
            "if", "while", "is", "function", "contains", "arguments",  "return",
            "char", "number", "string"]
python_keywords = ["str", "range", "setattr", "_constants",
                   "class", "dir", "globals",
                   "local_vars", "getattr",
                   "Start", "np", ]  # Python key-words also give problems that we use in the compiled langauge

user_functions = {}  # Store user functions with their return type
variables = defaultdict(dict)  # Store user variables

type_warnings = []  # List with types that are not declared yet
types = ["char", "number", "string", "void"]  # This is a global that defines all the types
built_in_types = copy.deepcopy(types)
built_in_functions_general = {
    "char":         ("char", "char"),
    "number":       ("number", "number"),
    "string":       ("string", "string"),
    "print":        ("_print", "void"),
    "print_raw":    ("_print_memory_obj", "void"),
    "input_number": ("_input_number", "number"),
    "input_char":   ("_input_char", "char"),
    "input_string": ("_input_string", "string"),
    "len":          ("_len", "number"),
    "++":           ("_add_string", "string"),
    "+":            ("_add", "number"),
    "-":            ("_sub", "number"),
    "*":            ("_mul", "number"),
    "/":            ("_div", "number"),
    "%":            ("_mod", "number"),
    "^":            ("_pow", "number"),
    "==":           ("_eqlVal", "number"),
    "===":          ("_eqlRef", "number"),
    ">":            ("_gt", "number"),
    "<":            ("_lt", "number"),
    ">=":           ("_gte", "number"),
    "<=":           ("_lte", "number"),
    "&":            ("_and", "number"),
    "|":            ("_or", "number"),
    "!":            ("_not", "number")
}

built_in_functions = {k: v[1] for k, v in built_in_functions_general.items()}
built_in_function_names = {k: v[0] for k, v in built_in_functions_general.items()}

def symbolType(line, symbol, scope, member=""):
    #first check if the symbol is simply defined directly (e.g. global and local vars)
    left = symbol
    right = ""

    while len(left.split(".")) > 0:
        type_match = match(line, left, scope, member)

        # It is not correct so look for one shorter fit
        if type_match is None:
            if "." in left:
                right = left.rsplit(".", 1)[1] + (("." + right) if len(right) > 0 else "")
                left = left.rsplit(".", 1)[0]
                continue
            else:
                break

        if len(right) > 0:  #we need to resolve some right part
            for elem in right.split("."):
                org_type_match = type_match
                type_match = symbolType(line, elem, scope, type_match)
                if type_match is None:  # not a valid bracket
                    if elem in types:
                        raise StartError(f"In line {line}, a <{elem}> is used to access a member of <{org_type_match}>, this is not possible!")
                    elif elem[:7] == "string/":
                        raise StartError(f"In line {line}, an unknown member '{elem.split('/')[1]}' is used!")
                    elif org_type_match in built_in_types:
                        raise StartError(f"In line {line}, a member is accessed of a simple type with '{elem}' which is not possible!")
                    elif (elem in built_in_functions or elem in user_functions) and org_type_match in types:
                        raise StartError(f"In line {line}, '{elem}' is used to get a member of {org_type_match} which is not possible as '{elem}' has the wrong return type!")
                    else:
                        raise StartError(f"In line {line}, '{elem}' is used which is undefined!")
            return type_match
        else:  #we have everything here
            return type_match

    if member == "":  # Check that it is the highest call (in the recursive stack) of symbolType
        if symbol[:7] == "number/":
             raise StartError(f"In line {line}, '{symbol.split('/')[1]}' is used to access a member of a type which is not possible!")
        raise StartError(f"In line {line}, '{symbol}' is used which is not defined in the scope '{scope_2_str(scope)}'!")

    #if we end up here, there are no symbols to match anymore, so there is no match
    return

def match(line, symbol, scope, member):
    """ member determines if the symbol can be found as a member of a type. """
    # Make a difference between string and member name
    if symbol[:7] == "string/":
        type, member_name = symbol.split("/")
        symbol = member_name if member != "" else type
    elif symbol[:7] == "number/":
        type, member_name = symbol.split("/")
        symbol = member_name if member != "" and "*" not in variables[member] else type

    # handle unknown types
    if member == "*":
        return "*"

    # Search in new functions
    functions_name = f"{member}.{symbol}" if member else symbol
    if functions_name in user_functions:
        return user_functions[functions_name]
    elif symbol in user_functions and (not MEMBER_TYPES_RESTRICTED or user_functions[symbol] == "string") and member not in built_in_types and member in types:
        if len(t := set(variables[member].values())) == 1:  # If a type has only members of one type we also know the potential type
            return list(t)[0]
        return "*"

    # Search in built-in functions
    if symbol in built_in_functions and member == "":  # or ignore types, symbol not in types
        return built_in_functions[symbol]
    elif symbol in built_in_functions and (not MEMBER_TYPES_RESTRICTED or built_in_functions[symbol] == "string") and member not in built_in_types and member in types:
        if len(t := set(variables[member].values())) == 1:  # If a type has only members of one type we also know the potential type
            return list(t)[0]
        return "*"

    # Search in variables
    if symbol in variables[scope] and member == "":
        return variables[scope][symbol]
    elif symbol in variables[member]:
        return variables[member][symbol]
    elif "*" in variables[member] and (not MEMBER_TYPES_RESTRICTED or symbolType(line, symbol, scope) == "number"):
        return variables[member]["*"]
    elif "0" in variables[member] and (not MEMBER_TYPES_RESTRICTED or symbolType(line, symbol, scope) == "number"):
        return variables[member]["0"]

    return None

def toSymbol(t, scope, line):
    result = ""
    if isinstance(t, Token):  # it is a token, simply return the token value (for now return nothing, we deal with all tokens in the Tree parser)
        # return t.value
        return ""
    elif t is None:
        raise StartError(f"Compile Error: line {line} is not properly parsed!")
    elif not isinstance(t, Tree):  # Should not happen but if there is for example still a None in the tree this solves it
        return ""

    if t.data == 'variable':  # Variable Tree, so its bracketed
        if val(t, "name") is not None:
            return val(t, "name")
        else:
            key = toSymbol(get(t, "expression"), scope, line)
            name = f"{toSymbol(t.children[0],  scope, line)}.{key}"
            return name

    elif t.data == "class_variable":
        if get(t, 'variable') is not None:
            return f"{scope.split('.', 1)[0]}.{toSymbol(get(t, 'variable'), scope, line)}"
        else:  # something is wrong
            return f"{scope.split('.', 1)[0]}.{toSymbol(t.children[0], scope, line)}"

    elif t.data == "expression":  # just relay to the next Tree object
        return toSymbol(t.children[0], scope, line)

    elif t.data == "function_call":
        if get(t, "variable")!=None:
            var_name = toSymbol(get(t, 'variable'), scope, line)
            if var_name == "this":
                var_name = scope.split(".")[0]
            func_name = val(t, 'function')
            return f"{var_name}.{func_name}"
        elif val(t, "function") == "string" and t.children[1].children[0].children[0].data == "constant":
            return f"string/{val(t.children[1].children[0].children[0], 'string')[1:-1]}"
        elif val(t, "function") == "number" and t.children[1].children[0].children[0].data == "constant":
            return f"number/{val(t.children[1].children[0].children[0], 'number')}"
        else:
            return val(t, "function")

    return result

class StartError(Exception):
    pass

def get(t, data):
    """ find children in the tree that contain data (char, charvalue, number, ...?)
    """
    for child in t.children:
        if isinstance(child, Tree) and child.data == data:
            return child

def val(t, data):
    o = get(t, data)
    if o is None:
        return None
    else:
        return o.children[0].value

def scope_2_str(scope):
    return scope if scope != "" else "global"

def find_line_numbers(obj):
    while True:
        try:
            return obj.line
        except AttributeError:  # keep looking
            children = obj.children
            if len(children) == 0:  # no children so no line number can be found
                return
            obj = children[0]
        except TypeError:  # no line number can be found
            return

def add_variables(scope, var, var_type, line):
    """ Add a variable to the variable dict that is defined in start """
    # check if the variable is not already defined
    if var in variables[scope]:
        raise StartError(f"The variable '{var}' is already defined in the scope '{scope_2_str(scope)}' as a <{variables[scope][var]}> type! Therefore, it can not be redefined in line {line} as <{var_type}>.")
    # check if the variable is defined
    if var_type not in types:
        # There is no reason to use a type in global scope that is not defined
        if scope == "":
            raise StartError(f"In line {line}, the variable '{var}' in scope 'global' is defined as <{var_type}>, however, <{var_type}> is not defined! Make sure you define a type before you using it!")
        # Add to type_warnings as there are some circular types declarations that can only be checked after compiling everything.
        type_warnings.append((scope, var, var_type, line))

    variables[scope][var] = var_type

def add_function(function, rtype, line):
    """ Add a function to the user_function dict that is defined in start """
    # check if the function is not already defined
    if function in user_functions:
        raise StartError(f"The function '{function}' is already defined in the scope '{function.rsplit('.', 1)[0]}'! Therefore, it can not be redefined in line {line}.")

    if rtype not in types:
        raise StartError(f"The return type <{rtype}> used in the function '{function}' in line {line} is not defined! Make sure you define a type before using it!")

    user_functions[function] = rtype

def variable_exists(name, scope, line):
    # print(name, scope, line)
    if name == "this":
        if len(scope.split(".")) != 2:
            raise StartError(f"In line {line}, '{name}' is used which is outside a type which is not possible.")
    elif name not in variables[scope]:
        raise StartError(f"In line {line}, '{name}' is used which is not declared.")

def toPython(t, state, indent, scope):
    """
    This goes through the grammar tree and recursively builds the python file
    that has the same functionality as the start code.

    @param t: A (sub)Tree given by the grammar rules
    @type t: Tree
    @param state: A counter for which argument is added to a function or class
    @type state: str
    @param indent: The number of indents currently needed for the python code, e.g., everything in a function has one indent.
    @type indent: str
    @param scope: ?
    @type scope: str
    @return: The python code for this subtree
    @rtype: str
    """
    result = ""
    if isinstance(t, Token):  # it is a token, simply return the token value (for now return nothing, we deal with all tokens in the Tree parser)
        # return t.value
        return ""
    elif not isinstance(t, Tree):  # Should not happen but if there is for example still a None in the tree this solves it
        return ""

    line = find_line_numbers(t)

    if t.data == 'variable_declaration' or t.data == 'constant_declaration':
        # define the var in the global scope
        if scope == "":
            add_variables(scope, val(t, 'name'), val(t, "type"), line)
            result += f"{indent}local_vars['{val(t, 'name')}'] = {val(t, 'type')}()\n"
            if t.data == 'constant_declaration':
                result += f"{indent}local_vars.set_constant('{val(t, 'name')}')\n"
        # this is in a function
        elif scope[-9:] == ":function":
            add_variables(scope[:-9], val(t, 'name'), val(t, "type"), line)
            result = f"{indent}local_vars['{val(t, 'name')}'] = {val(t, 'type')}()\n"  # this makes the type, strongly typed
            if t.data == 'constant_declaration':
                result += f"{indent}local_vars.set_constant('{val(t, 'name')}')\n"
            result += f"{indent}local_vars['{val(t, 'name')}'] = args{state}\n"
        elif scope[-6:] == ":class":
            add_variables(scope[:-6], val(t, 'name'), val(t, "type"), line)
            result = f"{indent}self.{val(t, 'name')} = {val(t, 'type')}()\n"  # this makes the type, strongly typed
            result += f"{indent}self.{val(t, 'name')} = self.{val(t, 'name')} if args{state} is None else args{state}\n"  # handles empty constructor
            if t.data == 'constant_declaration':
                result += f"{indent}self.set_constant('{val(t, 'name')}')\n"
        else:  # local function/method variable
            add_variables(scope, val(t, 'name'), val(t, "type"), line)
            result += f"{indent}local_vars['{val(t, 'name')}'] = {val(t, 'type')}()\n"
            if t.data == 'constant_declaration':
                result += f"{indent}local_vars.set_constant('{val(t, 'name')}')\n"
        return result

    elif t.data == 'type_declaration':
        # Get the type of the object in the tree. This makes python code like coordinate.get() possible.
        type_dec = val(t, "type")

        # check if a variable is already declared and if not add it to the global type list
        if type_dec not in types:
            types.append(type_dec)
            add_function(type_dec, type_dec, line)  # adding the constructor as a function
        else:
            raise SyntaxError(f'In line {line}, type <{type_dec}> is defined while it was already defined')

        result = f"\n{indent}class {type_dec}(Start):\n"

        # if it is a shorthand type def, parse the shorthand notation and do all that here
        if get(t, "short_hand") is not None:
            # if a class is a sequence give it a type instead of init all variables with the same type
            result += f"{indent}\ttype = {val(t.children[1], 'type')}\n"

            if val(t.children[1], 'length') == "*":
                result += f"{indent}\tlen = np.inf\n\n"
            else:
                result += f"{indent}\tlen = {int(val(t.children[1], 'length'))}\n\n"

            # create the init method
            result += f"{indent}\tdef __init__(self, *args):\n"  # shorthand has the same arguments as a sequences
            result += f"{indent}\t\tsuper().__init__()\n"
            t = get(t, "short_hand")
            # no length. so we need to configure this class as a "variable length, any attr goes" (set) type.
            if val(t, 'length') == "*":
                result += f"{indent}\t\targ_len = len(args)\n"
                add_variables(type_dec, "*", val(t, 'type'), line)
            else:
                for n in range(int(val(t, 'length'))):
                    add_variables(type_dec, str(n), val(t, 'type'), line)
                result += f"{indent}\t\targ_len = {int(val(t, 'length'))}\n"
            result += f"{indent}\t\tfor i in range(arg_len):\n"
            result += f"{indent}\t\t\tsetattr(self, str(i), args[i] if i < len(args) else {val(t, 'type')}())\n"
        else:  # if not a shorthand, parse the content of the code block using the current type's scope
            init_code = ""
            argCount = 0
            attr_types = {}
            # Go through all the children that are in the type_declaration tree and either add a new function
            # or add a variable to the class. Each variable is added to the class as a class attribute.
            for child in t.children:
                if isinstance(child, Tree) and child.data in ['variable_declaration', 'constant_declaration']:
                    attr_types[val(child, 'name')] = val(child, 'type')
                    init_code += toPython(child, str(argCount), indent + "\t\t", type_dec + ":class")
                    argCount += 1

            # class attributes
            result += f"{indent}\ttype = {attr_types}\n"

            # build the __init__ method in python
            arguments = ', '.join(f"args{i}=None" for i in range(argCount))
            result += f"{indent}\tdef __init__(self, {arguments}):\n"
            result += f"{indent}\t\tsuper().__init__()\n"
            result += init_code

            # add the methods to the class
            for child in t.children:
                if isinstance(child, Tree) and child.data == 'function_declaration':
                    result += toPython(child, state, indent + "\t", type_dec + ".")

        return result  # no need to add enter as each class ends with a function

    elif t.data == 'function_declaration':
        function = scope + val(t, "name")
        return_type = val(t, "type")

        if function not in user_functions:  # built-in functions are not allowed as name
            add_function(function, return_type, line)
        else:
            raise StartError(f"On line {line}, the function '{function}' is defined while it is already defined!")

        method = "self, " if scope != "" else ""
        # Make sure a definition has whitespace above it and add self as argument if it is a method
        arguments = toPython(get(t, "argument_declaration"), state, indent + "\t", val(t, "name"))
        result = f"\n{indent}def {val(t, 'name')}({method}{arguments}):\n"
        result += f"{indent}\tlocal_vars = StronglyTypedDict('{val(t, 'name')}')\n"
        for child in t.children:
            # skip argument_declaration
            if child.data == "argument_declaration":
                arg = 0
                for child_var in child.children:
                    result += toPython(child_var, str(arg), indent + "\t", scope + val(t, 'name') + ":function")  # set the scope to function
                    arg += 1
            # any variable will be possibly set to the arg in args
            elif isinstance(child, Tree) and (get(child, "variable_declaration") or get(child, "constant_declaration")):
                result += toPython(child, "", indent + "\t",  scope + val(t, "name"))  # set the scope to function
            else:
                result += toPython(child, state, indent + "\t",  scope + val(t, "name"))  # set the scope to function
        # add new line at the end of a function
        return result + "\n"

    # This makes input for a python function or method
    elif t.data == "argument_declaration":
        return ", ".join(f"args{arg}" for arg in range(len(t.children)))

    # return statement for a function
    elif t.data == "return":
        # empty return is default for python so no code is needed (unless it is not add the end)
        if len(t.children) > 0:
            return f"{indent}return {toPython(t.children[0], state, indent, scope)}\n"
        return f"{indent}return\n"

    elif t.data == "statement":  # pass it on with a newline for the next statement
        return f"{indent}{toPython(t.children[0], state, indent, scope)}\n"

    elif t.data == 'assignment':
        # Check the types of both sides of the assigment
        var = get(t, "variable") or get(t, "class_variable")
        leftSymbol = toSymbol(var, scope, line)
        leftType = symbolType(line, leftSymbol, scope)
        if leftType is None:
            raise StartError(f"In line {line}, the type of the left-hand side of the assignment could not be determined. Check the types used!")

        expr = get(t, "expression")
        rightSymbol = toSymbol(expr, scope, line)
        rightType = symbolType(line, rightSymbol, scope)
        if rightType is None:
            raise StartError(f"In line {line}, the type of the right-hand side of the assignment could not be determined. Check the types used!")

        if leftType != rightType and leftType != "*" and rightType != "*":
            raise StartError(f"For the assignment in line {line}, the left-hand side '{leftSymbol}' has a different type <{leftType}> than the right-hand side '{rightSymbol}' of type <{rightType}>!")
            # raise StartError(f"In line {line}: Type mismatch <%s> with <%s>." % (leftSymbol+":"+leftType, rightSymbol+":"+rightType))

        # Create the right hand side of the assignment
        expression = toPython(expr, state, '', scope)
        # check if the expression is an attribute of a Python object instead of a "just" a value
        if get(t, 'expression').children[0].data == 'variable' and len(get(t, 'expression').children[0].children) == 2:
            expression = f"getattr({expression})"

        if get(t, 'variable') is not None and len(get(t, 'variable').children) == 1:  # assigning a variable in the global scope
            var = val(var, 'name')
            if val(t, "assign_operator") == "->":
                return f"local_vars['{var}'] = {expression}"
            elif val(t, "assign_operator") == "=":
                return f"local_vars['{var}'] = {expression}.clone()"
            elif val(t, "assign_operator") == ":=":
                return f"{expression}.copy(local_vars['{var}'])"
        elif get(t, 'class_variable') is not None:  # class_variable is used
            var = toPython(var, state, '', scope)
            if val(t, "assign_operator") == "->":
                return f"{var} = {expression}"
            elif val(t, "assign_operator") == "=":
                return f"{var} = {expression}.clone()"
            elif val(t, "assign_operator") == ":=":
                return f"{expression}.copy({var})"
        else:
            var = toPython(var, state, '', scope)
            if val(t, "assign_operator") == "->":
                return f"setattr({var}, {expression})"
            elif val(t, "assign_operator") == "=":
                return f"setattr({var}, {expression}.clone())"
            elif val(t, "assign_operator") == ":=":
                return f"{expression}.copy(getattr({var}))"

    elif t.data == 'variable':  # variable Tree, so its bracketed
        if t.children[0].data == 'class_variable':  # a member of a class variable: self.coord ...
            name = toPython(get(t, "expression"), state, "", scope)
            if get(t.children[0], 'variable') is not None:  # a member of a member of a class variable: self.coord["x"]
                variable = val(get(t.children[0], 'variable'), 'name')
                variable_exists(variable, scope.split(".")[0], line)
                try:
                    name = f"{str(eval(name))}"
                except NameError:
                    name = f"str({name})"
                variable_exists(name, variables[scope.split(".")[0]][variable], line)
                return f"self.{variable}, {name}"
            else:  # a member of a member (expressed as variable) of a class variable: getitem(getitem(self, <variable>), name)
                # name checking is not possible here because the object is unknown due to the variable
                return f"{str(toPython(t.children[0], state, '', scope))}, str({name})"
        elif val(t, "name") is not None:
            if val(t, "name") == "this":
                variable_exists("this", scope, line)
                return f"self"

            variable_exists(val(t, "name"), scope, line)
            return f"local_vars['{val(t, 'name')}']"
        else:  # getitem from variable
            key = toPython(get(t, "expression"), state, "", scope)  # key is checked in toPython
            variable = val(get(t, 'variable'), 'name')
            # this tries to make the python code a bit more readable by making a key string into a python str
            try:
                key = f"'{str(eval(key))}'"
            except NameError:
                key = f"str({key})"

            if variable is None:  # deeply nested attribute calls need to be handled differently
                # Variable should be checked in the nesting
                variable = toPython(get(t, "variable"), state, "", scope)
                return f"getattr({variable}), {key}"
            variable_exists(variable, scope, line)
            return f"local_vars['{variable}'], {key}"

    elif t.data == "class_variable":  # Using "this[..]"
        if get(t, 'variable') is None:  # expression is used in this[<expr>]
            attr = toPython(t.children[0], state, indent, scope)
            # TODO: test using tosymbol if attr is correct type
            return f"self.__dict__[str({attr})]"

        variable = val(get(t, 'variable'), 'name')
        variable_exists(variable, scope.split(".")[0], line)
        return f"self.{variable}"

    elif t.data == "expression":  # just relay to the next Tree object
        return toPython(t.children[0], state, indent, scope)

    elif t.data == "function_call":
        # Get the function's name
        function = val(t, "function")
        prefix = ""

        arguments = toPython(get(t, 'arguments'), state, '', scope)

        # first parse the variable if it is there.
        variable = None
        if (var := get(t, "variable")) is not None:
            variable = toPython(var, state, "", scope)
            if variable == "self":
                symbol = scope.split(".")[0]
            else:
                symbol = symbolType(line, toSymbol(get(t, "variable"), scope, line), scope)
            if f"{symbol}.{function}" not in user_functions:
                raise StartError(f"In line {line}: Function <{function}> not defined in <{symbol}>!")
            return f"{variable}.{function}({arguments})"

        if function not in user_functions and function not in built_in_functions:
            raise StartError(f"In line {line}: Function or constructor {function} not defined in '{scope_2_str(scope if len(scope.split('.')) < 2 else '')}' scope!")

        if function in built_in_functions:
            function = built_in_function_names[function]
        result += f"{function}({arguments})"
        return result

    elif t.data in ["terms", "string_terms"]:
        if get(t, "number") is not None:
            return f"number({val(t, 'number')})"
        elif get(t, "string") is not None:
            return f"string({val(t, 'string')})"
        else:
            return toPython(get(t, t.children[0].data), state, "", scope)

    elif t.data == "arguments":
        result = []
        for child in t.children:
            if isinstance(child, Tree) and child.data in ["expression", "terms", "string_terms"]:
                if (get(child.children[0], 'variable') or get(child.children[0], 'class_variable')) is not None:
                    if len(get(child, child.children[0].data).children) == 2:
                        result.append(f"getattr({toPython(child, state, '', scope)})")
                        continue
                result.append(toPython(child, state, "", scope))
        return ", ".join(result)

    elif t.data == "constant":  # just return the token value
        if get(t, "number") is not None:
            return val(t, 'number')
        if get(t, "char") is not None:
            return val(get(t, 'char'), 'charvalue')
        if get(t, "string") is not None:
            return val(t, 'string')

    elif t.data == "if_block":
        # start an if block with an Enter
        result = f"\n{indent}if {toPython(get(t, 'expression'), state, '', scope)}:\n"
        result += toPython(get(t, 'block'), state, indent + '\t', scope)
        # check for else
        if (else_block := get(t, 'else_block')) is not None:
            result += f"\n{indent}else:\n"
            result += toPython(get(else_block, 'block'), state, indent + '\t', scope)
        return result

    elif t.data == "while_block":
        # start a while block with an Enter
        result = f"\n{indent}while {toPython(get(t, 'expression'), state, '', scope)}:\n"
        result += toPython(get(t, 'block'), state, indent + '\t', scope)
        return result

    # skip these as only their children need to be processed
    elif t.data in ["name", "function_member", "block", "type"]:
        for child in t.children:
            result += toPython(child, state, indent, scope)
    else:
        # print('Unknown instruction trying children: %s' % t.data)
        raise SyntaxError(f'Unknown instruction: {t.data}')

    return result

def compile(parse_tree):
    result = ""
    for inst in parse_tree.children:
        result += toPython(inst, state="", indent="", scope="")
    return result

def remove_none(tree):
    """ Recursively remove all None values from the tree. """
    if isinstance(tree, Tree):
        filtered_children = [remove_none(child) for child in tree.children if child is not None]
        return Tree(tree.data, filtered_children)
    else:
        return tree

class ParseTransform1(Transformer):
    def class_variable(self, items):
        """ This transforms the expression of the class_variable to a variable with a name or leave it as an expression """
        if items[0].children[0].data == "constant" and items[0].children[0].children[0].data == "string":
            line = find_line_numbers(items[0])
            token = Token('CNAME', items[0].children[0].children[0].children[0].value[1:-1])
            token.line = line
            name = Tree('name', [token])
            variable = Tree(Token('RULE', 'variable'), [name])
            return Tree('class_variable', [variable])
        return Tree('class_variable', items)

    def type(self, items):
        """ check if a type is not a keyword """
        if items[0].value in ["string", "char", "number"]:
            return Tree('type', items)

        if items[0].value in keywords:
            raise SyntaxError(f"ERROR: '{items[0].value}' is used as a name of a type. The name of a type can not be a keyword!")
        elif (items[0].value in python_keywords or
              items[0].value in built_in_function_names.values() or
              items[0].value in built_in_function_names.keys()):
            raise SyntaxError(f"ERROR: '{items[0].value}' is used as a name of a type but the name of a type can not be a restricted word!")
        return Tree('type', items)

    def name(self, items):
        """ check if a name is not a keyword """
        if items[0].value in keywords:
            raise SyntaxError(f"ERROR: '{items[0].value}' is used as a variable name or function name. The name of a variable or function can not be a keyword!")
        elif (items[0].value in python_keywords or
              items[0].value in built_in_function_names.values() or
              items[0].value in built_in_function_names.keys()):
            raise SyntaxError(f"ERROR: '{items[0].value}' is used as a name of a type but the name of a type can not be a restricted word!")
        return Tree('name', items)

    def comment(self, items):
        """ Remove comment from tree"""
        return None

    def WSE(self, items):
        """ Remove enters """
        return None

    def parentheses(self, items):
        """ Skip parentheses """
        return items[0]

    def instruction(self, items):
        """ Skip instructions """
        return items[0]

    def operation(self, items):
        """ Skip operation """
        return items[0]

    def function_call(self, items):
        """ transform function_calls, skip double and make infix to prefix"""
        # skip double function_calls
        if items[0].data == 'function_call' and len(items) == 1:
            return items[0]
        # prefix for math operators to functions
        elif items[0].data in ['math_operator', 'string_operator']:
            arguments = Tree('arguments', [items[1], items[2]])
            function = items[0]
            function.data = 'function'
            return Tree('function_call', [function, arguments])
        # fix "" to string notation, so "" is always the input of the string constructor.
        # This is done by marking the "string" part of the tree as complete,
        # otherwise a function call is added in "string"
        elif items[0].data == "function" and items[0].children[0].value in types:
            expression = []
            for child in items[1].children:
                expression.append(Tree('expression_complete', child.children))
            arguments = Tree('arguments', expression)
            return Tree('function_call', [items[0], arguments])
        elif len(items) > 1:
            # infix to prefix
            if items[1].data in ['operator2', 'math_operator', 'string_operator']:
                arguments = Tree('arguments', [items[0], items[2]])
                function = items[1]
                function.data = 'function'
                return Tree('function_call', [function, arguments])

        return Tree('function_call', items)

class ParseTransform2(Transformer):
    def function_member(self, items):
        """ empty function_members are removed (for example function_members containing a comment)"""
        if items[0] is None:
            return None
        return Tree('function_member', items)

    def expression_complete(self, items):
        """ Reset to expression, this functions as filter for string expressions"""
        return Tree('expression', items)

    def expression(self, items):
        """ This make sure that every string is processed using the String constructor """
        # find string expressions
        if items[0].data == "constant" and items[0].children[0].data in types:
            # find incomplete string expressions, they do not have the complete token
            # add the string function call to it, so that "" will be turned into string("")
            if len(items) == 1:
                expression = Tree('expression', items)
                arguments = Tree('arguments', [expression])
                token = Token('RULE', items[0].children[0].data)
                token.line = find_line_numbers(items[0])
                function = Tree('function', [token])
                function_call = Tree('function_call', [function, arguments])
                return Tree('expression', [function_call])
            else:  # remove complete token
                return Tree('expression', items[:1])

        return Tree('expression', items)

def main(fileName, long_names):
    with open(Path(__file__).parent / Path('start_grammar.ebnf'), 'r') as file:
        # Read the entire contents of the file into a string
        grammar = file.read()

    with open(fileName, 'r') as file:
        # Read the entire contents of the file into a string
        source = file.read() + "\n"  # Make sure there is always a proper end of file

    try:
        try:
            parser = Lark(grammar, parser='earley', propagate_positions=True)
            parse_tree = parser.parse(source)
        except UnexpectedInput as e:
            raise StartError(f"Syntax Error in line {e.line}: \n{e._context}")
    except StartError as e:
        print(e)
        exit()

    parse_tree = ParseTransform1().transform(parse_tree)
    parse_tree = ParseTransform2().transform(parse_tree)
    parse_tree = remove_none(parse_tree)

    # print(parse_tree.pretty())

    target = compile(parse_tree)

    # check at the end of the compiler of all types are defined
    for scope, var, var_type, line in type_warnings:
        if var_type not in types:
            raise StartError(f"In line {line}, the variable '{var}' in scope '{scope}' is defined as <{var_type}>, however, <{var_type}> is not defined! Make sure you define a type before you using it!")
        warnings.warn(f"In line {line}, the variable '{var}' in scope '{scope}' is defined as <{var_type}> before the type is declared. Make sure that you declare a type before using it (if possible)!")

    f = open((Path(fileName).parent.resolve() / Path(fileName).stem).with_suffix(".py"), "w")
    import_string = "from start_compiler import import_start\n\n"
    import_string += f"import_start.LONG_NAMES = {long_names}\n\n"
    import_string += "attrlist = dir(import_start)\n"
    import_string += "for attr in attrlist:\n"
    import_string += "\tif attr[:2] != '__':\n"
    import_string += "\t\tglobals()[attr] = getattr(import_start, attr)\n\n"

    import_string += target
    f.write(import_string)
    f.close()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python -m start_compiler.compile <source.start>")
        sys.exit(1)

    # check if the long names for printing is given as a flag
    long_names = True if '-n' in sys.argv else False  # find flag
    try:
        file_name = [arg for arg in sys.argv[1:] if Path(arg).suffix == ".start"][0]  # find filename
    except IndexError:
        raise RuntimeError("No filename wit a .start extension could be found as input! Use :python -m start_compiler.compile <source.start>")
    main(file_name, long_names)
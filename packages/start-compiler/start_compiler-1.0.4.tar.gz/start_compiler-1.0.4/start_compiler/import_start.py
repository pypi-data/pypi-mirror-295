import copy
import numpy as np
import gc
import traceback

class StronglyTypedDict(dict):
    def __init__(self, name):
        self.name = name
        self.__constants = {}
        super().__init__()

    def set_constant(self, key):
        self.__constants[key] = True

    def __setitem__(self, key, value):
        # Check if variable is constant
        if key in self.__constants:
            # Check first time assigning
            if self.__constants[key]:
                self.__constants[key] = False
            else:
                raise ValueError(f"The variable '{key}' in '{self.name}' is constant and can not be reassigned with the value '{value}'!")

        org_value = self.get(key)
        if org_value is not None:
            if type(org_value) != type(value):
                raise ValueError(f"The variable '{key}' in '{self.name}' is of type <{type(org_value).__name__}> and can not be set with <{type(value).__name__}>!")
        super().__setitem__(key, value)

    def __getitem__(self, item):
        try:
            return super().__getitem__(item)
        except KeyError:
            raise NameError(f"The variable '{item}' does not exist in the current scope of {self.name}, e.g., a function!")

_globalScope = True
local_vars = StronglyTypedDict('global')

class StartError(Exception):
    pass

class Start():
    type = None  # Makes each class strongly typed
    len = None  # needed for sequences

    def __init__(self):
        self._constants = {}

    def copy(self, other):
        for attr_name, attr_value in vars(self).items():
            vars(other)[attr_name] = copy.deepcopy(attr_value)

    def clone(self):
        return copy.deepcopy(self)

    def set_constant(self, key):
        self._constants[key] = True

    def find_object_name(self):
        """ Find the name of the object self"""
        # geneal references
        name = []

        # no variables are connected to this object, meaning that it is used in the init (maybe somewhere else)
        if not gc.get_referrers(self):
            return type(self).__name__

        for obj_ref in gc.get_referrers(self):
            if isinstance(obj_ref, dict):
                for attr_name, obj in obj_ref.items():
                    if obj is self:
                        # Try to identify the owner object of this dict
                        potential_owners = []
                        for potential_owner in gc.get_referrers(obj_ref):
                            if getattr(potential_owner, '__dict__', None) is obj_ref:
                                potential_owners.append(potential_owner.find_object_name())  # find the name of the variables that point to this object
                        if len(potential_owners) > 0:
                            name.append(f"{'/'.join(potential_owners)}.{attr_name}")
                        else:
                            name.append(attr_name)
            else:  # class attributes
                for attr_name in dir(obj_ref):
                    if getattr(obj_ref, attr_name) is self:
                        name.append(f"{Start.find_object_name(obj_ref)}.{attr_name}")

        # ignore local/global names space dict
        if name == ["StronglyTypedDict"]:
            return ""
        return "/".join(name)

    def trace_value_error(self, key, error, value=None, org_type=None):
        self.value_error(key, error, value, org_type)

        """
        This code recovers the line in the Python file with the original error.
        If we can somehow build a Python to Start code mapping then we can trace back which line in 
        the Start code created the error. This would make errors much easier to solve.
        """
        # try:
        #     self.value_error(key, error, value, org_type)
        # except ValueError as e:
        #     for stack in traceback.extract_stack():
        #         if stack.name == "<module>":
        #             print(stack, stack.lineno)
        #     raise(e)

    def value_error(self, key, error, value=None, org_type=None):
        name = self.find_object_name()
        if error == 0:
            raise ValueError(f"The variable '{name}' is of type <{type(self).__name__}> which is a constant type and can not be accessed with a name or key! The key '{key}' is used to access it. A '/' means that multiple variables point to the same object.")
        elif error == 1:
            raise ValueError(f"The variable '{name}' is of type <{type(self).__name__}> which is a complex type and can only be accessed with a name! The number '{key}' is used to access it. A '/' means that multiple variables point to the same object.")
        elif error == 2:
            raise ValueError(f"The variable '{name}' is of type <{type(self).__name__}> which is a sequence and can only be accessed with a number! The name '{key}' is used to access it. A '/' means that multiple variables point to the same object.")
        elif error == 3:
            raise ValueError(f"The variable '{name}' is of type <{type(self).__name__}> which is a sequence with a length of '{type(self).len}' and therefore it can not be set with index '{key}'! A '/' means that multiple variables point to the same object.")
        elif error == 4:
            raise ValueError(f"The variable '{name}' is of type '{type(self).__name__}' which does not contain '{key}' as attribute! A '/' means that multiple variables point to the same object.")
        elif error == 5:
            raise ValueError(f"The variable '{name}' is of type '{type(self).__name__}' which contains an attribute '{key}' that is of the unknown type {type(self).type[key]}!")
        elif error == 6:
            raise ValueError(f"The variable '{name}.{key}' is of type <{org_type.__name__}> and can not be set with <{type(value).__name__}>!")
        elif error == 7:
            raise ValueError(f"The variable '{name}.{key}' is constant and can not be reassigned with the value '{value}'!")

    def __eq__(self, other):
        for key, value in self.__dict__.items():
            if getattr(other, key) != value:
                return False

        return repr(self) == repr(other)

    def __getattr__(self, key):
        # only catch start objects
        if key[:2] == "__":
            return super(type(self), self).__getattribute__(key)

        # create an object if it does not exists
        if key not in self.__dict__ and type(self).len is np.inf:
            self.__dict__[key] = type(self).type()
            return self.__dict__[key]
        return super(type(self), self).__getattribute__(key)

    def __setattr__(self, key, value):
        # Skip if this is an attribute set in the init of a class
        if key == "value" or key == "_constants":
            return super().__setattr__(key, value)

        if key in self._constants:
            # Check first time assigning
            if self._constants[key]:
                self._constants[key] = False
            else:
                self.trace_value_error(key, 7, value)

        # check if a correct key is used
        if isinstance(self, char | number):
            if key != "value":
                self.trace_value_error(key, 0)
        elif isinstance(type(self).type, dict) and key.lstrip("-").isdigit():  # a complex type should not be accessed with a number
            self.trace_value_error(key, 1)
        elif not isinstance(type(self).type, dict):
            if not key.isdigit():  # a sequence should be a number
                self.trace_value_error(key, 2)
            elif int(key) >= type(self).len:  # the index should fit a sequence with a constant length.
                self.trace_value_error(key, 3)

        # check for correct type
        org_type = type(getattr(self, key, None))
        if isinstance(None, org_type):
            if isinstance(type(self).type, dict):  # Check if the type is complex not a sequence
                if key not in type(self).type:  # Check if the key exists
                    self.trace_value_error(key, 4)
                if type(self).type[key] == type(value).__name__:  # check type by name as both the compiler and import_start do not have access to new python classes
                    org_type = type(value)
                else:  # This could happen if variables are used to circumvent the compiler
                    self.trace_value_error(key, 5)
            else:
                org_type = type(self).type

        if not isinstance(value, org_type):
            self.trace_value_error(key, 6, value, org_type)
        super().__setattr__(key, value)

    def __len__(self):
        return len([k for k in self.__dict__ if k[0] != "_"])

    def __bool__(self):
        return bool(self.value)

    def __str__(self):
        return f"{''.join(str(value) for key, value in self.__dict__.items() if (hasattr(value, 'value') or isinstance(value, Start)) and key[0] != '_')}"

    def __repr__(self):
        # check which flag is used a compile time, this global is dynamically added to the file
        if LONG_NAMES:
            return f"{type(self).__name__}({', '.join(('index ' + key if key.isdigit() else key) + ' = ' + repr(value) for key, value in self.__dict__.items() if hasattr(value, 'value') or isinstance(value, Start))})"
        return f"[{', '.join(repr(value) for key, value in self.__dict__.items() if (hasattr(value, 'value') or isinstance(value, Start)) and key[0] != '_')}]"


class number(Start):
    type = int | float

    def __init__(self, value=0):
        super().__init__()
        try:
            self.value = float(value)
        except ValueError:
            raise ValueError(f"The value '{value}' is not a number!")

    def __str__(self):
        return str(int(self.value) if int(self.value) == self.value else self.value)

    def __repr__(self):
        return repr(int(self.value) if int(self.value) == self.value else self.value)

class char(Start):
    type = str

    def __init__(self, value=''):
        super().__init__()
        if isinstance(value, int):
            self.value = str(chr(value))
        else:
            self.value = str(value)

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value

class string(Start):
    type = str

    def __init__(self, value=""):
        super().__init__()
        self.value = str(value)

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value

def _print(*args):
    """ Normal print """
    _print_general(repr, " ", *args)

def _print_general(print_option, delimiter, *args):
    """ general print """
    r = []
    for obj in args:
        if isinstance(obj, Start):
            r.append(print_option(obj))
        elif obj is not None:
            r.append(obj)
    print(delimiter.join(r))

def _print_memory_obj(*args):
    """ print memory"""
    _print_general(str, "", *args)

def _input_number():
    i = input()
    try:
        float(i)
    except ValueError:
        raise TypeError(f"The input '{i}' is not a number!")
    return number(i)

def _input_char():
    i = input()
    if len(i.strip()) != 1:
        raise TypeError(f"The input '{i}' is not a char!")
    return char(i)

def _input_string():
    i = input()
    return string(i)

def _len(obj):
    return number(len(obj))

def _add(n1, n2):
    if not isinstance(n2, type(n1)):
        raise ValueError(f"Can not add two objects that are not both numbers! The types are {type(n1).__name__} and {type(n2).__name__}.")
    return number(n1.value + n2.value)

def _add_string(n1, n2):
    if not isinstance(n2, string) or not isinstance(n1, string):
        if isinstance(n2, number) and isinstance(n1, number):  # TODO: temporarily fix
            return _add(n1, n2)
        raise ValueError(f"Can not concatenate two objects that are not both strings! The types are {type(n1).__name__} and {type(n2).__name__}.")
    return string(repr(n1) + repr(n2))

def _sub(n1, n2):
    return number(n1.value - n2.value)

def _mul(n1, n2):
    return number(n1.value * n2.value)

def _div(n1, n2):
    return number((float)(n1.value) / (float)(n2.value))

def _mod(n1, n2):
    return number(n1.value % n2.value)

def _pow(n1, n2):
    return number(n1.value ** n2.value)

def _eqlVal(n1, n2):
    return number(n2 == n1)

def _eqlRef(n1, n2):
    return number(n2 is n1)

def _gt(n1, n2):
    return number(n1.value > n2.value)

def _lt(n1, n2):
    return number(n1.value < n2.value)

def _gte(n1, n2):
    return number(n1.value >= n2.value)

def _lte(n1, n2):
    return number(n1.value <= n2.value)

def _and(n1, n2):
    return number(n2.value != 0 and n1.value != 0)

def _or(n1, n2):
    return number(n2.value != 0 or n1.value != 0)

def _not(n1):
    return number(n1.value == 0)

def _bool(n):
    return n.value != 0

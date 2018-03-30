from .bits import Bits
from ..ast.base import _make_name

from .. import operations
from .bool import Bool
from .bv import BV


class String(Bits):
    """
    Base class that represent the AST of a String object and implements all the operation useful to create and modify the AST.

    Do not instantiate this class directly, instead use StringS or StringV to construct a symbol or value, and then use
    operations to construct more complicated expressions.
    """
    def __init__(self, *args, **kwargs):
        str_len = kwargs['length']
        kwargs['length'] *= 8
        super(String, self).__init__(*args, **kwargs)
        self.string_length = str_len

    def __getitem__(self, rng):
        if type(rng) is slice:
            high = rng.start / 8 if rng.start is not None else self.string_length - 1
            low = rng.stop / 8 if rng.stop is not None else 0
            if high < 0:
                high = self.string_length + high
            if low < 0:
                low = self.string_length + low

            # Because we are indexing from the end, what was high becomes low and vice-versa
            high_str_idx = self.string_length - 1 - low
            low_str_idx = self.string_length - 1 - high
            return StrExtract(low_str_idx, high_str_idx + 1 - low_str_idx, self)
        else:
            return Substr(int(rng+7), int(rng), self)

def StringS(name, size, uninitialized=False, explicit_name=False, **kwargs):
    """
    Create a new symbolic string (analogous to z3.String())

    :param name:                 The name of the symbolic string (i. e. the name of the variable)
    :param size:                 The size in bytes of the string (i. e. the length of the string)
    :param uninitialized:        Whether this value should be counted as an "uninitialized" value in the course of an
                                 analysis.
    :param bool explicit_name:   If False, an identifier is appended to the name to ensure uniqueness.

    :returns:                    The String object representing the symbolic string
    """
    n = _make_name(name, size, False if explicit_name is None else explicit_name)
    result = String("StringS", (n, uninitialized), length=size, symbolic=True, eager_backends=None, uninitialized=uninitialized, variables={n}, **kwargs)
    return result

def StringV(value, length=None, **kwargs):
    """
    Create a new Concrete string (analogous to z3.StringVal())

    :param value: The constant value of the concrete string

    :returns:                    The String object representing the concrete string
    """

    if length is None:
        length = len(value)

    if length < len(value):
        raise ValueError("Can't make a concrete string value longer than the specified length!")

    result = String("StringV", (value, len(value)), length=length, **kwargs)
    return result

StrConcat = operations.op('StrConcat', (String, String), String, calc_length=operations.concat_length_calc, bound=False)
StrSubstr = operations.op('StrSubstr', (BV, BV, String),
                        String, calc_length=operations.substr_length_calc, bound=False)
StrExtract = operations.op('StrExtract', ((int, long), (int, long), String),
                              String, extra_check=operations.str_extract_check,
                              calc_length=operations.str_extract_length_calc, bound=False)
StrLen = operations.op('StrLen', (String, int), BV, calc_length=operations.strlen_bv_size_calc, bound=False)
StrReplace = operations.op('StrReplace', (String, String, String), String,
                        extra_check=operations.str_replace_check,
                        calc_length=operations.str_replace_length_calc, bound=False)
StrContains = operations.op("StrContains", (String, String), Bool, bound=False)
StrPrefixOf = operations.op("StrPrefixOf", (String, String), Bool, bound=False)
StrSuffixOf = operations.op("StrSuffixOf", (String, String), Bool, bound=False)
StrIndexOf = operations.op("StrIndexOf", (String, String, int), BV, calc_length=operations.strindexof_bv_size_calc, bound=False)
StrToInt = operations.op("StrToInt", (String, int), BV, calc_length=operations.strtoint_bv_size_calc, bound=False)

# Equality / inequality check
String.__eq__ = operations.op('__eq__', (String, String), Bool)
String.__ne__ = operations.op('__ne__', (String, String), Bool)

# String manipulation
String.__add__ = StrConcat
String.StrSubstr = staticmethod(StrSubstr)
String.StrExtract = staticmethod(StrExtract)
String.StrConcat = staticmethod(StrConcat)
String.StrLen = staticmethod(StrLen)
String.StrReplace = staticmethod(StrReplace)
String.StrContains = staticmethod(StrContains)
String.StrPrefixOf = staticmethod(StrPrefixOf)
String.StrSuffixOf = staticmethod(StrSuffixOf)
String.StrIndexOf = staticmethod(StrIndexOf)
String.StrToInt = staticmethod(StrToInt)
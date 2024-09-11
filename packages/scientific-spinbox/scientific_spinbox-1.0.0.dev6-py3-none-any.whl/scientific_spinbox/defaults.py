THOUSAND_SEPARATOR = ' '
UNIT_SEPARATOR = ' '
_default_interface = None

multiplier_symbols = {
    "micro": {
        "preferred": "u",
        "possibles": ['u', 'µ', 'μ']
    },
}

def set_default_interface(interface):
    global _default_interface
    _default_interface = interface

def get_default_interface():
    global _default_interface
    return _default_interface
from __future__ import print_function

__version__ = '2.2.0'

try:
    from .prompt import prompt
    from .questions import Text, Password, Confirm, List, Checkbox, \
        load_from_dict, load_from_json

    __all__ = ['prompt', 'Text', 'Password', 'Confirm', 'List', 'Checkbox',
               'load_from_list', 'load_from_dict', 'load_from_json']
except ImportError as e:
    print("An error was found, but returning just with the version: %s" % e)

__version__ = '0.0.2'

import os
import importlib
import inspect

def auto_import_functions():
    for name in os.listdir(os.path.dirname(__file__)):
        if os.path.isdir(os.path.join(os.path.dirname(__file__), name)) and not name.startswith('__'):
            try:
                module = importlib.import_module(f'.{name}', package=__name__)
                for item_name, item in inspect.getmembers(module):
                    if not item_name.startswith('_'):
                        globals()[item_name] = item
            except ImportError as e:
                print(f"Failed to import module {name}: {e}")

auto_import_functions()
del auto_import_functions

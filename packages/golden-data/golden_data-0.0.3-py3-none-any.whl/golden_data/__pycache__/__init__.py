
import importlib
import inspect

def auto_import_functions():
    for name in os.listdir(os.path.dirname(__file__)):
        if name.endswith('.py') and not name.startswith('__'):
            module = importlib.import_module(f'.{name[:-3]}', package=__name__)
            for item_name, item in inspect.getmembers(module):
                if inspect.isfunction(item) and not item_name.startswith('_'):
                    globals()[item_name] = item

auto_import_functions()
del auto_import_functions

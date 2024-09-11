from setuptools import setup, find_packages
import os 

root_dir = 'golden_data'
version = '0.0.2'

# 创建缺失的 __init__.py 文件
for subdir, dirs, files in os.walk(root_dir):
    if '__init__.py' not in files:
        init_file_path = os.path.join(subdir, '__init__.py')
        with open(init_file_path, 'w') as f:
            # 添加自动导出代码
            f.write("""
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
""")
        print(f'Created __init__.py with auto-export in {subdir}')

# 创建顶层 __init__.py
with open(os.path.join(root_dir, '__init__.py'), 'w') as file:
    file.write(f"__version__ = '{version}'\n")
    file.write("""
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
""")

with open('./requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='golden_data',
    version=version,
    author='gquant',
    description='quantitative financial data collector.',
    packages=find_packages(),
    package_data={
        'golden_data': ['*.*', '**/*.*']
    }, 
    include_package_data=True,
    install_requires=requirements, 
)

from setuptools import setup, find_packages
import os

root_dir = 'golden_data'
version = '0.0.3'

# 遍历 root_dir 下的所有 .py 文件，并将 from .xxx import * 写入 __init__.py
init_content = []
for subdir, dirs, files in os.walk(root_dir):
    if not '__init__.py' in files:
        init_file_path = os.path.join(subdir, '__init__.py')
        open(init_file_path, 'a').close()
        print(f'Created __init__.py in {subdir}')

    for file in files:
        if file.endswith('.py') and file != '__init__.py':
            module_name = os.path.splitext(file)[0]
            init_content.append(f"from .{module_name} import *")

# 将内容写入 __init__.py
init_file_path = os.path.join(root_dir, '__init__.py')
with open(init_file_path, 'w') as init_file:
    init_file.write(f"__version__ = '{version}'\n")
    init_file.write("\n".join(init_content))

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
from setuptools import setup, find_packages
import os 

root_dir = 'golden_data'
version='0.0.1'

for subdir, dirs, files in os.walk(root_dir):
    if not '__init__.py' in files:
        init_file_path = os.path.join(subdir, '__init__.py')
        open(init_file_path, 'a').close()
        print(f'Created __init__.py in {subdir}')

with open('./__init__.py', 'w') as file:
    file.write(f"__version__ = '{version}'\n")


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


from setuptools import setup, find_packages

# pip install -m venv venv
# source venv/bin/activate
# pip install pytest
# venv/bin/pytest

# pip install build twine
# python -m build
# python -m twine upload --verbose dist/happydata-0.0.2*
# pip install happydata

setup(
    name='happydata',
    version='0.0.3',
    author="Daqian",
    packages=find_packages(exclude=['tests', 'tests.*','venv']),
    zip_safe=False,
    description='happy data loading,writing, transforming without third party library',
    long_description='happy data loading,writing, transforming without third party library',
    license='MIT license',
    keywords=['data', 'data loading', 'data writing', 'data transforming','json','jsonl','gz'],
    platforms='Independant',
    url='https://github.com/daqiancode/happydata',
)
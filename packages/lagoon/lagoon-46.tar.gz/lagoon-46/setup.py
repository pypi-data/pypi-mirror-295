from setuptools import find_packages, setup

def long_description():
    with open('README.md') as f:
        return f.read()

setup(
    name = 'lagoon',
    version = '46',
    description = 'Concise layer on top of subprocess, similar to sh project',
    long_description = long_description(),
    long_description_content_type = 'text/markdown',
    url = 'https://pypi.org/project/lagoon/',
    author = 'foyono',
    author_email = 'shrovis@foyono.com',
    packages = find_packages(),
    py_modules = ['screen'],
    install_requires = ['aridity>=73', 'diapyr>=25'],
    package_data = {'': ['*.pxd', '*.pyx', '*.pyxbld', '*.arid', '*.aridt', '*.dkr']},
    entry_points = {'console_scripts': []},
)

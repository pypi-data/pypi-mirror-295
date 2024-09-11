from setuptools import setup, find_packages

setup(
    name='exem-odoo',
    version='1.0.2',
    description='Odoo API in it\'s greatest simplicity.',
    long_description_content_type='text/markdown',
    long_description=open('README.md').read(),
    url='https://gitlab.com/exem2/libraries/api/odoo',
    author='Félix BOULE--REIFF',
    author_email='boulereiff@exem.fr',
    license='BSD 2-clause',
    install_requires=[],
    py_modules=[
        'Odoo',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: BSD License'
    ],
)

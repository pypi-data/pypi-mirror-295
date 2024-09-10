# setup.py
from setuptools import setup, find_packages

setup(
    name='text_processor_nlp',
    version='0.1',
    packages=find_packages(),
    install_requires=['spacy>=3.0.0',], 
    author='Farhan Siddiqui',
    author_email='Farhan.siddiqui1572@gmail.com',
    description='A short description of the package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/SiddiqueFarhan/pypi_demo',  

    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)

# setup.py
from setuptools import setup, find_packages

setup(
    name='printingpackagebyfarhan',
    version='0.2',
    packages=find_packages(),
    install_requires=[],  # Add dependencies here if needed
    author='Farhan Siddiqui',
    author_email='Farhan.siddiqui1572@gmail.com',
    description='A short description of the package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/SiddiqueFarhan/pypi_demo',  # Replace with your GitHub repo URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)

import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst'), 'rb') as rdm:
    README = rdm.read()

setup(
    name='busy',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    description='Python Programing Editor',
    long_description=README.decode(),
    url='https://github.com/naritotakizawa/busy',
    author='Narito Takizawa',
    author_email='toritoritorina@gmail.com',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    entry_points={'console_scripts': [
        'busy = busy.main:main',
        'busy-simple = busy.simple:main',
    ]},
    install_requires=['flake8', 'Pygments'],
)

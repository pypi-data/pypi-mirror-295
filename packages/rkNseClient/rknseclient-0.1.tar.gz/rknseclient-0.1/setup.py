# setup.py

from setuptools import setup, find_packages

setup(
    name='rkNseClient',
    version='0.1',
    author='kamalkavin96',
    author_email='kamalkavin68@gmail.com',
    description='A Python client for NSE API to fetch stock data and indices',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/kamalkavin68/rk-nse-client',
    packages=find_packages(),
    install_requires=['requests'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

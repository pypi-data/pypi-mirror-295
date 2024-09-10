from setuptools import setup, find_packages

setup(
    name='rkNseClient',
    version='0.4',
    packages=find_packages(),
    install_requires=[
        "pandas==2.2.2" ,
        "pydantic==2.9.1" ,
        "requests==2.32.3" ,
        "setuptools==74.1.2" ,
        "wheel==0.44.0" ,
        "twine==5.1.1"
    ],
    description='A short description of the package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='kamalkavin96',
    author_email='kamalkavin68@gmail.com',
    url='https://github.com/kamalkavin68/rkNseClient',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)

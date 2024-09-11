from setuptools import setup, find_packages

setup(
    name='pywithmysql',
    version='0.2.0',
    description='The library to work with mysql for python',
    author='DanikBlatota777',
    author_email='danylo29bro@gmail.com',
    url='https://github.com/hardusss/pywithmysql',
    packages=find_packages(),
    install_requires=[
        'pymysql',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

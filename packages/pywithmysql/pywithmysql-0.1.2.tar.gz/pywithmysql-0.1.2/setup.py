
#### 2. **Розміщення `README.md` у `setup.py`**

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='pywithmysql',
    version='0.1.2',
    description='The library to work with MySQL databases for Python',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/hardusss/pywithmysql',
    author='DanikBlatota777',
    author_email='danylo29bro@gmail.com',
    packages=find_packages(),
    install_requires=[
        'pymysql'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

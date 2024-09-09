from setuptools import setup, find_packages

VERSION = '0.1.3'
DESCRIPTION = 'Esse pacote só diz égua'
LONG_DESCRIPTION = ""

with open("./README.md", "r", encoding="utf-8") as fh:
    LONG_DESCRIPTION = fh.read()

setup(
        name="dizegua",
        version=VERSION,
        author="Thalyson Wilker",
        author_email="thalison.wilker@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[],
        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)
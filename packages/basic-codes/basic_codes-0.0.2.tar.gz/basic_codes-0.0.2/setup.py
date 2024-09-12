from setuptools import setup, find_packages

VERSION = '0.0.2' 
DESCRIPTION = 'A collection of basic Python topics with sample code for learning.'
LONG_DESCRIPTION = '''This package includes a variety of basic Python programming topics,
                   complete with sample code and explanations to aid in learning Python.
                   It is designed for beginners who want to get a solid understanding of fundamental Python concepts.
                   The topics covered include basic syntax, data structures, control flow, functions, and more.
                   This package aims to provide a hands-on approach to learning by offering practical examples and exercises.'''

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="basic_codes", 
        version=VERSION,
        author="Fawaskp",
        author_email="<fawaskp1010@gmail.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'

        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ],
        license='MIT',
)
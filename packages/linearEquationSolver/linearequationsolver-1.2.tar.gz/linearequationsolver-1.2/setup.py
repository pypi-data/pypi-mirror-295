from setuptools import setup,find_packages

long_descript = open("README.md").read()

setup(
    name="linearEquationSolver",
    version="1.2",
    description="Module to solve linear equations in 2 and 3 variables",
    long_description_content_type="text/markdown",
    long_description= long_descript,
    license="MIT",
    author="Sanjeevan Rames",
    author_email="sanjeevanrames11@gmail.com",
    packages=find_packages(exclude=["tests"]),
    install_requires=[],
    keywords=["python","linear Equation"]
    
)
from setuptools import setup,find_packages

setup(
    name="linearEquationSolver",
    version="1.1",
    description="Module to solve linear equations in 2 and 3 variables",
    license="MIT",
    author="Sanjeevan Rames",
    author_email="sanjeevanrames11@gmail.com",
    packages=find_packages(exclude=["tests"]),
    install_requires=[],
    keywords=["python","linear Equation"]
)
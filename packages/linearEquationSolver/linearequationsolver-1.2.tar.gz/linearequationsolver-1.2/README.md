# Linear Equation Solver

This package is to solve linear equations of two variables and three variables

## License

refer to LICENSE in github

## Installation

```bash
pip install linearEquationSolver==1.1

```

## Usage

Say you have these equations: 2x+y=15, 3x-y=5

The numbers of the first equation: 2,1,15 should be added in an array and the numbers of the second equation: 3,-1,5 in another array
```python
import linearEquation

eqOne = [2,1,15]
eqTwo = [3,-1,5]

print(linearEquation.linearEquationsTwo(eqOne,eqTwo))
```
The output will be a tuple: ('4.000', '7.000')

The usage of linearEquationThree is similar to linearEquationTwo, except each array would have one more value in it and a third array is needed
For instance: x-y+z=2, 2x-y-z=-6, 2x+2y+z = -3

```python
import linearEquation

eqOne = [1,-1,1,2]
eqTwo = [2,-1,-1,-6]
eqThree = [2,2,1,-3]

print(linearEquation.linearEquationThree(eqOne,eqTwo,eqThree))
```
The output is as follows: ('-2.000', '-1.000', '3.000')

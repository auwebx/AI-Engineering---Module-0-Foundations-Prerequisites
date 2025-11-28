from utils.math_utils import add, Calculator

print(add(10, 20))
calc = Calculator("TestCalc")
calc.add_and_record(5, 7)
calc.add_and_record(100, 337)
print(calc.get_history())
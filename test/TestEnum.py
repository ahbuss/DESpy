from Simkit import Priority

print(Priority.HIGH.value)
print(type(Priority.HIGH.value))
print(type(Priority.LOW))

print( (1.0, Priority.HIGH.value) > (1.0, Priority.HIGHER.value))
# print()
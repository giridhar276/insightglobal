
# all the list of builtin functions and exceptions in python
print(dir(__builtins__))

val = 10
print(id(val))
alist = [10,20,20]
print(id(alist))

# range(start,stop,step)
print(list(range(10)))
print(list(range(2,10,2)))
print(list(range(1,10,2)))
alist = [10,20]
print(max(alist))
print(min(alist))
print(sum(alist))

name = input("Enter you name:")
print(name)
age = input("enter your age:")
print("after after 10 years:" , age + 10)
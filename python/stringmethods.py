

name = "python programming"
# slicing 
# string[start:stop:step]
print(name[0:5])
print(name[7:10])
print(name[0:18:2])
print(name[::])
print(name[:])
print(name[-1])
print(name[-6:-2:-1])
print(name[::-1])

# methods
print(name.upper())
print(name.isupper()) 
print(name.lower())
print(name.islower())
print(name.split(" "))
print(name.replace("python", "java"))
aname = "  python   "
print(len(aname))
print(len(aname.strip()))
print(len(aname.lstrip()))
print(len(aname.rstrip()))
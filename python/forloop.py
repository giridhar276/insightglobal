#string
name = "python"
for char in name:
    print(char)
#list
numbers = [10,20,30,40,50]
for num in numbers:
    print(num)

#dictionary - display keys
book = {"chap1":10 ,"chap2":20,"chap3":30}
for key in book.keys():
    print(key)
#dictionary - display values
for value in book.values():
    print(value) 
# dictionary - display key-value pairs
for key,value in book.items():
    print(key, ":", value)

# set 
aset = {10,10,10,20,30,30,30}
for value in aset:
    print(value)
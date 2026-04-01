alist = [34,56,32,67,89,23,64]
# list.append(value) - add a single value to the end of the list
alist.append(50)

#list.extend(list) - add multiple values to the end of the list
alist.extend([90,100,110])

# list.insert(index, value) - insert a value at a specific index
alist.insert(2, 45) 

# list.pop(index) - remove and return the value at the specified index (default is the last item)
alist.pop(0)

#list.remove(value )
if 32 in alist:
    alist.remove(32)
else:
    print("Value not found in the list")

alist.sort() # sort the list in ascending order
print(alist)
alist.sort(reverse=True) # sort the list in descending order
print(alist)

alist.reverse()
print(alist)

# get the count of values
print(alist.count(67))

print(alist.index(89))
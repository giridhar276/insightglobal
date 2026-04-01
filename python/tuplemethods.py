
## tuple is immutable 

atup = (40,50,60)

getcount = atup.count(50) # count the occurrences of a value in the tuple
print(getcount)

print(atup.index(40))


atup = (40,50,60)

#atup[0] = 400
print(atup)
## typecasting - convert from one object to another object
atup = (40,50,60)
alist = list(atup)
alist.append(70)
atup = tuple(alist)
print(atup)
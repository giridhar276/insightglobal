
# set is UNORDEDED collection of UNIQUE items of same type
aset = {10,10,20,30,30}
bset = {30,30,30,40,50,50}
print(aset)
print(bset)

print(aset.union(bset)) # combine two sets and return a new set with unique values
print(aset.intersection(bset)) # return a new set with values that are common to both sets
print(aset.difference(bset)) # return a new set with values that are in aset but not in bset


print(aset.issubset(bset)) # check if aset is a subset of bset
print(aset.issuperset(bset)) # check if aset is a superset of bset
print(aset.isdisjoint(bset)) # check if aset and bset have no common


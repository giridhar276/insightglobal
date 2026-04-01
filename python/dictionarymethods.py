book = {"chap1":10 ,"chap2":20,"chap3":30}
# add new key-value pair
book["chap4"] = 40
book["chap5"] = 50
book["chap6"] = 60
print(book)
# display values
print(book["chap1"])
print(book["chap2"])

# dictionary methods 
print(book.keys()) # get all the keys in the dictionary
print(book.values()) # get all the values in the dictionary
print(book.items()) # get all the key-value pairs in the dictionary

book.pop("chap1") # remove a key-value pair by key
print(book)
book.popitem() # remove the last key-value pair added to the dictionary
print(book)


### combining two dictionaries
book = {"chap1":10 ,"chap2":20,"chap3":30}
newbook = {"chap4":40 ,"chap5":50,"chap6":60}
 
finalbook = { **book, **newbook} # merge two dictionaries
print("updated dictionary:", finalbook)

book.update(newbook) # book is updated with the key-value pairs from newbook
print("updated dictionary:", book)
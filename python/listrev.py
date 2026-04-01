alist = [10,20,30,40,30]
revlist = []

for val in alist:
    revlist = [val] + revlist 

print(revlist)

uniquelist = []
sentences = ["hello world", "hello python", "data world"]
for string in sentences:
    data = string.split(" ") 
    uniquelist.extend(data)

print(list(set(uniquelist  )))

# fixed arguments
def display(a,b):
    print(a,b)
display(10,20)

# default arguments 
def display(a = 0,b = 0,c = 0,d = 0):
    print(a,b,c,d)
display()       # 0 0 0 0
display(10)     # 10 0 0 0
display(10,20)  # 10 20 0 0
display(10,20,30)  # 10 20 30 0
display(10,20,30,40) # 10 20 30 40  

#keyword arguments
def display(b,a,c):
    print(a,b,c)
display(c=30,a=10,b=20) 

# variable length arguments
def display(*data):
    print(data)
    print("Max:",max(data))
    for val in data:
        print(val)
display(10,20,30,40,50,60,70,80,90,100,45,3,56,32,64,3,6445)

def displayinfo(**data):
    print(data)
displayinfo(chap1 = 10 , chap2 = 20)




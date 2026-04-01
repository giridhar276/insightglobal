# Every OS contains processes that keeps running 
# EVery process contains system calls
# traditional way 
# fixed arguments
def display(a,b):
    c = a + b
    return c
total = display(10,20)
print(total)

# pythonic way
# lambda function 
# lambda is the replacement of single line function
# faster in execution than normal function
#functionname = lambda variables : expression
display = lambda a,b  : a + b
total = display(10,20)
print(total)

# lambda with condition
greatest = lambda a,b : a if a > b else b
output = greatest(10,20) 



upper = lambda s: s.upper()
print(upper("hello"))  # HELLO


result = lambda marks: "Pass" if marks >= 35 else "Fail"
print(result(30))  # Fail
  

#  Positive, Negative or Zero
sign = lambda x: "Positive" if x > 0 else "Negative" if x < 0 else "Zero"
print(sign(-5))  # Negative

2024

leap_year = lambda y: "Leap" if (y % 4 == 0 and y % 100 != 0) or (y % 400 == 0) else "Not Leap"
print(leap_year(2020))  # Leap
print(leap_year(2019))  # Not Leap

password_check = lambda pwd: "Strong" if len(pwd) >= 8 else "Weak"
print(password_check("pass123"))  # Weak


################################# map(function,iterable)###############

alist = [10,20,30,40]
# [15,25,35,45]   

blist = []
for val in alist:
    blist.append(val + 5)
print(blist)

def increment(x):
    return x + 5
#########map(function,iterable)
print(list(map(increment,alist)))

#######################
## map with  lambda function
print(list(map(lambda x : x+5,alist)))




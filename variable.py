
#1.
pi = 22 / 7
print("Value of pi:", pi)
print("Data type:", type(pi))

#2.
# for = 4
# print(for)

# Why does this happen? for is a reserved keyword in Python — it's part of the language's grammar (used for loops). Python has 35 keywords like for, if, while, class, return, etc. These cannot be used as identifiers (variable/function names). Fix: rename to for_val = 4 or number = 4.

#3.
principal = 10000  
rate      = 5    
time      = 3     
simple_interest = (principal * rate * time) / 100
print("Principal Amount : ₹", principal)
print("Rate of Interest : ", rate, "%")
print("Time            : ", time, "years")
print("Simple Interest : ₹", simple_interest)
age = int(input("enter age:"))
if(age < 18):
    print("Cannot vote")
else:
    print("can vote")


n1,n2,n3 = int(input("Enter 3 numbers: "))
if(n1>=n2 and n1>=n3):
    print(n1," is bigger")
elif(n2>=n1 and n2>=n3):
    print(n2," is bigger")
else:
    print(n2," is bigger")


num = int(input("Enter a number: "))
if(num%7==0):
    print(num," is divisible by 7")
else:
        print(num," is divisible not by 7")

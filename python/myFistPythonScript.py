name = "Frank"
age = 80
if age < 50:
    print("You are young")
elif age == 50:
    print("You are old")
else:
    print("Yes youre old, but dont worry")

if name == "Saul":
    print("Hello there " + name)
else:
    print("You are not " + name)

nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
totalOfSum = 0
for num in nums:
    totalOfSum = totalOfSum + num
    print(totalOfSum)
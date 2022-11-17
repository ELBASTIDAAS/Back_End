from config import me

print(me)


#read

print(me["first"])
print(me['first'] + " " + me['last'])

#modify
me["first"] = "Miguel B."
print(me["first"])

#add new key
me["prefered_color"] = "blue"
print(me)


address = me["address"]
print(str(address["number"]) + " " + address["street"] + " " + address["city"])
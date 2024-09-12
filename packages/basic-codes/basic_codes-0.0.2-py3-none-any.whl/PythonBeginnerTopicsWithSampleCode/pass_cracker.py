from random import randint
import os

'''
not practical (not working)
'''

user_pass = input("Enter  Your password here")

comps = []
special_characters = "!@#$%^&*()-=_+[]{}|;:'\",.<>/?`~"

comps.extend([chr(i) for i in range(ord('a'), ord('k') + 1)])
# comps.extend([chr(i) for i in range(ord('A'), ord('Z') + 1)])
comps.extend([str(i) for i in range(1,7)])
# comps.extend(list(special_characters))

pwd = ""
guessed = []
print(comps)
print(len(comps))
while (pwd!=user_pass ):
    pwd = ""
    for char in range(len(comps)):
        guess_pwd = comps[randint(0,len(comps)-1)]
        pwd = str(guess_pwd) + str(pwd)
        if pwd == user_pass:
            break
        print(pwd)
        # os.system("clear")
    # guessed.append(pwd)

print('Your Password is ',pwd)
print(guessed)

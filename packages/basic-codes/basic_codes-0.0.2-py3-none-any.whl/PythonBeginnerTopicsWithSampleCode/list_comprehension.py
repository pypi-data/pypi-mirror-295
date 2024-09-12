'''
Find all of the numbers from 1 to 80 that are divisible by 8
'''
# result  = [num for num in range(81) if num%8 ==0 ] 


'''
Count the number of spaces in a string
'''
# string = "Practice Problems to Drill List Comprehension in Your Head."
# result  = len([char for char in string if char == ' ']) 


'''
Remove all of the vowels in a string (use string above)
'''
# vowels = 'aeiouAEIOU'
# result = "".join([char for char in string if char not in vowels])


'''
Use a dictionary comprehension to count the length of each word in a sentence
'''
# words = string.split(' ')
# result = {word:len(word) for word in words}


'''
Use a nested list comprehension to find all of the numbers from 1 to 1000 that are divisible by any single digit besides 1 (2 to 9)
'''
# divisibles = [2,3,4,5,6,7,8,9]
# result = [num for num in range(1,1001) if True in [num%n==0 for n in divisibles] ]
# print(result)
def descending_order(num):
    list = str(num)
    newlist = int(''.join(sorted(list, reverse=True)))
    return newlist


print(descending_order(12345679))


def isisogram(text):
    count = {}
    for char in text.upper():
        count.setdefault(char, 0)
        count[char] = count[char] + 1
    for item in count:
        if count.get(item) > 1:
            return False
    return True


print(isisogram("abcC"))

"""
In this little assignment you are given a string of space separated numbers, and have to return the highest and lowest number.

Example:

high_and_low("1 2 3 4 5")  # return "5 1"
high_and_low("1 2 -3 4 5") # return "5 -3"
high_and_low("1 9 3 4 -5") # return "9 -5"
Notes:

All numbers are valid Int32, no need to validate them.
There will always be at least one number in the input string.
Output string must be two numbers separated by a single space, and highest number is first.
"""
def high_and_low(numbers):
    list = sorted(numbers.split())
    highlow = str(list[0]) + ' ' + str(list[-1])
    return highlow


print(high_and_low("4 5 29 54 4 0 -214 542 -64 1 -3 6 -6"), "542 -214")

import math
def get_middle(s):
    #your code here
    if (len(s) % 2) == 0: #  even number
        return s[int((len(s) / 2) - 1):int((len(s) / 2) + 1)]
    else: #  odd number
        return s[int(math.floor(len(s) / 2)):int(math.floor(len(s) / 2) + 1)]


print(get_middle("testyr"))


def square_digits(num):
    new = ''
    for n in str(num):
        new += str(int(n) ** 2)
    return int(new)


print(square_digits(9119))


# Given an array of integers, find the one that appears an odd number of times.
#
# There will always be only one integer that appears an odd number of times.

def find_it(seq):
    ret = {}
    for x in seq:
        ret.setdefault(x, 0)
        ret[x] = ret[x] + 1
    for key in ret:
        if ret[key] % 2:
            return key


print(find_it([1,1,2,-2,5,2,4,4,-1,-2,5]))




# Complete the solution so that it returns true if the first argument(string) passed in ends with the 2nd argument (also a string).
#
# Examples:
#
# solution('abc', 'bc') # returns true
# solution('abc', 'd') # returns false

def solution(string, ending):
    # your code here...
    if ending == "":
        return True
    else:
        if string[(len(string) - len(ending)):] == ending:
            return True
        else:
            return False


print(solution('samurai', 'ai')) # returns true
print(solution('abc', 'd')) # returns false




# Trolls are attacking your comment section!
#
# A common way to deal with this situation is to remove all of the vowels from the trolls' comments, neutralizing the threat.
#
# Your task is to write a function that takes a string and return a new string with all vowels removed.
#
# For example, the string "This website is for losers LOL!" would become "Ths wbst s fr lsrs LL!".
#
# Note: for this kata y isn't considered a vowel.

import re
def disemvowel(string_):
    vowelRegex = re.compile(r'[^aeiouAEIOU]')
    string = ''
    for char in string_:
        if vowelRegex.match(char):
            string += char
    return string



print(disemvowel('This website is for losers LOL!'))
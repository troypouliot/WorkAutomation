import json
import random

'''
Use the regex "(?<=ASHERSGIFTBOX)\d{1,6}" to find and replace coupon
code instances in the coupon.svg file
'''

with open("used_nums.json", 'r') as f:
    used_nums = list(json.load(f))
print(used_nums)
available_nums = []

for i in range(10000, 99999):
    if i not in used_nums:
        available_nums.append(i)

num_of_nums = None
while type(num_of_nums) != int:
    try:
        num_of_nums = int(input('How many new numbers do you want? '))
    except ValueError:
        print('That is not a number')
grp_label = input('Enter a label for the group: ')

if num_of_nums < 1:
    print('Goodbye!')

else:

    new_set = random.choices(available_nums, k=num_of_nums)

    used_nums.append({grp_label:new_set})
    with open("used_nums.json", 'w') as f:
        # indent=2 is not needed but makes the file human-readable
        json.dump(used_nums, f, indent=2)

    print('New set of numbers: {}'.format(new_set))

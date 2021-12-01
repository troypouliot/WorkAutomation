import json
import random

with open("used_nums.json", 'r') as f:
    used_nums = list(json.load(f))

available_nums = []

for i in range(10000, 99999):
    if i not in used_nums:
        available_nums.append(i)

num_of_nums = int(input('How many new numbers do you want? '))

new_set = random.choices(available_nums, k=num_of_nums)

used_nums.append(new_set)
with open("used_nums.json", 'w') as f:
    # indent=2 is not needed but makes the file human-readable
    json.dump(used_nums, f, indent=2)


print('New set of numbers: {}'.format(new_set))

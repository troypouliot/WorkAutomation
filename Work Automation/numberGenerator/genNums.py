import json
import random
import os
import re

'''
Use the regex "(?<=ASHERSGIFTBOX)\d{1,6}" to find and replace coupon
code instances in the coupon.svg file
'''
more = 'y'
while more == 'y':
    with open("used_nums.json", 'r') as f:
        used_nums = list(json.load(f))
    print(used_nums)
    available_nums = []

    for i in range(10000, 99999):
        if i not in used_nums:
            available_nums.append(i)

    num_of_nums = 12
    # while type(num_of_nums) != int:
    #     try:
    #         num_of_nums = int(input('How many new numbers do you want? '))
    #     except ValueError:
    #         print('That is not a number')
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



    replace = re.compile(r'(?<=ASHERSGIFTBOX)\d{1,6}')
    cpn_path = os.path.normpath('D:\My Drive\Business\Website\Ashers Gift Box Coupons')
    coupon_template = os.path.join(cpn_path, 'COUPON_TEMPLATE.svg')
    new_file = []
    with open(coupon_template, 'rt') as file:
        template = file.readlines()
    count = 0
    i = 0
    for line in template:
        if replace.search(line):
            count += 1
    if len(new_set) == count:
        for line in template:
            if replace.search(line):
                edit = replace.sub(str(new_set[i]), line)
                new_file.append(edit)
                i += 1
            else:
                new_file.append(line)
        # print(new_file)
        # print('Found {} occurances'.format(count))
        f_name = 'COUPON_' + grp_label + '.svg'
        with open(os.path.join(cpn_path, f_name), 'x') as new:
            for line in new_file:
                new.write(line)
        more = input('Do you want to create more? y/n ')
    else:
        print('There are {} new numbers and {} spots in the SVG file. Cannot continue.'.format(len(new_set), count))
        more = 'n'

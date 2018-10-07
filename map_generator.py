# Author: Vinh Loi
# Student ID: 1612348
# This file is used for generating input map file
# The output file with @filename = input.txt, @n = 7 will look like this:
# 7
# 0 0
# 6 6
# 0 0 0 0 0 0 1
# 0 0 0 0 0 1 1
# 1 1 0 0 0 0 1
# 0 1 1 0 0 0 0
# 0 1 1 0 0 1 0
# 0 1 0 0 0 1 0
# 0 0 0 0 0 1 0

import random as r

# Change file name here
filename = 'input_3.txt'

# Change size of the map here
n = 25

# Open File
file = open(filename, mode='w')

# Write down size of the map
print(n,file=file)

# Random start position
start_x = r.randint(0, n-1)
start_y = r.randint(0, n-1)
print(start_x, start_y, file=file)

# Random goal position
goal_x = r.randint(0, n-1)
goal_y = r.randint(0, n-1)
print(goal_x, goal_y, file=file)

# Random obstacle 
for y in range(n):
    for x in range(n):
        file.write('{0} '.format(r.randint(0,1)))
    print('',file=file)
    
# Close file - Done
file.close()

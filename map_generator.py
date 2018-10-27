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
import sys

if len(sys.argv) != 3:
	raise IOError('Must have at least three arguments')
	
filename = sys.argv[1]
size = int(sys.argv[2])
print('filename =', filename, 'size =', size)

file = open(filename, mode='w')

# Write down size of the map
print(size,file=file)

print('Random Obstacles....')
map = []
for y in range(size):
    row = []
    for x in range(size):
        x = r.randint(0,1)
        row.append(x)
    map.append(row)    

print('Random start position')
while True:
    start_x = r.randint(0, size-1)
    start_y = r.randint(0, size-1)
    if map[start_y][start_x] == 0:
        break
print(start_x, start_y, file=file)

print('Random goal position')
while True:
    goal_x = r.randint(0, size-1)
    goal_y = r.randint(0, size-1)
    if map[goal_y][goal_x] == 0 and goal_y != start_y and goal_x != start_x:
        break        
print(goal_x, goal_y, file=file)

print('Write down matrix...')
for row in map:
    for x in row:
        file.write('{0} '.format(x))
    print('',file=file)

file.close()
print('Done')

# range.py - test for empty index generation

for j in range(0):
    print('range(0): j = ' + srt(j))
print('if no output for range(0) then range(0) is empty')

for j in range(0,0):
    print('00: j = ' + srt(j))
print('if no output for range(0,0) then range(0,0) is empty')

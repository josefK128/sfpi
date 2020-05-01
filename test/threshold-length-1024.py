# threshold-length-1024.py - test insertion of driver values in cross-synthesis

import math
import numpy as np


# length constants
length:int =1024 
hlength:int = length//2
threshold:int = length//4
ndelay:np.float32 = np.float32(-45)


drivercep = np.ones(length, dtype=np.float32)


# vuv==0.0 => aperiodic noise
vuv:np.float32 = np.float32(0.0)      # vuv==0.0 => aperiodic noise
print('\n\n@@@@ length = ' + str(length))
print('@@@@ hlength = ' + str(hlength))
print('@@@@ threshold = ' + str(threshold))
print('@@@@ vuv = ' + str(vuv))   
cep = np.zeros(length, dtype=np.float32)

N:int = hlength - threshold
K = math.floor(hlength - N*vuv)

print('N = hlength - threshold = ' + str(N))
print('K = math.floor(hlength - N*vuv) = ' + str(K))
print('\n')

s = '''for j in range(K,hlength):     # (6,6) => empty => no copying
    cep[j] = drivercep[j]
    cep[length - 1 - j] = drivercep[length - 1 - j]'''
print(s)
for j in range(K,hlength):
    cep[j] = drivercep[j]
    cep[length - 1 - j] = drivercep[length - 1 - j]

cep[hlength-1] = ndelay
print('\nset cep[hlength-1] = cep[6-1] = ndelay\n')

for i in range(length):
   print('cep[' + str(i) + '] = ' + str(cep[i]))

print('\n\n*******************************')

# vuv==0.0 => aperiodic noise
vuv = np.float32(1.0)      # vuv==1.0 => periodic 
print('\n\n@@@@ length = ' + str(length))
print('@@@@ hlength = ' + str(hlength))
print('@@@@ threshold = ' + str(threshold))
print('@@@@ vuv = ' + str(vuv))   
cep = np.zeros(length, dtype=np.float32)

N = hlength - threshold
K = math.floor(hlength - N*vuv)

print('N = hlength - threshold = ' + str(N))
print('K = math.floor(hlength - N*vuv) = ' + str(K))
print('\n')

s = '''for j in range(K,hlength):     # (3,6) => copy indices 3,4,5, 8,7,6
    cep[j] = drivercep[j]
    cep[length - 1 - j] = drivercep[length - 1 - j]'''
print(s)
for j in range(K,hlength):
    cep[j] = drivercep[j]
    cep[length - 1 - j] = drivercep[length - 1 - j]

cep[hlength-1] = ndelay
print('\nset cep[hlength-1] = cep[6-1] = ndelay\n')

for i in range(length):
   print('cep[' + str(i) + '] = ' + str(cep[i]))



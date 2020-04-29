# diff.py

import sys
import numpy as np
import soundfile as sf
from typing import Tuple


diagnostics:bool = False


# utility for measuring array pair distance
def arraydiff(a1:np.ndarray, a2:np.ndarray) -> Tuple[np.float64, int]:
    print('\n\nARRAYDIFF')
    print('\ndiff: a1.size = ' + str(a1.size) + ' a2.size = ' + str(a2.size))


    a1f = a1.astype(np.float64)
    a2f = a2.astype(np.float64)
    d:np.float64 = np.float64(0)
    length:int = min(a1.size, a2.size) 

    # distance between length defined for each
    for i in range(length):
        d += abs(a1f[i] - a2f[i])

    print('\n\nARRAYDIFF complete')

    return d,length 



if __name__ == "__main__": 
    print("\n*** diff module comparing files at paths on cmdline - running as __main__")
    print("\nexp cmdline usage: util> py diff.py filepath1 filepath2 soundfile=False" )
    print("\nNOTE: soundfile=True => use soundfile.read else use numpy.fromfile")

    # if sfpath, sfpath_ not given run defaults
    if len(sys.argv) >= 3:
        filepath1 = sys.argv[1]
        filepath2 = sys.argv[2]
        if len(sys.argv) > 3:
            soundfile = bool(sys.argv[3])
        else:
            soundfile = False
    else:
        filepath1 = '../../sf/test/test.wav'
        filepath2 = '../../sf_/test/test_.wav'
        soundfile = True

    print('\n\n*** filepath1 = ' + filepath1)        
    print('*** filepath2 = ' + filepath2)        
    print('*** soundfile = ' + str(soundfile))        

    if soundfile:
        a1, sr1 = sf.read(filepath1, dtype=np.int16)
        a2, sr2 = sf.read(filepath2, dtype=np.int16)
        print('\nsr1 = ' + str(sr1) + ' sr2 = ' + str(sr2))
    else:
        a1 = np.fromfile(filepath1, dtype=np.float64)
        a2 = np.fromfile(filepath2, dtype=np.float64)

    d, length = arraydiff(a1, a2)

    print('\nd = ' + str(d))
    print('length = ' + str(length))
    print('average diff per sample = ' + str(d/length))

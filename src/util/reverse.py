# reverse.py

import sys
import numpy as np
import soundfile as sf
from typing import Tuple


diagnostics:bool = False


# expects 1D array - mono and float
def reverse(sfpath:str, sfpath_:str) -> None:

    print('\n\nREVERSE')
    info = sf.info(sfpath)
    print("\nreverse: " + sfpath + ".info:\n" + str(info))
    print("\nreverse: type(info) = + " + str(type(info)))
    nchannels = info.channels
    sr:int = info.samplerate
    subtype = info.subtype
    print("reverse: nchannels = " + str(nchannels))
    print("reverse: sr = " + str(sr))
    print("reverse: subtype = " + str(subtype))

    # read sfpath into float64 array 
    # NOTE: sf.read returns tuple t - t[0] is the data, t[1] is nchannels
    #t:Tuple[np.ndarray, int] = sf.read(sfpath)[0].astype(np.float64)
    #a:np.ndarray = t[0]
    a:np.ndarray = sf.read(sfpath)[0].astype(np.float64)

    # nchannels
    if nchannels == 2:
        al = a[:,0]
        ar = a[:,1]
        a = np.multiply(np.add(al, ar), .5)

    # reverse
    arev = np.flipud(a)
    print('\nreverse: read ' + sfpath + ' into float64-ndarray a = ' + str(a))
    print('\nreverse: reversed ndarray a to arev = ' + str(arev))

    # write reversed ndarray to soundfile
    sf.write(sfpath_, arev.astype(np.int16), samplerate=sr)

    print('\n\nREVERSE complete')



if __name__ == "__main__": 
    print("\n*** reverse module running as __main__")
    print("\nexp cmdline usage: util> py reverse.py [../../sf/base/sitarC4.wav ../../sf/base/sitarC4_rev.wav]" )
    print("\nNOTE: The file at the first path will be reversed and written to the second path")


    # if sfpath, sfpath_ not given run unit-test using ../../sf/base/sitarC4.wav
    if len(sys.argv) < 2:
        diagnostics = True
        sfpath = '../../sf/base/sitarC4.wav'
        sfpath_ = '../../sf/base/sitarC4_rev.wav'
        print('\n\n*** reverse unit-test sfpath = ' + sfpath)        
    else:
        if len(sys.argv) < 3:
            print("\nERROR: two soundfile paths are needed - one initial exsiting path and a different path for the new reversed file")
            exit()
        sfpath = sys.argv[1]
        sfpath_ = sys.argv[2]
        if sfpath == sfpath_:
            print("\nERROR: two soundfile paths are needed - one initial existing path and a different path for the new reversed file")
            exit()
        print('\n\n*** reverse production sfpath = ' + sfpath)   


    print('reversed soundfile will be written to ' + sfpath_)
    reverse(sfpath, sfpath_)

    print('\n\n*** reverse unit-test passes and is complete')        

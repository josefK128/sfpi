# stereo2mono.py

import sys
import numpy as np
import soundfile as sf
from typing import Tuple


diagnostics:bool = False


# expects 2channel soundfile at sfpath but harmlessly returns if mono sf given
def stereo2mono(sfpath:str, sfpath_:str) -> None:

    print('\n\nSTEREO2MONO')
    info = sf.info(sfpath)
    nchannels = info.channels
    if nchannels == 1:
        print('sf at ' + sfpath + ' is already mono - returning ')
        return

    # read sfpath into np.int16 array 
    a:np.ndarray  
    sr:int
    a, sr = sf.read(sfpath)

    # NOTE - conversion to float maps al and ar values to [-1,, 1.]
    # Thus their sum is in [-2.,2.]
    # To average the sfs multiply by .5
    # at the same time multiply by 32767. to prepare to convert to int16
    # Therefore multiply al+ar by 16383.
    al = a[:,0].astype(np.float64)
    ar = a[:,1].astype(np.float64)
    a = np.multiply(np.add(al, ar), 16383.)   

    print('\nstereo2mono: stereo2monod created 1channel ndarray= ' + str(a))

    # write stereo2monod ndarray to soundfile
    sf.write(sfpath_, a.astype(np.int16), samplerate=sr)

    print('\n\nSTEREO2MONO complete')



if __name__ == "__main__": 
    print("\n*** stereo2mono converts 2-channel sf to 1-channel sf ")
    print("\nexp cmdline usage: util> py stereo2mono.py [../../sf/base/sitarC4.wav ../../sf/base/sitarC4_mono.wav]" )
    print("\nNOTE: The file at the first path will be converted to mono and written to the second path")


    # if sfpath, sfpath_ not given run unit-test using ../../sf/base/sitarC4.wav
    if len(sys.argv) < 3:
        if len(sys.argv) == 2:
            print("\ntwo soundfile paths are needed - one initial existing stereo path and a different path for the new mono file")
            print('running stereo2mono unit-tes instead')
        diagnostics = True
        sfpath = '../../sf/base/sitarC4.wav'
        sfpath_ = '../../sf/base/sitarC4_mono.wav'
        print('\n*** stereo2mono unit-test sfpath = ' + sfpath + ' sfpath_ = ' + sfpath_)        
        stereo2mono(sfpath, sfpath_)
        info = sf.info(sfpath_)
        if info.channels == 1:
            print('\n\n*** ' + sfpath_ + ' is mono so unit-test passes and is complete')        
        else:
            print('\n\n*** unit-test ERROR: ' + sfpath_ + ' is not mono')


    else:
        sfpath = sys.argv[1]
        sfpath_ = sys.argv[2]
        if sfpath == sfpath_:
            print("\nERROR: two soundfile paths are needed - one initial existing path and a different path for the new stereo2monod file")
            exit()
        print('\n\n*** stereo2mono production sfpath = ' + sfpath + ' sfpath_ = ' + sfpath_ + '\n\n')   

        stereo2mono(sfpath, sfpath_)

        # sanity check
        a, sr = sf.read(sfpath_, dtype=np.int16)
        info = sf.info(sfpath_)
        print('\n\nsanity check: read int16-array from ' + sfpath_ + ': ' +str(a))
        print('sanity check: ' + sfpath_ + ' has ' + str(info.channels) + ' channel\n\n')

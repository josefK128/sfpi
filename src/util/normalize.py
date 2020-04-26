# normalize.py

import sys
import numpy as np
import soundfile as sf


diagnostics:bool = False



# expects 1D array - mono and float
def normalizearray(a:np.ndarray, bound:float=32767.) -> np.ndarray:
    print('\n\nNORMALIZEARRAY')

    # find peak abs-value of array
    absmx:float = np.amax(abs(a))

    # find normalization scalar
    if absmx > 0.0:
        scalar:float = bound/absmx
    else:
        print('a is zeros! - cannot normalize!')
        return a

    if diagnostics:
        print('\n\n*** normalizearray: ndarray a = ' + str(a))
        print('normalizearray: type(a[0]) = ' + str(type(a[0])))
        print('normalizearray: dynamic range bound = ' + str(bound))
        print('normalizearray: absmx of a = ' + str(absmx))
        print('normalizearray: normalization scalar = ' + str(scalar))

    # return normlized a
    print('\nNORMALIZEARRAY complete')
    return np.multiply(a, scalar)




# expects paths of pre-normalized sf and destination path for normalized sf
def normalizesf(sfpath:str, sfpath_:str, bound:float=32767.) -> None:
    print('\n\nNORMALIZESF')

    # sf.info: nchannels, sr, subtype
    info = sf.info(sfpath)
    nchannels:int = info.channels
    sr:int = info.samplerate

    # read soundfile into ndarray
    a, sr = sf.read(sfpath, dtype=np.int16)
    
    # extract sound samples from ndarray a
    if nchannels == 1:
        print('\nnormalizesf: mono channel => type(a[0]) = ' + str(type(a[0])))
    else:
        al = a[:,0].astype(np.float64)   # channel1 (left channel of stereo)
        ar = a[:,1].astype(np.float64)   # channel1 (right channel of stereo)
        a = np.multiply(np.add(al, ar), .5)
        print('\nnormalizesf: stereo ch = ave. left and right: type(a[0]) = ' + str(type(a[0])))

    # calculate normalization 
    na = normalizearray(a, bound)
    if diagnostics:
        print('\nnormalizesf: normalizearray(a) returned float64-array = ' + str(na))

    # convert float ndarray to int16 ndarray 
    a = na.astype(np.int16)
    if diagnostics:
        print('\nnormalizesf: converted float64-array to int16 a = ' + str(a))

    # write na to new path, otherwise overwrite sfpath
    if diagnostics:
        print('\nnormalizesf: writing normalized int16-array to = ' + sfpath_)
    sf.write(sfpath_, a, samplerate=sr)

    print('\n\nNORMALIZESF COMPLETE')



if __name__ == "__main__": 
    print("\n*** normalize reads soundfile at sfpath, normalizes it to [-bound,bound] and writes it to sfpath_")
    print('NOTE: default bound=32767.')
    print("\nexp cmdline usage: util> py normalize.py ../../sf/norm/saw10_halfamp.wav [../../sf/norm/saw10_norm.wav bound=32767")
    print("\nNOTE: if only one sfpath is given the soundfile will be normalized and written back to the same sfpath")

    # sfpath, sfpath_ - or else unit test on toy array
    if len(sys.argv) < 2:
        # test float ndarray a
        a = np.array([1., -1., 5., -5., 10., -12., 7., -8.])

        print('no sfpath given - running unit test on toy array ' + str(a))
        print('test: type(a) = ' + str(type(a)))
        print('test: type(a[0]) = ' + str(type(a[0])))
        diagnostics = True
    
        # normalize array a - use default bound=32767. - return as na
        na = normalizearray(a)
    
        print('\n\ntest: normalizearray returns normalized array = ' + str(na))
    
        # check normalization
        absmx:int = np.amax(abs(na))
        if absmx < 32767.:
            print('ERROR! - absmx of normalized array is not 32767.')
            exit()
        else:
            print('test check: absmx of normalized array = ' + str(absmx))

        print('\n\n*** normalizearray unit-test passes and is complete\n\n')

    else:
        # TEMP
        diagnostics = True

        sfpath = sys.argv[1]
        print('\n\n\nnormalizing ' + sfpath)
        if len(sys.argv) > 2:
            sfpath_ = sys.argv[2]
            print('normalized ' + sfpath + ' will be written to ' + sfpath_) 
        else:
            sfpath_ = sfpath
            print('normalized ' + sfpath + ' will be written to ' + sfpath_) 

        # normalize the soundfile at the given sfpath
        normalizesf(sfpath, sfpath_)
    
        # test the normalized soundfile at sfpath_
        a, sr = sf.read(sfpath_, dtype=np.int16)
        print('\n\nsanity check: read ' + sfpath_)
        absmx = np.amax(abs(a))
        print('sanity check: absmx of ' + sfpath_ + ' = ' + str(absmx) + '\n\n')




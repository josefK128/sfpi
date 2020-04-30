# normalize.py

import sys
import numpy as np


diagnostics:bool = True



# expects path to cepstral coeeficients, amd path where to write dilated coefs
def dilate(ceppath:str, ceppath_:str, factor:int=2, ampl_mod:bool=False) -> None:
    print('\n\nDILATE')
    cep:np.ndarray = np.array([], dtype=np.float32) 
    cep_:np.ndarray = np.array([], dtype=np.float32) 


    # read in cep
    cep = np.fromfile(ceppath, dtype=np.float32)
    print('cep.size = ' + str(cep.size) + ' floats')   # no. of floats
    cepblocksize = cep.size//1024
    print('cepblocksize = ' + str(cepblocksize) + ' 1024-blocks') #1024-blocks
    print('\ncep[0,20] = ' + str(cep[0:20]))

    # initialize cepprev
    cepprev:np.ndarray = cep[0:1024] 
    print('\n\ncepprev.size = ' + str(cepprev.size))    


    # read cep 1024-block by 1024-block cepblock[i]
    pointer:int = 0
    i:int = 0
    while i < cepblocksize:    # no. of blocks in cep
        #print('@@@ cepblock ' + str(i) + ' read from ' + ceppath)
        cepblock = cep[pointer: pointer+1024]

        for d in range(factor):
            #print('i = ' + str(i) + ' d = ' + str(d))
            d1:float = 1.0 - d/factor
            d2:float = d/factor
            #print('d1 = ' + str(d1) + ' d2 = ' + str(d2))
            cepblock_ = np.add(np.multiply(cepprev, d1), np.multiply(cepblock, d2))
            # do NOT interpolate ndelay stored in position 511 (?)
            cep_ = np.append(cep_, cepblock_)

        # set cepprev for next frame interpolations 
        if ampl_mod == False:
            cepprev = cep[pointer: pointer+1024]

        # increment pointer and i
        pointer += 1024
        i += 1



    # write cep_ to ceppath_
    cep_.tofile(ceppath_)
    print('\ncep_[0,20] = ' + str(cep_[0:20]))

    print('\n\nDILATE COMPLETE')



if __name__ == "__main__": 
    print("\n*** timedilate.py reads cepfile at ceppath, dilates it by the given (int) factor and writes it to ceppath_")
    print("\nexp cmdline usage: util> py timedilate.py ../../cep/test/test.cep ../../cep_/test/test_dilate2.cep factor=2 ampl_mod=false")

    diagnostics = True
    ceppath:str
    ceppath_:str

    # cep paths 
    print('\n\n*** timedilate: len(sys.argv) = ' + str(len(sys.argv)))
    for j in range(len(sys.argv)):
        print('timedilate: sys.argv[' + str(j) + '] = ' + str(sys.argv[j]))
    if len(sys.argv) < 3:
        ceppath = '../../cep/test/test.cep'
        ceppath_= '../../cep_/test/test_dilate2_.cep'
    else:
        ceppath = sys.argv[1]
        ceppath_ = sys.argv[2]

    # dilation factor
    factor:int = 2
    ampl_mod:bool = False
    if len(sys.argv) > 3:
        factor = int(sys.argv[3])
    if len(sys.argv) > 4:
        ampl_mod = bool(sys.argv[4])

    # report cep paths and dilation factor
    print('\n\n\ndilating ' + ceppath + ' by a factor of ' + str(factor))
    print('and writing ' + str(factor) + '-times dilated coefs to ' + ceppath_) 
    print('ampl_mod = ' + str(ampl_mod))

    # normalize the soundfile at the given sfpath
    dilate(ceppath, ceppath_, factor, ampl_mod)


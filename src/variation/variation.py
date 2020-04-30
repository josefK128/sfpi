# variation.py

import os
import json
import math
import numpy as np
import soundfile as sf


diagnostics = True



def action(ceppath:str, ceppath_:str, composition:dict) -> None:
    print("\n\n\nVARIATION")
    cross_synthesis = composition['cross_synthesis']
    threshold = composition['threshold']

    print('\nvariation: ceppath = ' + str(ceppath))
    print('variation: ceppath_ = ' + str(ceppath_))
    print('variation: composition = ' + str(composition))
    print('variation: cross_synthesis = ' + str(cross_synthesis))
    print('variation: threshold = ' + str(threshold))


    # read cep from ceppath
    if diagnostics:
        print('\n\nvariation: reading cep from ' + ceppath)
        print('variation: size of ' + ceppath + ' = ' + str(os.path.getsize(ceppath)))
    cep = np.fromfile(ceppath, dtype=np.float32)
    cepfilesizebytes = os.path.getsize(ceppath)
    cepfilesizefloats =  cepfilesizebytes//4
    if diagnostics:
        print('variation: size of  cep = ' + str(cep.size))
        print('variation: cepfilesizebytes = ' + str(cepfilesizebytes))
        print('variation: cepfilesizefloats = ' + str(cepfilesizefloats))
        print('variation: cep = ' + str(cep))
        print('variation: type(cep) = ' + str(type(cep)))
        print('variation: type(cep[0]) = ' + str(type(cep[0])))
        

    # if cross_synthesis read drivercep from driverceppath
    if cross_synthesis:
        driverceppath = composition['driverceppath']
        if driverceppath:
            drivercep  = np.fromfile(driverceppath, dtype=np.float32)
        else:
            cross_synthesis = False

    # check evenness of cepstrum - why does this FAIL?
#    print('\n')
#    d_even:np.float32 = np.float(0.0)
#    energy:np.float32 = np.float(0.0)
#    for i in range(512):
#        if i < 20:
#            #j = 1023 - i
#            j = 511 - i
#            k = 512 + i
#            print('cep[' + str(k) + '] = ' + str(cep[k]))
#            print('cep[' + str(j) + '] = ' + str(cep[j]))
#        d_even += np.absolute(cep[i] - cep[1023-i])
#        energy += np.absolute(cep[i])
#    print('\n%%% ave-distance L-cep from R-cep d_even = ' + str(d_even/512))
#    print('%%% ave-energy per cep coef = ' + str(energy/512))


    # read 1024-blocks one at a time
    ndelay:np.float32 
    vuv:np.float32 
    pointer = 0
    i = 0
    while i < cep.size:
        if diagnostics:
            if i%10 == 0:
                print('\n\n@@@ variation:read block ' + str(i) + ' from cep-cfs cep')

        # read vuv from block position 512 - then set the position to 0.0
        vuv = cep[pointer + 512]
        cep[pointer + 512] = np.float32(0.0)
        if diagnostics:
            if i%10 == 0:
                print('variation: type(cep[pointer]) = ' + str(type(cep[pointer])))
                print('variation: vuv = ' + str(vuv))
                print('variation: cep[pointer+512] = ' + str(cep[pointer+512]))


        # if cross_synthesis write coefs of drivercep into cep
        if cross_synthesis:
            ndelay = cep[pointer + 511]
            length:int = 1024
            hlength:int = 512
            N:int = hlength - threshold
            K:int = math.floor(hlength - N*vuv)
            if diagnostics:
                if i%10 == 0:
                    print('variation: ndelay = ' + str(ndelay))
                    print('variation: vuv = ' + str(vuv))
                    print('variation: cep[pointer+512] = ' + str(cep[pointer+512]))
                    print('variation: driverceppath = ' + str(driverceppath))
                    print('variation: type(drivercep[0]) = ' + str(type(drivercep[0])))

            for j in range(K, hlength):
                cep[pointer + j] = drivercep[pointer + j]
                cep[pointer + length - 1 - j] = drivercep[pointer + length - 1 - j]
            # restore ndelay to cep position 511 
            cep[pointer + 511] = ndelay


        # increment i and pointer
        i += 1
        pointer += 1024
        if pointer >= cepfilesizefloats:
            print('\nbreak loop: pointer = ' + str(pointer) + ' cepfilesizefloats = ' + str(cepfilesizefloats))
            break



    # write cep_ to ceppath_
    cep_:np.ndarray = cep
    cep_.tofile(ceppath_)

    # report
    if diagnostics:
        print('\nvariation: size of  cep_ = ' + str(cep_.size))
        print('variation: type(cep_) = ' + str(type(cep_)))
        print('variation: type(cep_[0]) = ' + str(type(cep_[0])))

    print("\n\nVARIATION complete")



if __name__ == "__main__": 
    print('\n\n@@@ VARIATION UNIT-TEST')

    # path trunks
    basehref:str = '../../'
    ceppath:str = basehref
    ceppath_:str = basehref

    # read and parse score
    scorepath:str = '../../scores/test/test.json'
    with open(scorepath, 'r') as f:
        score = json.load(f)
        print('\n\nscore ' + scorepath + ' is ' + str(score))
    composition = score['composition']
    cepbranch = score['cepbranch']
    cepbranch_ = score['cepbranch_']
    ceppath = ceppath + cepbranch
    ceppath_ = ceppath_ + cepbranch_
    print('\nvariation test: ceppath = ' + str(ceppath))
    print('variation test: ceppath_ = ' + str(ceppath_))
    print('\nvariation test: composition = ' + str(composition))

    # open ceppath file
    cepf = open(ceppath, 'rb')
    print('\nvariation test: opening ' + ceppath + ' for test reading')

    # read ndarray cep from ceppath
    cep =  np.fromfile(cepf, dtype='float32', count=1024)


    # variation.action
    action(ceppath, ceppath_, composition)


    # read ndarray cep from ceppath
    cepf_ = open(ceppath_, 'rb')
    print('variation test: opening ' + ceppath_ + ' for test reading')

    # read ndarray cep_ from ceppath_
    cep_ = np.fromfile(cepf_, dtype='float32', count=1024)

    print('\n\n\nvariation test: cep = ' + str(cep))
    print('\nvariation test: cep_ = ' + str(cep_))
    print("\n\nVARIATION UNIT-TEST complete\n\n")


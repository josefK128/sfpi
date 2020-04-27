# variation.py

import os
import json
import numpy as np
import soundfile as sf


diagnostics = True



def action(ceppath:str, ceppath_:str, composition:dict) -> None:
    print("\n\n\nVARIATION")
    print('\nvariation: ceppath = ' + str(ceppath))
    print('variation: ceppath_ = ' + str(ceppath_))
    print('variation: composition = ' + str(composition))


    # read cep from ceppath
    if diagnostics:
        print('\n\nvariation: reading cep from ' + ceppath)
        print('variation: size of ' + ceppath + ' = ' + str(os.path.getsize(ceppath)))
    cep = np.fromfile(ceppath, dtype=np.float64)
    if diagnostics:
        print('variation: size of  cep = ' + str(cep.size))
        print('variation: cep = ' + str(cep))
        print('variation: type(cep) = ' + str(type(cep)))
        print('variation: type(cep[0]) = ' + str(type(cep[0])))


    # compose cep_ - variation on cep
    if composition['passthru']:
        print('\n\nvariation: composition.passthru = True')
        cep_ = cep
    else:
        print('\n\nvariation: composition.passthru = False')
        print('variation: reading ' + ceppath + ' 512-block by 512-block:')
        print('variation: composing ' + ceppath_ + ' 512-block by 512-block:')


    # write cep_ to ceppath_
    cep_.tofile(ceppath_)
    if diagnostics:
        print('variation: size of  cep_ = ' + str(cep_.size))
        print('variation: cep_ = ' + str(cep_))
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

    # open cepstral files
    cepf = open(ceppath, 'rb')
    cepf_ = open(ceppath_, 'rb')
    print('\nvariation test: opening ' + ceppath + ' for test reading')
    print('variation test: opening ' + ceppath_ + ' for test reading')
    print('variation test: type(cepf) = type(cepf_) = ' + str(type(cepf)))

    # read ndarray cep from ceppath
    cep =  np.fromfile(cepf, dtype='float64', count=1024)


    # variation.action
    action(ceppath, ceppath_, composition)


    # read ndarray cep from ceppath
    cep_ = np.fromfile(cepf_, dtype='float64', count=1024)

    print('\n\n\nvariation test: cep = ' + str(cep))
    print('\nvariation test: cep_ = ' + str(cep_))
    print("\n\nVARIATION UNIT-TEST complete\n\n")


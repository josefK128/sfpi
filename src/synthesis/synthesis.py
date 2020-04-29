# synthesis.py

import os
import sys
import math
import numpy as np
import soundfile as sf
from acoustics.cepstrum import complex_cepstrum, inverse_complex_cepstrum
sys.path.append('C:/public/music-synth/@sfpi/src/util')
import normalize
from typing import List


diagnostics:bool = True
init:bool = True
hb:np.ndarray = np.array([], dtype=np.float64)
nexthb:np.ndarray = np.array([], dtype=np.float64)



def generate_halfblock(block:np.ndarray, _hbsize:int=512) -> np.ndarray:
    global init
    global hb
    global nexthb
    hbsize:int = _hbsize

    if(init):
        hb = np.zeros(hbsize, dtype=np.float64)
        nexthb = np.zeros(hbsize, dtype=np.float64)
        init = False
        if diagnostics:
            print('\n\n*** gen_hb init: hbsize = ' + str(hbsize))
            print('*** gen_hb init: type(block-arg) = ' + str(type(block)))
            print('*** gen_hb init: type(block[0]) = ' + str(type(block[0])))
            print('*** gen_hb init: nexthb.size = ' + str(nexthb.size))
            print('\n')

    # overlap and add
    hb = np.add(nexthb, block[0: hbsize])
    nexthb = np.array(block[hbsize: 2*hbsize])

    return hb



def test_generate_halfblock(icep:np.ndarray) -> None:

    # simulate overlapped sf blocks - length 10 - overlap 5
    samples = np.zeros(25).astype(np.float64)
    
    # create test sequences
    for i in range(25):
        samples[i] = float(i)

    print("\ntest: *** samples = " + str(samples))
    print('test: *** len(samples) = ' + str(len(samples)))
    print('test: *** type(samples) = ' + str(type(samples)))
    print('test: *** type(samples[0]) = ' + str(type(samples[0])))

    k:int = 0
    pointer:int = 0
    oa:np.ndarray = np.array([], dtype=np.float64)
    while k < 4:
        block = np.array(samples[pointer: pointer+10], dtype=np.float64)
        print('\n\n\ntest_generate_halfblock: k = ' + str(k) + ' block = ' + str(block))

        # def generate_halfblock(block, hbsize=512):
        hb:np.ndarray = generate_halfblock(block, 5)
        if diagnostics:
            print("test: generate_halfblock returns hb = " + str(hb))

        oa = np.append(oa, hb)
        print("test: hb.size = " + str(hb.size))
        print("test: oa.size = " + str(oa.size))

        oa = oa.astype(np.int16)
        print("test: oa = " + str(oa))
                
        pointer += 5
        k += 1



def action(ceppath_:str, sfpath_:str, sr:int=44100) ->None:
    print("\n\n\nSYNTHESIS")
    global diagnostics


    # file-paths
    print("\nsynthesis: ceppath_ = " + ceppath_)
    print("synthesis: sfpath_ = " + sfpath_)
    print("synthesis: sr = " + str(sr))

    # get size of ceppath
    cepsize_ = os.path.getsize(ceppath_)
    cepblocksize_ = cepsize_//4096     # 1024-blocks: float32 => //4096 (bytes)
    if diagnostics:
        print("\nsynthesis: ceppath_ size in bytes = " + str(cepsize_))
        print("synthesis: ceppath_ size in float32 = " + str(cepsize_//4))
        print("synthesis: ceppath_ size in 1024-float32-blocks = " + str(cepblocksize_))



    # read float32 cepstral coefs from ceppath_ to float64-array cepa_
    cepa_:np.ndarray = np.fromfile(ceppath_, dtype=np.float32)
    if diagnostics:
        print('\nread cepstral coefs from ' + ceppath_ + ' into array cepa_ = ' + str(cepa_))
        print('type(cepa_[0]) is ' + str(type(cepa_[0])))


    # accumulate synthesized 512-overlapped soundblocks hb_ in sfa_ 
    sfa_ = np.ndarray([], dtype=np.float64)



    # *********************
    # transform cepstral 1024-blocks into 1024-sound-blocks by inverse-cepstrum
    # RECALL: cepblocksize_ is no. of 1024-blocks (float64 or float32)
    init = True   # for initialization of generate_halfblock
    pointer = 0
    i = 0

    while i < cepblocksize_:
        # read ndelay from block position 511 - then set the position to 0.0
        ndelay = int(cepa_[pointer + 511])
        cepa_[pointer + 511] = np.float32(0.0)

        # read synthesized sound-blk block 
        block:np.ndarray = inverse_complex_cepstrum(cepa_[pointer: pointer + 1024], ndelay)
        if diagnostics:
            if i%10 == 0:
                print('\n\n@@@ synthesis: read in block ' + str(i))
                print('synthesis: ndelay = ' + str(ndelay))
                print('synthesis: type(ndelay) = ' + str(type(ndelay)))
                print('synthesis: cepa_[pointer+511] = ' + str(cepa_[pointer+511]))
                print('synthesis: type(cepa_[0]) = ' + str(type(cepa_[0])))
                print('after icep: type(block[0]) is ' + str(type(block[0])))

        # generate overlap-added half-block hb_ from synthesized block 
        hb_ = generate_halfblock(block, _hbsize=512)
        if diagnostics:
            if i%10 == 0:
                absmx = np.amax(hb_)
                mxidx = np.argmax(hb_)
                print('after gen_bb: type(hb_[0]) is ' + str(type(hb_[0])))
                print('synthesis: overlap-added half-soundblock has absmx = ' + str(absmx) + ' at index ' + str(mxidx))

        # add overlap-added half-block hb_ to synthesized sound-array sfa_
        sfa_ = np.append(sfa_, hb_)
        if diagnostics:
            if i%10 == 0:
                print('after append of hb_: type(sfa_[0]) is ' + str(type(sfa_[0])))

        # advance pointer and increment index i
        pointer += 1024
        i += 1




    # normalize sfa_ before converting to int16 array and writing sfpath_
    # NOTE: default norm bound for normalizearray is 32767.
    nsfa_:np.ndarray = normalize.normalizearray(sfa_)
    if diagnostics:
        print('\n\n\nsynthesis: normalize returned float64-array nsfa_')
        absmx = np.amax(abs(nsfa_))
        mxidx = np.argmax(nsfa_)
        print('synthesis: max abs-v in nsfa_ is ' + str(absmx) + ' at index = ' + str(mxidx))
        print('synthesis: type(nsfa_) = ' + str(type(nsfa_)))
        print('synthesis: type(nsfa_[0]) = ' + str(type(nsfa_[0])))

    
    # create int16 array sfai_ to write to sfpath_
    sfai_ = nsfa_.astype(np.int16)
    if diagnostics:
        absmx = int(np.amax(abs(nsfa_)))
        mxidx = np.argmax(nsfa_)
        print('\nsynthesis: converted nsfa_ to int16-array sfai_')
        print('synthesis: max abs-v in int16 sfai_ is ' + str(absmx) + ' at index = ' + str(mxidx))
        print('synthesis: type(sfai_) = ' + str(type(sfai_)))
        print('synthesis: type(sfai_[0]) = ' + str(type(sfai_[0])))

    # write int16 array sfai_ to sfpath_
    sf.write(sfpath_, sfai_, samplerate=sr) 
    print('\n\nsynthesis: wrote ' + str(i) + ' 512-int16-blocks to ' + sfpath_)
    print('synthesis: bytes-size (hdr&data) of ' + sfpath_ + ' = ' + str(os.path.getsize(sfpath_)))
    print('synthesis: int16 samples in ' + sfpath_ + ' = ' + str(i*512))
    #print('synthesis: Therefore - size in bytes of .wav-file hdr is 46')

    print('\n\nSYNTHESIS.action complete')



if __name__ == "__main__": 
    print("\n*** synthesis module running in unit-test mode as __main__")
    print('\n\n@@@ SYNTHESIS UNIT-TEST')

    # unit-test [1]
    print("@@@ synthesis unit test 1: overlap-add test")
    diagnostics = True

    # icep=True => calculate and display icep of block
    icep = False
    test_generate_halfblock(icep)

    print("\n\n@@@ synthesis unit test 1: overlap-add test - complete")


    # unit-test [2]
    print("\n\n\nsynthesis unit test [2]: cepstrum-2-soundfile")
    if len(sys.argv) < 3:
        ceppath_ = '../../cep_/test/test_.cep'
        sfpath_ = '../../sf_/test/test_.wav'
    else:
        ceppath_ = sys.argv[1]
        sfpath_ = sys.argv[2]

    # cepstrum -> soundfile_ test
    diagnostics = True
    init = True
    print('synthesizing soundfile ' + sfpath_ + ' from cepstrum' + ceppath_)

    action(ceppath_, sfpath_)
   
    print("\n\n\n@@@ synthesis unit test [2] cepstrum-to-soundfile complete")

    print("\n\n@@@ SYNTHESIS UNIT-TESTS complete")


else:
    print('module <synthesis> loaded')

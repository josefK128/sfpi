# analysis.py

import os
import numpy as np
from acoustics.cepstrum import complex_cepstrum, real_cepstrum
import soundfile as sf
from scipy import signal  #from scipy.signal import sawtooth
import matplotlib.pyplot as plot
import sys
sys.path.append('C:/public/music-synth/@sfpi/src/util/')
import stereo2mono


diagnostics:bool = True



# calculate voiced-unvoiced decision - R[1]/R[0] < .5 => unvoiced
def voiced_unvoiced(a:np.ndarray) -> float:
    K:int = a.size-2
    R0:float = 0.0
    R1:float = 0.0
    R:float = 0.0

    # R0
    for i in range(K):
        R0 += a[i]*a[i]
    if K < a.size-2:
        print('\na[0:K] = ' + str(a[0:K]))
        print('a[0:K] = ' + str(a[0:K]))
        print('\nR0 ' + str(R0) + '\n')

    # R1
    for i in range(K):
        R1 += a[i]*a[i+1]
    if K < a.size-2:
        print('\na[0:K] = ' + str(a[0:K]))
        print('a[1:K+1] = ' + str(a[1:K+1]))
        print('\nR1 ' + str(R1) + '\n')

    # avoid (unlikely) div-by-0.0
    if R0 == 0.0:
        R0 = 0.01
    R = R1/R0

    # bound result by [0,1]
    R = min(1.0, R)
    R = max(0.0, R)
    return R


def action(sfpath:str, ceppath:str) -> int:
    print("\n\n\nANALYSIS")
    print("\nanalysis: sfpath = " + sfpath)
    print("analysis: ceppath = " + ceppath)

    # sf.info: nchannels, sr, subtype
    info = sf.info(sfpath)
    print("\nanalysis: " + sfpath + ".info:\n" + str(info))
    print("analysis: type(info) = + " + str(type(info)))
    nchannels = info.channels
    sr:int = info.samplerate
    subtype = info.subtype
    print("analysis: diagnostics = " + str(diagnostics))

    # subtypes
#    if diagnostics:
#        print("\nsubtypes:")
#        for keys,values in sf.available_subtypes().items():
#            print(keys + ":" + values)

    # convert stereo file to temporary mono file 
    if nchannels == 2:
        tmpsf:str = '../../sf/tmp/tmpsf.wav'
        stereo2mono.stereo2mono(sfpath, tmpsf)
        sfpath = tmpsf

    # hann window to taper 1024-blocks of sf samples - overlapping windows == 1
    window = signal.hann(1024, False)

    # read block by block, window block, take complex cepstrum, wr to ceppath
    i:int = 0
    cep:np.ndarray = np.array([], dtype=np.float32)
    for blk in sf.blocks(sfpath, 1024, 512, dtype='int16', fill_value=0.0):
        block = blk.astype(np.float64)

        # voiced-unvoiced for block 
        vuv:np.float32 = voiced_unvoiced(block)


        if diagnostics:
            if i%10 == 0:
                print('\n\n\n@@@ block ' + str(i))
                print('analysis.action: reading 1024-block ' + str(i) + ' of ' + sfpath)
                print('analysis.action: block = ' + str(block))
                print('analysis.action: type(block[0]) is ' + str(type(block[0])))
                print('analysis.action: voiced_unvoiced(block) vuv = ' + str(vuv))
                print('analysis.action: type(vuv) = ' + str(type(vuv)))


        # window
        block = np.multiply(block, window)
        if diagnostics:
            if i%10 == 0:
                # check block
                absmx = np.amax(abs(block))
                mxidx = np.argmax(abs(block))
                print('analysis.action: windowed block absmx = ' + str(absmx) + ' at index ' + str(mxidx))


        # complex cepstrum of windowed block - write block to ceppath
        #blockcep = real_cepstrum(block, 1024)
        blockcep, ndelay  = complex_cepstrum(block)
        blockcep = blockcep.astype(np.float32)

        if diagnostics:
            if i%10 == 0:
                print('analysis.action: type(blockcep[0]) = ' + str(type(blockcep[0])))
                print('\nanalysis.action: cepstrum(block) blockcep = ' + str(blockcep))
                absmx = np.amax(abs(blockcep))
                mxidx = np.argmax(abs(blockcep))
                print('analysis.action: blockcep absmx = ' + str(absmx) + ' at index ' + str(mxidx))


        # encode ndelay for block as np.float32(ndelay) in blockcep[511] 
        # encode vuv for block as np.float32(ndelay) in blockcep[512] 
        ndelay = np.float32(ndelay)
        blockcep[511] = ndelay
        vuv = np.float32(vuv)
        blockcep[512] = vuv


        if diagnostics:
            if i%10 == 0:
                print('analysis.action: after conv to float32 type(ndelay) = ' + str(type(ndelay)))
                print('analysis.action: ndelay = ' + str(ndelay) + ' write to blockcep[511]')
                print('analysis.action: blockcep[511]  = ' + str(blockcep[511]))
                print('analysis.action: vuv = ' + str(vuv) + ': write to blockcep[512]')
                print('analysis.action: blockcep[512]  = ' + str(blockcep[512]))


        # append blockcep to cep
        cep = np.append(cep, blockcep)

        # increment block index
        i += 1



    # write ndarray cep to ceppath
    cep = cep.astype(np.float32)
    if diagnostics:
        print('\n\n\n&&&&&& analysis.action: writing cep to ' + ceppath + ' type(cep[0]) = ' + str(type(cep[0])))
    cep.tofile(ceppath)


    # report
    print('analysis.action: read ' + str(i) + ' overlapping sound-blocks from ' + sfpath)
    print('analysis.action: wrote ' + str(i) + ' cepstral-blocks to ' + ceppath)
    print('analysis.action: cepstral-blocks cep = ' + str(cep))

    # sanity check on cep 
    if diagnostics:
        sanity_cep = np.fromfile(ceppath, dtype=np.float32)  
        print("\n\nanalysis.action: sanity check: reading cepstral coefs sanity_cep from " + ceppath)
        print('analysis.action: els of sanity_cep have type ' + str(type(sanity_cep[0])))
        print('analysis.action: sanity_cep.size should be ' + str(i*1024))
    print("analysis.action: sanity_cep has size " + str(sanity_cep.size))
    print("analysis.action: ceppath has size (bytes) = " + str(os.path.getsize(ceppath)))

    print("\n\nANALYSIS complete\n\n")

    # return samplerate for use in synthesis sf.write
    return sr



if __name__ == "__main__": 
    print("\n*** analysis module running in unit-test mode as __main__")

    print('\n\n@@@ analysis unit test[1]:')

    # test voiced_unvoiced - although NOT PRESENTLY USED
    print('\n*** voiced_unvoiced test:')
    print('voiced_unvoiced returns result r in [0,1]')
    print('if r < .5 => block is unvoiced (aperiodic), else voiced (periodic)')

    samples = np.linspace(0, 1, 1024, dtype=np.float, endpoint=False)
    sine = np.sin(2 * np.pi * 5 * samples)      # freq=5, samples - [0,1]
    sinev = voiced_unvoiced(sine)
    print('\nvoiced_unvoiced test result for sine = ' + str(sinev))

    noise = np.random.normal(0, 1, 1024)  # (mean, stddev, nsamples)
    noisev = voiced_unvoiced(noise)
    print('voiced_unvoiced test result for noise = ' + str(noisev))


    # calculate and write cepstral coefs
    print('\n\n\n@@@ analysis unit test[2]:')
    if len(sys.argv) > 2:
        sfpath = sys.argv[1]
        ceppath = sys.argv[2]
    else:
        sfpath = '../../sf/test/test.wav' 
        ceppath = '../../cep/test/test.cep'
        diagnostics = True
    print('\n*** analysis test: calculate cepstral coefs for ' + sfpath)
    print('*** analysis test: write cepstral coefs to ' + ceppath)

    sr = action(sfpath, ceppath)
    print('\nanalysis.action returned sr = ' + str(sr))

    if sfpath == '../../sf/test/test.wav':
        print('\n\nsanity check: expect cepstral values from ' + sfpath + ': [-6.15914144  2.33930019  0.44331433 ... -0.99753415 -1.49761979 -2.99770543]')

    cep:np.ndarray = np.fromfile(ceppath, dtype=np.float64)
    print('\nsanity check: analysis wrote cepstral values ' + str(cep))


    print("\n\nANALYSIS unit test complete")


else:
    print('module <analysis> loaded')

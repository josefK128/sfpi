# test_cepsf_f32.py

import sys
import numpy as np
from scipy import signal
from acoustics.cepstrum import complex_cepstrum, inverse_complex_cepstrum, real_cepstrum
import soundfile as sf
sys.path.append('C:/public/music-synth/@sfpi/src/util')
import graph


# plot==True => process 1 blk - plot window, soundblk, cepblk, synth-soundblk
plot:bool = False



def test_cepsf(sfpath:str, ceppath:str) -> None:
    print("\n\n\nTEST_CEPSF_F32")
    print("\ntest_cepsf: sfpath = " + sfpath)
    print("test_cepsf: ceppath = " + ceppath)

    # sf.info: nchannels, sr, subtype
    info = sf.info(sfpath)
    print("\ntest_cepsf: " + sfpath + " sf.info:\n" + str(info))
    print("test_cepsf: type(info) = + " + str(type(info)))
    nchannels = info.channels
    sr:int = info.samplerate
    subtype = info.subtype
    print("test_cepsf: plot = " + str(plot))

    if nchannels == 2:
        print('test_cepsf requires a MONO file - exiting')
        exit()


    # hann window - taper 1024-blocks of sf samples
    # overlapping hann windows sum to identity 
    window = signal.hann(1024, False)
    if plot:
        graph.grapharray(window, 1024)


    # read block by block, window block, take complex cepstrum, wr to ceppath
    # NOTE: sf.blocks produces blocks in [-1.,1.] due to dtype=np.float32
    i:int = 0
    cep:np.ndarray = np.array([], dtype=np.float32)
    for block in sf.blocks(sfpath, 1024, 512, dtype='float32', fill_value=0.0):

        # 1024-block read in as float32 - normalized to [-1.,1.] !!!
        # window the block - converts to float64! - convert back to float32
        block = np.multiply(block, window).astype(np.float32)

        # plot needs values in [-1.,1.]
        if plot:
            graph.grapharray(block, 1024)


        # reading block as dtype=no.float32 maps to [-1.,1.]
        # therefore multiply by 32767. to restore int16 dynamic range
        #block = np.multiply(block, 32767.)
        if i%10 == 0:
            absmx = np.amax(abs(block))
            print('&&& i = ' + str(i) + ': absmax of block = ' + str(absmx))


        # cepstrum of windowed block - returned as float64 - convert to float32
        # ndelay is a int phase translation factor
        blockcep, ndelay = complex_cepstrum(block)
        blockcep = blockcep.astype(np.float32)
        ndelay = ndelay.astype(np.float32)
        if i%10 == 0:
            print('\n&&& i = ' + str(i) + ': after conv. to float32, ndelay = ' + str(ndelay))

        if plot:
            graph.grapharray(blockcep, 1024)


        # cepstral coefs of sound samples in block
        #print('\nblockcep = ' + str(blockcep))

        # simulate analysis setting blockcep[511] = ndelay (used by synthesis)
        blockcep[511] = ndelay
        

        # accumulate cepstral coefs in cep
        cep = np.append(cep, blockcep[0:512]).astype(np.float32)
        if i == 100:
            print('\ntest_cepsf: at np.append type(cep[0]) = ' + str(type(cep[0])))

        # 'correct' blockcep[511] and blockcep[512] which in analysis
        # both hold ndelay but are set to zero in synthesis
        blockcep[511] = 0.0
        blockcep[512] = 0.0


        # synthesized block = inverse cepstrum of blockcep
        # NOTE: block bounded by [-1.,1.] - see above - sf.blocks dtype=float32
        block = inverse_complex_cepstrum(blockcep, ndelay).astype(np.float32)
        if i == 100:
            print('\n\n*** test_cepsf: checking cep-icep 1024-block')
            print('&&& type(synthesized-block[0]) = ' + str(type(block[0])))
            mx = np.max(block)
            mn = np.min(block)
            mxidx = np.argmax(block)
            mnidx = np.argmin(block)
            print('block max = ' + str(mx) + ' at index ' + str(mxidx))
            print('block min = ' + str(mn) + ' at index ' + str(mnidx))
            print('block ' + str(i) + ' = ' + str(block))
            #print("*** type(block) is " + str(type(block)))
            #print("*** type(block[0]) is " + str(type(block[0])))

        # plot reconstructed waveform
        if plot:
            # scale from [-32767, 32767] to [-1.,1.] for graphing
            #block = np.divide(block, 32767.).astype(np.float32)
            graph.grapharray(block, 1024)


        # increment block index
        i+=1


        # if plot == True => make 4 plots and then break 
        if plot:
            if i == 1:
                break


    # cepstral coefs accumulated in cep
    if plot == False:
        #print('\n\ncep = ' + str(cep))
        cep.tofile(ceppath)

    print("\n\nTEST_CEPSF_F32 complete")




if __name__ == "__main__": 
    print('\n\n@@@ TEST_CEPSF_F32 e2e test:')

    # calculate and write cepstral coefs
    if len(sys.argv) == 1:
        sfpath = '../sf/test/test.wav'
        ceppath = '../cep/test/test_cepsf.cep' 
    else:
        sfpath = sys.argv[1]
        ceppath = sys.argv[2]

    test_cepsf(sfpath, ceppath)

    print('\n\n@@@ TEST_CEPSF_f32 e2e test complete:')


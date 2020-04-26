# generatewave.py

import sys
import numpy as np
import scipy.signal as signal
import soundfile as sf
import graph 


diagnostics = True


def generatewave(sfpath:str, type:str='unitdc', length:int=44100, freq:int=1) -> np.ndarray:

    print("\n\nGENERATEWAVE")
    print('\ngeneratewave: wave sfpath = ' + str(sfpath))

    # generate wave
    timepoints = np.linspace(0,1, length)
    if type == 'sawtooth':
        wave = signal.sawtooth(2*np.pi* freq * length * timepoints, width=1.0)
        # HACK !!!!
        if length == 2048:
            if wave[2047] == -1.0:
                print('\ngeneratewave: HACK - wave[2047] = -1.0 !!!!!!!!')
                wave[2047] = 1.0
                print('generatewave: HACK - after correction wave[2047] = ' + str(wave[2047]))
    if type == 'unitdc':
        wave = np.ones(length)


    # expand the wave to int16 bounds = [-32767,32767]
    wave = np.multiply(wave, 32767)
    if diagnostics:
        print('\n\ngeneratewave: wave = ' + str(wave))
        print('wave.size = ' + str(wave.size))


    # write wave to sfpath
    wavesf = wave.astype(np.int16)
    if diagnostics:
        print('generatewave: after conv to int16 wavesf = ' + str(wavesf))
        print('generatewave: wavesf.size = ' + str(wavesf.size))
    sf.write(sfpath, wavesf, samplerate=44100)

    print("\n\nGENERATEWAVE complete")

    return wave



if __name__ == "__main__": 
    print("\n*** generatewave module creates unitdc or sawtooth as int16 [-32767,32767] sfpath")
    print('\nNOTE: supplied sfpath arg only => use defaults (unitdc,44100,1)')
    print("exp cmdline usage: util> py generatewave.py ../../sf/test/unitdc.wav - generates default unitdc to default ../../sf/test/unitdc.wav")
    print('\nNOTE: non-default => use ALL arg positions!')
    print('exp cmdline usage: util> py generatewave.py ../../sf/test/sawshort.wav sawtooth 2018 1')


    # defaults: type, freq and length = 1sec at assumed sr=44100
    type:str = 'unitdc'
    length:int = 44100
    freq:int = 1

    if len(sys.argv) < 2:
        # test - generate unitdc with above defaults - diagnostics==True
        sfpath = '../../sf/test/unitdc.wav'
        diagnostics = True
    else:
        # non-default => use cmdline args ONLY
        sfpath = sys.argv[1]
        type = sys.argv[2]
        length = int(sys.argv[3])
        freq = int(sys.argv[4])
        
    # diagnostics
    print('\n\n\n@@@ generatewave: writing wave to sfpath = ' + sfpath)
    print('generatewave: type = ' + str(type))
    print('generatewave: freq = ' + str(freq))
    print('generatewave: length = ' + str(length))


    # create wave-file at sfpath 
    generatewave(sfpath, type=type, length =length, freq=freq)


    # sanity check
    wave, sr = sf.read(sfpath, dtype=np.int16)
    if diagnostics:
        print('\n\n@@@ generatewave test sanity: reading back ' + sfpath)
        print('generatewave test sanity: sr = ' + str(sr))
        print('generatewave test sanity: wave = ' + str(wave))
        print('generatewave test sanity: wave.size = ' + str(wave.size))

    # show generated wave-file
    graph.grapharray(np.divide(wave, 32767), length)


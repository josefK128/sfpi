# graph.py

import sys
import numpy as np
import soundfile as sf
import matplotlib.pyplot as plot
from typing import Tuple



def grapharray(a:np.ndarray, plotlength:int=44100) -> None:
    print('\n\nGRAPHARRAY')

    print('\ngrapharray: array size = ' + str(a.size))
    print('grapharray: plotlength = ' + str(plotlength))
    
    timepoints:int = np.linspace(0,1, plotlength)
    plot.plot(timepoints, a[0:plotlength])
    plot.title('waveform length = ' + str(plotlength))
    plot.xlabel('Time')
    plot.ylabel('Amplitude')
    plot.grid(True, which='both')
    plot.axhline(y=0, color='k')
    plot.ylim(-2,2)

    print('\n\nGRAPHARRAY complete')
    plot.show()


def graph(sfpath:str) -> None:
    print('\n\nGRAPH')

    info = sf.info(sfpath)
    print("\ngraph: " + sfpath + ".info:\n" + str(info))
    print("\ngraph: type(info) = + " + str(type(info)))
    nchannels = info.channels
    sr:int = info.samplerate
    subtype = info.subtype

    # read int16 sfpath into normalized float64 array 
    # NOTE: sf.read(file, dtype=float64, ...) - default array type is float64
    # NOTE: float64-ndarray is normalized to [-1.0,1.0]
    # NOTE: sf.read returns Tuple[np.ndarray, int] 
    T:Tuple[np.ndarray, int] = sf.read(sfpath)
    a:np.ndarray = T[0]
    sr = T[1]
    print('\n\ngraph: read ' + sfpath)
    print('\nint16-sf converted to normalized float64-ndarray a = ' + str(a))
    print('\ngraph: soundfile just read has sr = ' + str(sr))

    # nchannels
    if nchannels == 2:
        al = a[:,0]
        ar = a[:,1]
        a = np.multiply(np.add(al, ar), .5)
        print('\ngraph: converted a from stereo to mono - a = ' + str(a))

    # plot - grapharray()
    grapharray(a, a.size)

    print('\n\nGRAPH complete\n\n')




if __name__ == "__main__": 
    print("\n*** graph module running as __main__")
    print("cmdline usage: util> py graph.py sfpath='../../sf/test/unitdc.wav'")

    if( len(sys.argv) < 2):
        sfpath = '../../sf/test/unitdc.wav'
        print('\ngraph test: using default unitdc soundfile = ' + sfpath) 
    else:    
        sfpath = sys.argv[1]
        print('\ngraph: graphing soundfile at sfpath = ' + sfpath) 

    graph(sfpath)




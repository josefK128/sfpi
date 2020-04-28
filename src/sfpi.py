# sfpi.py

import sys
import json
import numpy as np
from scipy import signal  
import soundfile as sf
sys.path.append('C:/public/music-synth/@sfpi/src/analysis')
sys.path.append('C:/public/music-synth/@sfpi/src/variation')
sys.path.append('C:/public/music-synth/@sfpi/src/synthesis')
sys.path.append('C:/public/music-synth/@sfpi/src/util')
import analysis
import variation
import synthesis
import diff
from typing import Tuple



# command line args
print('\n\n\n@@@ SFPI')
print('\n\n*** cmdline use: src> py sfpi.py [score]  (no ext .json)')
print("\nNOTE: score is the path after '../scores/' without file ext. 'json'")
print("NOTE: no cmdline arg score => run analysis-synthesis E2E-TEST using scores/test/test.json and sf/test/sitarC4_mono.wav 1KHz 2 second single tone")
print("\n\nNOTE: sys.path:")
for path in sys.path:
    print(path)


# path trunks
scorepath:str = '../scores/'
basehref:str = '../'
sfpath:str = basehref
ceppath:str = basehref
ceppath_:str = basehref
sfpath_:str = basehref



# sfpi.py ENTRY POINT
if __name__ == '__main__':

    # no cmdline arg => use 'scores/test/test.json' as unit-test
    # else use cmdline arg as score for production run - diagnostics F
    if len(sys.argv) < 2:
        scorepath += 'test/test.json'
        print('\n\n\n@@@ sfpi: E2E-TEST using score ' + scorepath)
        print('test soundfile is sf/test/test.wav == sf/base/sitarC4_mono.wav')
    else:
        scorepath += sys.argv[1] + '.json'
        print('\n\n\n@@@ sfpi: ANALYSIS-SYNTHESIS using score ' + scorepath)


    # parse score
    with open(scorepath, 'r') as f:
        score = json.load(f)
        print('\n\nsfpi: score = ' + str(score))
    
        _analysis = score['_analysis']
        _variation = score['_variation']
        _synthesis = score['_synthesis']
        print('\nsfpi: run analysis = ' + str(_analysis))
        print('sfpi: run variation = ' + str(_variation))
        print('sfpi: run synthesis = ' + str(_synthesis))
    
        sfpath += score['sfbranch']
        ceppath += score['cepbranch']
        sfpath_ += score['sfbranch_']
        ceppath_ += score['cepbranch_']
        print('sfpi: sfpath = ' + str(sfpath))
        print('sfpi: ceppath = ' + str(ceppath))
        print('sfpi: sfpath_ = ' + str(sfpath_))
        print('sfpi: ceppath_ = ' + str(ceppath_))

        sr = score['sr']
        composition = score['composition']
        print('sfpi: sr = ' + str(sr))
        print('sfpi: composition = ' + str(composition))
        

        # process score
        if _analysis:
            sr = analysis.action(sfpath, ceppath)
            score['sr'] = sr
            print('\nsfpi: after analysis.action return is sr = ' + str(sr))
    
        if _variation:
            variation.action(ceppath, ceppath_, composition)
            print('\nsfpi: after variation.action - no return')
        
        if _synthesis:
            synthesis.action(ceppath_, sfpath_, sr)
            print('\nsfpi: after synthesis.action - no return')

            # compare original sf and synthesized sf
            print('\n\n\n\nsfpi: diff.arraydiff distance(' + sfpath + ', ' + sfpath_ + ')')
            # read in isf at sfpath
            print('\nsfpi: reading initial soundfile isf = ' + sfpath)
            isf, sr = sf.read(sfpath, dtype='int16')
            print('sfpi: isf = ' + str(isf))
            #print('sfpi: isf[1014:1040] = ' + str(isf[1014:1040]))
            print('sfpi: sr = ' + str(sr))

            # read in isf_ from sfpath_
            print("\n\nsfpi: reading synthesized isf_ from " + sfpath_)
            isf_, sr_ = sf.read(sfpath_, dtype='int16')
            print('sfpi: isf_ = ' + str(isf_))
            #print('sfpi: isf_[1014:1040] = ' + str(isf_[1014:1040]))
            print('sfpi: sr_ = ' + str(sr_))

            # test - average error per sample
            # NOTE diff.arraydiff expects two int16 soundfiles
            print('\n\nsfpi: comparing isf and isf_')
            d, length = diff.arraydiff(isf, isf_)
            print('\n\nsfpi: total distance d = ' + str(d))
            print('sfpi: number of indices measured = ' + str(length))
            print('sfpi: *** sample distance d/length = ' + str(d/length))
            print('\nsfpi: NOTE: diff>0 even in variation passthru (exp:e2e-test) due to:')
            print('[1] cep_[512]=cep_[513]=0.0 after storing ndelay and vuv respectively')
            print('[2] possible global phase-error introduced in phase-unwrapping')
            print('However: there is no perceptible difference between the original file and the synthesized file')

            print('\n\n@@@ SFPI PROCESSING complete')

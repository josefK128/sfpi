import numpy as np

#from scipy.signal import (complex_cepstrum, inverse_complex_cepstrum,
#                          real_cepstrum, minimum_phase, sawtooth)
from scipy.signal import sawtooth
#from acoustics.cepstrum import *
from acoustics.cepstrum import complex_cepstrum, inverse_complex_cepstrum

from numpy.testing import (assert_array_almost_equal)
from typing import List


def test_complex_cepstrum() -> None:
    """The period of a periodic harmonic will show up as a peak in a
    complex cepstrum.
    """

    print("\n\n\n@@@@@@@@ TEST_CEPSTRUM: estimation of fundamental")
    duration:float = 5.0
    sr:float = 8000.0
    samples:int = int(sr * duration)
    t:List[float] = np.arange(samples) / sr
    fundamental:float = 100.0
    print("\nactual fundamental = " + str(fundamental))

    signal:np.ndarray = sawtooth(2. * np.pi * fundamental * t)
    print("\nusing sawtooth fundamental 100 => period = 80 (for sr=8000)")
#    for i in range(170):
#        if signal[i] == -1.0:
#            print("\n*******************")
#        print("signal["+str(i)+"] = " + str(signal[i]))
    ceps, _ = complex_cepstrum(signal)
    print("\nthen, since period = sr/fund = " + str(sr/fundamental))
    print("\nthe estimated fundamental = " + str(1.0/t[ceps.argmax()]))
    assert (fundamental == 1.0 / t[ceps.argmax()])

    print("\n\nTEST_CEPSTRUM: estimation of fundamental complete")



def test_inverse_complex_cepstrum() -> None:
    """Applying the complex cepstrum and then the inverse complex cepstrum
    should result in the original sequence.
    """
    print("\n\n\n@@@@@@@@ TEST_CEPSTRUM cep-icep == identity")
    x:np.ndarray = np.array([1.,4.,3.,7.,5.,6.,7.,7.,-5.,-4.,-3.,4.,-6.,6.,5.,9.,2.,1.])
    print("\nsignal x = " + str(x))

    ceps, ndelay = complex_cepstrum(x)
    print("\nndelay = " + str(ndelay))
    print("\nceps = " + str(ceps))

    y:np.ndarray = inverse_complex_cepstrum(ceps, ndelay)
    print("\ny = icep(cep(x)) = " + str(y))

    assert_array_almost_equal(x, y)
    print("\n\nTEST_CEPSTRUM: cep-icep == identity complete")


# run tests
test_complex_cepstrum()
test_inverse_complex_cepstrum()

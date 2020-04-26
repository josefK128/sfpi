    # read sfpath into np.int16 array 
    a:np.ndarray  
    sr:int
    a, sr = sf.read(sfpath)

    # convert stereo/mono int16-file to mono float-file 
    # NOTE - conversion to float maps al and ar values to [-1,, 1.]
    # Thus their sum is in [-2.,2.]
    # To average the sfs multiply by .5
    # at the same time multiply by 32767. to prepare to convert to int16
    # Therefore multiply al+ar by 16383.
    if nchannels == 2:
        al = a[:,0].astype(np.float64)
        ar = a[:,1].astype(np.float64)
        a = np.multiply(np.add(al, ar), 16383.)   
    else:
        a = a.astype(np.float64)

# ************************************************************
    # read sfpath into np.int16 array 
    a:np.ndarray  
    sr:int
    a, sr = sf.read(sfpath, dtype=np.float32)

    # convert stereo/mono int16-file to mono float-file 
    # NOTE - conversion to float maps al and ar values to [-1,, 1.]
    # Thus their sum is in [-2.,2.]
    # To average the sfs multiply by .5
    # at the same time multiply by 32767. to prepare to convert to int16
    # Therefore multiply al+ar by 16383.
    if nchannels == 2:
        al = a[:,0].astype(np.float32)
        ar = a[:,1].astype(np.float32)
        a = np.multiply(np.add(al, ar), 16383.)   
    else:
        a = a.astype(np.float64)


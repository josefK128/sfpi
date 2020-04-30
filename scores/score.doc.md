__score.doc.md__



 * scenarios of use:

     1 analysis of soundfile writes cepstral coefs file:
         _analysis: true
         _variation: false
         _synthesis: false

     2 cross-synthesis or time-stretch
         _analysis: false
         _variation: true
         _synthesis: true

     3 analysis of resonator for cross-synth - provide driverceppath driver
         _analysis: true
         _variation: true
         _synthesis: true



 * cross-synthesis:
     replace coefs of cep (ceppath) with coefs of drivercep (driverceppath)

     vuv:float is measure of degree of periodicity of the sound frame
     vuv near 0.0 => noise
     vuv near 1.0 => periodicity
     length:int = 1024
     hlength:int = 512
     N:int = hlength - threshold
     K:int = math.floor(hlength - N\*vuv)
    
     Say threshold = 128
     Then N = 512 - 128 = 384
     and  K = math.floor(512 - 384*vuv)
     vuv = 0.0 (noise) => range(K,hlength) = range(512,512) 
         => no copy,  so cep is entirely the original 'resonator' sf
     vuv = 1.0 (periodic) => range(K,hlength) = range(128,512) 
         => copy into cep[128,510] and cep[512,896] (cep[511] = ndelay !!!)


     Then replace cep coefs by drivercep coefs 
    
     for j in range(K, hlength):
         cep[pointer + j] = drivercep[pointer + j]
         cep[pointer + length - 1 - j] = drivercep[pointer + length - 1 - j]
'


* example e2e test score test.json:

{ "_analysis": true,
  "_variation": true,
  "_synthesis": true,

  "sfbranch": "sf/test/test.wav",           # directory of sf for analysis
  "cepbranch": "cep/test/test.cep",   # directory of cep for sfpath sf
  "cepbranch_": "cep_/test/test_.cep",  # directory of cep-coefs from variation
  "sfbranch_": "sf_/test/test_.wav",      # directory of synthesized sf

  "composition":{"cross_synthesis": false,
                 "driverceppath": null, 
                 "threshold": 128 }
}


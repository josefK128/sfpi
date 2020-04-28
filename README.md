__README.md__  

###### SFPI - Synthesis from Performance Information
###### Python cepstrum analysis-synthesis system for audio/music synthesis and variational autoencoder for vocal style transfer



###### setup

* install python 3.X (current latest 3.8.X) - see 
  https://www.python.org/downloads/ - simply click download button and follow 
  defaults for installation
  
* clone the repo - all the needed python application modules are in /src

  

* NOTE: there is an index.js Nodejs Socket.IO server and index.html Socket.IO client with corresponding entries in package.json for npm install and live-server launch - these files and package.json entries are for future possible Electron and/or web development and can be IGNORED with respect to the featured Python audio cepstral analysis-synthesis Variational Autoencoder application .



* NOTE: the Python sfpi application is intended to run in a virtual environment in order to simplify dependencies and deliver a self-contained package for application use. The first step is to create the virtual environment locally using the built-in utility 'venv':

  ​    (1)  sfpi> python -m venv env - this creates a directory 'env' 

  ​    (2)  the virtual environment should contain its own local copy of Python so that outside the virtual    

  ​           environment the system version of Python (and other modules to be installed presently) may       

  ​           vary independently of the sfpi application.

  ​    (3)  run 'which python' to verify the local executable is preferred - sfpi/env/scripts/python

  ​    (4)  make certain that the Python package/module installer is up to date: 

  ​           python -m pip install --upgrade pip

  ​    (5)  install all needed dependencies:  pip install -r requirements.txt

  ​    (6)  this application makes use of Python annotations (>=3.6) to enable type-check 'linting' via MyPy:

  ​           cd src.  

  ​           src> mypy  **/\*.py

  ​           This type-check should respond with: 'success: no issues found in 10 source files'

  

* to run an end-to-end test of the application itself -  src> py sfpi test/test - this orchestrates the application execution according the the 'score'  ../scores/test/test.json
  
* In this e2e-test an end-to-end test: **analysis.py** reads soundfile  ../*sf/test/test.wav* and writes a cepstral coefficients file  ../*cep/test/test.cep*;  **variation.py**  reads *../cep/test/test.cep* and writes the identical file to ../*cep\_/test/test\_.cep* (normaly variation.py will vary the cepstral file to create a new synthesized output soundfile but in the case it simply does a passthru); finally **synthesis.py**  reads *../cep\_/test/test\_.cep* and creates the output soundfile ../*sf\__/test/test\__.wav*.
  
  
  
* Other runs of the application are controlled by a composed score-file, say 

  scores/branch-directory-name/score-name.json  

  To launch the application with this score run src> py sfpi  branch-directory-name/score-name   (no prior path or .json extension is needed)

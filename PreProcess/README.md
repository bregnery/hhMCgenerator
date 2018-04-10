Pre-processing Instructions
===========================

TestingPreProcess.py is a framework lite program that makes a flat root tree
from the MiniAOD information. This program is intended only for validation of 
Monte Carlo simulation and not for doing a full analysis.

This was made to run with CMSSW_8_0_21

    cmsrel CMSSW_8_0_21
    cd CMSSW_8_0_21/src/
    git clone https://github.com/bregnery/hhMCgenerator.git
    scram b
    cmsenv
    cd hhMCgenerator

To run the preprocessing

    cd PreProcess/
    python TestingPreProcess.py


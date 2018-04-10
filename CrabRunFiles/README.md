CRAB Instructions
=================

First, set up the CRAB environment and obtain a proxy

    CRAB
    vprox

Now, clone this repository in the proper CMSSW release and compile

    cmsrel CMSSW_7_1_30
    cd CMSSW_7_1_30/src/
    git clone https://github.com/bregnery/hhMCgenerator.git
    scram b
    cmsenv
    cd hhMCgenerator

Then, store your gridpack on EOS and update submitGENSIMcrab.py to contain the
proper input files. Now, begin production of LHE and GEN-SIM files.

    cd CrabRunFiles/
    crab submit submitGENSIMcrab.py

After GEN-SIM production, a more recent version of CMSSW is needed. Obtain
this CMSSW release and compile
 
    cmsrel CMSSW_8_0_21
    cd CMSSW_8_0_21/src/
    git clone https://github.com/bregnery/hhMCgenerator.git
    scram b
    cmsenv
    cd hhMCgenerator 

Then, update submitGENSIMRAWcrab.py and produce GEN-SIM-RAW

    cd CrabRunFiles/
    crab submit submitGENSIMRAWcrab.py

Now, update submitAODSIMcrab.py and produce AODSIM

    crab submit submitAODSIMcrab.py

Finally, update submitMiniAODcrab.py and produce MiniAOD

    crab submit submitMiniAODcrab.py

If the whole process was successful, the output should be Radion_hh_wwww_M3500_MiniAOD.root
stored on EOS

Useful CRAB Commands
--------------------

To test, get estimates, and then submit do a crab dry run

    crab submit --dryrun submit.py
    crab proceed

To resubmit failed jobs

    crab resubmit crab_projecs/<project_directory>

To view job status go to: https://dashb-cms-job-task.cern.ch 


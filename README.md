Di-Higgs to WWWW Monte Carlo Generator
======================================

This repository contains programs that use gridpacks to produce GEN-SIM, GEN-SIM RAW, 
AODSIM, MiniAOD and LHE files in CMSSW. The gridpacks must be preduced with 
MadGraph5_aMC@NLO. A gridpack generator is available at this link: 
https://github.com/bregnery/MadGraphCardsForCMSSW

Instructions
============

These programs should be run on CERN's lxplus or Fermilab's lpc.

GEN-SIM and LHE Production
--------------------------

Production of GEN-SIM and LHE files requires CMSSW_7_1_30.

### Environment Set Up ###

Obtain the proper CMSSW release, clone this repository, and compile.

    cmsrel CMSSW_7_1_30
    cd CMSSW_7_1_30/src/
    git clone https://github.com/bregnery/hhMCgenerator.git
    scram b
    cmsenv
    cd hhMCgenerator

Make sure to copy your gridpack into this director. For more information about gridpacks,
please see https://github.com/bregnery/MadGraphCardsForCMSSW.

### Obtain Necessary Python Fragments ###

Use MCM to find the proper fragment, then download it.

    curl -s --insecure https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_fragment/B2G-RunIISummer15wmLHEGS-01167 --retry 2 --create-dirs -o Configuration/GenProduction/python/B2G-RunIISummer15wmLHEGS-01167-fragment.py 
    [ -s Configuration/GenProduction/python/B2G-RunIISummer15wmLHEGS-01167-fragment.py ]
    scram b

Now modify the python fragment to input the proper grid pack. In B2G-RunIISummer15wmLHEGS-01167-fragment.py
line 5 should be altered to include the gridpack tarball file. 

     args = cms.vstring('<gridpack_tarball>.tar.xz'),

Also make sure that the fragment contains a number of events 
less than or equal to the number of events used in the MadGraph cards
that produced the gridpack.

### Produce a cfg file with cmsdriver ###

Now the python fragment can be used to produce a configuration file.

    cmsDriver.py Configuration/GenProduction/python/B2G-RunIISummer15wmLHEGS-01167-fragment.py --fileout file:B2G-RunIISummer15wmLHEGS-01167.root --mc --eventcontent RAWSIM,LHE --customise SLHCUpgradeSimulations/Configuration/postLS1Customs.customisePostLS1,Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM,LHE --conditions MCRUN2_71_V1::All --beamspot Realistic50ns13TeVCollision --step LHE,GEN,SIM --magField 38T_PostLS1 --python_filename B2G-RunIISummer15wmLHEGS-01167_1_cfg.py --no_exec -n 97

### Produce GEN-SIM and LHE ###

Now use the configuration file to produce GEN-SIM and LHE files.

    scram b
    cmsRun B2G-RunIISummer15wmLHEGS-01167_1_cfg.py

If the program runs correctly, you should have a .root file to use with the next step.

GEN-SIM-DIGI-RAW and AODSIM Production
--------------------------------------

 

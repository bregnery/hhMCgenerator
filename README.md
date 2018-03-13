Di-Higgs to WWWW Monte Carlo Generator
======================================

This repository contains programs that use gridpacks to produce GEN-SIM, GEN-SIM RAW, 
AODSIM, MiniAOD and LHE files in CMSSW. The gridpacks must be preduced with 
MadGraph5_aMC@NLO. A gridpack generator is available at this link: 
https://github.com/bregnery/MadGraphCardsForCMSSW

Instructions
============

These programs should be run on CERN's lxplus or Fermilab's lpc.

Local Run Instructions
----------------------

First, clone this repository in the proper CMSSW release and compile

    cmsrel CMSSW_7_1_30
    cd CMSSW_7_1_30/src/
    git clone https://github.com/bregnery/hhMCgenerator.git
    scram b
    cmsenv
    cd hhMCgenerator

Then, store your gridpack here and begin production of LHE and GEN-SIM files.

    cd LocalRunFiles/
    cmsRun B2G-RunIISummer15wmLHEGS-01167_1_cfg.py

After GEN-SIM production, a more recent version of CMSSW is needed. Obtain
this CMSSW release and compile
 
    cmsrel CMSSW_8_0_21
    cd CMSSW_8_0_21/src/
    git clone https://github.com/bregnery/hhMCgenerator.git
    scram b
    cmsenv
    cd hhMCgenerator 

Then, produce GEN-SIM-RAW and AODSIM

    cd LocalRunFiles/
    cmsRun B2G-RunIISummer16DR80Premix-01267_1_cfg.py
    cmsRun B2G-RunIISummer16DR80Premix-AODSIM_2_cfg.py

Finally, produce MiniAOD

    cmsRun B2G-RunIISummer16MiniAODv2_Radion_hh_wwww_M3500-MiniAOD_1_cfg.py

If the whole process was successful, the output should be Radion_hh_wwww_M3500_MiniAOD.root

CRAB Instructions
-----------------

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

CMSSW cfg.py Production Instructions
====================================

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

Now modify the python fragment to input the proper grid pack. In CMSSW_X_X_X/src/Configuration/Genproduction/python/B2G-RunIISummer15wmLHEGS-01167-fragment.py
line 5 should be altered to include the gridpack tarball file. 

     args = cms.vstring('<gridpack_tarball>.tar.xz'),

Also make sure that the fragment contains a number of events 
less than or equal to the number of events used in the MadGraph cards
that produced the gridpack.

### Produce a cfg file with cmsdriver ###

*This step can be skipped* by using the provided B2G-RunIISummer15wmLHEGS-01167_1_cfg.py file as a template.
If necessary a cfg file can be produced using cmsdriver with the python fragment.

    cmsDriver.py Configuration/GenProduction/python/B2G-RunIISummer15wmLHEGS-01167-fragment.py --fileout file:B2G-RunIISummer15wmLHEGS-01167.root --mc --eventcontent RAWSIM,LHE --customise SLHCUpgradeSimulations/Configuration/postLS1Customs.customisePostLS1,Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM,LHE --conditions MCRUN2_71_V1::All --beamspot Realistic50ns13TeVCollision --step LHE,GEN,SIM --magField 38T_PostLS1 --python_filename B2G-RunIISummer15wmLHEGS-01167_1_cfg.py --no_exec -n 97

### Produce GEN-SIM and LHE ###

Now use the configuration file to produce GEN-SIM and LHE files.

    scram b
    cmsRun B2G-RunIISummer15wmLHEGS-01167_1_cfg.py

If the program runs correctly, you should have a .root file to use with the next step.

GEN-SIM-RAW and AODSIM Production
--------------------------------------

Production of GEN-SIM-RAW and AODSIM files requires CMSSW_8_0_21.

### Environment Set Up ###

Obtain the proper CMSSW release, clone this repository, and compile.

    cmsrel CMSSW_8_0_21
    cd CMSSW_8_0_21/src/
    git clone https://github.com/bregnery/hhMCgenerator.git
    scram b
    cmsenv
    cd hhMCgenerator

Make sure to copy your GEN-SIM and LHE files from the previous step to the new directory.

    cp ../../../CMSSW_7_1_30/src/hhMCgenerator/B2G-RunIISummer15wmLHEGS-01167_inLHE.root .
    cp ../../../CMSSW_7_1_30/src/hhMCgenerator/B2G-RunIISummer15wmLHEGS-01167.root .

### Produce cfg file with cmsdriver ###
 
*This step can be skipped* by using the provided B2G-RunIISummer16DR80Premix-01267_1_cfg.py 
and B2G-RunIISummer16DR80Premix-AODSIM_2_cfg.py files as templates.
If necessary a cfg file can be produced using cmsdriver. Note that the DAS client has changed so you will need
to copy the pile up files from B2G-RunIISummer16DR80Premix-01267_1_cfg.py.

    cmsDriver.py step1 --fileout file:Radion_hh_wwwww_M3500_GEN-SIM-RAW.root  --pileup_input "dbs:/Neutrino_E-10_gun/RunIISpring15PrePremix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v2-v2/GEN-SIM-DIGI-RAW" --mc --eventcontent PREMIXRAW --datatier GEN-SIM-RAW --conditions 80X_mcRun2_asymptotic_2016_TrancheIV_v6 --step DIGIPREMIX_S2,DATAMIX,L1,DIGI2RAW,HLT:@frozen2016 --nThreads 4 --datamix PreMix --era Run2_2016 --python_filename B2G-RunIISummer16DR80Premix-01267_1_cfg.py --no_exec --customise Configuration/DataProcessing/Utils.addMonitoring -n 97

    cmsDriver.py step2 --filein file:Radion_hh_wwwww_M3500_GEN-SIM-RAW.root --fileout file:B2G-RunIISummer16DR80Premix-Radion_hh_wwww_M3500_AODSIM.root --mc --eventcontent AODSIM --runUnscheduled --datatier AODSIM --conditions 80X_mcRun2_asymptotic_2016_TrancheIV_v6 --step RAW2DIGI,RECO,EI --nThreads 4 --era Run2_2016 --python_filename B2G-RunIISummer16DR80Premix-AODSIM_2_cfg.py --no_exec --customise Configuration/DataProcessing/Utils.addMonitoring -n 97

### Produce GEN-SIM-RAW and AODSIM ###

Now use the configuration file to produce GEN-SIM-RAW.

    scram b
    cmsRun B2G-RunIISummer16DR80Premix-01267_1_cfg.py

If the program was successful the output will be Radion_hh_wwwww_M3500_GEN-SIM-RAW.root.
Then use the next configuration file to produce AODSIM.

    scram b
    cmsRun B2G-RunIISummer16DR80Premix-AODSIM_2_cfg.py

Now there should be B2G-RunIISummer16DR80Premix-Radion_hh_wwww_M3500_AODSIM.root

MiniAOD Production
------------------

This final step also requires CMSSW_8_0_21. There should be no additional environment set up needed.

### Produce cfg file with cmsdriver ###

*This step can be skipped* by using the provided B2G-RunIISummer16MiniAODv2_Radion_hh_wwww_M3500-MiniAOD_1_cfg.py file as a template.
If necessary a cfg file can be produced using cmsdriver.

    cmsDriver.py step1 --fileout file:Radion_hh_wwww_M3500_MiniAOD.root --mc --eventcontent MINIAODSIM --runUnscheduled --datatier MINIAODSIM --conditions 80X_mcRun2_asymptotic_2016_TrancheIV_v6 --step PAT --nThreads 4 --era Run2_2016 --python_filename B2G-RunIISummer16MiniAODv2_Radion_hh_wwww_M3500-MiniAOD_1_cfg.py --no_exec --customise Configuration/DataProcessing/Utils.addMonitoring -n 82

### Produce MiniAOD ###

Now use the configuration file to produce MiniAOD.

    scram b
    cmsRun B2G-RunIISummer16MiniAODv2_Radion_hh_wwww_M3500-MiniAOD_1_cfg.py

If the whole process was successful, the output should be Radion_hh_wwww_M3500_MiniAOD.root

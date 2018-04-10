Local Run Instructions
======================

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


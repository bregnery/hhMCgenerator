from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()

config.General.requestName = 'Radion_hh_wwww_jets_M2000_GEN-SIM-RAW-100k'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.General.transferLogs = False

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'B2G-RunIISummer16DR80Premix_Radion_hh_wwww_M2000_GEN-SIM-RAW_cfg.py'
config.JobType.numCores = 4
config.JobType.maxMemoryMB = 5000

config.Data.inputDataset = '/MinBias/bregnery-Radion_hh_wwww_jets_M2000_GEN-SIM-100k_RAWSIMoutput-3f464eaef0b8b95c67a5ece847b51684/USER'
config.Data.inputDBS = 'phys03'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.Data.outLFNDirBase = '/store/user/bregnery/' 
config.Data.publication = True
config.Data.outputDatasetTag = 'Radion_hh_wwww_jets_M2000_GEN-SIM-RAW-100k'

config.Site.blacklist = ['T3_US_UMiss', 'T3_FR_IPNL', 'T2_CH_CSCS_HPC']
config.Site.storageSite = 'T3_US_FNALLPC'

from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()

config.General.requestName = 'Radion_hh_wwww_jets_GEN-SIM-RAW'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.General.transferLogs = False

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'B2G-RunIISummer16DR80Premix_Radion_hh_wwww_GEN-SIM-RAW_cfg.py'
config.JobType.numCores = 4
config.JobType.maxMemoryMB = 5000

config.Data.inputDataset = '/MinBias/bregnery-Radion_hh_wwww_jets_GEN-SIM_RAWSIMoutput-e677a3076ab91377c0ed4257643b4df4/USER'
config.Data.inputDBS = 'phys03'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.Data.outLFNDirBase = '/store/user/bregnery/' 
config.Data.publication = True
config.Data.outputDatasetTag = 'Radion_hh_wwww_jets_GEN-SIM-RAW'

config.Site.storageSite = 'T3_US_FNALLPC'

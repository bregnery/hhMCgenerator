from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()

config.General.requestName = 'Radion_hh_wwww_jets_M3500_GEN-SIM-100k'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.General.transferLogs = False

config.JobType.pluginName = 'PrivateMC'
config.JobType.psetName = 'B2G-RunIISummer15wmLHEGS_Radion_hh_wwww_M3500_GENSIM_cfg.py'

#config.Data.userInputFiles = ['run_generic_tarball_cvmfs.sh']
config.Data.outputPrimaryDataset = 'MinBias'
config.Data.splitting = 'EventBased'
config.Data.unitsPerJob = 250
NJOBS = 400  # This is not a configuration parameter, but an auxiliary variable that we use in the next line.
config.Data.totalUnits = config.Data.unitsPerJob * NJOBS
config.Data.outLFNDirBase = '/store/user/bregnery/' 
config.Data.publication = True
config.Data.outputDatasetTag = 'Radion_hh_wwww_jets_M3500_GEN-SIM-100k'

config.Site.blacklist = ['T3_US_UMiss', 'T3_FR_IPNL']
config.Site.storageSite = 'T3_US_FNALLPC'

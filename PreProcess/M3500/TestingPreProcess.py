import sys
import os
import math
import glob
import ROOT as root
from array import array
root.gROOT.SetBatch(True)

# load FWLite C++ libraries
root.gSystem.Load("libFWCoreFWLite.so");
root.gSystem.Load("libDataFormatsFWLite.so");
root.FWLiteEnabler.enable()

# load FWlite python libraries
from DataFormats.FWLite import Handle, Events

class Collections(object):
    '''
    Simple collection manager for FWLite
    '''

    def __init__(self):
        self.__collections = {}

    def add(self, name, cppType, label):
        self.__collections[name] = {'handle': Handle(cppType), 'label': label,}

    def get(self, name, event):
        label = self.__collections[name]['label']
        handle = self.__collections[name]['handle']
        event.getByLabel(label,handle)
        return handle.product()

def deltaPhi(phi0,phi1):
    result = phi0-phi1
    while result>root.TMath.Pi():
        result -= 2*root.TMath.Pi()
    while result<=-root.TMath.Pi():
        result += 2*root.TMath.Pi()
    return result

def deltaR(eta0,phi0,eta1,phi1):
    deta = eta0-eta1
    dphi = deltaPhi(phi0,phi1)
    return root.TMath.Sqrt(deta**2+dphi**2)


typeMap = {
    'I': int,
    'l': long,
    'F': float,
    'C': str,
}
arrayMap = {
    'I': 'i',
    'l': 'L',
    'F': 'f',
}

class AnalysisTree(object):
    def __init__(self):
        self.results = {}
        self.tree = root.TTree("AnalysisTree","AnalysisTree")
        self.results['run'] = array('i',[0])
        self.results['lumi'] = array('i',[0])
        self.results['event'] = array('L',[0])
        self.tree.Branch('run',self.results['run'],'run/I')
        self.tree.Branch('lumi',self.results['lumi'],'lumi/I')
        self.tree.Branch('event',self.results['event'],'event/l')

    def add(self,var,rootType):
        if var in self.results:
            logging.error('Attempting to add repeated variable "{0}"'.format(var))
            return
        if rootType in arrayMap:
            self.results[var] = array(arrayMap[rootType],[0])
            self.tree.Branch(var,self.results[var],'{0}/{1}'.format(var,rootType))
        else:
            self.results[var] = rootType
            self.tree.Branch(var,self.results[var])

    def set_run_lumi_event(self,run,lumi,event):
        self.results['run'][0] = run
        self.results['lumi'][0] = lumi
        #self.results['event'][0] = event

    def set(self,var,val):
        if var not in self.results:
            logging.error('No variable "{0}" in tree'.format(var))
            return
        if callable(val):
            val(self.results[var])
        else:
            self.results[var][0] = val

    def fill(self):
        self.tree.Fill()

    def clone(self):
        self.tree.CloneTree()
    
    def write(self):
        self.tree.Write()

    def reset(self):
        for var in self.results:
            self.results[var][0] = 0

def sortJets(jets):

    jetLead = None
    jetSublead = None
    jet3 = None
    jet4 = None

    # Get Leading Jet
    if len(jets) > 0:
        for ijet,jet in enumerate(jets):
            if jetLead == None: jetLead = jets[ijet]
            if jetLead != None and jets[ijet].pt() > jetLead.pt(): jetLead == jets[ijet]
        #print "Lead Jet pT: ", jetLead.pt()

    # Get Subleading Jet
    if len(jets) > 1:
        for jjet,jet in enumerate(jets):
            if jetSublead == None and jetLead.pt() > jets[jjet].pt(): 
                jetSublead = jets[jjet]
            if jetSublead != None and jetLead.pt() > jets[jjet].pt() > jetSublead.pt(): 
                jetSublead = jets[jjet]
        #print "Sublead Jet pT: ", jetSublead.pt()
    
    #Get Jet 3
    if len(jets) > 2:
        for kjet,jet in enumerate(jets):
            if jet3 == None and jetSublead.pt() > jets[kjet].pt(): 
                jet3 = jets[kjet]
            if jet3 != None and jetSublead.pt() > jets[kjet].pt() > jet3.pt():
                jet3 = jets[kjet]
        #print "Jet 3 pT: ", jet3.pt()

    #Get Jet 4
    if len(jets) > 3:
        for ljet,jet in enumerate(jets):
            if jet4 == None and jet3.pt() > jets[ljet].pt(): 
                jet4 = jets[ljet]
            if jet4 != None and jet3.pt() > jets[ljet].pt() > jet4.pt():
                jet4 = jets[ljet]
        #print "Jet 4 pT: ", jet4.pt()

    return jetLead, jetSublead, jet3, jet4


def process(events,**kwargs):
    maxEvents = kwargs.pop('maxEvents',-1)
    reportEvery = kwargs.pop('reportEvery',1000)

    tree = kwargs.pop('tree',None)

    #==================================
    # Load Collections ////////////////
    #==================================

    collections = Collections()

    collections.add("genParticles", "std::vector<reco::GenParticle>", "prunedGenParticles")
    collections.add("jets", "std::vector<pat::Jet>", "slimmedJets")
    collections.add("jetsAK8", "std::vector<pat::Jet>", "slimmedJetsAK8")
    collections.add("primaryVertices", "std::vector<reco::Vertex>", "offlineSlimmedPrimaryVertices")

    #==================================
    # Event Loop //////////////////////
    #==================================

    numEvents = events.size()
    if maxEvents>=0: numEvents = min(numEvents,maxEvents)
    for i,event in enumerate(events):
        if maxEvents>=0 and i>=maxEvents: break
        if i%reportEvery==0: print 'Processing event {0}/{1}'.format(i+1,numEvents)

        tree.reset()       
 
        #=================================
        # Event Variables ////////////////
        #=================================
        aux = event.eventAuxiliary()
        run, lumi, evt = aux.run(), aux.luminosityBlock(), aux.event()
        evtkey = (run,lumi,evt)
        #print ':'.join([str(x) for x in [run,lumi,evt]])
        #print ''

        tree.set_run_lumi_event(run,lumi,event)

        #================================
        # Vertices //////////////////////
        #================================
        vertices = collections.get('primaryVertices', event)

        tree.set('nPrimaryVertices', len(vertices) )

        #================================
        # genHiggs //////////////////////
        #================================
        genParticles = collections.get('genParticles', event)

        genHiggs1 = None
        genHiggs2 = None
        virtualW1 = None
        virtualW2 = None
        nGenHiggs = 0
        nVirGenWs = 0

        #print("Event number ", i)

        for ipart, genPart in enumerate(genParticles):
            if genHiggs1 == None and genPart.pdgId() == 25 and 40 > genPart.status() > 20:
                genHiggs1 = genPart
            elif genHiggs1 != None and genHiggs2 == None and genHiggs1 != genPart and genPart.pdgId() == 25 and 40 > genPart.status() > 20:
                genHiggs2 = genPart
            if genPart.pdgId() == 25 and 40 > genPart.status() > 20:
                nGenHiggs = nGenHiggs + 1\

            #print("PDG ID: ", genPart.pdgId() )
            #print("PDG Status: ", genPart.status() )

        tree.set('nGenHiggs', nGenHiggs)
        if genHiggs1 != None:
            tree.set('GenHiggs1_pt', genHiggs1.pt() )
            tree.set('GenHiggs1_eta', genHiggs1.eta() )
            tree.set('GenHiggs1_phi', genHiggs1.phi() )
            
            # Get virutal W bosons
            if genHiggs1.numberOfDaughters() == 3:
                nVirGenWs = nVirGenWs + 1
                if abs(genHiggs1.daughter(0).pdgId() ) == 24:
                    daughter1 = root.TLorentzVector(genHiggs1.daughter(1).px(), genHiggs1.daughter(1).py(), genHiggs1.daughter(1).pz(), genHiggs1.daughter(1).energy() )
                    daughter2 = root.TLorentzVector(genHiggs1.daughter(2).px(), genHiggs1.daughter(2).py(), genHiggs1.daughter(2).pz(), genHiggs1.daughter(2).energy() )
                    virtualW1 = daughter1 + daughter2
                if abs(genHiggs1.daughter(2).pdgId() ) == 24:
                    daughter1 = root.TLorentzVector(genHiggs1.daughter(0).px(), genHiggs1.daughter(0).py(), genHiggs1.daughter(0).pz(), genHiggs1.daughter(0).energy() )
                    daughter2 = root.TLorentzVector(genHiggs1.daughter(1).px(), genHiggs1.daughter(1).py(), genHiggs1.daughter(1).pz(), genHiggs1.daughter(1).energy() )
                    virtualW1 = daughter1 + daughter2
            if genHiggs1.numberOfDaughters() == 4:
                    print("Two offshell W bosons!!!") 

        if genHiggs1 == None:
            tree.set('GenHiggs1_pt', 0 )
            tree.set('GenHiggs1_eta', 0 )
            tree.set('GenHiggs1_phi', 0 )
        if genHiggs2 != None:
            tree.set('GenHiggs2_pt', genHiggs2.pt() )
            tree.set('GenHiggs2_eta', genHiggs2.eta() )
            tree.set('GenHiggs2_phi', genHiggs2.phi() )

            # Get virtual W bosons
            if genHiggs2.numberOfDaughters() == 3:
                nVirGenWs = nVirGenWs + 1
                if abs(genHiggs2.daughter(0).pdgId() ) == 24:
                    daughter1 = root.TLorentzVector(genHiggs2.daughter(1).px(), genHiggs2.daughter(1).py(), genHiggs2.daughter(1).pz(), genHiggs2.daughter(1).energy() )
                    daughter2 = root.TLorentzVector(genHiggs2.daughter(2).px(), genHiggs2.daughter(2).py(), genHiggs2.daughter(2).pz(), genHiggs2.daughter(2).energy() )
                    virtualW2 = daughter1 + daughter2
                if abs(genHiggs2.daughter(2).pdgId() ) == 24:
                    daughter1 = root.TLorentzVector(genHiggs2.daughter(0).px(), genHiggs2.daughter(0).py(), genHiggs2.daughter(0).pz(), genHiggs2.daughter(0).energy() )
                    daughter2 = root.TLorentzVector(genHiggs2.daughter(1).px(), genHiggs2.daughter(1).py(), genHiggs2.daughter(1).pz(), genHiggs2.daughter(1).energy() )
                    virtualW2 = daughter1 + daughter2
        #    if genHiggs2.numberOfDaughters() == 4:
        #            print("Two offshell W bosons!!!") 

        if genHiggs2 == None:
            tree.set('GenHiggs2_pt', 0 )
            tree.set('GenHiggs2_eta', 0 )
            tree.set('GenHiggs2_phi', 0 )

        tree.set('nVirGenWs', nVirGenWs)
        if virtualW1 != None:
            tree.set('virGenW1_pt', virtualW1.Pt() )
            tree.set('virGenW1_phi', virtualW1.Phi() )
            tree.set('virGenW1_eta', virtualW1.Eta() )
            tree.set('virGenW1_mass', virtualW1.M() )

        if virtualW1 == None:
            tree.set('virGenW1_pt', 0 )
            tree.set('virGenW1_phi', 0 )
            tree.set('virGenW1_eta', 0 )
            tree.set('virGenW1_mass', 0 )

        if virtualW2 != None:
            tree.set('virGenW2_pt', virtualW2.Pt() )
            tree.set('virGenW2_phi', virtualW2.Phi() )
            tree.set('virGenW2_eta', virtualW2.Eta() )
            tree.set('virGenW2_mass', virtualW2.M() )

        if virtualW2 == None:
            tree.set('virGenW2_pt', 0 )
            tree.set('virGenW2_phi', 0 )
            tree.set('virGenW2_eta', 0 )
            tree.set('virGenW2_mass', 0 )

        #================================
        # genWboson /////////////////////
        #================================
        genW1 = None
        genW2 = None
        genW3 = None
        genW4 = None
        nGenWs = 0

        
        for ipart, genPart in enumerate(genParticles):
            if genW1 == None and abs(genPart.pdgId() ) == 24 and 50 > genPart.status() > 20:
                genW1 = genPart
            elif genW1 != None and genW2 == None and genW1 != genPart and abs(genPart.pdgId() ) == 24 and 50 > genPart.status() > 20:
                genW2 = genPart
            elif genW1 != None and genW2 != None and genW3 == None and genW1 != genPart and genW2 != genPart and abs(genPart.pdgId() ) == 24 and 50 > genPart.status() > 20:
                genW3 = genPart
            elif genW1 != None and genW2 != None and genW3 != None and genW4 == None and genW1 != genPart and genW2 != genPart and genW3 != genPart and abs(genPart.pdgId() ) == 24 and 50 > genPart.status() > 20:
                genW4 = genPart
            if abs(genPart.pdgId() ) == 24 and 50 > genPart.status() > 20:
                nGenWs = nGenWs + 1\

        nGenWs = nGenWs + nVirGenWs
        tree.set('nGenWs', nGenWs)
        if genW1 != None:
            tree.set('GenW1_pt', genW1.pt() )
            tree.set('GenW1_eta', genW1.eta() )
            tree.set('GenW1_phi', genW1.phi() )
            tree.set('GenW1_mass', genW1.mass() )
        if genW1 == None:
            tree.set('GenW1_pt', 0 )
            tree.set('GenW1_eta', 0 )
            tree.set('GenW1_phi', 0 )
            tree.set('GenW1_mass', 0 )
        if genW2 != None:
            tree.set('GenW2_pt', genW2.pt() )
            tree.set('GenW2_eta', genW2.eta() )
            tree.set('GenW2_phi', genW2.phi() )
            tree.set('GenW2_mass', genW2.mass() )
        if genW2 == None:
            tree.set('GenW2_pt', 0 )
            tree.set('GenW2_eta', 0 )
            tree.set('GenW2_phi', 0 )
            tree.set('GenW2_mass', 0 )
        if genW3 != None:
            tree.set('GenW3_pt', genW3.pt() )
            tree.set('GenW3_eta', genW3.eta() )
            tree.set('GenW3_phi', genW3.phi() )
            tree.set('GenW3_mass', genW3.mass() )
        if genW3 == None:
            tree.set('GenW3_pt', 0 )
            tree.set('GenW3_eta', 0 )
            tree.set('GenW3_phi', 0 )
            tree.set('GenW3_mass', 0 )
        if genW4 != None:
            tree.set('GenW4_pt', genW4.pt() )
            tree.set('GenW4_eta', genW4.eta() )
            tree.set('GenW4_phi', genW4.phi() )
            tree.set('GenW4_mass', genW4.mass() )
        if genW4 == None:
            tree.set('GenW4_pt', 0 )
            tree.set('GenW4_eta', 0 )
            tree.set('GenW4_phi', 0 )
            tree.set('GenW4_mass', 0 )

        #================================
        # Jets //////////////////////////
        #================================
        jets = collections.get('jets', event)

        tree.set('nJets', len(jets) )

        jetLead, jetSublead, jet3, jet4 = sortJets(jets)

        if jetLead != None:
            tree.set('LeadJet_pt', jetLead.pt() )
            tree.set('LeadJet_eta', jetLead.eta() ) 
            tree.set('LeadJet_mass', jetLead.mass() )
            tree.set('LeadJet_phi', jetLead.phi() )
        elif jetLead == None:
            tree.set('LeadJet_pt', 0 )
            tree.set('LeadJet_eta', 0 ) 
            tree.set('LeadJet_mass', 0 )
            tree.set('LeadJet_phi', 0 )
        if jetSublead != None: 
            tree.set('SubLeadJet_pt', jetSublead.pt() )
            tree.set('SubLeadJet_eta', jetSublead.eta() ) 
            tree.set('SubLeadJet_mass', jetSublead.mass() )
            tree.set('SubLeadJet_phi', jetSublead.phi() )
        elif jetSublead == None: 
            tree.set('SubLeadJet_pt', 0 )
            tree.set('SubLeadJet_eta', 0 ) 
            tree.set('SubLeadJet_mass', 0 )
            tree.set('SubLeadJet_phi', 0 )
        if jet3 != None:
            tree.set('Jet3_pt', jet3.pt() )
            tree.set('Jet3_eta', jet3.eta() ) 
            tree.set('Jet3_mass', jet3.mass() )
            tree.set('Jet3_phi', jet3.phi() )
        elif jet3 == None:
            tree.set('Jet3_pt', 0 )
            tree.set('Jet3_eta', 0 ) 
            tree.set('Jet3_mass', 0 )
            tree.set('Jet3_phi', 0 )
        if jet4 != None:
            tree.set('Jet4_pt', jet4.pt() )
            tree.set('Jet4_eta', jet4.eta() ) 
            tree.set('Jet4_mass', jet4.mass() )
            tree.set('Jet4_phi', jet4.phi() )
        elif jet4 == None:
            tree.set('Jet4_pt', 0 )
            tree.set('Jet4_eta', 0 ) 
            tree.set('Jet4_mass', 0 )
            tree.set('Jet4_phi', 0 )
        
	#=================================
        # JetsAK8 ////////////////////////
        #=================================
        jetsAK8 = collections.get('jetsAK8', event)

        tree.set('nJetsAK8', len(jetsAK8) )

        jetAK8Lead, jetAK8Sublead, jet3AK8, jet4AK8 = sortJets(jetsAK8)

        if jetAK8Lead != None:
            tree.set('LeadAK8Jet_pt', jetAK8Lead.pt() )
            tree.set('LeadAK8Jet_eta', jetAK8Lead.eta() ) 
            tree.set('LeadAK8Jet_mass', jetAK8Lead.mass() )
            tree.set('LeadAK8Jet_phi', jetAK8Lead.phi() )
            tree.set('LeadAK8Jet_softdrop_mass', jetAK8Lead.userFloat("ak8PFJetsCHSSoftDropMass") )
        elif jetAK8Lead == None:
            tree.set('LeadAK8Jet_pt', 0 )
            tree.set('LeadAK8Jet_eta', 0 ) 
            tree.set('LeadAK8Jet_mass', 0 )
            tree.set('LeadAK8Jet_phi', 0 )
            tree.set('LeadAK8Jet_softdrop_mass', 0 )
        if jetAK8Sublead != None: 
            tree.set('SubLeadAK8Jet_pt', jetAK8Sublead.pt() )
            tree.set('SubLeadAK8Jet_eta', jetAK8Sublead.eta() ) 
            tree.set('SubLeadAK8Jet_mass', jetAK8Sublead.mass() )
            tree.set('SubLeadAK8Jet_phi', jetAK8Sublead.phi() )
            tree.set('SubLeadAK8Jet_softdrop_mass', jetAK8Sublead.userFloat("ak8PFJetsCHSSoftDropMass") )
        elif jetAK8Sublead == None: 
            tree.set('SubLeadAK8Jet_pt', 0 )
            tree.set('SubLeadAK8Jet_eta', 0 ) 
            tree.set('SubLeadAK8Jet_mass', 0 )
            tree.set('SubLeadAK8Jet_phi', 0 )
            tree.set('SubLeadAK8Jet_softdrop_mass', 0 )
        if jet3AK8 != None:
            tree.set('Jet3AK8_pt', jet3.pt() )
            tree.set('Jet3AK8_eta', jet3.eta() ) 
            tree.set('Jet3AK8_mass', jet3.mass() )
            tree.set('Jet3AK8_phi', jet3.phi() )
            tree.set('Jet3AK8_softdrop_mass', jet3AK8.userFloat("ak8PFJetsCHSSoftDropMass") )
        elif jet3AK8 == None:
            tree.set('Jet3AK8_pt', 0 )
            tree.set('Jet3AK8_eta', 0 ) 
            tree.set('Jet3AK8_mass', 0 )
            tree.set('Jet3AK8_phi', 0 )
            tree.set('Jet3AK8_softdrop_mass', 0 )
        if jet4AK8 != None:
            tree.set('Jet4AK8_pt', jet4.pt() )
            tree.set('Jet4AK8_eta', jet4.eta() ) 
            tree.set('Jet4AK8_mass', jet4.mass() )
            tree.set('Jet4AK8_phi', jet4.phi() )
            tree.set('Jet4AK8_softdrop_mass', jet4AK8.userFloat("ak8PFJetsCHSSoftDropMass") )
        elif jet4AK8 == None:
            tree.set('Jet4AK8_pt', 0 )
            tree.set('Jet4AK8_eta', 0 ) 
            tree.set('Jet4AK8_mass', 0 )
            tree.set('Jet4AK8_phi', 0 )
            tree.set('Jet4AK8_softdrop_mass', 0 )
      
        #==================================
        # Fill Tree ///////////////////////
        #==================================
        tree.fill() 
       

#redirector = 'root://cms-xrd-global.cern.ch'
#redirector = 'root://cmsxrootd.fnal.gov'

files = glob.glob("/afs/cern.ch/work/b/bregnery/public/HHwwwwMCgenerator/CMSSW_8_0_21/src/hhMCgenerator/RootFiles/M3500/*.root") 

#[
#    '../RootFiles/M3500/Radion_hh_wwww_M3500_MiniAOD_1.root',
#]

outFile = root.TFile("Radion_HH_wwww_FWLite.root",'RECREATE')
outFile.cd()

#==================================
# Add the Tree Branches ///////////
#==================================

tree = AnalysisTree()

tree.add('nGenHiggs', 'F')
tree.add('GenHiggs1_pt', 'F')
tree.add('GenHiggs1_phi', 'F')
tree.add('GenHiggs1_eta', 'F')
tree.add('GenHiggs2_pt', 'F')
tree.add('GenHiggs2_phi', 'F')
tree.add('GenHiggs2_eta', 'F')

tree.add('nVirGenWs', 'F')
tree.add('virGenW1_pt','F')
tree.add('virGenW1_phi','F')
tree.add('virGenW1_eta','F')
tree.add('virGenW1_mass','F')
tree.add('virGenW2_pt','F')
tree.add('virGenW2_phi','F')
tree.add('virGenW2_eta','F')
tree.add('virGenW2_mass','F')

tree.add('nGenWs', 'F')
tree.add('GenW1_pt', 'F')
tree.add('GenW1_phi', 'F')
tree.add('GenW1_eta', 'F')
tree.add('GenW1_mass', 'F')
tree.add('GenW2_pt', 'F')
tree.add('GenW2_phi', 'F')
tree.add('GenW2_eta', 'F')
tree.add('GenW2_mass', 'F')
tree.add('GenW3_pt', 'F')
tree.add('GenW3_phi', 'F')
tree.add('GenW3_eta', 'F')
tree.add('GenW3_mass', 'F')
tree.add('GenW4_pt', 'F')
tree.add('GenW4_phi', 'F')
tree.add('GenW4_eta', 'F')
tree.add('GenW4_mass', 'F')

tree.add('LeadJet_pt', 'F')
tree.add('LeadJet_eta', 'F')
tree.add('LeadJet_mass', 'F')
tree.add('LeadJet_phi', 'F')
tree.add('SubLeadJet_pt', 'F')
tree.add('SubLeadJet_eta', 'F')
tree.add('SubLeadJet_phi', 'F')
tree.add('SubLeadJet_mass', 'F')
tree.add('Jet3_pt', 'F')
tree.add('Jet3_eta', 'F')
tree.add('Jet3_mass', 'F')
tree.add('Jet3_phi', 'F')
tree.add('Jet4_pt', 'F')
tree.add('Jet4_eta', 'F')
tree.add('Jet4_mass', 'F')
tree.add('Jet4_phi', 'F')
tree.add('nJets', 'F')

tree.add('LeadAK8Jet_pt', 'F')
tree.add('LeadAK8Jet_eta', 'F')
tree.add('LeadAK8Jet_mass', 'F')
tree.add('LeadAK8Jet_softdrop_mass', 'F')
tree.add('LeadAK8Jet_phi', 'F')
tree.add('SubLeadAK8Jet_pt', 'F')
tree.add('SubLeadAK8Jet_eta', 'F')
tree.add('SubLeadAK8Jet_mass', 'F')
tree.add('SubLeadAK8Jet_softdrop_mass', 'F')
tree.add('SubLeadAK8Jet_phi', 'F')
tree.add('Jet3AK8_pt', 'F')
tree.add('Jet3AK8_eta', 'F')
tree.add('Jet3AK8_mass', 'F')
tree.add('Jet3AK8_softdrop_mass', 'F')
tree.add('Jet3AK8_phi', 'F')
tree.add('Jet4AK8_pt', 'F')
tree.add('Jet4AK8_eta', 'F')
tree.add('Jet4AK8_mass', 'F')
tree.add('Jet4AK8_softdrop_mass', 'F')
tree.add('Jet4AK8_phi', 'F')
tree.add('nJetsAK8', 'F')
tree.add('nPrimaryVertices', 'F')

   
events = Events(files)
process(events,maxEvents=100000,tree=tree)
    
outFile.Write()
outFile.Close() 
   

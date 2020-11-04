// -*- C++ -*-
//
// Package:    PFHCalib/PFHadHLT
// Class:      PFHadHLT
// 
/**\class PFHadHLT PFHadHLT.cc PFHadCalib/PFHadHLT/plugins/PFHadHLT.cc
Description: [one line class summary]
Implementation:
[Notes on implementation]
*/
//
// Original Author:  Dr. Lee Sehwook
//         Created:  Thu, 26 Mar 2015 07:49:04 GMT
//
//


// system include files
#include <memory>

// user include files

#include "JMETriggerAnalysis/NTuplizers/plugins/PFHadHLT.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"
#include "DataFormats/ParticleFlowReco/interface/PFBlock.h"
#include "DataFormats/ParticleFlowReco/interface/PFBlockElementTrack.h"

#include "FWCore/Framework/interface/ESHandle.h"

#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/Utilities/interface/Exception.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "TLorentzVector.h"

//
// constants, enums and typedefs
//

//
// static data member definitions
//

using namespace std;
using namespace edm;
using namespace reco;

//
// constructors and destructor
//
PFHadHLT::PFHadHLT(const edm::ParameterSet& iConfig)
{
	nCh = std::vector<unsigned int>(10,static_cast<unsigned int>(0));
	nEv = std::vector<unsigned int>(2,static_cast<unsigned int>(0));

	//now do what ever initialization is needed
	//hltpfcandTag      = iConfig.getParameter<edm::InputTag>("HLTPFCandidates");
	//PFSimParticlesTag = iConfig.getParameter<edm::InputTag>("PFSimParticles");

	hltpfcandTag =  consumes<reco::PFCandidateCollection> ( iConfig.getParameter<edm::InputTag>("HLTPFCandidates") );
	//PFSimParticlesTag = consumes<reco::PFCandidateCollection> ( iConfig.getParameter<edm::InputTag>("PFSimParticles") ) ;
	PFSimParticlesTag = consumes<reco::PFSimParticleCollection> ( iConfig.getParameter<edm::InputTag>("PFSimParticles") ) ;
	genParInfoTag = consumes<reco::GenParticleCollection>(iConfig.getParameter<edm::InputTag>("genParTag"));

	// Smallest track pt
	ptMin_ = iConfig.getParameter<double>("ptMin");

	// Smallest track p
	pMin_ = iConfig.getParameter<double>("pMin");

	// Smallest raw HCAL energy linked to the track
	hcalMin_ = iConfig.getParameter<double>("hcalMin");

	// Largest ECAL energy linked to the track to define a MIP
	ecalMax_ = iConfig.getParameter<double>("ecalMax");

	// Smallest number of pixel hits
	nPixMin_ = iConfig.getParameter<int>("nPixMin");

	// Smallest number of track hits in different eta ranges
	nHitMin_ = iConfig.getParameter< std::vector<int> > ("nHitMin");
	nEtaMin_ = iConfig.getParameter< std::vector<double> > ("nEtaMin");

	// The root tuple
	outputfile_ = iConfig.getParameter<std::string>("rootOutputFile"); 
	tf1 = new TFile(outputfile_.c_str(), "RECREATE");  
	s = new TTree("s"," PFCalibration");


}


PFHadHLT::~PFHadHLT()
{

	// do anything here that needs to be done at desctruction time
	// (e.g. close files, deallocate resources etc.)

	std::cout << "Total number of events .............. " << nEv[0] << std::endl;
	std::cout << "Number of events with 1 Sim Particle  " << nEv[1] << std::endl;

	std::cout << "Number of PF candidates ............. " << nCh[0] << std::endl;
	std::cout << "Number of PF Charged Hadrons......... " << nCh[1] << std::endl;
	std::cout << " - With pt > " << ptMin_ << " GeV/c ................ " << nCh[2] << std::endl;
	std::cout << " - With E_HCAL > " << hcalMin_ << " GeV .............. " << nCh[3] << std::endl;
	std::cout << " - With only 1 track in the block ... " << nCh[4] << std::endl;
	std::cout << " - With p > " << pMin_ << " GeV/c ................. " << nCh[5] << std::endl;
	std::cout << " - With at least " << nPixMin_ << " pixel hits ....... " << nCh[6] << std::endl;
	std::cout << " - With E_ECAL < " << ecalMax_ << " GeV ............ " << nCh[8] << std::endl;
	std::cout << " - PF - Gen track matching ..... " << nCh[7] << std::endl;

	tf1->cd();
	s->Write();
	tf1->Write();
	tf1->Close();  

}



//
// member functions
//

// ------------ method called for each event  ------------
	void
PFHadHLT::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
	//using namespace edm;
	Reset_variables();

	edm::Handle<GenParticleCollection> genParticles;
	iEvent.getByToken(genParInfoTag, genParticles); /* get genParticle information */

	Handle<HltParticleFlow> hltpf;
	//iEvent.getByLabel(hltpfcandTag, hltpf);
	iEvent.getByToken(hltpfcandTag, hltpf);

	Handle<PFSimParticleCollection> trueParticles;
	//bool isSimu = iEvent.getByLabel(PFSimParticlesTag, trueParticles);
	bool isSimu = iEvent.getByToken(PFSimParticlesTag, trueParticles);

	pfcsID.clear();
	Eecal_.clear();
	Ehcal_.clear();
	dr_.clear();

	nEv[0]++;
	std::vector<int> genPart;
	genPart.clear();
	if ( isSimu ) { 
		for( GenParticleCollection::const_iterator itGenPar = genParticles->begin(); itGenPar != genParticles->end(); itGenPar++ ){
			float dR_ = -1;
			float mindR_ = 99;
			if(itGenPar->status() == 1){
				//if(abs(itGenPar->pdgId()) == 211) cout << "charge : " << itGenPar->pdgId() << ", pT : " << itGenPar->pt() << ", eta : " << itGenPar->eta() << ", phi : " << itGenPar->phi() << endl;
				if(itGenPar->pdgId() == -211){
					for ( GenParticleCollection::const_iterator jtGenPar = genParticles->begin(); jtGenPar != genParticles->end(); jtGenPar++ ){
						if(itGenPar != jtGenPar){
							dR_ = reco::deltaR(itGenPar->eta(), itGenPar->phi(), jtGenPar->eta(), jtGenPar->phi());
							if(dR_ < mindR_) mindR_ = dR_;
						}
					}
					//dr_.push_back(mindR_);
					if(mindR_ > 1.){
						for(int itTruePar=0;itTruePar<(int)(*trueParticles).size();itTruePar++) {
              const reco::PFSimParticle& ptc = (*trueParticles)[itTruePar];
							if((*trueParticles)[itTruePar].charge()>0) continue;
							const reco::PFTrajectoryPoint& gen = (*trueParticles)[itTruePar].trajectoryPoint(reco::PFTrajectoryPoint::ClosestApproach);
							dR_ = reco::deltaR(itGenPar->eta(), itGenPar->phi(), gen.momentum().Eta(),gen.momentum().Phi());
							if(dR_ > 0.01) continue;
							nEv[1]++;

							// Check if there is a reconstructed track
							isCharged = false;
							for( HltParticleFlow::const_iterator ithltPF = hltpf->begin(); ithltPF != hltpf->end(); ithltPF++ )  
							{
								const reco::PFCandidate& pfc = *ithltPF;
								//std::cout << "Id = " << pfc.particleId() << std::endl;
								if ( pfc.particleId() < 4 ) 
								{ 
									isCharged = true;
									break;
								}
							}

							//neutron

							if ( !isCharged || fabs((*trueParticles)[itTruePar].charge()) < 1E-10 ) 
							{ 
								reco::PFTrajectoryPoint::LayerType ecalEntrance = reco::PFTrajectoryPoint::ECALEntrance;
								const reco::PFTrajectoryPoint& tpatecal = ((*trueParticles)[itTruePar]).extrapolatedPoint( ecalEntrance );

								eta_ = tpatecal.positionREP().Eta();

								if ( fabs(eta_) < 1E-10 ) return; 

								phi_ = tpatecal.positionREP().Phi();
								true_ = std::sqrt(tpatecal.momentum().Vect().Mag2());
								p_ = 0.;

								ecal_ = 0.;
								hcal_ = 0.;

								for( HltParticleFlow::const_iterator ithltPF = hltpf->begin(); ithltPF != hltpf->end(); ithltPF++ )  
								{
									const reco::PFCandidate& pfc = *ithltPF;

									double deta = eta_ - pfc.eta();
									double dphi = phi_ - pfc.phi();
									double dR = std::sqrt(deta*deta+dphi*dphi);

									if ( pfc.particleId() == 4 && dR < 0.04 ) ecal_ += pfc.rawEcalEnergy();
									if ( pfc.particleId() == 5 && dR < 0.2 )  hcal_ += pfc.rawHcalEnergy();

								} 

								s->Fill();

								return;
							}

							//pion(pi-)

							for( HltParticleFlow::const_iterator ithltPF = hltpf->begin(); ithltPF != hltpf->end(); ithltPF++ )  
							{

								const reco::PFCandidate& pfc = *ithltPF;
								nCh[0]++;

								if ( pfc.particleId() != 1 ) continue;
								nCh[1]++;

								if ( pfc.pt() < ptMin_ ) continue;
								nCh[2]++;

								double ecalRaw = pfc.rawEcalEnergy();
								double hcalRaw = pfc.rawHcalEnergy();
								double hoRaw = pfc.rawHoEnergy();

								if ( ecalRaw + hcalRaw < hcalMin_ ) continue;
								nCh[3]++;

								const PFCandidate::ElementsInBlocks& theElements = pfc.elementsInBlocks();

								if( theElements.empty() ) continue;

								const reco::PFBlockRef blockRef = theElements[0].first;
								PFBlock::LinkData linkData =  blockRef->linkData();
								const edm::OwnVector<reco::PFBlockElement>& elements = blockRef->elements();

								unsigned int nTracks = 0;
								unsigned iTrack = 999999;

								for(unsigned iEle=0; iEle<elements.size(); iEle++) 
								{
									PFBlockElement::Type type = elements[iEle].type();
									switch( type )
									{
										case PFBlockElement::TRACK:
											iTrack = iEle;
											nTracks++;
											break;
										default:
											continue;
									}
								}

								if ( nTracks != 1 ) continue;
								nCh[4]++;

								const reco::PFBlockElementTrack& et = dynamic_cast<const reco::PFBlockElementTrack &>( elements[iTrack] );
								double p = et.trackRef()->p();  
								double pt = et.trackRef()->pt(); 
								double eta = et.trackRef()->eta();
								// double phi = et.trackRef()->phi();

								if ( p < pMin_ || pt < ptMin_ ) continue;
								nCh[5]++;

								unsigned int tobN = 0;
								unsigned int tecN = 0;
								unsigned int tibN = 0;
								unsigned int tidN = 0;
								unsigned int pxbN = 0;
								unsigned int pxdN = 0;
								const reco::HitPattern& hp = et.trackRef()->hitPattern();
								switch ( et.trackRef()->algo() ) 
								{
									case TrackBase::hltIter0:
									case TrackBase::hltIter1:
										//case TrackBase::hltIter2:
									case TrackBase::highPtTripletStep:
										tobN += hp.numberOfValidStripTOBHits();
										tecN += hp.numberOfValidStripTECHits();
										tibN += hp.numberOfValidStripTIBHits();
										tidN += hp.numberOfValidStripTIDHits();
										pxbN += hp.numberOfValidPixelBarrelHits(); 
										pxdN += hp.numberOfValidPixelEndcapHits(); 
										break;
									case TrackBase::hltIter3:
									case TrackBase::hltIter4:
									case TrackBase::hltIterX:
									default:
										break;
								}
								int inner = pxbN+pxdN;
								int outer = tibN+tobN+tidN+tecN;

								if ( inner < nPixMin_ ) continue;
								nCh[6]++;

								bool trackerHitOK = false;
								double etaMin = 0.;
								for ( unsigned int ieta=0; ieta<nEtaMin_.size(); ++ieta ) 
								{ 
									if ( fabs(eta) < etaMin ) break;

									double etaMax = nEtaMin_[ieta];
									trackerHitOK = fabs(eta)>etaMin && fabs(eta)<etaMax && inner+outer>nHitMin_[ieta]; 

									if ( trackerHitOK ) break;

									etaMin = etaMax;
								}

								//if ( !trackerHitOK ) continue;
								//nCh[7]++;

								if ( ecalRaw > ecalMax_ ) continue;
								nCh[8]++;

								/*
									 std::cout << "Selected track : p = " << p << "; pt = " << pt 
									 << "; eta/phi = " << eta << " " << phi << std::endl
									 << "PF Ch. hadron  : p = " << pfc.p() << "; pt = " << pfc.pt()
									 << "; eta/phi = " << pfc.eta() << " " << pfc.phi() << std::endl
									 << "Nb of hits (pix/tot) " << inner << " " << inner+outer << std::endl;
									 std::cout << "Raw Ecal and HCAL energies : ECAL = " << ecalRaw 
									 << "; HCAL = " << hcalRaw << std::endl;
									 */

								reco::PFTrajectoryPoint::LayerType ecalEntrance = reco::PFTrajectoryPoint::ECALEntrance;
								const reco::PFTrajectoryPoint& tpatecal = ptc.extrapolatedPoint( ecalEntrance );
								//cout << tpatecal.isValid() << endl;
								//cout << "eta " << tpatecal.positionREP().Eta() << endl;
								//cout << "phi " << tpatecal.positionREP().Phi() << endl;
								//cout << "dr " << reco::deltaR(tpatecal.positionREP().Eta(), tpatecal.positionREP().Phi(), gen.momentum().Eta(),gen.momentum().Phi()) << endl;
                if(!tpatecal.isValid()) continue;
								eta_ = tpatecal.positionREP().Eta();
								phi_ = tpatecal.positionREP().Phi();
                //if(abs(eta_) > 1.5) continue;
                if(reco::deltaR(gen.momentum().Eta(),gen.momentum().Phi(), eta_, phi_) > 0.1) continue;
                nCh[7]++;
								true_ = std::sqrt(tpatecal.momentum().Vect().Mag2());
								pfcsID.push_back(pfc.particleId()); 
								Eecal_.push_back(ecalRaw);
								Ehcal_.push_back(hcalRaw);
								dr_.push_back(reco::deltaR(gen.momentum().Eta(),gen.momentum().Phi(), eta_, phi_));
								p_ = p;
								ecal_ = ecalRaw;
								hcal_ = hcalRaw;
								ho_ = hoRaw;
								charge_ = pfc.charge();
								s->Fill();
							}
						}
					}
				}
			}
		}
	}
		/*
			 int num=0;
			 for( HltParticleFlow::const_iterator ithltPF = hltpf->begin(); ithltPF != hltpf->end(); ithltPF++ )  num++;
			 cout <<  num << endl;
			 if ( (*trueParticles).size() != 2 ) {
//cout<<"simparticlesize : " << (*trueParticles).size() <<endl;
return;
}
nEv[1]++;
*/    


//std::cout << "isCharged ? " << isCharged << std::endl;

/* 
	 for (HltParticleFlow::const_iterator ithltPF = hltpf->begin() ; ithltPF != hltpf->end(); ithltPF++)
	 {
	 std::cout << ithltPF->rawEcalEnergy() << "   " << ithltPF->rawHcalEnergy() << "   " << ithltPF->particleId() <<  std::endl;
	 }
	 */

}


// ------------ method called once each job just before starting event loop  ------------
	void 
PFHadHLT::beginJob()
{
	Book_trees();
}

// ------------ method called once each job just after ending the event loop  ------------
	void 
PFHadHLT::endJob() 
{
}

// ------------ method called when starting to processes a run  ------------
/*
	 void 
	 PFHadHLT::beginRun(edm::Run const&, edm::EventSetup const&)
	 {
	 }
	 */

// ------------ method called when ending the processing of a run  ------------
/*
	 void 
	 PFHadHLT::endRun(edm::Run const&, edm::EventSetup const&)
	 {
	 }
	 */

// ------------ method called when starting to processes a luminosity block  ------------
/*
	 void 
	 PFHadHLT::beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
	 {
	 }
	 */

// ------------ method called when ending the processing of a luminosity block  ------------
/*
	 void 
	 PFHadHLT::endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
	 {
	 }
	 */

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
PFHadHLT::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
	//The following says we do not know what parameters are allowed so do no validation
	// Please change this to state exactly what you do use, even if it is no parameters
	edm::ParameterSetDescription desc;
	desc.setUnknown();
	descriptions.addDefault(desc);
}

/// Booking trees
void PFHadHLT::Book_trees()
{

	//s->Branch("genpt"	,&gen_pt_,   "gen_pt/F");  
	//s->Branch("genE"	,&gen_E_,   "gen_E/F");  
	//s->Branch("geneta" ,&gen_eta_, "gen_eta/F");  
	//s->Branch("genphi" ,&gen_phi_, "gen_phi/F");
	s->Branch("true",&true_,"true/F");  
	s->Branch("p"   ,&p_,   "p/F");  
	s->Branch("ecal",&ecal_,"ecal/F");  
	s->Branch("hcal",&hcal_,"hcal/F");  
	s->Branch("eta" ,&eta_, "eta/F");  
	s->Branch("phi" ,&phi_, "phi/F");
	s->Branch("pfcs",&pfcsID);  
	s->Branch("Eecal",&Eecal_);
	s->Branch("Ehcal",&Ehcal_);
	s->Branch("dr",&dr_);
	s->Branch("ho",&ho_,"ho/F");  
	s->Branch("charge",&charge_,"charge/I");  

}

/// Reset variables
void PFHadHLT::Reset_variables()
{
	gen_pt_    = -999999;
	gen_E_    = -999999;
	gen_eta_  = -999999;
	gen_phi_  = -999999;
	true_ = -999999;
	p_    = -999999;
	ecal_ = -999999;
	hcal_ = -999999;
	eta_  = -999999;
	phi_  = -999999;
	//pfcID_  = -999999;
	ho_ = -999999;
	charge_ = -999999;
}

//define this as a plug-in
DEFINE_FWK_MODULE(PFHadHLT);
/*	
		int flag=-1;//, antiflag=-1;
		flag = ((*trueParticles)[0].charge()<0) ? 0 : 1;
//antiflag = ((*trueParticles)[0].charge()<0) ? 1 : 0;
//cout << (*trueParticles)[0].charge() << endl;
//cout << (*trueParticles)[1].charge() << endl;
const reco::PFTrajectoryPoint& gen1 = (*trueParticles)[flag].trajectoryPoint(reco::PFTrajectoryPoint::ClosestApproach); //pi-
//const reco::PFTrajectoryPoint& gen2 = (*trueParticles)[antiflag].trajectoryPoint(reco::PFTrajectoryPoint::ClosestApproach); //pi+
TLorentzVector pion_1(gen1.momentum().Pt(),gen1.momentum().Eta(),gen1.momentum().Phi(),gen1.momentum().E());
//TLorentzVector pion_2(gen2.momentum().Pt(),gen2.momentum().Eta(),gen2.momentum().Phi(),gen2.momentum().E());
double temp_pt=0, temp_eta=0, temp_phi=0, temp_energy=0;

//GenParticleCollection::const_iterator itGenParBegin = genParticles->begin();
for ( GenParticleCollection::const_iterator itGenPar = genParticles->begin(); itGenPar != genParticles->end(); itGenPar++ ){
if(itGenPar->status() == 1){
if(itGenPar->pdgId() == -211){ temp_pt=itGenPar->pt(); temp_eta=itGenPar->eta(); temp_phi=itGenPar->phi(); temp_energy = itGenPar->energy();}
}
}

TLorentzVector gen_pion(temp_pt, temp_eta, temp_phi, temp_energy);
//cout << "gen pion info : " << gen_pion.pt() << ", " << gen_pion.eta() << ", " << gen_pion.phi() << endl;
//cout << "pion charge : " << (*trueParticles)[0].charge() << ", pt : " << pion_1.pt() << ", eta : " << pion_1.eta()<< ", phi : " << pion_1.phi() << endl;
//cout << "pion charge : " << (*trueParticles)[1].charge() << ", pt : " << pion_2.pt() << ", eta : " << pion_2.eta()<< ", phi : " << pion_2.phi() << endl;
//cout << "delta R of two pions : " << reco::deltaR(pion_1.eta(),pion_1.phi(),pion_2.eta(),pion_2.phi()) << endl;

gen_E_ = temp_energy;
gen_pt_ = temp_pt;
gen_eta_ = temp_eta;
gen_phi_ = temp_phi;
//s->Fill();

if(reco::deltaR(pion_1.eta(),pion_1.phi(),gen_pion.eta(),gen_pion.phi()) > 0.2) return;
*/

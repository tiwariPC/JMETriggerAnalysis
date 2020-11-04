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
	nEv = std::vector<unsigned int>(3,static_cast<unsigned int>(0));

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
	std::cout << "Number of isolated pions " << nEv[1] << std::endl;
	std::cout << "Number of true particles within dR = 0.01 of an isolated pion " << nEv[2] << std::endl;
	std::cout << "Number of true particles with track matching " << nCh[7] << std::endl;

	std::cout << "Number of PF candidates ............. " << nCh[0] << std::endl;
	std::cout << "Number of PF Charged Hadrons......... " << nCh[1] << std::endl;
	std::cout << " - With pt > " << ptMin_ << " GeV/c ................ " << nCh[2] << std::endl;
	std::cout << " - With E_HCAL > " << hcalMin_ << " GeV .............. " << nCh[3] << std::endl;
	std::cout << " - With only 1 track in the block ... " << nCh[4] << std::endl;
	std::cout << " - With p > " << pMin_ << " GeV/c ................. " << nCh[5] << std::endl;
	std::cout << " - With at least " << nPixMin_ << " pixel hits ....... " << nCh[6] << std::endl;
	std::cout << " - With E_ECAL < " << ecalMax_ << " GeV ............ " << nCh[8] << std::endl;

	tf1->cd();
	s->Write();
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

	nEv[0]++;
	std::vector<int> genPart;
	genPart.clear();
	if ( isSimu ) { 
		for( GenParticleCollection::const_iterator itGenPar = genParticles->begin(); itGenPar != genParticles->end(); itGenPar++ ){
			float dR_ = -1;
			float mindR_ = 99;

			// Gen and true particle selection
			if(itGenPar->status() == 1 && itGenPar->pdgId() == -211){
				for ( GenParticleCollection::const_iterator jtGenPar = genParticles->begin(); jtGenPar != genParticles->end(); jtGenPar++ ){
					if(itGenPar != jtGenPar && itGenPar->status() == 1){
						dR_ = reco::deltaR(itGenPar->eta(), itGenPar->phi(), jtGenPar->eta(), jtGenPar->phi());
						if(dR_ < mindR_) mindR_ = dR_;
					}
				}

				if(mindR_ > 1.){  // Pion isolation
					nEv[1]++;
					//Etrue_.clear(); pfc_ecal.clear(); pfc_hcal.clear(); pfc_dr.clear();

					for(int itTruePar=0;itTruePar<(int)(*trueParticles).size();itTruePar++) {
                                        	// Only consider negatively charged particles
			                	const reco::PFSimParticle& ptc = (*trueParticles)[itTruePar];
						if(ptc.charge()>0) continue;

                                        	// There should be true particle within deltaR = 0.01 of the gen particle
						const reco::PFTrajectoryPoint& gen = ptc.trajectoryPoint(reco::PFTrajectoryPoint::ClosestApproach);
						dR_ = reco::deltaR(itGenPar->eta(), itGenPar->phi(), gen.momentum().Eta(),gen.momentum().Phi());
						if(dR_ > 0.01) continue;
						nEv[2]++;

						// Check if there is a reconstructed track *in the event*
						isCharged = false;
						for( HltParticleFlow::const_iterator ithltPF = hltpf->begin(); ithltPF != hltpf->end(); ithltPF++ ){
							const reco::PFCandidate& pfc = *ithltPF;
							//std::cout << "Id = " << pfc.particleId() << std::endl;
							if ( pfc.particleId() < 4 ) { 
								isCharged = true;
								break;
							}
						}
						reco::PFTrajectoryPoint::LayerType ecalEntrance = reco::PFTrajectoryPoint::ECALEntrance;
						const reco::PFTrajectoryPoint& tpatecal = ptc.extrapolatedPoint( ecalEntrance );
						if(!tpatecal.isValid()) continue;
						eta_ = tpatecal.positionREP().Eta();
						phi_ = tpatecal.positionREP().Phi();
						true_ = std::sqrt(tpatecal.momentum().Vect().Mag2());

						// The extrapolated track should be within 0.1 of the true particle
						if(reco::deltaR(gen.momentum().Eta(),gen.momentum().Phi(), eta_, phi_) > 0.1) continue;
						nCh[7]++;

						true_energy.push_back(true_);
						true_eta.push_back(eta_);
						true_phi.push_back(phi_);
						true_dr.push_back(reco::deltaR(gen.momentum().Eta(),gen.momentum().Phi(), eta_, phi_));
						true_isCharged.push_back(isCharged);
					} // end of true particle loop
				} // isolation > 1
			} // stable gen particle pdgid = -211
		}  // end of all gen particles loop


		// Reco pion(pi-) selection
		for( HltParticleFlow::const_iterator ithltPF = hltpf->begin(); ithltPF != hltpf->end(); ithltPF++ ) {
			const reco::PFCandidate& pfc = *ithltPF;
			nCh[0]++;

			if ( pfc.particleId() != 1 ) continue;
			nCh[1]++;

			if ( pfc.pt() < ptMin_ ) continue;
			nCh[2]++;

			double ecalRaw = pfc.rawEcalEnergy();
			double hcalRaw = pfc.rawHcalEnergy();
			if ( ecalRaw + hcalRaw < hcalMin_ ) continue;
			nCh[3]++;

			const PFCandidate::ElementsInBlocks& theElements = pfc.elementsInBlocks();

			if( theElements.empty() ) continue;

			const reco::PFBlockRef blockRef = theElements[0].first;
			PFBlock::LinkData linkData =  blockRef->linkData();
			const edm::OwnVector<reco::PFBlockElement>& elements = blockRef->elements();

			unsigned int nTracks = 0;
			unsigned iTrack = 999999;

			for(unsigned iEle=0; iEle<elements.size(); iEle++) {
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

			if ( p < pMin_ || pt < ptMin_ ) continue;
			nCh[5]++;

			unsigned int tobN = 0;
			unsigned int tecN = 0;
			unsigned int tibN = 0;
			unsigned int tidN = 0;
			unsigned int pxbN = 0;
			unsigned int pxdN = 0;
			const reco::HitPattern& hp = et.trackRef()->hitPattern();
			switch ( et.trackRef()->algo() ) {
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
			for ( unsigned int ieta=0; ieta<nEtaMin_.size(); ++ieta ) { 
				if ( fabs(eta) < etaMin ) break;

				double etaMax = nEtaMin_[ieta];
				trackerHitOK = fabs(eta)>etaMin && fabs(eta)<etaMax && inner+outer>nHitMin_[ieta]; 

				if ( trackerHitOK ) break;

				etaMin = etaMax;
			}

			if ( ecalRaw > ecalMax_ ) continue;
			nCh[8]++;

			pfc_ecal.push_back(ecalRaw);
			pfc_hcal.push_back(hcalRaw);
			pfc_eta.push_back(pfc.eta());
			pfc_phi.push_back(pfc.phi());
			pfc_charge.push_back(pfc.charge());
			pfc_id.push_back(pfc.particleId());
			trackRef_p.push_back(p);
		}  // end of pion (pi-) loop

		s->Fill();
	} // isSimu

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
	s->Branch("true_energy",&true_energy);
	s->Branch("true_eta",&true_eta);
	s->Branch("true_phi",&true_phi);
	s->Branch("true_dr",&true_dr);
	s->Branch("true_isCharged",&true_isCharged);
	s->Branch("pfc_ecal",&pfc_ecal);
	s->Branch("pfc_hcal",&pfc_hcal);
	s->Branch("pfc_eta",&pfc_eta);
	s->Branch("pfc_phi",&pfc_phi);
	s->Branch("pfc_charge",&pfc_charge);
	s->Branch("pfc_id",&pfc_id);
	s->Branch("trackRef_p",&trackRef_p);
}

/// Reset variables
void PFHadHLT::Reset_variables()
{
	true_energy.clear();
	true_eta.clear();
	true_phi.clear();
	true_dr.clear();
	true_isCharged.clear();
	pfc_ecal.clear();
	pfc_hcal.clear();
	pfc_eta.clear();
	pfc_phi.clear();
	pfc_charge.clear();
	pfc_id.clear();
	trackRef_p.clear();	
}

//define this as a plug-in
DEFINE_FWK_MODULE(PFHadHLT);

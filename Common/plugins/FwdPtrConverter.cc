#include <JMETriggerAnalysis/NTuplizers/plugins/FwdPtrConverter.h>
#include <FWCore/Framework/interface/MakerMacros.h>

#include <DataFormats/ParticleFlowCandidate/interface/PFCandidate.h>

typedef FwdPtrConverter<reco::PFCandidate> FwdPtrRecoPFCandidateConverter;
DEFINE_FWK_MODULE(FwdPtrRecoPFCandidateConverter);

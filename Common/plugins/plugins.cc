#include "JMETriggerAnalysis/Common/plugins/PFCandidateHistogrammer.h"

#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"

typedef PFCandidateHistogrammer<reco::PFCandidate> RecoPFCandidateHistogrammer;
typedef PFCandidateHistogrammer<pat::PackedCandidate> PATPackedCandidateHistogrammer;

DEFINE_FWK_MODULE(RecoPFCandidateHistogrammer);
DEFINE_FWK_MODULE(PATPackedCandidateHistogrammer);

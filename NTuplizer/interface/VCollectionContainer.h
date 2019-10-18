#ifndef JMETriggerAnalysis_VCollectionContainer_h
#define JMETriggerAnalysis_VCollectionContainer_h

#include <FWCore/Utilities/interface/EDGetToken.h>
#include <string>

template <class T>
class VCollectionContainer {

 public:
  explicit VCollectionContainer(const std::string&, const std::string&, const edm::EDGetToken&);
  virtual ~VCollectionContainer() {}

  virtual void fill(const T&) = 0;

  void setName(const std::string& str) { name_ = str; }

  const std::string& name() const { return name_; }
  const std::string& inputTagLabel() const { return inputTagLabel_; }
  const edm::EDGetToken& token() const { return token_; }

 protected:
  std::string name_;
  const std::string inputTagLabel_;
  const edm::EDGetToken token_;
};

template<class T>
VCollectionContainer<T>::VCollectionContainer(const std::string& name, const std::string& inputTagLabel, const edm::EDGetToken& token)
 : name_(name), inputTagLabel_(inputTagLabel), token_(token) {

//  edm::LogWarning("CaloMETCollectionContainer") << label_ << " " << inputTag_.label();
}

#endif

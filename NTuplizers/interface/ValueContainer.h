#ifndef JMETriggerAnalysis_NTuplizers_ValueContainer_h
#define JMETriggerAnalysis_NTuplizers_ValueContainer_h

#include <string>
#include <FWCore/Utilities/interface/EDGetToken.h>

template <class T>
class ValueContainer {

 public:
  explicit ValueContainer(const std::string& name, const std::string& inputTagLabel, const edm::EDGetTokenT<T>& token) : name_(name), inputTagLabel_(inputTagLabel), token_(token) {}
  virtual ~ValueContainer() {}

  void setValue(const T foo){ value_ = foo; }
  T& value() { return value_; }

  const std::string& name() const { return name_; }
  const std::string& inputTagLabel() const { return inputTagLabel_; }
  const edm::EDGetTokenT<T>& token() const { return token_; }

 protected:
  const std::string name_;
  const std::string inputTagLabel_;
  const edm::EDGetTokenT<T> token_;

  T value_;
};

#endif

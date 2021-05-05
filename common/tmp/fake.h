#include <TFile.h>
#include <TH1F.h>

#include "HTTutilities/Jet2TauFakes/interface/FakeFactor.h"

double getDYWeight(double genMass);
void shutdown();

class HistProvider {
 public:
  static HistProvider& instance() {
    static HistProvider instance;
    return instance;
  }

  const TH1F& hist() const {
    return *h_QCD;
  }

  FakeFactor& ffout() const {
    return *ff;
  }

  // private:
  HistProvider();
  ~HistProvider();
  
  TFile* f_in; 
  TFile* ff_in; 
  TH1F* h_QCD;
  //  TH1F* h_W;
  //  TH1F* h_tt;
  FakeFactor* ff;
};


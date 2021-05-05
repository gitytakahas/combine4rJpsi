#include "fake.h"
#include <TROOT.h>
#include <TTree.h>
#include <iostream>
#include <cstdlib>
#include <string>


HistProvider::HistProvider() {

  std::cout << "Reading files ..." << std::endl;
  
  std::string fname = "/t3home/ytakahas/work/analysis/CMSSW_9_4_9/src/datacard/2017/tautau/signal_twotaus_os_tau1_tight/m_vis_ff.root";
  f_in = new TFile(fname.c_str());
  h_QCD = dynamic_cast<TH1F*>(f_in->Get("QCD"));


  std::string ffname_2017_tt = "/t3home/ytakahas/work/analysis/CMSSW_9_4_9/src/HTTutilities/Jet2TauFakes/data/SM2017/tight/vloose/tt/fakeFactors.root";
  ff_in = new TFile(ffname_2017_tt.c_str());
  ff = (FakeFactor*)ff_in->Get("ff_comb");

  

  //  h_W = dynamic_cast<TH1F*>(f_in->Get("QCD"));
  //  h_tt = dynamic_cast<TH1F*>(f_in->Get("QCD"));

  //  if (!h_frac)
  //    std::cerr << "ERROR: Not getting histogram out of file in DYReweighting" << std::endl;

}

HistProvider::~HistProvider() {
}

void shutdown(){
  std::cout << "test" << std::endl;
  delete HistProvider::instance().f_in;
  delete HistProvider::instance().ff_in;
  delete HistProvider::instance().ff;
}

double getDYWeight(double genMass) {

  const TH1F& h_frac = HistProvider::instance().hist();
  FakeFactor& ffout = HistProvider::instance().ffout();
  //  double weight = h_frac.GetBinContent(h_frac.GetXaxis()->FindBin(genMass));


  std::vector<double> inputs(8);

//  inputs[0] = (double)pt_1;
//  inputs[1] = (double)pt_2;
//  inputs[2] = (double)dm;
//  inputs[3] = (double)njets;
//  inputs[4] = (double)mvis;

  inputs[0] = (double)1.;
  inputs[1] = (double)1.;
  inputs[2] = (double)1.;
  inputs[3] = (double)1.;
  inputs[4] = (double)1.;
  inputs[5] = 1.;
  inputs[6] = 0.;
  inputs[7] = 0.;

  Double_t weight = ffout.value(inputs);

  return weight;
}

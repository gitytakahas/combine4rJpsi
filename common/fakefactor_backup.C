#include "TMath.h"
#include "TFile.h"
#include "TH1F.h"
#include <iostream>
#include "TROOT.h"

#include "HTTutilities/Jet2TauFakes/interface/FakeFactor.h"


TString ffname_2017_tt = "/t3home/ytakahas/work/analysis/CMSSW_9_4_9/src/HTTutilities/Jet2TauFakes/data/SM2017/tight/vloose/tt/fakeFactors.root";
TFile *fffile_2017_tt = new TFile(ffname_2017_tt);
FakeFactor* ff_2017_tt = (FakeFactor*)fffile_2017_tt->Get("ff_comb");


TString ffname_2017_mt = "/t3home/ytakahas/work/analysis/CMSSW_9_4_9/src/HTTutilities/Jet2TauFakes/data/SM2017/tight/vloose/mt/fakeFactors.root";
TFile *fffile_2017_mt = new TFile(ffname_2017_mt);
FakeFactor* ff_2017_mt = (FakeFactor*)fffile_2017_mt->Get("ff_comb");



/// THIS SHOULD BE CHANGED !!!

TString ffname_2018_tt = "/t3home/ytakahas/work/analysis/CMSSW_9_4_9/src/HTTutilities/Jet2TauFakes/data/SM2017/tight/vloose/tt/fakeFactors.root";
TFile *fffile_2018_tt = new TFile(ffname_2018_tt);
FakeFactor* ff_2018_tt = (FakeFactor*)fffile_2018_tt->Get("ff_comb");

TString ffname_2018_mt = "/t3home/ytakahas/work/analysis/CMSSW_9_4_9/src/HTTutilities/Jet2TauFakes/data/SM2017/tight/vloose/mt/fakeFactors.root";
TFile *fffile_2018_mt = new TFile(ffname_2018_mt);
FakeFactor* ff_2018_mt = (FakeFactor*)fffile_2018_mt->Get("ff_comb");


///////////////////////////////


TString fracname_2017_tau1 = "/t3home/ytakahas/work/analysis/CMSSW_9_4_9/src/datacard/2017/tautau/signal_twotaus_os_tau1_tight/m_vis_template.root";
TFile *fracfile_2017_tau1 = new TFile(fracname_2017_tau1);
TH1F* h_2017_QCD_tau1 = (TH1F*) fracfile_2017_tau1->Get("QCD");
TH1F* h_2017_W_tau1 = (TH1F*) fracfile_2017_tau1->Get("W");
TH1F* h_2017_tt_tau1 = (TH1F*) fracfile_2017_tau1->Get("tt");

TString fracname_2017_tau2 = "/t3home/ytakahas/work/analysis/CMSSW_9_4_9/src/datacard/2017/tautau/signal_twotaus_os_tau2_tight/m_vis_template.root";
TFile *fracfile_2017_tau2 = new TFile(fracname_2017_tau2);
TH1F* h_2017_QCD_tau2 = (TH1F*) fracfile_2017_tau2->Get("QCD");
TH1F* h_2017_W_tau2 = (TH1F*) fracfile_2017_tau2->Get("W");
TH1F* h_2017_tt_tau2 = (TH1F*) fracfile_2017_tau2->Get("tt");


/// THIS SHOULD BE CHANGED !!!

TString fracname_2018_tau1 = "/t3home/ytakahas/work/analysis/CMSSW_9_4_9/src/datacard/2017/tautau/signal_twotaus_os_tau1_tight/m_vis_template.root";
TFile *fracfile_2018_tau1 = new TFile(fracname_2018_tau1);
TH1F* h_2018_QCD_tau1 = (TH1F*) fracfile_2018_tau1->Get("QCD");
TH1F* h_2018_W_tau1 = (TH1F*) fracfile_2018_tau1->Get("W");
TH1F* h_2018_tt_tau1 = (TH1F*) fracfile_2018_tau1->Get("tt");

TString fracname_2018_tau2 = "/t3home/ytakahas/work/analysis/CMSSW_9_4_9/src/datacard/2017/tautau/signal_twotaus_os_tau2_tight/m_vis_template.root";
TFile *fracfile_2018_tau2 = new TFile(fracname_2018_tau2);
TH1F* h_2018_QCD_tau2 = (TH1F*) fracfile_2018_tau2->Get("QCD");
TH1F* h_2018_W_tau2 = (TH1F*) fracfile_2018_tau2->Get("W");
TH1F* h_2018_tt_tau2 = (TH1F*) fracfile_2018_tau2->Get("tt");

///////////////////////////////



TString fracname_2017_tau = "/t3home/ytakahas/work/analysis/CMSSW_9_4_9/src/datacard/2017/mutau/signal_twotaus_os_tau1_tight/m_vis_template.root";
TFile *fracfile_2017_tau = new TFile(fracname_2017_tau);
TH1F* h_2017_QCD_tau = (TH1F*) fracfile_2017_tau->Get("QCD");
TH1F* h_2017_W_tau = (TH1F*) fracfile_2017_tau->Get("W");
TH1F* h_2017_tt_tau = (TH1F*) fracfile_2017_tau->Get("tt");


/// THIS SHOULD BE CHANGED !!!
TString fracname_2018_tau = "/t3home/ytakahas/work/analysis/CMSSW_9_4_9/src/datacard/2017/mutau/signal_twotaus_os_tau1_tight/m_vis_template.root";
TFile *fracfile_2018_tau = new TFile(fracname_2018_tau);
TH1F* h_2018_QCD_tau = (TH1F*) fracfile_2018_tau->Get("QCD");
TH1F* h_2018_W_tau = (TH1F*) fracfile_2018_tau->Get("W");
TH1F* h_2018_tt_tau = (TH1F*) fracfile_2018_tau->Get("tt");
///////////////////////////////



Double_t getFF(Double_t pt_1, Double_t pt_2, Int_t dm, Int_t njets, Double_t mvis, int year, int channel, int sysid){

  if(channel==0){
    std::cout << "ERROR: channel = 0 is not possible !"  << std::endl;
  }

  std::vector<double> inputs(8);

  inputs[0] = (double)pt_1;
  inputs[1] = (double)pt_2;
  inputs[2] = (double)dm;
  inputs[3] = (double)njets;
  inputs[4] = (double)mvis;

  double frac_qcd = -1;
  double frac_w = -1;
  double frac_tt = -1;


  if(channel==1){ // tauh-tauh with tau1

    if(year==2017){

      frac_qcd = h_2017_QCD_tau1->GetBinContent(h_2017_QCD_tau1->FindBin(mvis));
      frac_w = h_2017_W_tau1->GetBinContent(h_2017_W_tau1->FindBin(mvis));
      frac_tt = h_2017_tt_tau1->GetBinContent(h_2017_tt_tau1->FindBin(mvis));

    }else if(year==2018){

      frac_qcd = h_2018_QCD_tau1->GetBinContent(h_2018_QCD_tau1->FindBin(mvis));
      frac_w = h_2018_W_tau1->GetBinContent(h_2018_W_tau1->FindBin(mvis));
      frac_tt = h_2018_tt_tau1->GetBinContent(h_2018_tt_tau1->FindBin(mvis));

    }


  }else if(channel==2){ // tauh-tauh with tau2

    if(year==2017){

      frac_qcd = h_2017_QCD_tau2->GetBinContent(h_2017_QCD_tau2->FindBin(mvis));
      frac_w = h_2017_W_tau2->GetBinContent(h_2017_W_tau2->FindBin(mvis));
      frac_tt = h_2017_tt_tau2->GetBinContent(h_2017_tt_tau2->FindBin(mvis));

    }else if(year==2018){

      frac_qcd = h_2018_QCD_tau2->GetBinContent(h_2018_QCD_tau2->FindBin(mvis));
      frac_w = h_2018_W_tau2->GetBinContent(h_2018_W_tau2->FindBin(mvis));
      frac_tt = h_2018_tt_tau2->GetBinContent(h_2018_tt_tau2->FindBin(mvis));

    }

  }

  if(frac_qcd==-1 || frac_w == -1 || frac_tt == -1){
    std::cout << "ERRPR: the FF fraction is below 1" << std::endl;
  }


  inputs[5] = frac_qcd;
  inputs[6] = frac_w;
  inputs[7] = frac_tt;




  Double_t ffweight = -1;

  if(year==2017){
    
    ffweight = ff_2017_tt->value(inputs);
    
  }else if(year==2018){
    
    ffweight = ff_2018_tt->value(inputs);
    
  }



  if(ffweight==-1){
    std::cout << "ERRPR: the FF fraction is -1" << std::endl;    
  }


  //  std::cout << "check: (QCD, W, tt) = " << frac_qcd << " " << frac_w << " " << frac_tt << " -> " << ffweight  << " (" << year << " " << channel << " " << sysid  << std::endl;


  return ffweight;

}











Double_t getFFL(Double_t pt, Int_t dm, Int_t njets, Double_t mvis, Double_t pfmt, Double_t iso, int year, int channel, int sysid){

  if(channel==1 || channel == 2){
    std::cout << "ERROR: channel = 1 or 2 is not possible !"  << std::endl;
  }


  std::vector<double> inputs(9);

  inputs[0] = (double)pt;
  inputs[1] = (double)dm;
  inputs[2] = (double)njets;
  inputs[3] = (double)mvis;
  inputs[4] = (double)pfmt;
  inputs[5] = (double)iso;

  double frac_qcd = -1;
  double frac_w = -1;
  double frac_tt = -1;


  if(year==2017){
    frac_qcd = h_2017_QCD_tau->GetBinContent(h_2017_QCD_tau->FindBin(mvis));
    frac_w = h_2017_W_tau->GetBinContent(h_2017_W_tau->FindBin(mvis));
    frac_tt = h_2017_tt_tau->GetBinContent(h_2017_tt_tau->FindBin(mvis));
  }else if(year==2018){
    frac_qcd = h_2018_QCD_tau->GetBinContent(h_2018_QCD_tau->FindBin(mvis));
    frac_w = h_2018_W_tau->GetBinContent(h_2018_W_tau->FindBin(mvis));
    frac_tt = h_2018_tt_tau->GetBinContent(h_2018_tt_tau->FindBin(mvis));
  }


  if(frac_qcd==-1 || frac_w == -1 || frac_tt == -1){
    std::cout << "ERRPR: the FF fraction is below 1" << std::endl;
  }


  inputs[6] = frac_qcd;
  inputs[7] = frac_w;
  inputs[8] = frac_tt;


  Double_t ffweight = -1;

  if(year==2017){
    
    ffweight = ff_2017_mt->value(inputs);
    
  }else if(year==2018){
    
    ffweight = ff_2018_mt->value(inputs);
    
  }


  if(ffweight==-1){
    std::cout << "ERRPR: the FF fraction is -1" << std::endl;    
  }


  //  std::cout << "check: (QCD, W, tt) = " << frac_qcd << " " << frac_w << " " << frac_tt << " -> " << ffweight  << " (" << year << " " << channel << " " << sysid  << std::endl;


  return ffweight;

}


void shutdown(){
  delete ff_2017_tt;
  delete ff_2017_mt;
  delete ff_2018_tt;
  delete ff_2018_mt;
  
  //  std::cout << test << " release memories" << std::endl;
}


void fakefactor(){
  std::cout << std::endl;
  std::cout << "Initialize fakefactor.C ... " << std::endl;
  std::cout << std::endl;
  
  //  ReadFile();

  //  ff_file->Close();

}


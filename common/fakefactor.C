#include "TMath.h"
#include "TFile.h"
#include "TH1F.h"
#include <iostream>
#include "TROOT.h"

#include "HTTutilities/Jet2TauFakes/interface/FakeFactor.h"

// Need to be defined in global
TFile *ff_file;
FakeFactor* ff;

TFile *fracfile_tau;
TH1F* h_QCD_tau1;
TH1F* h_W_tau1;
TH1F* h_tt_tau1;

//TFile *fracfile_tau2;
TH1F* h_QCD_tau2;
TH1F* h_W_tau2;
TH1F* h_tt_tau2;



void ReadFile(string channel, string category, string year){

  string prefix = "mt";
  if(channel == "tt") prefix = "tt";
  if(channel == "eletau") prefix = "et";

  TString ffname = "/t3home/ytakahas/work/analysis/CMSSW_9_4_9/src/HTTutilities/Jet2TauFakes/data/SM" + year + "/tight/vloose/" + prefix + "/fakeFactors.root";
  std::cout << "Reading FF file = " << ffname << std::endl;

  ff_file = new TFile(ffname);
  ff = (FakeFactor*)ff_file->Get("ff_comb");
  
  TString fracname_tau1 = "/work/ineuteli/analysis/LQ_legacy/plots/fakefactor/" + year + "/fakeFactor_fractions_m_vis_" + prefix + "_" + year + ".root";

  std::cout << "Reading FF file = " << fracname_tau1 << std::endl;

  TString qcdname = category + "/QCD";
  TString ewjname = category + "/EWJ";
  TString ttjname = category + "/TTJ";

  if(channel == "tt"){
    qcdname += "_1";
    ewjname += "_1";
    ttjname += "_1";
  }

  fracfile_tau = new TFile(fracname_tau1);
  h_QCD_tau1 = (TH1F*) fracfile_tau->Get(qcdname);
  h_W_tau1 = (TH1F*) fracfile_tau->Get(ewjname);
  h_tt_tau1 = (TH1F*) fracfile_tau->Get(ttjname);
  
  if(channel == "tt"){

    //    TString fracname_tau2 = "/work/ineuteli/analysis/LQ_legacy/plots/fakefactor/" + year + "/fakeFactor_fractions_m_vis_" + channel + "_" + year + ".root";
    //    std::cout << "Reading FF file = " << fracname_tau2 << std::endl;
    
    //    fracfile_tau2 = new TFile(fracname_tau2);

    TString qcdname2 = category + "/QCD_2";
    TString ewjname2 = category + "/EWJ_2";
    TString ttjname2 = category + "/TTJ_2";

    h_QCD_tau2 = (TH1F*) fracfile_tau->Get(qcdname2);
    h_W_tau2 = (TH1F*) fracfile_tau->Get(ewjname2);
    h_tt_tau2 = (TH1F*) fracfile_tau->Get(ttjname2);

    
  }

  std::cout << "Reading file ends ..." << std::endl;

}




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

//    if(year==2017){
//
//      frac_qcd = h_2017_QCD_tau1->GetBinContent(h_2017_QCD_tau1->FindBin(mvis));
//      frac_w = h_2017_W_tau1->GetBinContent(h_2017_W_tau1->FindBin(mvis));
//      frac_tt = h_2017_tt_tau1->GetBinContent(h_2017_tt_tau1->FindBin(mvis));
//
//    }else if(year==2018){
//
//      frac_qcd = h_2018_QCD_tau1->GetBinContent(h_2018_QCD_tau1->FindBin(mvis));
//      frac_w = h_2018_W_tau1->GetBinContent(h_2018_W_tau1->FindBin(mvis));
//      frac_tt = h_2018_tt_tau1->GetBinContent(h_2018_tt_tau1->FindBin(mvis));
//
//    }


    frac_qcd = h_QCD_tau1->GetBinContent(h_QCD_tau1->FindBin(mvis));
    frac_w = h_W_tau1->GetBinContent(h_W_tau1->FindBin(mvis));
    frac_tt = h_tt_tau1->GetBinContent(h_tt_tau1->FindBin(mvis));



  }else if(channel==2){ // tauh-tauh with tau2

//    if(year==2017){
//
//      frac_qcd = h_2017_QCD_tau2->GetBinContent(h_2017_QCD_tau2->FindBin(mvis));
//      frac_w = h_2017_W_tau2->GetBinContent(h_2017_W_tau2->FindBin(mvis));
//      frac_tt = h_2017_tt_tau2->GetBinContent(h_2017_tt_tau2->FindBin(mvis));
//
//    }else if(year==2018){
//
//      frac_qcd = h_2018_QCD_tau2->GetBinContent(h_2018_QCD_tau2->FindBin(mvis));
//      frac_w = h_2018_W_tau2->GetBinContent(h_2018_W_tau2->FindBin(mvis));
//      frac_tt = h_2018_tt_tau2->GetBinContent(h_2018_tt_tau2->FindBin(mvis));
//
//    }

    frac_qcd = h_QCD_tau2->GetBinContent(h_QCD_tau2->FindBin(mvis));
    frac_w = h_W_tau2->GetBinContent(h_W_tau2->FindBin(mvis));
    frac_tt = h_tt_tau2->GetBinContent(h_tt_tau2->FindBin(mvis));


  }

  if(frac_qcd==-1 || frac_w == -1 || frac_tt == -1){
    std::cout << "ERRPR: the FF fraction is below 1" << std::endl;
  }


  inputs[5] = frac_qcd;
  inputs[6] = frac_w;
  inputs[7] = frac_tt;




  Double_t ffweight = -1;

  //  if(year==2017){
    
  ffweight = ff->value(inputs);
    
//  }else if(year==2018){
//    
//    ffweight = ff_2018_tt->value(inputs);
//    
//  }



  if(ffweight==-1){
    std::cout << "ERRPR: the FF fraction is -1" << std::endl;    
  }


  //  std::cout << "check: (QCD, W, tt) = " << frac_qcd << " " << frac_w << " " << frac_tt << " -> " << ffweight  << " (" << year << " " << channel << " " << sysid  << std::endl;


  return ffweight;

}











Double_t getFFL(Double_t pt, Int_t dm, Int_t njets, Double_t mvis, Double_t pfmt, Double_t iso, int year, int sysid){


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


//  if(year==2017){
//    frac_qcd = h_2017_QCD_tau->GetBinContent(h_2017_QCD_tau->FindBin(mvis));
//    frac_w = h_2017_W_tau->GetBinContent(h_2017_W_tau->FindBin(mvis));
//    frac_tt = h_2017_tt_tau->GetBinContent(h_2017_tt_tau->FindBin(mvis));
//  }else if(year==2018){
//    frac_qcd = h_2018_QCD_tau->GetBinContent(h_2018_QCD_tau->FindBin(mvis));
//    frac_w = h_2018_W_tau->GetBinContent(h_2018_W_tau->FindBin(mvis));
//    frac_tt = h_2018_tt_tau->GetBinContent(h_2018_tt_tau->FindBin(mvis));
//  }

  frac_qcd = h_QCD_tau1->GetBinContent(h_QCD_tau1->FindBin(mvis));
  frac_w = h_W_tau1->GetBinContent(h_W_tau1->FindBin(mvis));
  frac_tt = h_tt_tau1->GetBinContent(h_tt_tau1->FindBin(mvis));


  if(frac_qcd==-1 || frac_w == -1 || frac_tt == -1){
    std::cout << "ERRPR: the FF fraction is below 1" << std::endl;
  }


  inputs[6] = frac_qcd;
  inputs[7] = frac_w;
  inputs[8] = frac_tt;


  Double_t ffweight = -1;

  //  if(year==2017){
    
  ffweight = ff->value(inputs);
    
    //  }else if(year==2018){
    
    //    ffweight = ff_2018_mt->value(inputs);
    
    //  }


  if(ffweight==-1){
    std::cout << "ERRPR: the FF fraction is -1" << std::endl;    
  }


  //  std::cout << "check: (QCD, W, tt) = " << frac_qcd << " " << frac_w << " " << frac_tt << " -> " << ffweight  << " (" << year << " " << channel << " " << sysid  << std::endl;


  return ffweight;

}


void shutdown(){
//  delete ff_2017_tt;
//  delete ff_2017_mt;
//  delete ff_2018_tt;
//  delete ff_2018_mt;
  delete ff;
  
  //  std::cout << test << " release memories" << std::endl;
}


void fakefactor(){
  std::cout << std::endl;
  std::cout << "Initialize fakefactor.C ... " << std::endl;
  std::cout << std::endl;
  
  //  ReadFile();

  //  ff_file->Close();

}


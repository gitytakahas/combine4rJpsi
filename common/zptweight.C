/*
 * @short: provide Z pt weights at drawing level
 * @author: Izaak Neutelings (June 2018)
 *
 */

#include "TROOT.h"
#include "TFile.h"
#include "TH2.h"
#include "TH2F.h"
#include <iostream>
#include <algorithm>
using namespace std;
TH2F* zpthist;


void readZptFile(Int_t year=2018){  
  
  if(year!=2016 and year!=2017 and year!=2018){
    std::cout << ">>> fakeRate.C::readFakeRateFile: Warning! Year "<<year<<" not recognized! Using 2017 instead..."<<std::endl;
    year = 2017;
  }
  TString filename  = TString::Format("/work/ineuteli/analysis/LQ_legacy/plots/Zpt/%d/Zpt_weights_%d_Izaak.root",year,year);
    
  std::cout << ">>> opening " << filename << std::endl;
  TFile *file = new TFile(filename);
  zpthist = (TH2F*) file->Get("zptmass_weights");
  zpthist->SetDirectory(0);
  file->Close();
  
}

Float_t getZpt(Float_t m_genboson, Float_t pt_genboson){
  //Int_t xbin = zpthist->GetXaxis()->FindBin(m_genboson);
  //Int_t ybin = zpthist->GetYaxis()->FindBin(pt_genboson);
  //while(xbin<1) xbin++; while(xbin>zpthist->GetXaxis()->GetNbins()) xbin--;
  //while(ybin<1) ybin++; while(ybin>zpthist->GetYaxis()->GetNbins()) ybin--;
  //return histIWN->GetBinContent(xbin,ybin);
  
  //  std::cout << m_genboson << ", " << pt_genboson << " -> " << zpthist->GetBinContent(zpthist->GetXaxis()->FindBin(m_genboson),zpthist->GetYaxis()->FindBin(pt_genboson)) << std::endl;
  return zpthist->GetBinContent(zpthist->GetXaxis()->FindBin(m_genboson),zpthist->GetYaxis()->FindBin(pt_genboson));
}

Float_t getZpt_Down(Float_t m_genboson, Float_t pt_genboson, Float_t shift=0.90){
  return 1.+shift*(getZpt(m_genboson,pt_genboson)-1.);
}

Float_t getZpt_Up(Float_t m_genboson, Float_t pt_genboson, Float_t shift=1.10){
  return 1.+shift*(getZpt(m_genboson,pt_genboson)-1.);
}


void zptweight(){
  std::cout << ">>> initializing zptweights.C ... " << std::endl;
}


/*
 * @short: provide fake rate weights at drawing level
 * @author: Izaak Neutelings (April 2018)
 *
 */

#include "TROOT.h"
#include "TMath.h"
#include "TFile.h"
//#include "TH1.h"
//#include "TH1F.h"
#include "TGraphAsymmErrors.h"
#include "TF1.h"
#include "TH2.h"
#include "TH2D.h"
#include <iostream>
#include <algorithm>
//#include <string>
using namespace std;

Float_t zero = 0.0;
TString Iso            = "Iso"; // cut-based combined isolation
TString MVAoldDM       = "MVAoldDM";
TString MVAoldDM2017v1 = "MVAoldDM2017v1";
TString MVAoldDM2017v2 = "MVAoldDM2017v2";
TString MVAnewDM2017v2 = "MVAnewDM2017v2";
TString _ID, _WP;

std::map<Int_t,TGraphAsymmErrors*> fakeRates;     // DM -> TGAE(pt) -> weight
std::map<Int_t,TH2D*>              fakeRates2D;   // DM -> TH2D(pt,mass) -> weight
std::map<Int_t,Float_t>            flatFakeRates; // DM -> weight
std::vector<Int_t> decayModes = { 0, 1, 10, 11 };

// READ fake rates
void readFakeRateFile(const std::string& id, const std::string& wp, Int_t year, TString channel="mutau"){
    
    _ID = id;
    _WP = wp;
    
    fakeRates.clear();
    fakeRates2D.clear();
    flatFakeRates.clear();
    
    if(year!=2016 and year!=2017 and year!=2018){
      std::cout << ">>> fakeRate.C::readFakeRateFile: Warning! Year "<<year<<" not recognized! Using 2017 instead..."<<std::endl;
      year = 2017;
    }
    //TString filename  = TString::Format("PlotTools/fakeRate/fakeRate%d.root",year);
    TString filename  = TString::Format("/shome/ineuteli/analysis/LQ_legacy/plots/fakerate/%d/fakeRate%d.root",year,year);

    
    std::cout << ">>> opening "<<filename<<std::endl;
    TFile* file = new TFile(filename);
    TDirectory* dir = (TDirectory*) file->GetDirectory(channel);
    for(Int_t dm: decayModes){
      if(dm==11 and !_ID.Contains("new")) continue;
      //std::cout << ">>> loading in id "<<id<<", wp "<<wp<<", dm "<<dm;
      
      // HIST NAMES
      TString wpden         = "VL";
      if(wp=="VL") wpden = "VVL";

      std::cout << " >>> working point of denominator = " << wpden << std::endl;

      TString histname      = TString::Format("%s_%sover%sn%s_dm%d",_ID.Data(),_WP.Data(),wpden.Data(),_WP.Data(),dm);
      TString histname2D    = TString::Format("%s_%sover%sn%s_dm%d_%s",_ID.Data(),_WP.Data(),wpden.Data(),_WP.Data(),dm,(dm==0 ? "eta" : "mass"));
      TString histname_flat = TString::Format("flatFR_over%s_dm%d",wpden.Data(),dm);
      //std::cout << ": " << histname << ", " << histname2D << ", " << histname_flat << std::endl;
      
      // FAKE RATE vs. PT
      //std::cout << ">>> loading " << histname << std::endl;
      fakeRates[dm] = (TGraphAsymmErrors*) dir->Get(histname);
      if(!fakeRates[dm])
        std::cout<<">>>   fakeRate.C::readFakeRateFile: Warning! No fake rate graph (\""<<histname<<"\") for "<<id<<", WP "<<wp<<", DM"<<dm<<std::endl;
      
      // FAKE RATE vs. PT vs. MASS/ETA
      //std::cout << ">>> loading " << histname2D << std::endl;
      fakeRates2D[dm] = (TH2D*) dir->Get(histname2D);
      if(!fakeRates2D[dm])
        std::cout<<">>>   fakeRate.C::readFakeRateFile: Warning! No fake rate TH2D (\""<<histname2D<<"\") for "<<id<<", WP"<<wp<<", DM"<<dm<<std::endl;
      
      // FLAT FAKE RATE
      //std::cout << ">>> loading " << histname_flat << std::endl;
      TH2D* hist_flat = (TH2D*) dir->Get(histname_flat);
      TString wpfull = wp + (_WP.Contains("L") ? "oose" : (_WP.Contains("M") ? "edium" : "ight"));
      if(!hist_flat)
        std::cout<<">>>   fakeRate.C::readFakeRateFile: Warning! No TH2D (\""<<histname_flat<<"\") for DM"<<dm<<std::endl;
      Int_t xbin = hist_flat->GetXaxis()->FindBin(wpfull);
      Int_t ybin = hist_flat->GetYaxis()->FindBin(_ID);
      if(xbin<1 or xbin>hist_flat->GetXaxis()->GetNbins())
        std::cout<<">>>   fakeRate.C::readFakeRateFile: Warning! WP"<<wp<<" not found in \""<<histname_flat<<"\""<<std::endl;
      if(ybin<1 or ybin>hist_flat->GetYaxis()->GetNbins())
        std::cout<<">>>   fakeRate.C::readFakeRateFile: Warning! ID"<<id<<" not found in \""<<histname_flat<<"\""<<std::endl;
      flatFakeRates[dm] = hist_flat->GetBinContent(xbin,ybin);
      if(flatFakeRates[dm]<=0.0)
        std::cout<<">>>   fakeRate.C::readFakeRateFile: Warning! No valid flat fake rate ("<<flatFakeRates[dm]<<") found for "<<id<<", WP "<<wp<<", DM"<<dm<<" in \""<<histname_flat<<"\", bin ("<<xbin<<","<<ybin<<")"<<std::endl;
      
      //fakeRates[dm]->SetDirectory(0)
      fakeRates2D[dm]->SetDirectory(0);
      
    }
    file->Close();
}



// NOMINAL fake rate vs. pt
Float_t getFakeRate(Float_t pt, Int_t dm){
  Float_t fakeRate = 0.0;
  if(dm==11 and !_ID.Contains("new")) return 0.0;
  if(std::find(decayModes.begin(),decayModes.end(),dm)!=decayModes.end()){
    fakeRate = fakeRates[dm]->Eval(pt);
  }
  //std::cout << ">>> getFakeRate: pt="<<pt<<", decayMode="<<dm<<", FR="<<fakeRate<<std::endl;
  return fakeRate; // TMath::Max(zero,fakeRate);
}

// NOMINAL fake rate vs. mass vs. pt
Float_t getFakeRate(Float_t pt, Float_t mass, Int_t dm){
  //std::cout << ">>> getFakeRate: " << pt << ", " << mass << ", " << dm << ", " << id << std::endl;
  Float_t fakeRate = 0.0;
  if(dm==0)
    return getFakeRate(pt,dm);
  if(dm==11 and !_ID.Contains("new")) return 0.0;
  if(std::find(decayModes.begin(),decayModes.end(),dm)!=decayModes.end()){
    Int_t ipt = TMath::Min(fakeRates2D[dm]->GetXaxis()->FindBin(pt),   fakeRates2D[dm]->GetXaxis()->GetNbins());
    Int_t im  = TMath::Min(fakeRates2D[dm]->GetYaxis()->FindBin(mass), fakeRates2D[dm]->GetYaxis()->GetNbins());
    fakeRate  = fakeRates2D[dm]->GetBinContent(ipt,im);
    while(fakeRate==0.0 and ipt>0){
      ipt -= 1;
      fakeRate = fakeRates2D[dm]->GetBinContent(ipt,im);
    }
  }
  //std::cout << ">>> getFakeRate: FR="<<std::setw(9)<<fakeRate<<", pt="<<std::setw(9)<<pt<<", mass="<<std::setw(9)<<mass<<", id="<<id<<std::endl;
  return fakeRate;
}

// NOMINAL fake rate vs. mass/eta vs. pt
Float_t getFakeRate(Float_t pt, Float_t mass, Float_t eta, Int_t dm){
  //std::cout << ">>> getFakeRate: " << pt << ", " << mass << " / " << eta << ", " << dm << ", " << id << std::endl;
  Float_t fakeRate = 0.0;
  if(dm!=0)
    return getFakeRate(pt,mass,dm);
  Int_t ipt  = TMath::Min(fakeRates2D[0]->GetXaxis()->FindBin(pt),        fakeRates2D[0]->GetXaxis()->GetNbins());
  Int_t ieta = TMath::Min(fakeRates2D[0]->GetYaxis()->FindBin(fabs(eta)), fakeRates2D[0]->GetYaxis()->GetNbins());
  fakeRate   = fakeRates2D[0]->GetBinContent(ipt,ieta);
  while(fakeRate==0.0 and ipt>0){
    ipt -= 1;
    fakeRate = fakeRates2D[0]->GetBinContent(ipt,ieta);
  }
  //std::cout << ">>> getFakeRate: FR="<<std::setw(9)<<fakeRate<<", pt="<<std::setw(9)<<pt<<" (i="<<ipt<<"), eta="<<std::setw(9)<<eta<<" (i="<<ieta<<"), id="<<id<<std::endl;
  return fakeRate;
}



// DOWN fake rate vs. pt
Float_t getFakeRateDown(Float_t pt, Int_t dm){
  Float_t fakeRate = 0.0;
  if(dm==11 and !_ID.Contains("new")) return 0.0;
  if(std::find(decayModes.begin(),decayModes.end(),dm)!=decayModes.end()){
    fakeRate = flatFakeRates[dm];
  }
  return fakeRate;
}

// DOWN fake rate vs. mass vs. pt
Float_t getFakeRateDown(Float_t pt, Float_t mass, Int_t dm){
  return getFakeRateDown(pt,dm);
}

// DOWN fake rate vs. mass/eta vs. pt
Float_t getFakeRateDown(Float_t pt, Float_t mass, Float_t eta, Int_t dm){
  return getFakeRateDown(pt,dm);
}



// UP fake rate vs. mass
Float_t getFakeRateUp(Float_t pt, Int_t dm){
  Float_t fakeRate = 0.0;
  if(dm==11 and !_ID.Contains("new")) return 0.0;
  if(std::find(decayModes.begin(),decayModes.end(),dm)!=decayModes.end()){
    fakeRate = fakeRates[dm]->Eval(pt);
    fakeRate = 2*fakeRate - flatFakeRates[dm];
  }
  return fakeRate;
}

// UP fake rate vs. mass vs. pt
Float_t getFakeRateUp(Float_t pt, Float_t mass, Int_t dm){
  Float_t fakeRate = 0.0;
  if(dm==11 and !_ID.Contains("new")) return 0.0;
  if(std::find(decayModes.begin(),decayModes.end(),dm)!=decayModes.end()){
    fakeRate = getFakeRate(pt,mass,dm);
    fakeRate = 2*fakeRate - flatFakeRates[dm];
  }
  return fakeRate;
}

// UP fake rate vs. mass/eta vs. pt
Float_t getFakeRateUp(Float_t pt, Float_t mass, Float_t eta, Int_t dm){
  Float_t fakeRate = 0.0;
  if(dm==11 and !_ID.Contains("new")) return 0.0;
  if(std::find(decayModes.begin(),decayModes.end(),dm)!=decayModes.end()){
    fakeRate = getFakeRate(pt,mass,eta,dm);
    fakeRate = 2*fakeRate - flatFakeRates[dm];
  }
  return fakeRate;
}



void fakeRate(){
  //std::cout << std::endl;
  std::cout << ">>> initializing fakeRate.C ... " << std::endl;
  //std::cout << std::endl;
  //readFakeRateFile();
}



/*
 * @short: provide fake rate weights at drawing level
 * @author: Izaak Neutelings (April 2018)
 *
 */

#include <iomanip> // for setw
#include "TROOT.h"
#include "TMath.h"
#include "TFile.h"
//#include "TH1.h"
//#include "TH1F.h"
#include "TGraphAsymmErrors.h"
#include "TF1.h"
#include "TH2.h"
#include "TH2F.h"
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

std::map<TString,std::map<Int_t,TGraphAsymmErrors*>> fakeRates;   // DM -> TGAE(pt) -> weight
std::map<TString,std::map<Int_t,TH2F*>>              fakeRates2D; // DM -> TH2F(pt,mass) -> weight
std::map<TString,std::map<Int_t,Float_t>>            flatFakeRates;
std::vector<TString> IDs = { MVAoldDM2017v2 }; // Iso, MVAoldDM, MVAoldDM2017v1, MVAoldDM2017v2, MVAnewDM2017v2 };
std::vector<Int_t> decayModes = { 0, 1, 10, 11 };
TString ID = MVAoldDM2017v2;
void setID(const std::string& id){ ID=id; }


// READ fake rates
void readFakeRateFile(int year, TString channel="mutau"){
  
  TString filename  = TString::Format("$SFRAME_DIR/../plots/fakerate/%d/fakeRate%d.root",year,year);
  
  if(year==2017)
    flatFakeRates = {
      {MVAoldDM2017v1, {{0, 6706./26978.},{1,12640./57044.},{10,6493./31601.}}},
      {MVAoldDM2017v2, {{0,12854./38362.},{1,16005./70304.},{10,4901./31097.}}},
      {MVAnewDM2017v2, {{0,15984./47451.},{1,21849./87487.},{10,7007./42683.},{11,1618./23603.}}}
    };
  else
    flatFakeRates = {
      //{MVAoldDM2017v1, {{0, 6706./26978.},{1,12640./57044.},{10,6493./31601.}}},
      {MVAoldDM2017v2, {{0,19911./60256.},{1,24114./109588.},{10,9594./61260.}}},
      //{MVAnewDM2017v1, {{0,15984./47451.},{1,21849./87487.},{10,7007./42683.},{11,1618./23603.}}}
    };
  
  std::cout << ">>> opening "<<filename<<std::endl;
  TFile *file = new TFile(filename);
  for(TString id: IDs){
    TString wp = "T";
    for(Int_t dm: decayModes){
      if(dm==11 and !id.Contains("new")) continue;
      //std::cout << ">>> loading in wp "<<std::setw(3)<<wp<<", dm "<<std::setw(2)<<dm;
      TString histname  = channel+"/"+id+"_"+wp+"overVLn"+wp+"_dm";
      histname += dm;
      //std::cout << ": " << histname << std::endl;
      fakeRates[id][dm] = (TGraphAsymmErrors*) file->Get(histname);
      if(dm==0) fakeRates2D[id][dm] = (TH2F*) file->Get(histname+"_eta");
      else      fakeRates2D[id][dm] = (TH2F*) file->Get(histname+"_mass");
      
      if(!fakeRates[id][dm])
        std::cout<<">>>   fakeRate.C::readFile: no fake rate graph (\""<<histname<<"\") for "<<id<<", DM"<<dm<<std::endl;
      if(!fakeRates2D[id][dm]){
        if(dm==0)
          std::cout<<">>>   fakeRate.C::readFile: no fake rate TH2F (\""<<histname<<"_eta\") for "<<id<<", DM"<<dm<<std::endl;
        else
          std::cout<<">>>   fakeRate.C::readFile: no fake rate TH2F (\""<<histname<<"_mass\") for "<<id<<", DM"<<dm<<std::endl;
      }
    }
  }
}



// NOMINAL fake rate vs. pt
Float_t getFakeRate(Float_t pt, Int_t dm, TString id=ID){
  Float_t fakeRate = 0.0;
  if(dm==11 and !id.Contains("new")) return 0.0;
  if(std::find(decayModes.begin(),decayModes.end(),dm)!=decayModes.end()){
    fakeRate = fakeRates[id][dm]->Eval(pt);
  }
  //std::cout << ">>> getFakeRate: pt="<<pt<<", decayMode="<<dm<<", FR="<<fakeRate<<std::endl;
  return fakeRate; // TMath::Max(zero,fakeRate);
}

// NOMINAL fake rate vs. mass vs. pt
Float_t getFakeRate(Float_t pt, Float_t mass, Int_t dm, TString id=ID){
  //std::cout << ">>> getFakeRate: " << pt << ", " << mass << ", " << dm << ", " << id << std::endl;
  Float_t fakeRate = 0.0;
  if(dm==0)
    return getFakeRate(pt,dm);
  if(dm==11 and !id.Contains("new")) return 0.0;
  if(std::find(decayModes.begin(),decayModes.end(),dm)!=decayModes.end()){
    Int_t ipt = TMath::Min(fakeRates2D[id][dm]->GetXaxis()->FindBin(pt),   fakeRates2D[id][dm]->GetXaxis()->GetNbins());
    Int_t im  = TMath::Min(fakeRates2D[id][dm]->GetYaxis()->FindBin(mass), fakeRates2D[id][dm]->GetYaxis()->GetNbins());
    fakeRate  = fakeRates2D[id][dm]->GetBinContent(ipt,im);
    while(fakeRate==0.0 and ipt>0){
      ipt -= 1;
      fakeRate = fakeRates2D[id][dm]->GetBinContent(ipt,im);
    }
  }
  //std::cout << ">>> getFakeRate: FR="<<std::setw(9)<<fakeRate<<", pt="<<std::setw(9)<<pt<<", mass="<<std::setw(9)<<mass<<", id="<<id<<std::endl;
  return fakeRate;
}

// NOMINAL fake rate vs. mass/eta vs. pt
Float_t getFakeRate(Float_t pt, Float_t mass, Float_t eta, Int_t dm, TString id=ID){
  //std::cout << ">>> getFakeRate: " << pt << ", " << mass << " / " << eta << ", " << dm << ", " << id << std::endl;
  Float_t fakeRate = 0.0;
  if(dm!=0)
    return getFakeRate(pt,mass,dm);
  if(dm==11 and !id.Contains("new")) return 0.0;
  Int_t ipt  = TMath::Min(fakeRates2D[id][0]->GetXaxis()->FindBin(pt),        fakeRates2D[id][0]->GetXaxis()->GetNbins());
  Int_t ieta = TMath::Min(fakeRates2D[id][0]->GetYaxis()->FindBin(fabs(eta)), fakeRates2D[id][0]->GetYaxis()->GetNbins());
  fakeRate   = fakeRates2D[id][0]->GetBinContent(ipt,ieta);
  while(fakeRate==0.0 and ipt>0){
    ipt -= 1;
    fakeRate = fakeRates2D[id][0]->GetBinContent(ipt,ieta);
  }
  //std::cout << ">>> getFakeRate: FR="<<std::setw(9)<<fakeRate<<", pt="<<std::setw(9)<<pt<<" (i="<<ipt<<"), eta="<<std::setw(9)<<eta<<" (i="<<ieta<<"), id="<<id<<std::endl;
  return fakeRate;
}



// DOWN fake rate vs. pt
Float_t getFakeRateDown(Float_t pt, Int_t dm, TString id=ID){
  Float_t fakeRate = 0.0;
  if(dm==11 and !id.Contains("new")) return 0.0;
  if(std::find(decayModes.begin(),decayModes.end(),dm)!=decayModes.end()){
    fakeRate = flatFakeRates[id][dm];
  }
  return fakeRate;
}

// DOWN fake rate vs. mass vs. pt
Float_t getFakeRateDown(Float_t pt, Float_t mass, Int_t dm, TString id=ID){
  return getFakeRateDown(pt,dm,id);
}

// DOWN fake rate vs. mass/eta vs. pt
Float_t getFakeRateDown(Float_t pt, Float_t mass, Float_t eta, Int_t dm, TString id=ID){
  return getFakeRateDown(pt,dm,id);
}



// UP fake rate vs. mass
Float_t getFakeRateUp(Float_t pt, Int_t dm, TString id=ID){
  Float_t fakeRate = 0.0;
  if(dm==11 and !id.Contains("new")) return 0.0;
  if(std::find(decayModes.begin(),decayModes.end(),dm)!=decayModes.end()){
    fakeRate = fakeRates[id][dm]->Eval(pt);
    fakeRate = 2*fakeRate - flatFakeRates[id][dm];
  }
  return fakeRate;
}

// UP fake rate vs. mass vs. pt
Float_t getFakeRateUp(Float_t pt, Float_t mass, Int_t dm, TString id=ID){
  Float_t fakeRate = 0.0;
  if(dm==11 and !id.Contains("new")) return 0.0;
  if(std::find(decayModes.begin(),decayModes.end(),dm)!=decayModes.end()){
    fakeRate = getFakeRate(pt,mass,dm,id);
    fakeRate = 2*fakeRate - flatFakeRates[id][dm];
  }
  return fakeRate;
}

// UP fake rate vs. mass/eta vs. pt
Float_t getFakeRateUp(Float_t pt, Float_t mass, Float_t eta, Int_t dm, TString id=ID){
  Float_t fakeRate = 0.0;
  if(dm==11 and !id.Contains("new")) return 0.0;
  if(std::find(decayModes.begin(),decayModes.end(),dm)!=decayModes.end()){
    fakeRate = getFakeRate(pt,mass,eta,dm,id);
    fakeRate = 2*fakeRate - flatFakeRates[id][dm];
  }
  return fakeRate;
}



void fakeRate(){
  //std::cout << std::endl;
  std::cout << ">>> initializing fakeRate.C ... " << std::endl;
  //std::cout << std::endl;
  //readFakeRateFile();
}



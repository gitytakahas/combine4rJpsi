#include <iostream>     // std::cout
#include <algorithm>  // std::max

void examplews(){
  // As usual, load the combine library to get access to the RooParametricHist
  gROOT->SetBatch();
  gSystem->Load("libHiggsAnalysisCombinedLimit.so");

  // Output file and workspace
  TFile *fOut = new TFile("param_ws.root","RECREATE");
  RooWorkspace wspace("wspace","wspace");

  // better to create the bins rather than use the "nbins,min,max" to avoid spurious warning about adding bins with different 
  // ranges in combine - see https://root-forum.cern.ch/t/attempt-to-divide-histograms-with-different-bin-limits/17624/3 for why!
  const int nbins = 36;
  double xmin=0.;
  double xmax=36;

  RooRealVar var("tau_rhomass_unrolled_coarse","Tau rhomass unrolled bin ID",nbins,xmin,xmax);
  RooArgList vars(var);

  //////////////////////////////////
  // control region 
  //////////////////////////////////

  TFile *file_sb = new TFile("/work/ytakahas/work/analysis/CMSSW_10_2_10/src/rJpsi/anal/combine_sb3p5_sr4_simultaneous/2018/tau_rhomass_unrolled_coarse_sb.root");

  //Loop on all the histos
  TIter next_sb(file_sb->GetListOfKeys());
  TKey *key_sb;

  while ((key_sb = (TKey*)next_sb())) {
    

    TClass *cl = gROOT->GetClass(key_sb->GetClassName());
    if (!cl->InheritsFrom("TH1")) continue;

    TH1 *h = (TH1*)key_sb->ReadObj();

    TString name_string = h->GetName();
    name_string += "_sb";

    std::cout << name_string << std::endl;

    RooDataHist rdh(name_string,"sb",vars,h);
    wspace.import(rdh);
  }
    
  TH1F* data_histo_sb = (TH1F*)file_sb->Get("data_obs");
  TH1F* bc_jpsi_tau_3p = (TH1F*)file_sb->Get("bc_jpsi_tau_3p");
  TH1F* bc_jpsi_tau_N3p = (TH1F*)file_sb->Get("bc_jpsi_tau_N3p");
  TH1F* bc_others = (TH1F*)file_sb->Get("bc_others");
  TH1F* bc_jpsi_dst = (TH1F*)file_sb->Get("bc_jpsi_dst");

  // fakes
  std::vector<RooRealVar> bins; 

  for(int i=1; i<=nbins; i++){

    stringstream s;
    s << i;
    
    string mystring1 = "bg_bin" + s.str() + "_sb";
    string mystring2 = "Background yield in control region, bin " + s.str();
    
    double val = data_histo_sb->GetBinContent(i) - bc_jpsi_tau_3p->GetBinContent(i) - bc_jpsi_tau_N3p->GetBinContent(i) - bc_others->GetBinContent(i) - bc_jpsi_dst->GetBinContent(i);
    //    double unc = bc_jpsi_tau_3p->GetBinContent(i) + bc_jpsi_tau_N3p->GetBinContent(i);
    double unc = TMath::Sqrt(data_histo_sb->GetBinContent(i));

    std::cout << i << " " << val << " " << unc << std::endl;
    
    //    RooRealVar bin(mystring1.c_str(), mystring2.c_str(), val, max(0., val - 5*unc), val + 5*unc);
    RooRealVar bin(mystring1.c_str(), mystring2.c_str(), val, max(0., val - 10*unc), val + 10*unc);

    bins.push_back(bin);
  }
    
  RooArgList fakes_sb_bins;
  for(int i=0; i<nbins; i++){
    fakes_sb_bins.add(bins[i]);
  }


  RooParametricHist rph_fakes_sb("fakes_sb", "Background PDF in control region",var,fakes_sb_bins, *data_histo_sb);
  RooAddition rph_fakes_sb_norm("fakes_sb_norm","Total Number of events from background in signal region",fakes_sb_bins); 

  wspace.import(rph_fakes_sb);
  wspace.import(rph_fakes_sb_norm,RooFit::RecycleConflictNodes());



  ///////////////////////////////////////
  /// SIGNAL REGION
  ///////////////////////////////////////


  TFile *file_sr = new TFile("/work/ytakahas/work/analysis/CMSSW_10_2_10/src/rJpsi/anal/combine_sb3p5_sr4_simultaneous/2018/tau_rhomass_unrolled_coarse_sr.root");

  //Loop on all the histos
  TIter next_sr(file_sr->GetListOfKeys());
  TKey *key_sr;
  while ((key_sr = (TKey*)next_sr())) {

    TClass *cl = gROOT->GetClass(key_sr->GetClassName());
    if (!cl->InheritsFrom("TH1")) continue;

    TH1 *h = (TH1*)key_sr->ReadObj();
    TString name_string = h->GetName();
    name_string += "_sr";


    RooDataHist rdh(name_string,"sr",vars,h);
    wspace.import(rdh);
  }

  TH1F* data_histo_sr = (TH1F*)file_sr->Get("data_obs");





  //  RooRealVar efficiency("efficiency", "efficiency nuisance parameter",0.);

  //  RooFormulaVar TF("TF","Trasnfer factor","2*0.092*TMath::Power(1.02,@0)",RooArgList(efficiency) );



  RooRealVar TF("TF","Transfer factor",0.092); 
  TF.setConstant(); 

  std::vector<RooFormulaVar> bins_sr; 
  for(int i=1; i<=nbins; i++){
    stringstream s;
    s << i;
    string mystring1 = "bg_bin" + s.str() + "_sr";
    string mystring2 = "Background yield in signal region, bin " + s.str();

    RooFormulaVar bin(mystring1.c_str(),mystring2.c_str()," @0*@1",RooArgList(TF, bins[i-1]));
    bins_sr.push_back(bin);
  }

  RooArgList fakes_sr_bins;
  for(int i=0; i<nbins; i++){
    fakes_sr_bins.add(bins_sr[i]);
  }

  RooParametricHist rph_fakes_sr("fakes_sr", "Background PDF in signal region", var, fakes_sr_bins, *data_histo_sr);
  RooAddition rph_fakes_sr_norm("fakes_sr_norm","Total Number of events from background in signal region", fakes_sr_bins);


  wspace.import(rph_fakes_sr);
  wspace.import(rph_fakes_sr_norm,RooFit::RecycleConflictNodes());


  fOut->cd();
  wspace.Write();
  
  // Clean up
  fOut->Close();
  fOut->Delete();
    

}

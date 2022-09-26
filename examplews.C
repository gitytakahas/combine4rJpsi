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
  const int nbins = 25;
  double xmin=0.;
  double xmax=25;

  RooRealVar var("tau_rhomass_unrolled_coarse","Tau rhomass unrolled bin ID",nbins,xmin,xmax);
  RooArgList vars(var);

  //////////////////////////////////
  // control region 
  //////////////////////////////////

  TFile *file_sb = new TFile("/work/ytakahas/work/analysis/CMSSW_10_2_10/src/rJpsi/anal/combine_sb3p5_sr4_simultaneous/2018/tau_rhomass_unrolled_coarse_sb.root");
  //TFile *file_sb = new TFile("output/sm_cards/LIMITS/common/rJpsi_sb_2_2018_90.input.root");
  //  file_sb->cd("rJpsi_sb_2_2018");
  //  TDirectory* dir_sb = gDirectory;

  //Loop on all the histos
  TIter next_sb(file_sb->GetListOfKeys());
  TKey *key_sb;

  while ((key_sb = (TKey*)next_sb())) {
    

    TClass *cl = gROOT->GetClass(key_sb->GetClassName());

    std::cout << "class name = " << key_sb->GetClassName() << std::endl;
    if (!cl->InheritsFrom("TH1")) continue;

    TH1 *h = (TH1*)key_sb->ReadObj();

    TString name_string = h->GetName();
    name_string += "_sb";

    std::cout << name_string << std::endl;

//    TH1F*  histo_tmp = (TH1F*)file_sb->Get(h->GetName());
//
//    TH1F histo(name_string, name_string,nbins,xmin, xmax);
//    for(int i=1; i<=nbins; i++){
//      histo.SetBinContent(i,histo_tmp->GetBinContent(i));
//      histo.SetBinError(i,histo_tmp->GetBinError(i));
//    }

//    RooDataHist rdh(name_string,"sb",vars,&histo);
    RooDataHist rdh(name_string,"sb",vars,h);
    wspace.import(rdh);
  }
    
  TH1F* data_histo_sb = (TH1F*)file_sb->Get("data_obs");
  TH1F* bc_jpsi_tau_3p_sb = (TH1F*)file_sb->Get("bc_jpsi_tau_3p");
  TH1F* bc_jpsi_tau_N3p_sb = (TH1F*)file_sb->Get("bc_jpsi_tau_N3p");
  TH1F* bc_others_sb = (TH1F*)file_sb->Get("bc_others");
  TH1F* bc_jpsi_dst_sb = (TH1F*)file_sb->Get("bc_jpsi_dst");

  // fakes
  std::vector<RooRealVar> bins; 

  for(int i=1; i<=nbins; i++){

    stringstream s;
    s << i;
    
    string mystring1 = "bg_bin" + s.str() + "_sb";
    string mystring2 = "Background yield in control region, bin " + s.str();
    
    double val = data_histo_sb->GetBinContent(i) - bc_jpsi_tau_3p_sb->GetBinContent(i) - bc_jpsi_tau_N3p_sb->GetBinContent(i) - bc_others_sb->GetBinContent(i) - bc_jpsi_dst_sb->GetBinContent(i);
    //    double unc = bc_jpsi_tau_3p->GetBinContent(i) + bc_jpsi_tau_N3p->GetBinContent(i);
    double unc = TMath::Sqrt(val);

    std::cout << "SB:" << i << ": " << data_histo_sb->GetBinContent(i) << " - " << bc_jpsi_tau_3p_sb->GetBinContent(i) << " - " << bc_jpsi_tau_N3p_sb->GetBinContent(i) << " - " << bc_others_sb->GetBinContent(i) << " - " << bc_jpsi_dst_sb->GetBinContent(i) << " = "  << val << " " << unc << std::endl;
    
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
  //TFile *file_sr = new TFile("output/sm_cards/LIMITS/common/rJpsi_sr_1_2018_90.input.root");
  //  file_sr->cd("rJpsi_sr_2_2018");
  //  TDirectory* dir_sr = gDirectory;


  //Loop on all the histos
  TIter next_sr(file_sr->GetListOfKeys());
  TKey *key_sr;
  while ((key_sr = (TKey*)next_sr())) {

    TClass *cl = gROOT->GetClass(key_sr->GetClassName());
    if (!cl->InheritsFrom("TH1")) continue;

    TH1F *h = (TH1F*)key_sr->ReadObj();
    TString name_string = h->GetName();
    name_string += "_sr";


//    TH1F*  histo_tmp = (TH1F*)file_sr->Get(h->GetName());
//
//    TH1F histo(name_string, name_string,nbins,xmin, xmax);
//    for(int i=1; i<=nbins; i++){
//      histo.SetBinContent(i,histo_tmp->GetBinContent(i));
//      histo.SetBinError(i,histo_tmp->GetBinError(i));
//    }
//
//    RooDataHist rdh(name_string,"sb",vars,&histo);

    RooDataHist rdh(name_string,"sr",vars,h);
    wspace.import(rdh);
  }

  TH1F* data_histo_sr = (TH1F*)file_sr->Get("data_obs");
  TH1F* bc_jpsi_tau_3p_sr = (TH1F*)file_sr->Get("bc_jpsi_tau_3p");
  TH1F* bc_jpsi_tau_N3p_sr = (TH1F*)file_sr->Get("bc_jpsi_tau_N3p");
  TH1F* bc_others_sr = (TH1F*)file_sr->Get("bc_others");
  TH1F* bc_jpsi_dst_sr = (TH1F*)file_sr->Get("bc_jpsi_dst");



  for(int i=1; i<=nbins; i++){    

    double val = data_histo_sr->GetBinContent(i) - bc_jpsi_tau_3p_sr->GetBinContent(i) - bc_jpsi_tau_N3p_sr->GetBinContent(i) - bc_others_sr->GetBinContent(i) - bc_jpsi_dst_sr->GetBinContent(i);

    std::cout << "SR:" << i << ": " << data_histo_sr->GetBinContent(i) << " - " << bc_jpsi_tau_3p_sr->GetBinContent(i) << " - " << bc_jpsi_tau_N3p_sr->GetBinContent(i) << " - " << bc_others_sr->GetBinContent(i) << " - " << bc_jpsi_dst_sr->GetBinContent(i) << " = " << val << std::endl;

  }



  RooRealVar efficiency("efficiency", "efficiency nuisance parameter",0.);

  RooFormulaVar TF("TF","Trasnfer factor","0.092*2*TMath::Power(1.04,@0)",RooArgList(efficiency) );



  //  RooRealVar TF("TF","Transfer factor",0.092); 
  //  TF.setConstant(); 

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

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

  //////////////////////////////////
  // control region 
  //////////////////////////////////

  TFile *input_file = new TFile("/work/ytakahas/work/analysis/CMSSW_10_2_10/src/rJpsi/anal/combine_sb3p5_sr4_simultaneous/2018/tau_rhomass_unrolled_var.root");
  input_file->cd("sb");
  TDirectory* dir_sb = gDirectory;
  TH1D* data_histo_sb = (TH1D*)dir_sb->Get("data_obs");
  TH1D* bc_jpsi_tau_3p_sb = (TH1D*)dir_sb->Get("bc_jpsi_tau_3p");
  TH1D* bc_jpsi_tau_N3p_sb = (TH1D*)dir_sb->Get("bc_jpsi_tau_N3p");
  TH1D* bc_others_sb = (TH1D*)dir_sb->Get("bc_others");
  TH1D* bc_jpsi_dst_sb = (TH1D*)dir_sb->Get("bc_jpsi_dst");
  TH1D* bg_ul_sb = (TH1D*)dir_sb->Get("bg_ul");

  const int nbins = data_histo_sb->GetXaxis()->GetNbins();
  double xmin=data_histo_sb->GetXaxis()->GetXmin();
  double xmax=data_histo_sb->GetXaxis()->GetXmax();

  std::cout << "(nbins, xmin, xmax) = " <<  nbins << " " << xmin << " " << xmax << std::endl;

  RooRealVar var("tau_rhomass_unrolled_coarse","Tau rhomass unrolled bin ID",nbins,xmin,xmax);
  RooArgList vars(var);



  //Loop on all the histos
  TIter next_sb(dir_sb->GetListOfKeys());
  TKey *key_sb;

  while ((key_sb = (TKey*)next_sb())) {
    

    TClass *cl = gROOT->GetClass(key_sb->GetClassName());

    std::cout << "class name = " << key_sb->GetClassName() << std::endl;
    if (!cl->InheritsFrom("TH1")) continue;

    TH1 *h = (TH1*)key_sb->ReadObj();

    TString name_string = h->GetName();
    TString name_rdhstring = name_string;
    name_rdhstring += "_sb";

    std::cout << name_string << std::endl;

//    TH1F*  histo_tmp = (TH1F*)input_file->Get(h->GetName());
//
//    TH1F histo(name_string, name_string,nbins,xmin, xmax);
//    for(int i=1; i<=nbins; i++){
//      histo.SetBinContent(i,histo_tmp->GetBinContent(i));
//      histo.SetBinError(i,histo_tmp->GetBinError(i));
//    }

//    RooDataHist rdh(name_string,"sb",vars,&histo);
    RooDataHist rdh(name_rdhstring,"sb",vars,h);
    wspace.import(rdh);

    
    if(name_string=="bc_others" || 
       name_string=="bc_jpsi_dst" || 
       name_string=="bc_jpsi_tau_3p" || 
       name_string=="bc_jpsi_tau_N3p"){

      //      std::cout << "This is IT!!!!!!!!!!!!!!!!!!!!!!!!!!!!" << std::endl;

      for(int ibin=1; ibin <= nbins; ibin++){

	for(int isUp=0; isUp<2; isUp++){
	  
	  TString bbb_string = h->GetName();
	  bbb_string += "_";
	  bbb_string += h->GetName();
	  bbb_string += "_bbb";
	  bbb_string += ibin;
	  bbb_string += (isUp==0) ? "Up" : "Down";
	  bbb_string += "_sb";
	
	  TH1D histo(bbb_string, bbb_string, nbins, xmin, xmax);	
	  
	  for(int jbin=1; jbin <= nbins; jbin++){
	    if(jbin==ibin){
	      if(isUp==0){
		histo.SetBinContent(jbin, h->GetBinContent(jbin) + h->GetBinError(jbin));
	      }else{
		histo.SetBinContent(jbin, h->GetBinContent(jbin) - h->GetBinError(jbin));
	      }
	      histo.SetBinError(jbin, h->GetBinError(jbin)*histo.GetBinContent(jbin)/h->GetBinContent(jbin));
	    }else{
	      histo.SetBinContent(jbin, h->GetBinContent(jbin));
	      histo.SetBinError(jbin, h->GetBinError(jbin));
	    }
	  }

	  RooDataHist rdh_bbb(bbb_string,"sb",vars,&histo);
	  wspace.import(rdh_bbb);
	  
	}
      }

//
//    TH1F histo(name_string, name_string,nbins,xmin, xmax);
//    for(int i=1; i<=nbins; i++){
//      histo.SetBinContent(i,histo_tmp->GetBinContent(i));
//      histo.SetBinError(i,histo_tmp->GetBinError(i));
//    }


      
       
    }
    

  }
    

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


  //  TFile *file_sr = new TFile("/work/ytakahas/work/analysis/CMSSW_10_2_10/src/rJpsi/anal/combine_sb3p5_sr4_simultaneous/2018/tau_rhomass_unrolled_coarse_sr.root");
  //TFile *file_sr = new TFile("output/sm_cards/LIMITS/common/rJpsi_sr_1_2018_90.input.root");

  input_file->cd();
  
  input_file->cd("sr");
  TDirectory* dir_sr = gDirectory;


  //Loop on all the histos
  TIter next_sr(dir_sr->GetListOfKeys());
  TKey *key_sr;
  while ((key_sr = (TKey*)next_sr())) {

    TClass *cl = gROOT->GetClass(key_sr->GetClassName());
    if (!cl->InheritsFrom("TH1")) continue;

    TH1D *h = (TH1D*)key_sr->ReadObj();
    TString name_string = h->GetName();
    TString name_rdhstring = name_string;
    name_rdhstring += "_sr";


//    TH1D*  histo_tmp = (TH1D*)file_sr->Get(h->GetName());
//
//    TH1D histo(name_string, name_string,nbins,xmin, xmax);
//    for(int i=1; i<=nbins; i++){
//      histo.SetBinContent(i,histo_tmp->GetBinContent(i));
//      histo.SetBinError(i,histo_tmp->GetBinError(i));
//    }
//
//    RooDataHist rdh(name_string,"sb",vars,&histo);

    RooDataHist rdh(name_rdhstring,"sr",vars,h);
    wspace.import(rdh);



    /// bbb uncertainties

    if(name_string=="bc_others" || 
       name_string=="bc_jpsi_dst" || 
       name_string=="bc_jpsi_tau_3p" || 
       name_string=="bc_jpsi_tau_N3p"){


      for(int ibin=1; ibin <= nbins; ibin++){

	for(int isUp=0; isUp<2; isUp++){
	  
	  TString bbb_string = h->GetName();
	  bbb_string += "_";
	  bbb_string += h->GetName();
	  bbb_string += "_bbb";
	  bbb_string += ibin;
	  bbb_string += (isUp==0) ? "Up" : "Down";
	  bbb_string += "_sr";
	
	  TH1D histo(bbb_string, bbb_string, nbins, xmin, xmax);	
	  
	  for(int jbin=1; jbin <= nbins; jbin++){
	    if(jbin==ibin){
	      if(isUp==0){
		histo.SetBinContent(jbin, h->GetBinContent(jbin) + h->GetBinError(jbin));
	      }else{
		histo.SetBinContent(jbin, h->GetBinContent(jbin) - h->GetBinError(jbin));
	      }
	      histo.SetBinError(jbin, h->GetBinError(jbin)*histo.GetBinContent(jbin)/h->GetBinContent(jbin));
	    }else{
	      histo.SetBinContent(jbin, h->GetBinContent(jbin));
	      histo.SetBinError(jbin, h->GetBinError(jbin));
	    }
	  }


	  RooDataHist rdh_bbb(bbb_string,"sr",vars,&histo);
	  wspace.import(rdh_bbb);
	  
	}
      }

//
//    TH1D histo(name_string, name_string,nbins,xmin, xmax);
//    for(int i=1; i<=nbins; i++){
//      histo.SetBinContent(i,histo_tmp->GetBinContent(i));
//      histo.SetBinError(i,histo_tmp->GetBinError(i));
//    }


      
       
    }
    





  }

  TH1D* data_histo_sr = (TH1D*)dir_sr->Get("data_obs");
  TH1D* bc_jpsi_tau_3p_sr = (TH1D*)dir_sr->Get("bc_jpsi_tau_3p");
  TH1D* bc_jpsi_tau_N3p_sr = (TH1D*)dir_sr->Get("bc_jpsi_tau_N3p");
  TH1D* bc_others_sr = (TH1D*)dir_sr->Get("bc_others");
  TH1D* bc_jpsi_dst_sr = (TH1D*)dir_sr->Get("bc_jpsi_dst");
  TH1D* bg_ul_sr = (TH1D*)dir_sr->Get("bg_ul");


  for(int i=1; i<=nbins; i++){    

    double val = data_histo_sr->GetBinContent(i) - bc_jpsi_tau_3p_sr->GetBinContent(i) - bc_jpsi_tau_N3p_sr->GetBinContent(i) - bc_others_sr->GetBinContent(i) - bc_jpsi_dst_sr->GetBinContent(i);

    std::cout << "SR:" << i << ": " << data_histo_sr->GetBinContent(i) << " - " << bc_jpsi_tau_3p_sr->GetBinContent(i) << " - " << bc_jpsi_tau_N3p_sr->GetBinContent(i) << " - " << bc_others_sr->GetBinContent(i) << " - " << bc_jpsi_dst_sr->GetBinContent(i) << " = " << val << std::endl;

  }



  //  RooRealVar efficiency("efficiency", "efficiency nuisance parameter",0.);

  //  RooFormulaVar TF("TF","Trasnfer factor","0.092",RooArgList(efficiency) );


  Float_t ratio = bg_ul_sr->Integral()/bg_ul_sb->Integral();
  
  std::cout << "ratio=" << ratio << std::endl;
  RooRealVar TF("TF","Transfer factor", ratio); 
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



/////  // shape for the fake estimates: 
/////
/////  TH1D fakes_param_up("fakes_ParamUp_sr","", nbins, xmin, xmax);
/////  TH1D fakes_param_down("fakes_ParamDown_sr","", nbins, xmin, xmax);
/////
/////  double p0 = 0.871;
/////  double p1 = 0.009;
/////
/////
/////  for(int i=1; i<=nbins; i++){
/////    //    float perc = (fakes_up_ch1_tmp->GetBinContent(i))/fakes_histo_ch2->GetBinContent(i)      ;
/////    //    std::cout<<"percentage "<<perc<<std::endl;
/////    double perc_up = p0 + p1*i;
/////    double perc_down = 2 - p0 - p1*i;
/////    
/////    fakes_param_up.SetBinContent(i, bins_sr[i-1].getVal()*perc_up);
/////    fakes_param_down.SetBinContent(i, bins_sr[i-1].getVal()*perc_down);
/////
/////  }
/////  
/////  RooDataHist rdh_fakes_param_up("fakes_ParamUp_sr","Bkg sys up",vars,&fakes_param_up);
/////  wspace.import(rdh_fakes_param_up);
/////
/////  RooDataHist rdh_fakes_param_down("fakes_ParamDown_sr","Bkg sys down",vars,&fakes_param_down);
/////  wspace.import(rdh_fakes_param_down);
/////
/////
/////
/////  // shape for the fake estimates (bbb): 
/////
/////  TH1D fakes_bbb_up("fakes_bbbUp_sr","", nbins, xmin, xmax);
/////  TH1D fakes_bbb_down("fakes_bbbDown_sr","", nbins, xmin, xmax);
/////
/////  TFile *file_ratio = new TFile("syst_bkg/tau_rhomass_unrolled_coarse_ratio.root");
/////  TH1D* ratio_hist = (TH1D*) file_ratio->Get("data_obs_sr_xl");
/////
/////  for(int i=1; i<=nbins; i++){
/////    //    float perc = (fakes_up_ch1_tmp->GetBinContent(i))/fakes_histo_ch2->GetBinContent(i)      ;
/////    //    std::cout<<"percentage "<<perc<<std::endl;
/////    double perc_up = ratio_hist->GetBinContent(i);
/////    double perc_down = 2 - ratio_hist->GetBinContent(i);
/////    
/////    fakes_bbb_up.SetBinContent(i, bins_sr[i-1].getVal()*perc_up);
/////    fakes_bbb_down.SetBinContent(i, bins_sr[i-1].getVal()*perc_down);
/////
/////  }
/////  
/////  RooDataHist rdh_fakes_bbb_up("fakes_bbbUp_sr","Bkg sys up",vars,&fakes_bbb_up);
/////  wspace.import(rdh_fakes_bbb_up);
/////
/////  RooDataHist rdh_fakes_bbb_down("fakes_bbbDown_sr","Bkg sys down",vars,&fakes_bbb_down);
/////  wspace.import(rdh_fakes_bbb_down);
  
/////  file_ratio->Close();





  fOut->cd();
  wspace.Write();
  
  // Clean up
  fOut->Close();
  fOut->Delete();
    

}

#include <iostream>     // std::cout
#include <algorithm>  // std::max

void examplews(){
  // As usual, load the combine library to get access to the RooParametricHist
  gROOT->SetBatch();
  gSystem->Load("libHiggsAnalysisCombinedLimit.so");


  bool isScale = false;
  //bool isScale = true;

  // Output file and workspace
  TFile *fOut;

  if(isScale){
    fOut = new TFile("datacard/param_tauhad_ws_scale.root","RECREATE");
  }else{
    fOut = new TFile("datacard/param_tauhad_ws.root","RECREATE");
  }
  

  RooWorkspace wspace("wspace","wspace");

  TString prefix = "tauhad";

  for(int year=2016; year < 2019; year++){
    //  for(int year=2018; year < 2019; year++){

    std::cout << "============================" << std::endl;
    std::cout << year << std::endl;
    std::cout << "============================" << std::endl;

    // better to create the bins rather than use the "nbins,min,max" to avoid spurious warning about adding bins with different 
    // ranges in combine - see https://root-forum.cern.ch/t/attempt-to-divide-histograms-with-different-bin-limits/17624/3 for why!

    //////////////////////////////////
    // control region 
    //////////////////////////////////
    TFile *input_file; 

    if(isScale){
      input_file = new TFile("/work/ytakahas/work/analysis/CMSSW_10_2_10/src/rJpsi/anal/combine_simultaneous/tau_rhomass_unrolled_var_scaled.root");
    }else{
      input_file = new TFile("/work/ytakahas/work/analysis/CMSSW_10_2_10/src/rJpsi/anal/combine_simultaneous/tau_rhomass_unrolled_var.root");
    }


    TString target_sr = prefix;
    target_sr += "_sr_";
    target_sr += year;

    TString target_sb = prefix;
    target_sb += "_sb_";
    target_sb += year;

    input_file->cd(target_sb);
    TDirectory* dir_sb = gDirectory;
    TH1D* data_histo_sb = (TH1D*)dir_sb->Get("data_obs");
    TH1D* jpsi_tau_sb = (TH1D*)dir_sb->Get("jpsi_tau");
    TH1D* bc_others_sb = (TH1D*)dir_sb->Get("bc_others");
    TH1D* jpsi_hc_sb = (TH1D*)dir_sb->Get("jpsi_hc");
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

      if (!cl->InheritsFrom("TH1")) continue;
      
      TH1 *h = (TH1*)key_sb->ReadObj();
      
      TString name_string = h->GetName();
      TString name_rdhstring = name_string;
      name_rdhstring += "_";
      name_rdhstring += target_sb; 

      RooDataHist rdh(name_rdhstring, target_sb, vars,h);
      wspace.import(rdh);

    
      if(name_string=="bc_others" || 
	 name_string=="jpsi_hc" || 
	 name_string=="jpsi_tau"){
	
	for(int ibin=1; ibin <= nbins; ibin++){

	  for(int isUp=0; isUp<2; isUp++){
	  
	    TString bbb_string = h->GetName();
	    bbb_string += "_";
	    bbb_string += h->GetName();
	    bbb_string += "_bbb";
	    bbb_string += ibin;
	    bbb_string += target_sb; 
	    bbb_string += (isUp==0) ? "Up" : "Down";
	    bbb_string += "_";
	    bbb_string += target_sb; 
	    //	    bbb_string += "_";
	    //	    bbb_string += target_sb;
	
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

	    RooDataHist rdh_bbb(bbb_string, target_sb, vars,&histo);
	    wspace.import(rdh_bbb);
	  
	  }
	}      
      }
    }
    

    // fakes
    std::vector<RooRealVar> bins; 

    string _str1(target_sb.Data());
    string _str2 = std::to_string(year);

    
    for(int i=1; i<=nbins; i++){
    
      stringstream s;
      s << i;
    
      
      string mystring1 = "bg_bin" + s.str() + "_" + _str1;
      string mystring2 = "Background yield for " + _str2 + " in control region, bin " + s.str();
      
      double val = data_histo_sb->GetBinContent(i) - jpsi_tau_sb->GetBinContent(i) - bc_others_sb->GetBinContent(i) - jpsi_hc_sb->GetBinContent(i);
      double unc = TMath::Sqrt(val);
      
      std::cout << year << ", SB:" << i << ": " << data_histo_sb->GetBinContent(i) << " - " << jpsi_tau_sb->GetBinContent(i) << " - " << bc_others_sb->GetBinContent(i) << " - " << jpsi_hc_sb->GetBinContent(i) << " = "  << val << " " << unc << std::endl;
      
      //    RooRealVar bin(mystring1.c_str(), mystring2.c_str(), val, max(0., val - 5*unc), val + 5*unc);
      RooRealVar bin(mystring1.c_str(), mystring2.c_str(), val, max(0., val - 10*unc), val + 10*unc);
      
      bins.push_back(bin);
    }
    
    RooArgList fakes_sb_bins;
    for(int i=0; i<nbins; i++){
      fakes_sb_bins.add(bins[i]);
    }


    string str_fake = "fakes_" + _str1;
    string str_fake_norm = "fakes_" + _str1 + "_norm";

    string str_fake_des = "Background PDF in control region for " + _str2;
    string str_fake_norm_des = "Total Number of events from background in SB for " + _str2;

    RooParametricHist rph_fakes_sb(str_fake.c_str(), str_fake_des.c_str(),var,fakes_sb_bins, *data_histo_sb);
    RooAddition rph_fakes_sb_norm(str_fake_norm.c_str(), str_fake_norm_des.c_str(),fakes_sb_bins); 
    
    wspace.import(rph_fakes_sb);
    wspace.import(rph_fakes_sb_norm,RooFit::RecycleConflictNodes());



    ///////////////////////////////////////
    /// SIGNAL REGION
    ///////////////////////////////////////


    //TFile *file_sr = new TFile("output/sm_cards/LIMITS/common/rJpsi_sr_1_2018_90.input.root");
    
    input_file->cd();
  
    input_file->cd(target_sr);
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
      name_rdhstring += "_";
      name_rdhstring += target_sr;
      
      //    std::cout << name_string << std::endl;
      
      RooDataHist rdh(name_rdhstring, target_sr, vars,h);
      wspace.import(rdh);
      
      /// bbb uncertainties

      if(name_string=="bc_others" || 
	 name_string=="jpsi_hc" || 
	 name_string=="jpsi_tau"){
	
	for(int ibin=1; ibin <= nbins; ibin++){
	  
	  for(int isUp=0; isUp<2; isUp++){
	    
	    TString bbb_string = h->GetName();
	    bbb_string += "_";
	    bbb_string += h->GetName();
	    bbb_string += "_bbb";
	    bbb_string += ibin;
	    bbb_string += target_sr;
	    bbb_string += (isUp==0) ? "Up" : "Down";	
	    bbb_string += "_";
	    bbb_string += target_sr;
	    //	    bbb_string += "_";
	    //	    bbb_string += target_sr;

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


	    RooDataHist rdh_bbb(bbb_string, target_sr,vars,&histo);
	    wspace.import(rdh_bbb);
	  
	  }
	}       
      }
    }
    
    TH1D* data_histo_sr = (TH1D*)dir_sr->Get("data_obs");
    TH1D* jpsi_tau_sr = (TH1D*)dir_sr->Get("jpsi_tau");
    TH1D* bc_others_sr = (TH1D*)dir_sr->Get("bc_others");
    TH1D* jpsi_hc_sr = (TH1D*)dir_sr->Get("jpsi_hc");
    TH1D* bg_ul_sr = (TH1D*)dir_sr->Get("bg_ul");
    
    
    for(int i=1; i<=nbins; i++){    

      double val = data_histo_sr->GetBinContent(i) - jpsi_tau_sr->GetBinContent(i) -  bc_others_sr->GetBinContent(i) - jpsi_hc_sr->GetBinContent(i);
      
      std::cout << year << ", SR:" << i << ": " << data_histo_sr->GetBinContent(i) << " - " << jpsi_tau_sr->GetBinContent(i) << " - " << bc_others_sr->GetBinContent(i) << " - " << jpsi_hc_sr->GetBinContent(i) << " = " << val << std::endl;

    }



    //  RooRealVar efficiency("efficiency", "efficiency nuisance parameter",0.);
    
    //  RooFormulaVar TF("TF","Trasnfer factor","0.092",RooArgList(efficiency) );
    TFile *bkgcorr_file = new TFile("/work/ytakahas/work/analysis/CMSSW_10_2_10/src/rJpsi/anal/bkgcorr/correction.root");
    TString corr_up = "envelope_up_";
    corr_up += year; 
    TString corr_down = "envelope_down_";
    corr_down += year; 

    TDirectory* dir_corr = gDirectory;
    TH1F* envelope_up = (TH1F*)dir_corr->Get(corr_up);
    TH1F* envelope_down = (TH1F*)dir_corr->Get(corr_down);






//    std::vector<RooRealVar> bins_up;
//    std::vector<RooRealVar> bins_down;
//
//    for(int i=1; i<=nbins; i++){
//    
//      stringstream s;
//      s << i;
//    
//      string mystring1_up = "envelope_bin" + s.str() + "_" + _str1 + ", up";
//      string mystring2_up = "envelope for " + _str2 + " in control region, bin " + s.str() + ", up";
//      
//      double val_up = envelope_up->GetBinContent(i);
//      RooRealVar bin_up(mystring1_up.c_str(), mystring2_up.c_str(), val_up);
//      
//      bins_up.push_back(bin_up);
//
//      string mystring1_down = "envelope_bin" + s.str() + "_" + _str1 + ", down";
//      string mystring2_down = "envelope for " + _str2 + " in control region, bin " + s.str() + ", down";
//      
//      double val_down = envelope_down->GetBinContent(i);
//      RooRealVar bin_down(mystring1_down.c_str(), mystring2_down.c_str(), val_down);
//      
//      bins_down.push_back(bin_down);
//
//
//    }







    Float_t ratio = bg_ul_sr->Integral()/bg_ul_sb->Integral();
    std::cout << "============================="<< std::endl;
    std::cout << "ratio=" << ratio << std::endl;
    std::cout << "============================="<< std::endl;

    string str_tf1 = "TF_" + _str2;
    string str_tf2 = "Transfer Factor for " + _str2;
    
    RooRealVar TF(str_tf1.c_str(), str_tf2.c_str(), ratio); 

    string _str3(target_sr.Data());

    std::vector<RooFormulaVar> bins_sr; 
    std::vector<RooFormulaVar> bins_sr_up; 
    std::vector<RooFormulaVar> bins_sr_down; 
    for(int i=1; i<=nbins; i++){
      stringstream s;
      s << i;

      string mystring1 = "bg_bin" + s.str() + "_" + _str3;
      string mystring2 = "Background yield for " + _str2 + " in signal region, bin " + s.str();
      
      RooFormulaVar bin(mystring1.c_str(),mystring2.c_str()," @0*@1",RooArgList(TF, bins[i-1]));
      bins_sr.push_back(bin);
      
//      //// up variations ...
//
//      string mystring1_up = "bg_bin" + s.str() + "_" + _str3 + "_up";
//      string mystring2_up = "Background yield for " + _str2 + " in signal region, bin " + s.str() + ", up variation";
//      
//      RooFormulaVar bin_up(mystring1_up.c_str(),mystring2_up.c_str()," @0*@1*@2",RooArgList(TF, bins[i-1], bins_up[i-1]));
//      bins_sr_up.push_back(bin_up);
//
//      //// down variations ...
//
//      string mystring1_down = "bg_bin" + s.str() + "_" + _str3 + "_down";
//      string mystring2_down = "Background yield for " + _str2 + " in signal region, bin " + s.str() + ", down variation";
//      
//      RooFormulaVar bin_down(mystring1_down.c_str(),mystring2_down.c_str()," @0*@1*@2",RooArgList(TF, bins[i-1], bins_down[i-1]));
//      bins_sr_down.push_back(bin_down);

    }

    RooArgList fakes_sr_bins;
    for(int i=0; i<nbins; i++){
      fakes_sr_bins.add(bins_sr[i]);
    }

    string _str_fake = "fakes_" + _str3;
    string _str_fake_norm = "fakes_" + _str3 + "_norm";

    string _str_fake_des = "Background PDF in signal region for " + _str2;
    string _str_fake_norm_des = "Total Number of events from background in signal region for " + _str2;

    RooParametricHist rph_fakes_sr(_str_fake.c_str(), _str_fake_des.c_str(),var,fakes_sr_bins, *data_histo_sr);
    RooAddition rph_fakes_sr_norm(_str_fake_norm.c_str(), _str_fake_norm_des.c_str(),fakes_sr_bins); 
    
    wspace.import(rph_fakes_sr);
    wspace.import(rph_fakes_sr_norm,RooFit::RecycleConflictNodes());



//    RooArgList fakes_sr_bins_up;
//    for(int i=0; i<nbins; i++){
//      fakes_sr_bins_up.add(bins_sr_up[i]);
//    }
//
//
//    string _str_fake_up = "fakes_fakeshape_" + _str2 + "Up_" + _str3;
//    string _str_fake_norm_up = "fakes_fakeshape_" + _str2 + "Up_" + _str3 + "_norm";
//
//    //    string _str_fake_up = "fakes_" + _str3 + "_up";
//    //    string _str_fake_norm_up = "fakes_" + _str3 + "_norm_up";
//
//    string _str_fake_up = "fakes_fakeshape_" + _str2 + "Up_" + _str3;
//    string _str_fake_des_up = "Background PDF in signal region for " + _str2 + ", up variation";
//    string _str_fake_norm_des_up = "Total Number of events from background in signal region for " + _str2 + ", up variation";
//
//    RooParametricHist rph_fakes_sr_up(_str_fake_up.c_str(), _str_fake_des_up.c_str(),var,fakes_sr_bins_up, *data_histo_sr);
//    RooAddition rph_fakes_sr_norm_up(_str_fake_norm_up.c_str(), _str_fake_norm_des_up.c_str(),fakes_sr_bins_up); 
//    
//    wspace.import(rph_fakes_sr_up);
//    wspace.import(rph_fakes_sr_norm_up, RooFit::RecycleConflictNodes());
//
//
//
//
//    RooArgList fakes_sr_bins_down;
//    for(int i=0; i<nbins; i++){
//      fakes_sr_bins_down.add(bins_sr_down[i]);
//    }
//
//
//    string _str_fake_down = "fakes_fakeshape_" + _str2 + "Down_" + _str3;
//    string _str_fake_norm_down = "fakes_fakeshape_" + _str2 + "Down_" + _str3 + "_norm";
//
//    string _str_fake_down = "fakes_fakeshape_" + _str2 + "Down_" + _str3;
//    string _str_fake_des_down = "Background PDF in signal region for " + _str2 + ", down variation";
//    string _str_fake_norm_des_down = "Total Number of events from background in signal region for " + _str2 + ", down variation";
//
//    RooParametricHist rph_fakes_sr_down(_str_fake_down.c_str(), _str_fake_des_down.c_str(),var,fakes_sr_bins_down, *data_histo_sr);
//    RooAddition rph_fakes_sr_norm_down(_str_fake_norm_down.c_str(), _str_fake_norm_des_down.c_str(),fakes_sr_bins_down); 
//    
//    wspace.import(rph_fakes_sr_down);
//    wspace.import(rph_fakes_sr_norm_down, RooFit::RecycleConflictNodes());




//    TH1F background_up("tbkg_CR_JESUp","",nbins,xbins);
//    background_up.SetBinContent(1,CRbin1.getVal()*1.01);
//    background_up.SetBinContent(2,CRbin2.getVal()*1.02);
//    background_up.SetBinContent(3,CRbin3.getVal()*1.03);
//    background_up.SetBinContent(4,CRbin4.getVal()*1.04);
//    RooDataHist bkg_CRhist_sysUp("bkg_CR_JESUp","Bkg sys up",vars,&background_up);
//    wspace.import(bkg_CRhist_sysUp);






    ////////////////////////////////////////
    // derive shape variations for the fakes
    ////////////////////////////////////////



    string fakename_up = "fakes_paramUp_" + _str2;
    string fakename_down = "fakes_paramDown_" + _str2;

    TH1F fakes_param_up(fakename_up.c_str(), "", nbins, xmin, xmax);
    TH1F fakes_param_down(fakename_down.c_str(),"", nbins, xmin, xmax);
    
    for(int i=1; i<=nbins; i++){
      
      fakes_param_up.SetBinContent(i, bins_sr[i-1].getVal()*envelope_up->GetBinContent(i));
      fakes_param_down.SetBinContent(i, bins_sr[i-1].getVal()*envelope_down->GetBinContent(i));
      
    }
    string _str_fake_up = "fakes_fakeshape_" + _str2 + "Up_" + _str3;
    string _str_fake_des_up = "Background PDF in signal region for " + _str2 + ", up variation";
    
    RooDataHist rdh_fakes_param_up(_str_fake_up.c_str(), _str_fake_des_up.c_str(), vars,&fakes_param_up);
    wspace.import(rdh_fakes_param_up);

    string _str_fake_down = "fakes_fakeshape_" + _str2 + "Down_" + _str3;
    string _str_fake_des_down = "Background PDF in signal region for " + _str2 + ", down variation";
    
    RooDataHist rdh_fakes_param_down(_str_fake_down.c_str(), _str_fake_des_down.c_str(), vars,&fakes_param_down);
    wspace.import(rdh_fakes_param_down);

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



  }

  fOut->cd();
  wspace.Write();
  
  // Clean up
  fOut->Close();
  fOut->Delete();
    

}

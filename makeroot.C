#include <iostream>
#include <fstream>
#include <TTree.h>
#include <TString.h>
#include <TFile.h>
#include <TGraph.h>
#include <TH1D.h>

using namespace std;

vector<int> load(TString name){
  ifstream ifs(name);
  if(ifs.fail()){

    cout<<"not found"<<endl;
  
      }
  vector<int> vec;
  int val=0;
  //if(!ifs)cout<<"not found file"<<endl;
  while(ifs >> val){
    vec.push_back(val);
  }
  return vec;
  
            }


TString LoadBase(){


  ifstream ifs("./basename.txt");

  TString name;


  ifs >> name;

  return name;

  
}


//#include "dataname.h"


int makeroot(){
  //  TString base ="../data/CS2000/20210823142829";
  gStyle->SetOptLogy(1);
  gStyle->SetOptLogz(1);
   TString base = LoadBase();
   cout<<"Loading  "<<base+".jpg"<<endl;

   TString hue_data        = "./hue.txt";
   TString saturation_data = "./saturation.txt";
   TString gray_data       = "./gray.txt";

   TString blue_data       = "./blue.txt";
   TString green_data      = "./green.txt";
   TString red_data        = "./red.txt";

   vector<int>hue_vec        = load(hue_data);
   vector<int>saturation_vec = load(saturation_data);
   vector<int>gray_vec       = load(gray_data);

   vector<int>blue_vec       = load(blue_data);
   vector<int>green_vec      = load(green_data);
   vector<int>red_vec        = load(red_data);

   TString filename   = base+".root";
   TFile* file        = new TFile(filename,"recreate");
   TTree* tree        = new TTree("HSV","HSV");

   TH1D*  hue_hist         = new TH1D("hue_hist","hue_hist",180,0,180);
   TH1D*  saturation_hist  = new TH1D("saturation_hist","saturation_hist",255,0,255);
   TH1D*  gray_hist        = new TH1D("gray_hist","gray_hist",255,0,255);



   
   TH2D* hue_gray          = new TH2D("HueVsGray","Hue VS Gray",180,0,180,255,0,255);
   TH2D* hue_satu          = new TH2D("HueVsSatu","Hue VS Satu",180,0,180,255,0,255);
   TH2D* satu_gray          = new TH2D("SatuVsGray","Hue VS Satu",255,0,255,255,0,255);


   //   TH2D* hue_gray          = new TH2D("Hue VS Gray","Hue VS Gray",180,0,180,255,0,255);


   TH1D*  blue_hist        = new TH1D("blue_hist","blue_hist",256,0,255);
   TH1D*  green_hist       = new TH1D("green_hist","green_hist",256,0,255);
   TH1D*  red_hist         = new TH1D("red_hist","red_hist",256,0,255);

   

   TGraph* hue_gr          = new TGraph();
   TGraph* saturation_gr   = new TGraph();
   TGraph* gray_gr         = new TGraph();

   
   
   hue_gr        -> SetTitle("hue;number;Hue-value");
   saturation_gr -> SetTitle("saturation;number;Saturation-value");
   gray_gr       -> SetTitle("gray;number;gray-value");
   
   
   int hue_val,saturation_val,gray_val,blue_val,green_val,red_val,row,col=0;

   const int row_max = 5432;
   const int col_max = 3648;

   tree -> Branch("Hue",&hue_val,"hue_val/I");  
   tree -> Branch("Saturation",&saturation_val,"hue_saturation_val/I");
   tree -> Branch("Gray",&gray_val,"gray_val/I");  
   tree -> Branch("Row",&row,"row/I");  
   tree -> Branch("Column",&col,"col/I");  

   cout<<"====Fill value===="<<endl;

   for(int num =0 ; num<hue_vec.size();num++){

     
     hue_val        = hue_vec[num];
     saturation_val = saturation_vec[num];
     gray_val       = gray_vec[num];

     blue_val       = blue_vec[num];
     green_val      = green_vec[num];
     red_val        = red_vec[num];


     row            = num/col_max;
     col            = num%col_max;
   
     tree->Fill();

     hue_hist        -> Fill(hue_val);
     saturation_hist -> Fill(saturation_val);
     gray_hist       -> Fill(gray_val);


     hue_satu        -> Fill(hue_val,saturation_val);
     hue_gray        -> Fill(hue_val,gray_val);
     satu_gray        -> Fill(saturation_val,gray_val);
     
     blue_hist       -> Fill(blue_val);
     green_hist      -> Fill(green_val);
     red_hist        -> Fill(red_val);
     
     hue_gr        ->SetPoint(num,num,hue_val);
     saturation_gr ->SetPoint(num,num,saturation_val);
     gray_gr       ->SetPoint(num,num,gray_val);

   }

   cout<<"====saving histgram & graph===="<<endl;
   
   // tree->Write();
   hue_hist        -> Write();
   saturation_hist -> Write();
   gray_hist       -> Write();

   hue_gray        -> Write();
   hue_satu        -> Write();
   satu_gray       -> Write();
   blue_hist       -> Write();
   green_hist      -> Write();
   red_hist        -> Write();
   
   hue_gr          -> Write();
   saturation_gr   -> Write();
   gray_gr         -> Write();



   auto cc = new TCanvas("cc","cc",800,600);
   cc -> SetBottomMargin(0.15);
   cc -> SetLeftMargin(0.15);


   hue_hist        -> GetXaxis() -> SetTitleSize(0.05);
   saturation_hist -> GetXaxis() -> SetTitleSize(0.05);
   gray_hist       -> GetXaxis() -> SetTitleSize(0.05);
   hue_gray        -> GetXaxis() -> SetTitleSize(0.05);
   hue_satu        -> GetXaxis() -> SetTitleSize(0.05);
   blue_hist       -> GetXaxis() -> SetTitleSize(0.05);
   green_hist      -> GetXaxis() -> SetTitleSize(0.05);
   red_hist        -> GetXaxis() -> SetTitleSize(0.05);
   
   cc->Print(base+".pdf[");

   hue_hist -> Draw();
   cc->Print(base+".pdf");
   
   saturation_hist -> Draw();
   cc->Print(base+".pdf");
   
   gray_hist -> Draw();
   cc->Print(base+".pdf");
   
   hue_gray -> Draw("colz");
   cc->Print(base+".pdf");
   
   hue_satu -> Draw("colz");
   cc->Print(base+".pdf");
   
   blue_hist -> Draw();
   cc->Print(base+".pdf");
   
   green_hist -> Draw();
   cc->Print(base+".pdf");
   
   red_hist -> Draw();
   cc->Print(base+".pdf");
   
   cc->Print(base+".pdf]");

   
   
   file->Close();
      



   return 0;
}




int main() {
  makeroot();
  return 0;
}


/*
vector<int>load(TString name){

  ifstream ifs(name);

  vector<int> vec;
  int val;

  if(!ifs)cout<<"not found file"<<endl;


  while(ifs>>val){

    vec.push_back(val);

    
  }

  return vec;

  
}

*/


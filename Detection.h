#ifndef BEC_SOFTWARE_DETECTION_H
#define BEC_SOFTWARE_DETECTION_H

#include <opencv2/opencv.hpp>
#include <iostream>
#include <fstream>
#include <vector>
#include <math.h>
#include <string>
#include <time.h>

using namespace std;

void Cycle(vector<int> &v_input, vector<int> &v_whitelength,vector<int> &v_whitecenter,vector<int> &v_blacklength,vector<int> &v_blackcenter){

  ///counting White Pixel


  
  int  size    = v_input.size();
  int WhitePixelStartIndex = 0;
  int WhitePixelEndIndex   = 0;


  for(int i = 0; i < size ; i++){// search start white pixel

    if(v_input[i] == 255 ){

      WhitePixelStartIndex = i;
      break;
      
    }// if v_input
        
  }// for int i = 0 ;

  


  for (int i = (size-1) ; i > 1 ; i-- ){// search end white pixel

    
    if(v_input[i] == 255 ){
      WhitePixelEndIndex = i;
      break;
      
    }
    
    
  } // for int i = (size-1) ; i < 1 ; i-- 



  int WhiteLength = 0;
  int BlackLength = 0;
  bool WhiteTurn  = true;
  bool BlackTurn  = false;

  
  for(int i = WhitePixelStartIndex; i < (WhitePixelEndIndex+1) ; i++){

    bool WhitePixel = (v_input[i] == 255);
    bool BlackPixel = (v_input[i] ==   0);
    
    if(WhitePixel){
      
      WhiteLength++;
    }//if
    

    if(BlackPixel){

      BlackLength++;
      
    } // else


    //   cout << "white Length=" << WhiteLength << "\t" << "black length=" << BlackLength << endl; 

    if( (WhiteTurn) && ( BlackPixel )  ){ //Switching white pixel to black pixel

      v_whitelength.push_back( WhiteLength );
      v_whitecenter.push_back(i); // easy
      WhiteLength = 0; // init

      WhiteTurn = false;
      BlackTurn = true;
      
      
    }//  if( (WhiteTurn) && ( BlackPixel )  )




    if( (BlackTurn) && (WhitePixel) ){

      v_blacklength.push_back( BlackLength );
      v_blackcenter.push_back(i); // easy

      BlackLength = 0; // init
      WhiteTurn = true;
      BlackTurn = false;
      
      
    }// if( (BlackTurn) && (WhitePixel) )
    
    
    
  }// for(int i = WhitePixelStartIndex; i < (WhitePixelEndIndex+1) ; i++)




  
}//void Cycle






void Judge(vector<int> &v_input, vector<int> &v_recordX,vector<int> &v_recordY,vector<int> &v_center,int row,int times){



  


  // Calculate Mean

  double size = v_input.size();
  double sum  = 0;

  for(int i =0;i<size;i++){

    sum += v_input[i];
    
    
  }//for int i=0;


  double mean = sum/size;



  // calculate Sigma


  double SumSquares = 0;

  for (int i=0;i<size;i++){


    SumSquares += (v_input[i]-mean)*(v_input[i]-mean);
    
  }//for int i=0;

  double variance = SumSquares/size;

  double sigma    = sqrt(variance); 



  // Judge


  double BottomLimit = mean - (times * sigma);// e.g 3 sigma
  double UpperLimit  = mean + (times * sigma);// e.g 3 sigma

  for(int i =0;i<size;i++){


    bool CUT = (v_input[i] < BottomLimit)||( v_input[i] > UpperLimit);

    if(CUT){

      int BadPixelIndex = v_center[i];
      v_recordX.push_back(BadPixelIndex);
      v_recordY.push_back(row);

      
      
    }//if CUT
    

    
  }//for int i=0
  

  
}//void Judge


int Binary(int val,int thr){


  if(val > thr ){

    return 255;
    
  }//if

  else{

    return 0;
  }
  

  

} // int Binary





void dilation(vector<int> &v_input){

  vector<int> v_index; // record the index of the white pixel. 

  int WhitePixel = 255;

  for(int i =0;i<v_input.size();i++){


    if(WhitePixel == v_input[i]){

      v_index.push_back(i);
      
    }//if White
    
       
  }// for int i = 0;



  for(int i = 0;i<v_index.size();i++){

    
    if(v_index[i] == 0){ // start pixel

      v_input[v_index[i]+1]  = WhitePixel;
      
    }// if v_index[i] == 0

    else if (v_index[i] == (v_input.size()-1)){ // end  pixel

      v_input[v_index[i]-1]  = WhitePixel;

      
    }// else if v_index[i] == (v_input.size-1)
    
    else{

      v_input[v_index[i]+1]  = WhitePixel;
      v_input[v_index[i]-1]  = WhitePixel;
      
    }//else
    
    
  }//for int i = 0; i<v_index.size()

  
  


  
}// void dilation


void erosion(vector<int> &v_input){

  vector<int> v_index; // record the index of the Black pixel. 

  int BlackPixel = 0;

  for(int i =0;i<v_input.size();i++){


    if(BlackPixel == v_input[i]){

      v_index.push_back(i);
      
    }//if White
    
       
  }// for int i = 0;



  for(int i = 0;i<v_index.size();i++){

    
    if(v_index[i] == 0){ // start pixel

      v_input[v_index[i]+1]  = BlackPixel;
      
    }// if v_index[i] == 0

    else if (v_index[i] == (v_input.size()-1)){ // end  pixel

      v_input[v_index[i]-1] = BlackPixel;

      
    }// else if v_index[i] == (v_input.size-1)
    
    else{

      v_input[v_index[i]+1]  = BlackPixel;
      v_input[v_index[i]-1]  = BlackPixel;
      
    }//else
    
    
  }//for int i = 0; i<v_index.size()

  
  


  
}// void dilation




void Reverse(vector< int > &v_input){

  for (int i = 0 ; i < v_input.size() ;i++){

    if(v_input[i] == 255 ){ // if white pixel

      v_input[i] = 0; // black
      
    }// if

    else{ // is black

      v_input[i] = 255; // black

      
      
    }//else
    
  }// for

  
  
  
}// Reverse






void Detection(){

  
  // define varable

  int val   = 0;
  int num   = 0;
  int thr   = 70;
  float times = 5;
  string dataname = "name";
  int const ColSize = 3648;
  vector <int> v_strip;
  vector <int> v_whitelength;
  vector <int> v_whitecenter;

  vector <int> v_blacklength;
  vector <int> v_blackcenter;

  vector <int> v_WhiteRecordX;
  vector <int> v_WhiteRecordY;

  vector <int> v_BlackRecordX;
  vector <int> v_BlackRecordY;


  string outputname;


  // read the photoname and parameter


  ifstream ifs("./setting.txt");

  ifs >> dataname >> thr >> times >> outputname;




  

  // define openCV Mat Class


  cv::Mat img;
  cv::Mat hsv;

  // read the photo
  cout << "Input" << "\t" << dataname << endl;
  img = cv::imread(dataname);
  

  // rotate

  if(img.rows == 3648 ){

    cv::rotate(img,img,cv::ROTATE_90_COUNTERCLOCKWISE ) ;
    cv::imwrite(dataname,img);
    img = cv::imread(dataname);

    
  }// if hsv.rows == 


  // convert BGR to HSV.
  cv::cvtColor(img,hsv,cv::COLOR_BGR2HSV);

  // calculate total pixel number

  
  double TotalPixelNum = (hsv.rows)*(hsv.cols);
  
  

  // Running pixel

 
  
  while(num < TotalPixelNum){

    int col = num % ColSize;
    int row=  num / ColSize;
    num++;
    
    if((row%2) == 1){
      
        continue;
    }//if
    
    //  cout << "row=" << row << endl; 

    
    cv::Vec3b* p_val = hsv.ptr<cv::Vec3b>(row);
    cv::Vec3b hsv_3b  = p_val[col];


    int satu = (int)hsv_3b[1];
    
    // push back pixel value
    val = Binary(satu,thr);    
    v_strip.push_back(val);


    bool STRIP = (v_strip.size() == ColSize);
    
    if(STRIP){

      
      //dilation(v_strip); // noise cut
      //erosion(v_strip); // noise cut

      Cycle(v_strip,v_whitelength,v_whitecenter,v_blacklength,v_blackcenter); // count White & Black line pixel
      Judge(v_whitelength,v_WhiteRecordX,v_WhiteRecordY,v_whitecenter,row,times); // write out white Bad pixel
      Judge(v_blacklength,v_BlackRecordX,v_BlackRecordY,v_blackcenter,row,times); // write out Black Bad pixel

      
      v_strip.clear();  // init

      v_whitelength.clear(); // init
      v_whitecenter.clear(); // init

      v_blacklength.clear(); // init
      v_blackcenter.clear(); // init
      //      break;

    }//if STRIP
       
    
    
  }//while


  //marking
  
  for(int i =0;i < v_WhiteRecordX.size(); i++){

    cv::circle(img,cv::Point(v_WhiteRecordX[i],v_WhiteRecordY[i]),75,cv::Scalar(0,0,255) ,5);
    
  }// for int i
  
  
  for(int i =0;i < v_BlackRecordX.size(); i++){

    cv::circle(img,cv::Point(v_BlackRecordX[i],v_BlackRecordY[i]),100,cv::Scalar(0,255,0) ,5);
    
  }// for int i
  
  

  // output

  //  string outputdir = "/Users/hikaru/Desktop/BEX/software/output/";
  cv::rotate(img, img, cv::ROTATE_90_CLOCKWISE);
  cv::imwrite(outputname,img);
  cout <<"OutPut"<<"\t" <<outputname << endl;

}   // void Detrction

#endif // BEC_SOFTWARE_DETECTION_H

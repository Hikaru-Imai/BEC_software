#ifndef BEC_SOFTWARE_DETECTION_H
#define BEC_SOFTWARE_DETECTION_H

#include <opencv2/opencv.hpp>
#include <iostream>
#include <fstream>
#include <vector>
#include <math.h>
#include <string>
using namespace std;

void Cycle(vector<int> &v_input, vector<int> &v_output,vector<int> &v_center,int mode){

  ///counting White Pixel


  
  int size = v_input.size();

  bool veto = true;
  bool trigger = false;
  int count =0;

  int start,end = 0;

  if( mode == 255){

    
  
  for(int i =0;i<size;i++){


    if((veto) &&(v_input[i]==255)){
      
      trigger = true;
      veto = false;
      start = i;
    
    } // if veto



    if((trigger) && (v_input[i]) == 255){

      count++;
      

    }//if trigger


    
    
    if((trigger) && (v_input[i]) == 0){

      veto  = true;
      trigger = false;
      end = i;
      //      int CenterPixel = (end+start)/2;
      int CenterPixel = end;
      v_output.push_back(count);
      v_center.push_back(CenterPixel);
      
      count = 0;

    }//if trigger
  }

  } /// if mode
 
    
  if( mode == 0){

    
  
  for(int i =0;i<size;i++){


    if((veto) &&(v_input[i]==0)){
      
      trigger = true;
      veto = false;
      start = i;
    
    } // if veto



    if((trigger) && (v_input[i]) == 0){

      count++;
      

    }//if trigger


    
    
    if((trigger) && (v_input[i]) == 255){

      veto  = true;
      trigger = false;
      end = i;
      //      int CenterPixel = (end+start)/2;
      int CenterPixel = end;
      v_output.push_back(count);
      v_center.push_back(CenterPixel);
      
      count = 0;

    }//if trigger


 
    
  }//for
  
  } /// if mode
  





  
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
  int times = 5;
  string dataname = "name";
  int const ColSize = 3648;
  vector <int> v_strip;
  vector <int> v_length;
  vector <int> v_center;

  vector <int> v_recordX;
  vector <int> v_recordY;


  string outputname;


  // read the photoname and parameter


  ifstream ifs("./setting.txt");

  ifs >> dataname >> thr >> times >> outputname;




  

  // define openCV Mat Class


  cv::Mat img;
  cv::Mat hsv;

  // read the photo
  
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

    if(row%2 == 0){
      continue;
    }//if
    
    //  cout << "row=" << row << endl; 
    int satu = hsv.at<cv::Vec3b>(row,col)[1]; // 0 ,1 ,2 means hue,saturation,gray

    
    // push back pixel value
    val = Binary(satu,thr);    
    v_strip.push_back(val);


    bool STRIP = (v_strip.size() == ColSize);
    
    if(STRIP){

      
      dilation(v_strip);
      erosion(v_strip);

      Cycle(v_strip,v_length,v_center,255); // count White line pixel
      Judge(v_length,v_recordX,v_recordY,v_center,row,times); // write out Bad pixel

      v_length.clear(); // inti
      v_center.clear(); // init

      Reverse(v_strip); // white -> black , black -> white

      Cycle(v_strip,v_length,v_center,0); // count White line pixel
      Judge(v_length,v_recordX,v_recordY,v_center,row,times); // write out Bad pixel
      

      
      v_strip.clear();  // init
      v_length.clear(); // inti
      v_center.clear(); // init


    }//if STRIP
       
    
    
  }//while




  

  // Write out


  ofstream ofs("BadPixel.txt");

  for(int i =0;i<v_recordX.size();i++){

    ofs<<v_recordX[i]<<"\t"<<v_recordY[i]<<endl;
    //cout<<v_recordX[i]<<"\t"<<v_recordY[i]<<endl;
  }//for int i=0;



  //marking

  for(int i =0;i < v_recordX.size(); i++){

    cv::circle(img,cv::Point(v_recordX[i],v_recordY[i]),50,cv::Scalar(255,255,0) ,5);
    
    
  }// for int i


  // output

  //  string outputdir = "/Users/hikaru/Desktop/BEX/software/output/";


  cout << outputname << endl;

  cv::imwrite(outputname,img);
  

  

}   // void Detrction

#endif // BEC_SOFTWARE_DETECTION_H

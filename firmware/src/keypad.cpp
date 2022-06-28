#include <Arduino.h>
#include "globalV.h"
using namespace std;

// other vars
long duration;
int distance;

//constants
const String keys[4][4] = {{"1","2","3","A"},{"4","5","6","B"},{"7","8","9","C"},{"*","0","#","D"}};
int count = 0;
void keypadSetup() {
  //Pins Setup
  pinMode(R1,OUTPUT);digitalWrite(R1,HIGH);
  pinMode(R2,OUTPUT);digitalWrite(R2,HIGH);
  pinMode(R3,OUTPUT);digitalWrite(R3,HIGH);
  pinMode(R4,OUTPUT);digitalWrite(R4,HIGH);
  pinMode(C1,INPUT);
  pinMode(C2,INPUT);
  pinMode(C3,INPUT);
  pinMode(C4,INPUT);
  //Serial Monitor Setup
  Serial.begin(9600);
}
/*
*START KEYPAD
*/
int scanCol(){
  int c1=digitalRead(C1);
  int c2=digitalRead(C2);
  int c3=digitalRead(C3);
  int c4=digitalRead(C4);
  if (c1){
    return 1;
  }else if (c2){
    return 2;
  }else if (c3){
    return 3;
  }else if (c4){
    return 4;
  }else{
    return 0;
  }  
}


int scanRow(int col){
    int activeCol;
    if (col>0){
        if(col==1) activeCol=C1;
        if(col==2) activeCol=C2;
        if(col==3) activeCol=C3;
        if(col==4) activeCol=C4;
        digitalWrite(R1,LOW);
        if(!digitalRead(activeCol)) return 1;
        digitalWrite(R2,LOW);
        if(!digitalRead(activeCol)) return 2;
        digitalWrite(R3,LOW);
        if(!digitalRead(activeCol)) return 3;
        digitalWrite(R4,LOW);
        if(!digitalRead(activeCol)) return 4;
    }else{
        return 0;
    }
}

String keypad(){
  int col = scanCol();
  int row = scanRow(col);
  Serial.print("row: ");
  Serial.print(row);
  Serial.print(" col: ");
  Serial.println(col);
  digitalWrite(R1,HIGH);
  digitalWrite(R2,HIGH);
  digitalWrite(R3,HIGH);
  digitalWrite(R4,HIGH);
  if(col>0&&row>0){
      return keys[row-1][col-1];
  }else{
    return "null";
  }
}

/*
*END KEYPAD
*/
void keyScanner() {
  //Keypad
  String letter=keypad();
  Serial.print("You enterd: ");
  Serial.println(letter);
}
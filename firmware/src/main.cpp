#include <Arduino.h>
#include <LiquidCrystal_I2C.h>

#include "globalV.h"
#include "rfid.h"
#include "keypad.h"
/*
  TODO
RFID and Keypad
*/
void setup() {
  Serial.begin(9600);
  pinMode(blinkPin,OUTPUT);
  setupRFID();
}

void loop() {
  //blinkTest();
  scanCard();
}

void blinkTest(){
  digitalWrite(blinkPin,HIGH);
  delay(1000);
  digitalWrite(blinkPin,LOW);
  delay(1000);
}
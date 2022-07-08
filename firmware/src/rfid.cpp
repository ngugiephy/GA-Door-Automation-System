#include <Arduino.h>
#include "globalV.h"

#include <SPI.h>
#include <MFRC522.h>
#include <LiquidCrystal_I2C.h>

MFRC522 mfrc522(SS_PIN, RST_PIN);  // Create MFRC522 instance
LiquidCrystal_I2C lcd(0x27,20,4);  // set the LCD address to 0x27 for a 16 chars and 2 line display

void setupRFID()
{
  pinMode(red, OUTPUT);
  pinMode(blue, OUTPUT);
  pinMode(green, OUTPUT);
  pinMode(buzzer, OUTPUT);
  pinMode(locker, OUTPUT);
  SPI.begin(); 
  lcd.init();
  lcd.backlight();
  lcd.begin(16,2);
  lcd.clear(); 
  lcd.print("Scan Card!");
  mfrc522.PCD_Init();   
  Serial.println("Approximate your card to the reader...");
  Serial.println();

}

void scanCard()
{
  if ( ! mfrc522.PICC_IsNewCardPresent()) 
  {
    return;
  }
  
  if ( ! mfrc522.PICC_ReadCardSerial()) 
  {
    return;
  }

  lcd.begin(16,2);
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("Scan card");
  Serial.print("UID tag :");
  String content= "";
  byte letter;
  for (byte i = 0; i < mfrc522.uid.size; i++) 
  {
     Serial.print(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " ");
     Serial.print(mfrc522.uid.uidByte[i], HEX);
     content.concat(String(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " "));
     content.concat(String(mfrc522.uid.uidByte[i], HEX));
  }
  Serial.println();
  Serial.print("Message : ");
  content.toUpperCase();
  lcd.print("Scan Card");    
  digitalWrite(blue, HIGH); 

  if (content.substring(1) == "73 78 D3 1C") // Make sure you change this with your own UID number
  {
    Serial.println("Authorised access");
    digitalWrite(blue, LOW);
    digitalWrite(green, HIGH);
    digitalWrite(buzzer, HIGH);    
    lcd.clear();
    lcd.setCursor(0,0);
    lcd.println("Authorised access");    
    digitalWrite(locker, LOW);
    Serial.println();
    delay(1000);
    digitalWrite(green, LOW);
    digitalWrite(blue, HIGH);
    digitalWrite(buzzer, LOW);
    delay(5000);
    digitalWrite(locker, HIGH);
    delay(2500);
   
        
  }
 
 else   {
    Serial.println(" Access denied");
    digitalWrite(blue, LOW);
    digitalWrite(red, HIGH);
    lcd.clear();
    lcd.setCursor(0,0);
    lcd.println("Access denied");
    digitalWrite(locker, HIGH);
    delay(1000);
    digitalWrite(red, LOW);
    digitalWrite(blue, HIGH);
    delay(2500);
    
  }
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.println("Scan Card");
}
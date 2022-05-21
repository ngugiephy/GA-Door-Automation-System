#include <LiquidCrystal_I2C.h>
#include <Wire.h>
#include <EEPROM.h>

#include <SPI.h>
#include <MFRC522.h>
 
#define SS_PIN 10
#define RST_PIN 9

#define red 5
#define blue 3
#define green 4

#define lock 6
#define buzzer 2

MFRC522 mfrc522(SS_PIN, RST_PIN);  
LiquidCrystal_I2C lcd(0x27, 16, 2);

 
void setup() 
{
  Serial.begin(9600);  
  pinMode(red, OUTPUT);
  pinMode(blue, OUTPUT);
  pinMode(green, OUTPUT);
  pinMode(buzzer, OUTPUT);
  pinMode(lock, OUTPUT);
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
void loop() 
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
    digitalWrite(lock, LOW);
    Serial.println();
    delay(1000);
    digitalWrite(green, LOW);
    digitalWrite(blue, HIGH);
    digitalWrite(buzzer, LOW);
    delay(5000);
    digitalWrite(lock, HIGH);
    delay(2500);
   
        
  }
 
 else   {
    Serial.println(" Access denied");
    digitalWrite(blue, LOW);
    digitalWrite(red, HIGH);
    lcd.clear();
    lcd.setCursor(0,0);
    lcd.println("Access denied");
    digitalWrite(lock, HIGH);
    delay(1000);
    digitalWrite(red, LOW);
    digitalWrite(blue, HIGH);
    delay(2500);
    
  }
lcd.clear();
lcd.setCursor(0,0);
lcd.println("Scan Card");
}
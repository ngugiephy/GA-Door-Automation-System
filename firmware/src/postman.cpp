#include <Arduino.h>
#include <string>

#include "globalV.h"

#include <WiFi.h>
#include <WiFiClient.h>
#include <WiFiAP.h>

/* 
Gearbox Members
Members@Gearbox
Happy_home
JMongare@123
FABIAN
Gisore@123
*/

const char* ssid     = "FABIAN";
const char* password = "Gisore@123";
//AP credentials
const char* mySSID = "ESP32-AP";
const char* myPassword = "esp32wifi";

WiFiServer server(80);

bool APflag = false;
void APsetup(){
  WiFi.softAP(mySSID, myPassword);
  IPAddress myIP = WiFi.softAPIP();
  Serial.println();
  Serial.print("AP IP address: ");
  Serial.println(myIP);
  APflag = true;
}

void serverSetup(){
    //start by connecting to a WiFi network

    Serial.println();
    Serial.println();
    Serial.print("Connecting to ");
    Serial.println(ssid);

    WiFi.begin(ssid, password);

    int countdown = 10; //countdown to switch to AP

    while (WiFi.status() != WL_CONNECTED) {
        delay(1000);
        Serial.print(".");
        if (countdown==0){ //switch to AP
          APsetup();
          break;
        }
        countdown-=1;
    }

    if (!APflag){
      Serial.println("");
      Serial.println("WiFi connected.");
      Serial.println("IP address: ");
      Serial.println(WiFi.localIP());
    }
    
    
    server.begin();
}

void runServer(){
  WiFiClient client = server.available();   // listen for incoming clients

  if(client){
    Serial.println("New Client.");
    while (client.connected()){
      String request;
      if(client.available()){ //receive client request
        request = client.readString();
        Serial.println(request);
      }
      String identifier = "Command: ";
      String command;
      if(request.indexOf(identifier)>0){
        //extract actual command
        int charIndex = request.indexOf(identifier)+identifier.length();
        while(request.charAt(charIndex)!='\r'){
          command+=request.charAt(charIndex);
          charIndex++;
        }
        //send response
        client.println("HTTP/1.1 200 OK");
        client.println("Content-type:text/json");
        client.println();//end of header
        
        if(command=="Test")
          client.print("{\"Test\":\"Hello server\"}");
        else if(command=="OFF"){
          digitalWrite(blinkPin,HIGH);
          client.print("{\"Response\":\"Light ON\"}");
        }
        else if(command=="ON"){
          digitalWrite(blinkPin,LOW);
          client.print("{\"Response\":\"Light Off\"}");
        }
        else
          client.print("{\"Error\":\"Command does not exist\"}");
        
        client.println();//end of response
        break;
      }
      if(request.indexOf(identifier)<0){
        client.println("HTTP/1.1 200 OK");
        client.println("Content-type:text/html");
        client.println();

        // the content of the HTTP response follows the header:
        client.print("<!DOCTYPE html><html lang=\"en\">");
        client.print("<body><h2>No script</h2>Click <a href=\"/H\">here</a> to turn the LED on pin 2 on.<br> Click <a href=\"/L\">here</a> to turn the LED on pin 2 off.<br></body>");

        // The HTTP response ends with another blank line:
        client.println();
        // break out of the while loop:
        break;
      }
    }
    
  }
}
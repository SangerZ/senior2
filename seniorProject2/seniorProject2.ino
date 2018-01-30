#include <ESP8266WiFi.h>    //https://github.com/esp8266/Arduino
#include <DNSServer.h>
#include <ESP8266WebServer.h>
#include <WiFiManager.h>     //https://github.com/tzapu/WiFiManager

#include <FirebaseArduino.h>
#include <EEPROM.h>
#include <time.h>

#include <Wire.h>

// set pin numbers:
#define D0 16             // USER LED Wake
#define ledPin  D0        // the number of the LED pin
#define D1 5
#define ConfigWiFi_Pin D1 
#define ESP_AP_NAME "ESP8266 Config AP"
void setup() 
{
  // initialize pin D0 as an output.
  pinMode(ledPin, OUTPUT);
  pinMode(ConfigWiFi_Pin,INPUT_PULLUP);

  Serial.begin(115200);
  digitalWrite(ledPin,LOW);//Turn on the LED
  //WiFiManager
  //Local intialization. Once its business is done, there is no need to keep it around
  WiFiManager wifiManager;
  if(digitalRead(ConfigWiFi_Pin) == LOW) // Press button
  {
    //reset saved settings
    Serial.print("entering configuration mode");
    wifiManager.resetSettings(); // go to ip 192.168.4.1 to config
  }
  //fetches ssid and password from EEPROM and tries to connect
  //if it does not connect, it starts an access point with the specified name
  //and goes into a blocking loop awaiting configuration
  wifiManager.autoConnect(ESP_AP_NAME); 
  while (WiFi.status() != WL_CONNECTED) 
  {
     delay(250);
     Serial.print(".");
  }
  Serial.println("WiFi connected");  
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
  digitalWrite(ledPin,HIGH);
}
void loop() 
{
 digitalWrite(D0, HIGH);  // turn off the LED  
 delay(2000);             // wait for two seconds
 digitalWrite(D0, LOW);   // turn on the LED
 delay(2000);             // wait for two seconds
}

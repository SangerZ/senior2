#include <ESP8266WiFi.h>
#include <SoftwareSerial.h>
//
#include <DNSServer.h>
#include <ESP8266WebServer.h>
#include <WiFiManager.h>
//
#include <FirebaseArduino.h>
#include <time.h>
//
#include "Timer.h"
//
//#define LED_BUILTIN 16
#define ledPin  LED_BUILTIN
#define D0 16
#define D1 5
#define D4 2
#define D5 14
#define D6 12
#define D7 13
#define PUMP_A D0
#define PUMP_B D4
#define PUMP_C D5
#define PH_PROBE D6
#define EC_PROBE D7
#define ESP_AP_NAME "HydroFarm Config"
#define ConfigWiFi_Pin D1
#define FIREBASE_HOST "thesmartfarm-7f3a5.firebaseio.com"
#define FIREBASE_AUTH "FcU8DPrOPxV5eigb7BXh2nJcsR48fg1mYdMnGJRY"
#define DEVICE_NUM "/5735451"
#define Input D2
#define Output D3

SoftwareSerial NodeSerial(Input, Output);

float ecBar = 1.5;
float phBar = 6.0;
float ecGet = 0.0;
float phGet = 0.0;
float phTemp = 0.0;
float ecTemp = -1.0;
int volume = 300;

Timer t;

void checkFirebase() {
  float phPeek, ecPeek;
  int volumePeek;
  //check wifi status first
  if (WiFi.status() == WL_CONNECTED) {
    FirebaseObject firebasePeek = Firebase.get("/5735451");
    phPeek = firebasePeek.getFloat("phTreshold");
    ecPeek = firebasePeek.getFloat("ecTreshold");
    volumePeek = firebasePeek.getInt("volume");

//    Serial.print("phPeek ");
//    Serial.println(phPeek);
//    Serial.print("ecPeek ");
//    Serial.println(ecPeek);
    
    if (phPeek != phBar) {
      phBar = phPeek;
      Serial.println(phBar);
    }
    if (ecPeek != ecBar) {
      ecBar = ecPeek;
      Serial.println(ecBar);
    }
    if (volumePeek != volume) {
      volume = volumePeek;
    }
  }
  Serial.println("finish checking firebase");
}

void checkPH() {
  phTemp = -1.0;
  Serial.println("**********entering checkPH***********");
  digitalWrite(PH_PROBE, LOW);
  NodeSerial.println(1);
  delay(10000);
  Serial.println("**********finish delay***********");
  
  //
  while (NodeSerial.available() || phTemp == -1.0) {
    phTemp = NodeSerial.parseFloat();
    Serial.print("ph : ");
    Serial.println(phTemp);
  }
  phGet = phTemp;
  phTemp = -1.0;
  if (phGet < phBar) {
    Serial.println("pH is too damn low");
    if (WiFi.status() == WL_CONNECTED) {
      Firebase.set("/5735451/lowpHAlert", true);
    }
    Serial.println("warning! The pH level is too low!");
    NodeSerial.println(3);
  }
  if (phGet > phBar) {//high ph level
    if (WiFi.status() == WL_CONNECTED) {
      Firebase.set("/5735451/lowpHAlert", false);
    }
    NodeSerial.println(4);
    //fill to reach the threshold
    float remaining  = phBar - phTemp;
    int duration = int(remaining * volume * 100);//need to fix this as this prob is the wrong formula
    digitalWrite(PUMP_C, LOW);
    delay(duration);
    digitalWrite(PUMP_C, HIGH);
  }
  digitalWrite(PH_PROBE, HIGH);
}

void checkEC() {
  ecTemp = -1.0;
  Serial.println("**********entering checkEC***********");
  digitalWrite(EC_PROBE, LOW);
  NodeSerial.println(2);
  delay(20000);
  Serial.println("**********finish delay***********");
  while (NodeSerial.available() || ecTemp == -1.0) {
    ecTemp = NodeSerial.parseFloat();
    Serial.print("ec : ");
    Serial.println(ecTemp);
  }
  Serial.println("escape ec while");
  ecGet = ecTemp;
  ecTemp = -1.0;
  Serial.print("ecGet ");
  Serial.println(ecGet);
  Serial.print("ecBar ");
  Serial.println(ecBar);
  if (ecGet < ecBar) {//not enough nutrient
    // set ec alarm to false
    if (WiFi.status() == WL_CONNECTED) {
      Firebase.set("/5735451/highECAlert", false);
    }
    NodeSerial.println(6);
    Serial.println("about to fill the nutrients");
    //fill
    //float remaining = (ecBar - ecGet) * (float)volume;
    float remaining  = ecBar - ecGet;
    int duration = int(remaining * 100 * volume);//this is still wrong. need to find out the speed of the doser pump

    Serial.print(remaining);
    Serial.print(" ");
    Serial.println(duration);

    
    digitalWrite(PUMP_A, LOW);
    delay(duration);
    digitalWrite(PUMP_A, HIGH);
    digitalWrite(PUMP_B, LOW);
    delay(duration);
    digitalWrite(PUMP_B, HIGH);
  }
  if (ecGet > ecBar) {
    //set ec alarm to true
    if (WiFi.status() == WL_CONNECTED) {
      Firebase.set("/5735451/highECAlert", true);
    }
    Serial.println("warning! The ec level is too high!");
    NodeSerial.println(5);
  }
  digitalWrite(EC_PROBE, HIGH);
}

void checkWaterQuality() {
  checkPH();
  checkEC();
  Serial.println("finish checking water");
  pushFirebase();
}

void pushFirebase(){
  time_t now = time(nullptr);
  //Serial.println(ctime(&now));
  StaticJsonBuffer<200> jsonBuffer;
  JsonObject& valueObject = jsonBuffer.createObject();
  valueObject["ec"] = ecGet;
  valueObject["ph"] = phGet;
  valueObject["time"] = ctime(&now);

  Firebase.push("/5735451Data/value", valueObject);
  Serial.println("finish pushing to firebase");
  delay(1000);
}

void setup() {
  Serial.begin(9600);
  pinMode(ledPin, OUTPUT);
  pinMode(ConfigWiFi_Pin, INPUT_PULLUP);
  pinMode(PUMP_A, OUTPUT);
  pinMode(PUMP_B, OUTPUT);
  pinMode(PUMP_C, OUTPUT);
  pinMode(EC_PROBE, OUTPUT);
  pinMode(PH_PROBE, OUTPUT);

  digitalWrite(PUMP_A, HIGH);
  digitalWrite(ledPin, HIGH);
  digitalWrite(PUMP_B, HIGH);
  digitalWrite(PUMP_C, HIGH);
  digitalWrite(EC_PROBE, HIGH);
  digitalWrite(PH_PROBE, HIGH);
  digitalWrite(PUMP_A, HIGH);

  WiFiManager wifiManager;
  if (digitalRead(ConfigWiFi_Pin) == LOW) {// Press button
    //reset saved settings
    Serial.print("entering configuration mode");
    wifiManager.resetSettings(); // go to ip 192.168.4.1 to config
  }
  wifiManager.autoConnect(ESP_AP_NAME);
  while (WiFi.status() != WL_CONNECTED){
    delay(250);
    Serial.print(".");
  }
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
  digitalWrite(ledPin, HIGH);

  Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);
  //check for preexisting branch of this device
  FirebaseObject flagCheck = Firebase.get("/5735451");
  String flagCheckName = flagCheck.getString("name");
  Serial.println("flagCheckName is : " + flagCheckName);
  if (flagCheckName.equals('\0')) {
    Firebase.set("/5735451/name", "defaultFarm");
    Firebase.set("/5735451/volume", 300);
    Firebase.set("/5735451/ecTreshold", 1.5);
    Firebase.set("/5735451/phTreshold", 6.0);
    Firebase.set("/5735451/lowpHAlert", false);
    Firebase.set("/5735451/highECAlert", false);
    Serial.println("set the farm");
  }
  else {
    Serial.println("farm already existed");
    Serial.println(flagCheckName + " : is the farm name");
  }
  pinMode(Input, INPUT);
  pinMode(Output, OUTPUT);

  //clock
int timezone = 7;
int dst = 0;
  configTime(timezone * 3600, dst, "pool.ntp.org", "time.nist.gov");
  Serial.println("\nWaiting for time");
  while (!time(nullptr)) {
    Serial.print(".");
    delay(1000);
  }

  //end clock

  NodeSerial.begin(57600);
  Serial.println();
  Serial.println();
  Serial.println("NodeMCU/ESP8266 Run");
  int tickEvent = t.every(100000, checkWaterQuality);
  //int tickEvent = t.every(900000, checkWaterQuality);
}

void loop() {
  // put your main code here, to run repeatedly:

  checkFirebase();
  t.update();
}

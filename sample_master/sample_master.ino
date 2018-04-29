#include <ESP8266WiFi.h>
#include <SoftwareSerial.h>
SoftwareSerial NodeSerial(D2, D3); // RX | TX

void setup() {
  pinMode(D2, INPUT);
  pinMode(D3, OUTPUT);
  Serial.begin(9600);
  NodeSerial.begin(57600);
  Serial.println();
  Serial.println();
  Serial.println(“NodeMCU / ESP8266 Run”);
}

void loop() {
  while (NodeSerial.available() > 0) {

    int i_data = NodeSerial.parseInt();
    float f_data = NodeSerial.parseFloat();
    if (NodeSerial.read() == ‘\n’) {
      Serial.print(“NodeMCU or ESP8266″); Serial.print(” : “);
      Serial.print(i_data); Serial.print(” : “);
      Serial.println(f_data);
    }
    delay(50);
  }
  delay(10);
}

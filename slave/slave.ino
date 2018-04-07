//int i_data = 1234;
//float f_data = 567.89;
#include <SoftwareSerial.h>
#include <EEPROM.h>
#include <OneWire.h>
#include <SimpleDHT.h>
SoftwareSerial NanoSerial(3, 2); // RX | TX

float ph;
float ec;

//ec bits
#define EEPROM_write(address, p) {int i = 0; byte *pp = (byte*)&(p);for(; i < sizeof(p); i++) EEPROM.write(address+i, pp[i]);}
#define EEPROM_read(address, p)  {int i = 0; byte *pp = (byte*)&(p);for(; i < sizeof(p); i++) pp[i]=EEPROM.read(address+i);}
#define ReceivedBufferLength 20
char receivedBuffer[ReceivedBufferLength + 1]; // store the serial command
byte receivedBufferIndex = 0;

#define ecSensorPin  A1  //EC Meter analog output,pin on analog 1
#define ds18b20Pin  2    //DS18B20 signal, pin on digital 2

#define SCOUNT  100           // sum of sample point
int analogBuffer[SCOUNT];    //store the analog value read from ADC
int analogBufferIndex = 0;

#define compensationFactorAddress 8    //the address of the factor stored in the EEPROM
float compensationFactor;

#define VREF 5000  //for arduino uno, the ADC reference is the power(AVCC), that is 5000mV

boolean enterCalibrationFlag = 0;
float ECvalue, ECvalueRaw;
int temperature;
SimpleDHT11 dht11;
int pinDHT11 = 6;
//end ec bits

//ph bits
#define SensorPin A0            //pH meter Analog output to Arduino Analog Input 0
#define Offset 0.00            //deviation compensate
#define LED 13
#define samplingInterval 20
#define printInterval 800
#define ArrayLenth  40    //times of collection
int pHArray[ArrayLenth];   //Store the average value of the sensor feedback
int pHArrayIndex = 0;
//end ph bits

void ecCalibration(byte mode){
    char *receivedBufferPtr;
    static boolean ecCalibrationFinish = 0;
    float factorTemp;
    switch(mode){
      case 0:
      if(enterCalibrationFlag)
         Serial.println(F("Command Error"));
      break;   
        
      case 1:
      enterCalibrationFlag = 1;
      ecCalibrationFinish = 0;
      Serial.println();
      Serial.println(F(">>>Enter Calibration Mode<<<"));
      Serial.println(F(">>>Please put the probe into the 12.88ms/cm buffer solution<<<"));
      Serial.println();
      break;
    
     case 2:
      if(enterCalibrationFlag){
          factorTemp = ECvalueRaw / 12.88;
          if((factorTemp>0.85) && (factorTemp<1.15)){
              Serial.println();
              Serial.println(F(">>>Confrim Successful<<<"));
              Serial.println();
              compensationFactor =  factorTemp;
              ecCalibrationFinish = 1;
          }
          else{
            Serial.println();
            Serial.println(F(">>>Confirm Failed,Try Again<<<"));
            Serial.println();
            ecCalibrationFinish = 0;
          }        
      }
      break;

        case 3:
        if(enterCalibrationFlag){
            Serial.println();
            if(ecCalibrationFinish){
               EEPROM_write(compensationFactorAddress, compensationFactor);
               Serial.print(F(">>>Calibration Successful"));
            }
            else Serial.print(F(">>>Calibration Failed"));       
            Serial.println(F(",Exit Calibration Mode<<<"));
            Serial.println();
            ecCalibrationFinish = 0;
            enterCalibrationFlag = 0;
        }
        break;
    }
}

int getMedianNum(int bArray[], int iFilterLen) {
  int bTab[iFilterLen];
  for (byte i = 0; i < iFilterLen; i++) {
    bTab[i] = bArray[i];
  }
  int i, j, bTemp;
  for (j = 0; j < iFilterLen - 1; j++) {
    for (i = 0; i < iFilterLen - j - 1; i++) {
      if (bTab[i] > bTab[i + 1]) {
        bTemp = bTab[i];
        bTab[i] = bTab[i + 1];
        bTab[i + 1] = bTemp;
      }
    }
  }
  if ((iFilterLen & 1) > 0) {
    bTemp = bTab[(iFilterLen - 1) / 2];
  }
  else {
    bTemp = (bTab[iFilterLen / 2] + bTab[iFilterLen / 2 - 1]) / 2;
  }
  return bTemp;
}

int readTemperature() {
  byte temperature = 0;
  byte humidity = 0;
  int err = SimpleDHTErrSuccess;
  while (1) {
    if ((err = dht11.read(pinDHT11, &temperature, &humidity, NULL)) == SimpleDHTErrSuccess) {
      Serial.print("Sample OK: ");
      Serial.print((int)temperature); Serial.print(" *C, ");
      Serial.print((int)humidity); Serial.println(" H");
      return (int)temperature;
    }
    else {
      Serial.print("Read DHT11 failed, err="); Serial.println(err); delay(1000);
      return 25;
    }
  }
}

void readCharacteristicValues() {
  EEPROM_read(compensationFactorAddress, compensationFactor);
  if (EEPROM.read(compensationFactorAddress) == 0xFF && EEPROM.read(compensationFactorAddress + 1) == 0xFF && EEPROM.read(compensationFactorAddress + 2) == 0xFF && EEPROM.read(compensationFactorAddress + 3) == 0xFF)
  {
    compensationFactor = 1.0;   // If the EEPROM is new, the compensationFactorAddress is 1.0(default).
    EEPROM_write(compensationFactorAddress, compensationFactor);
  }
}

float ecMeasure() {
  float storage[100];
  for (int i = 0; i < sizeof(storage); i++) {
    storage[i] = -1;
  }
  int counter = 0;
  while (storage[99] == -1) {
    static unsigned long analogSampleTimepoint = millis();
    if (millis() - analogSampleTimepoint > 30U) { //every 30ms,read the analog value from the ADC
      analogSampleTimepoint = millis();
      analogBuffer[analogBufferIndex] = analogRead(ecSensorPin);    //read the analog value and store into the buffer,every 40ms
      analogBufferIndex++;
      if (analogBufferIndex == SCOUNT)
        analogBufferIndex = 0;
    }

    static unsigned long tempSampleTimepoint = millis();
    if (millis() - tempSampleTimepoint > 850U) { // every 1.7s, read the temperature from DS18B20
      tempSampleTimepoint = millis();
      temperature = readTemperature();  // read the current temperature from the  DS18B20
    }

    static unsigned long printTimepoint = millis();
    if (millis() - printTimepoint > 1000U) {
      printTimepoint = millis();
      float AnalogAverage = getMedianNum(analogBuffer, SCOUNT);  // read the stable value by the median filtering algorithm
      float averageVoltage = AnalogAverage * (float)VREF / 1024.0;
      if (temperature == -1000) {
        temperature = 25.0;      //when no temperature sensor ,temperature should be 25^C default
        Serial.print(temperature, 1);
        Serial.print(F("^C(default)    EC:"));
      }
      else {
        Serial.print(temperature, 1);   //current temperature
        Serial.print(F("^C             EC:"));
      }
      float TempCoefficient = 1.0 + 0.0185 * (temperature - 25); //temperature compensation formula: fFinalResult(25^C) = fFinalResult(current)/(1.0+0.0185*(fTP-25.0));
      float CoefficientVolatge = (float)averageVoltage / TempCoefficient;
      if (CoefficientVolatge < 150) {
        Serial.println(F("No solution!")); //25^C 1413us/cm<-->about 216mv  if the voltage(compensate)<150,that is <1ms/cm,out of the range
      }
      else if (CoefficientVolatge > 3300) {
        Serial.println(F("Out of the range!")); //>20ms/cm,out of the range
      }
      else {
        if (CoefficientVolatge <= 448) {
          ECvalue = 6.84 * CoefficientVolatge - 64.32; //1ms/cm<EC<=3ms/cm
        }
        else if (CoefficientVolatge <= 1457) {
          ECvalue = 6.98 * CoefficientVolatge - 127; //3ms/cm<EC<=10ms/cm
        }
        else {
          ECvalue = 5.3 * CoefficientVolatge + 2278; //10ms/cm<EC<20ms/cm
        }
        ECvalueRaw = ECvalue / 1000.0;
        ECvalue = ECvalue / compensationFactor / 1000.0; //after compensation,convert us/cm to ms/cm
        Serial.print(ECvalue, 2);    //two decimal
        Serial.print(F("ms/cm"));
        if (enterCalibrationFlag) {           // in calibration mode, print the voltage to user, to watch the stability of voltage
          Serial.print(F("            Factor:"));
          Serial.print(compensationFactor);
        }
        Serial.println();
        float answer = ECvalue;
        //return answer;
        storage[counter] = answer;
        counter++;
      }
    }
  }
  float summation = 0;
  for (int i = 0; i < sizeof(storage); i++) {
    summation += storage[i];
  }
  summation = summation / sizeof(storage);
  return summation;
}

double avergearray(int* arr, int number) {
  int i;
  int max, min;
  double avg;
  long amount = 0;
  if (number <= 0) {
    Serial.println("Error number for the array to avraging!/n");
    return 0;
  }
  if (number < 5) { //less than 5, calculated directly statistics
    for (i = 0; i < number; i++) {
      amount += arr[i];
    }
    avg = amount / number;
    return avg;
  } else {
    if (arr[0] < arr[1]) {
      min = arr[0]; max = arr[1];
    }
    else {
      min = arr[1]; max = arr[0];
    }
    for (i = 2; i < number; i++) {
      if (arr[i] < min) {
        amount += min;      //arr<min
        min = arr[i];
      } else {
        if (arr[i] > max) {
          amount += max;  //arr>max
          max = arr[i];
        } else {
          amount += arr[i]; //min<=arr<=max
        }
      }//if
    }//for
    avg = (double)amount / (number - 2);
  }//if
  return avg;
}

float phMeasure() {
  float storage[100];
  for (int i = 0; i < (sizeof(storage)/sizeof(float)); i++) {
    storage[i] = 0.0;
  }
  Serial.println("finish init loop");
  static unsigned long samplingTime = millis();
  static unsigned long printTime = millis();
  static float pHValue, voltage;
  int counter = 0;
  while (counter < (sizeof(storage)/sizeof(float))) {
    if (millis() - samplingTime > samplingInterval) {
      pHArray[pHArrayIndex++] = analogRead(SensorPin);
      if (pHArrayIndex == ArrayLenth)pHArrayIndex = 0;
      voltage = avergearray(pHArray, ArrayLenth) * 5.0 / 1024;
      pHValue = 3.5 * voltage + Offset;
      samplingTime = millis();
    }
    if (millis() - printTime > printInterval) { //Every 800 milliseconds, print a numerical, convert the state of the LED indicator
      Serial.print("Voltage:");
      Serial.print(voltage, 2);
      Serial.print("    pH value: ");
      Serial.println(pHValue, 2);
      digitalWrite(LED, digitalRead(LED) ^ 1);
      printTime = millis();
      storage[counter] = pHValue;
      counter++;
      Serial.print(pHValue);
      Serial.print("   ");
      Serial.print(counter);
      Serial.print("   ");
      Serial.println((sizeof(storage)/sizeof(float)));
    }
    
  }
  float summation = 0;
  for (int l = 0; l < (sizeof(storage)/sizeof(float)); l++) {
    summation += storage[l];
    //summation += storage[l];
    Serial.println(storage[l]);
  }
  summation = summation / (sizeof(storage)/sizeof(float));
  return summation;
}

void setup(){
  pinMode(3, INPUT);
  pinMode(2, OUTPUT);
  pinMode(4, OUTPUT);//ph led
  pinMode(5, OUTPUT);//ec led
  Serial.begin(9600);
  NanoSerial.begin(57600);
}

void loop() {
  while (NanoSerial.available() > 0) {
    int cmd = NanoSerial.parseInt();
    switch (cmd) {
      case 1://check ph
        ph = 6.0;
        //ph = phMeasure();
        NanoSerial.println(ph);
        break;
      case 2://check ec
        //ec = 1.7;
        ec = ecMeasure();
        NanoSerial.println(ec);
        break;
      case 3: //ph too low warning physical
        digitalWrite(4, HIGH);
        break;
      case 4: //ph level is normal
        digitalWrite(4, LOW);
        break;
      case 5: //ec level is too high
        digitalWrite(5, HIGH);
        break;
      case 6: //ec level is normal
        digitalWrite(5, LOW);
        break;
      default:
        break;
    }
  }
}

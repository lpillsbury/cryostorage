/*************************************************** 
 *  Code modified from the max31865 example in the max31865 library
 *  Copyright below for the example.
 *  Our modifications written by LeahP, RitoBT
 *  
 ****************************************************
  This is a library for the Adafruit PT100/P1000 RTD Sensor w/MAX31865

  Designed specifically to work with the Adafruit RTD Sensor
  ----> https://www.adafruit.com/products/3328

  This sensor uses SPI to communicate, 4 pins are required to  
  interface
  Adafruit invests time and resources providing this open source code, 
  please support Adafruit and open-source hardware by purchasing 
  products from Adafruit!

  Written by Limor Fried/Ladyada for Adafruit Industries.  
  BSD license, all text above must be included in any redistribution
 ****************************************************/

#include <Adafruit_MAX31865.h>
#include <SPI.h>

// Use software SPI: CS, DI, DO, CLK
Adafruit_MAX31865 thermo = Adafruit_MAX31865(10, 11, 12, 13);
// use hardware SPI, just pass in the CS pin
//Adafruit_MAX31865 thermo = Adafruit_MAX31865(10);

// The value of the Rref resistor. Use 430.0 for PT100 and 4300.0 for PT1000
#define RREF      4300.0
// The 'nominal' 0-degrees-C resistance of the sensor
// 100.0 for PT100, 1000.0 for PT1000
#define RNOMINAL  1000.0

unsigned long start_time = millis();

void setup() {
  Serial.begin(9600);
  Serial.println("Temperature readings from inside the vacuum chamber");
  Serial.println("elapsed time(s)    resistance(ohms)");
  thermo.begin(MAX31865_2WIRE);  // set to 2WIRE given our sensor
}

void check_fault() {
// Check and print any faults
  uint8_t fault = thermo.readFault();
  if (fault) {
    Serial.print("Fault 0x"); Serial.println(fault, HEX);
    if (fault & MAX31865_FAULT_HIGHTHRESH) {
      Serial.println("RTD High Threshold"); 
    }
    if (fault & MAX31865_FAULT_LOWTHRESH) {
      Serial.println("RTD Low Threshold"); 
    }
    if (fault & MAX31865_FAULT_REFINLOW) {
      Serial.println("REFIN- > 0.85 x Bias"); 
    }
    if (fault & MAX31865_FAULT_REFINHIGH) {
      Serial.println("REFIN- < 0.85 x Bias - FORCE- open"); 
    }
    if (fault & MAX31865_FAULT_RTDINLOW) {
      Serial.println("RTDIN- < 0.85 x Bias - FORCE- open"); 
    }
    if (fault & MAX31865_FAULT_OVUV) {
      Serial.println("Under/Over voltage"); 
    }
    thermo.clearFault();
  }
}

float take_samples(){
  uint16_t rtd;
  float cumsum = 0;
  float ratio;
  for(int i = 0; i < 100; i++){
    rtd = thermo.readRTD();
    check_fault();
    ratio = rtd;
    ratio /= 32768;
    cumsum = cumsum + ratio;
    delay(2);
  }
  // return average ratio
  return cumsum/100 * RREF;
}

void loop() {
  float measured_resist;
  unsigned long nowtime = millis();
  measured_resist = take_samples();
  Serial.print((nowtime - start_time)/1000);  //will this be big enough for recording over days?
  Serial.print("\t");
  Serial.println(measured_resist);
  delay(10*1000);  //take a set of readings every 10 seconds
}

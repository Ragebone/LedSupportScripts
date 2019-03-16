#include "Arduino.h"
#include "FastLED.h"

#define TOTALMAINSIZE 1
#define TOTALCOMPLEMENTSIZE 2

#define MAINSTRIPE1SIZE 1
#define MAINSTRIPE1PIN 10

#define COMPLEMENTSTRIPE1SIZE 1
#define COMPLEMENTSTRIPE1PIN 8

#define COMPLEMENTSTRIPE2SIZE 1
#define COMPLEMENTSTRIPE2PIN 9

uint8_t b1, b2, b3, b4, b5;
uint16_t count, i, block;

CRGB mainstripe[TOTALMAINSIZE];
CRGB complementstripe[TOTALCOMPLEMENTSIZE];

void setup() {
  Serial.begin(115200);
  while(!Serial){}
  bool error = false;
  if(TOTALMAINSIZE != MAINSTRIPE1SIZE){
    error = true;
  }
  if(TOTALCOMPLEMENTSIZE != (COMPLEMENTSTRIPE1SIZE + COMPLEMENTSTRIPE2SIZE)){
    error = true;
  }
  if(error){
    pinMode(LED_BUILTIN, OUTPUT);
    while(true){
      Serial.println("Error in AVR Sketch, reflash with corrected LED Counts!");
      digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
      delay(1000);                       // wait for a second
      digitalWrite(LED_BUILTIN, LOW);    // turn the LED off by making the voltage LOW
      delay(1000);  
    }
  }


  FastLED.addLeds<WS2812B, MAINSTRIPE1PIN, GRB>(mainstripe, MAINSTRIPE1SIZE);

  FastLED.addLeds<WS2812B, COMPLEMENTSTRIPE1PIN, GRB>(complementstripe, COMPLEMENTSTRIPE1SIZE);
  FastLED.addLeds<WS2812B, COMPLEMENTSTRIPE2PIN, GRB>(complementstripe, COMPLEMENTSTRIPE2SIZE);

  FastLED.setBrightness(255);
  
  
}

void loop() {
  
    while(Serial.available() < 1){}
    b1 = Serial.read();
    while(Serial.available() < 1){}
    b2 = Serial.read();
    while(Serial.available() < 1){}
    b3 = Serial.read();

    for(i = 0; i < TOTALCOMPLEMENTSIZE; i++){
      complementstripe[i].r = b1;
      complementstripe[i].g = b2;
      complementstripe[i].b = b3;
    }

    for(count = 0; count < TOTALMAINSIZE;){
      while(Serial.available() < 1){}
      b1 = Serial.read();
      while(Serial.available() < 1){}
      b2 = Serial.read();

      block = ((256 * b1) + b2);


      // RunLength happens to be 0, that means delimiter.
      if(block == 0){
        // Move to the next FF byte, indicationg end of delimiter.
        for(i = 0; i < 6; i++){
          while(Serial.available() < 1){}
          b1 = Serial.read();  
          if(b1 > 100){
            break;
          }   
        }          
      }
      
      while(Serial.available() < 1){}
      b3 = Serial.read();
      while(Serial.available() < 1){}
      b4 = Serial.read();
      while(Serial.available() < 1){}
      b5 = Serial.read();

      
      for(i = count; i < (count + block); i++){
        if(i >= TOTALMAINSIZE){
          break;
        }
        mainstripe[i].r = b3;
        mainstripe[i].g = b4;
        mainstripe[i].b = b5; 
      }
      count += block;
    }
    FastLED.show();
}
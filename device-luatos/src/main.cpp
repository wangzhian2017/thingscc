#include <Arduino.h>

void setup() {
  Serial.begin(115200);

  pinMode(12,OUTPUT);
  pinMode(13,OUTPUT);
}

void loop() {
  Serial.println("LUATOS");

  
  digitalWrite(13,HIGH);
  digitalWrite(12,LOW);
  delay(1000);
  digitalWrite(13,LOW);
  digitalWrite(12,HIGH);
  delay(1000);
}


#include <Arduino.h>
#include <ESP32Servo.h>
#include <Stepper.h>

Servo myservo;

const int stepsPerRevolution = 100; 
Stepper myStepper(stepsPerRevolution, 5,8,4,9);

void setup() {
  Serial.begin(115200);
  // Allow allocation of all timers
	ESP32PWM::allocateTimer(0);
	ESP32PWM::allocateTimer(1);
	ESP32PWM::allocateTimer(2);
	ESP32PWM::allocateTimer(3);
  myservo.setPeriodHertz(50); // standard 50 hz servo
  myservo.attach(2, 500, 2500); // Attach the servo after it has been detatched

  myStepper.setSpeed(250);

  pinMode(12,OUTPUT);
  pinMode(13,OUTPUT);

}

void loop() {
  Serial.println("LUATOS");
  // //360度舵机
  // myservo.write(10); //0正方向的全速运行
  // delay(10000);
  // myservo.write(170); //180反方向的全速运行
  // delay(10000);
  // myservo.write(90); //不转动
  // delay(10000);

  // digitalWrite(13,HIGH);
  // digitalWrite(12,LOW);
  // delay(1000);
  // digitalWrite(13,LOW);
  // digitalWrite(12,HIGH);
  // delay(1000);

  myStepper.step(2048);
  delay(1000);
  myStepper.step(-2048);
  delay(1000);
}


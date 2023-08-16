#include <Arduino.h>
#include <ESP32Servo.h>
#include <Stepper.h>
#include <ShiftRegister74HC595.h>

Servo myservo;

//8拍情况下，电机是64步/圈，每步360° / 64 = 5.625°
//4拍情况下，电机是32步/圈
const int stepsPerRevolution = 100;  //步/圈 
Stepper myStepper(stepsPerRevolution, 5,8,4,9);

ShiftRegister74HC595<1> sr(0, 1, 2);

void setup() {
  Serial.begin(115200);
  // Allow allocation of all timers
	ESP32PWM::allocateTimer(0);
	ESP32PWM::allocateTimer(1);
	ESP32PWM::allocateTimer(2);
	ESP32PWM::allocateTimer(3);
  myservo.setPeriodHertz(50); // standard 50 hz servo
  myservo.attach(2, 500, 2500); // Attach the servo after it has been detatched

  myStepper.setSpeed(250); //圈/分

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

  //8拍情况下，还有1/64减速箱，所以转一圈（360）需要64 * 64 = 4096步
  //4拍情况下， 还有1/64减速箱，转一圈（360）需要64 * 32 = 2048步
  myStepper.step(2048);
  delay(1000);
  myStepper.step(-2048);
  delay(1000);

  // set all pins at once
  // uint8_t pinValues[] = { B10101010 }; 
  // sr.setAll(pinValues); 
  // delay(1000);
}


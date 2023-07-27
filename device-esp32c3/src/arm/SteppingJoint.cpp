#include "SteppingJoint.h"
#include <Arduino.h>

SteppingJoint::SteppingJoint(int pin1,int pin2,int pin3,int pin4)
{
    this->pin1=pin1;
    this->pin2=pin2;
    this->pin3=pin3;
    this->pin4=pin4;

    pinMode(pin1, OUTPUT);
    pinMode(pin2, OUTPUT);
    pinMode(pin3, OUTPUT);
    pinMode(pin4, OUTPUT);
}

SteppingJoint::~SteppingJoint()
{
}

void SteppingJoint::setPin(int in1, int in2, int in3, int in4){
    digitalWrite(pin1, in1);
    digitalWrite(pin2, in2);
    digitalWrite(pin3, in3);
    digitalWrite(pin4, in4); 
}


void SteppingJoint::stepForward(){
    //8拍模式
    float delay_time=60000/speed/total_step/8;
    setPin(1,0,0,0);
    delay(delay_time); // 延时ms，控制旋转速度
    setPin(1,1,0,0); 
    delay(delay_time); // 延时ms，控制旋转速度
    setPin(0,1,0,0); 
    delay(delay_time); // 延时ms，控制旋转速度
    setPin(0,1,1,0); 
    delay(delay_time); // 延时ms，控制旋转速度
    setPin(0,0,1,0); 
    delay(delay_time); // 延时ms，控制旋转速度
    setPin(0,0,1,1); 
    delay(delay_time); // 延时ms，控制旋转速度
    setPin(0,0,0,1); 
    delay(delay_time); // 延时ms，控制旋转速度
    setPin(1,0,0,1); 
    delay(delay_time); // 延时ms，控制旋转速度
}
void SteppingJoint::stepReverse(){
    //8拍模式
    float delay_time=60000/speed/total_step/8;
    setPin(1,0,0,0);
    delay(delay_time); // 延时ms，控制旋转速度
    setPin(1,0,0,1); 
    delay(delay_time); // 延时ms，控制旋转速度
    setPin(0,0,0,1); 
    delay(delay_time); // 延时ms，控制旋转速度
    setPin(0,0,1,1); 
    delay(delay_time); // 延时ms，控制旋转速度
    setPin(0,0,1,0); 
    delay(delay_time); // 延时ms，控制旋转速度
    setPin(0,1,1,0); 
    delay(delay_time); // 延时ms，控制旋转速度
    setPin(0,1,0,0); 
    delay(delay_time); // 延时ms，控制旋转速度

    setPin(1,1,0,0); 
    delay(delay_time); // 延时ms，控制旋转速度
}

float SteppingJoint::actToAngle(float angle,bool immediately){
    expect_angle=angle;
    if(immediately){
        this->angle=angle;
    }
    return angle;
}

float SteppingJoint::execute(){
    return angle;
}
float SteppingJoint::getAngle(){
    return angle;
}

int   SteppingJoint::getDirection(){
    float diff= expect_angle-angle;
    if(diff>0){
        return 1;
    }else if (diff<0)
    {
        return -1;
    }else
    {
        return 0;
    }
    
}
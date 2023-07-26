#include "ServoJoint.h"
#include <Arduino.h>


ServoJoint::ServoJoint(const char *name,int channel,int pin,float minAngle,float maxAngle
                        ,int resolution,int freq,float min_pulse_time,float max_pulse_time){
    this->name=name;
    this->channel=channel;
    this->pin=pin;
    if(minAngle<=maxAngle){
        this->min_angle=minAngle;
        this->max_angle=maxAngle;
    }else{
        this->min_angle=maxAngle;
        this->max_angle=minAngle;
    }
    
    this->resolution=resolution;
    this->freq=freq;
    this->total_pulse_time=1000/this->freq;
    this->min_pulse_time=min_pulse_time;
    this->max_pulse_time=max_pulse_time;
    const int total_pulse=pow(2,this->resolution);
    this->min_pulse=min_pulse_time*total_pulse/total_pulse_time;
    this->max_pulse=max_pulse_time*total_pulse/total_pulse_time;

    // 用于设置 LEDC 通道的频率和分辨率。
    ledcSetup(channel, freq, resolution); 
    // 将通道与对应的引脚连接
    ledcAttachPin(pin, channel); 
}

float ServoJoint::actToAngle(float angle,bool immediately){
    this->expect_angle=angle;
    if(immediately){
        this->angle=angle;
        ledcWrite(this->channel, calculatePWM(this->angle)); 
    }
    
    return  this->angle;
}

float ServoJoint::actToRatio(float ratio){
    if(ratio<0)
    {
        ratio=0;
    }else if (ratio>1)
    {
        ratio=1;
    }
    this->expect_angle=this->min_angle+ratio*(this->max_angle-this->min_angle);

    Serial.print("ratio:");
    Serial.print(ratio);
    Serial.print(";expect_angle:");
    Serial.println(this->expect_angle);
    return  this->angle;
}

float ServoJoint::act(){
    if(this->expect_angle!=this->angle){
        int diff=this->expect_angle-this->angle;
        if(diff > 0-this->inc_angle && diff < this->inc_angle)
        {
            this->angle=this->expect_angle;
        }
        else if(diff>0){
            this->angle+=this->inc_angle;
        }else {
            this->angle-=this->inc_angle;
        }
        
        if(this->angle<this->min_angle){
            this->angle=this->min_angle;
        }else if (this->angle>this->max_angle)
        {
            this->angle=this->max_angle;
        }
        ledcWrite(this->channel, calculatePWM(this->angle)); 
    }
    

    return  this->angle;
}

float ServoJoint::calculatePWM(float degree){
    if (degree < 0)
        degree = 0;
    if (degree > 180)
        degree = 180;
    //返回角度对应的脉冲
    return this->min_pulse+(this->max_pulse - this->min_pulse)*degree / 180; 
}

float ServoJoint::getAngle(){
    return  this->angle;
}


int   ServoJoint::getDirection(){
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

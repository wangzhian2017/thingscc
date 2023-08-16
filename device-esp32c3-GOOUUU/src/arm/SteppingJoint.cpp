#include "SteppingJoint.h"
#include <Arduino.h>

SteppingJoint::SteppingJoint(int pin1,int pin2,int pin3,int pin4)
{
    m_Stepper=new Stepper(stepsPerRevolution,pin1,pin3,pin2,pin4);
    m_Stepper->setSpeed(whatSpeed);
}

SteppingJoint::~SteppingJoint()
{
}



float SteppingJoint::actToAngle(float angle,bool immediately){
    expect_angle=angle;
    if(immediately){
        this->angle=angle;
    }
    return angle;
}

float SteppingJoint::execute(){
    if(this->expect_angle!=this->angle){
        int diff=this->expect_angle-this->angle;
        if(diff > 0-this->inc_angle && diff < this->inc_angle)
        {
            m_Stepper->step(this->expect_angle-this->angle);
            this->angle=this->expect_angle;
        }
        else if(diff>0){
            this->angle+=this->inc_angle;
            m_Stepper->step(calStep(this->inc_angle));
        }else {
            this->angle-=this->inc_angle;
            m_Stepper->step(-calStep(this->inc_angle));
        }
        
        if(this->angle<-360){
            this->angle +=360;
        }else if (this->angle>360)
        {
            this->angle-=360;
        }
    }
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

int   SteppingJoint::stop(){
    expect_angle=angle;
    return angle;
}

float SteppingJoint::calStep(float degree){
    //8拍情况下，还有1/64减速箱，所以转一圈（360）需要64 * 64 = 4096步
    //4拍情况下， 还有1/64减速箱，转一圈（360）需要64 * 32 = 2048步
    float step=degree*stepsPerRevolution*whatSpeed/360;
    return step;
}
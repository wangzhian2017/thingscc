#include "Arm.h"
#include <Arduino.h>
#include "ServoJoint.h"


Arm::Arm(/* args */)
{
   grab_joint=new ServoJoint("grab",0,1,0,122);//new ServoJoint("grab",0,1,30,120);
   lift_joint=new ServoJoint("lift",1,2,10,95);
   backforward_joint= new ServoJoint("backforward",2,3,75,180);
   rotate_joint= new ServoJoint("rotate",3,10);
}

Arm::~Arm()
{
}

float Arm::grab(float angle_ratio){
    float angle=grab_joint->actToRatio(angle_ratio);
    return angle;
}
float Arm::lift(float angle_ratio){
     float angle=lift_joint->actToRatio(angle_ratio);
     return angle;
}
float Arm::backforward(float angle_ratio){
     float angle=backforward_joint->actToRatio(angle_ratio);
     return angle;
}
float Arm::rotate(float angle_ratio){
     float angle=rotate_joint->actToRatio(angle_ratio);
     return angle;
}
float Arm::getGrabAngle(){
    return grab_joint->getAngle();
}
float Arm::getLiftAngle(){
    return lift_joint->getAngle();
}
float Arm::getBackforwardAngle(){
    return backforward_joint->getAngle();
}
float Arm::getRotateAngle(){
    return rotate_joint->getAngle();
}


void Arm::initialization(float angle_grab,float angle_lift,float angle_rotate,float angle_backforward){
    grab_joint->actToAngle(angle_grab,true);
    lift_joint->actToAngle(angle_lift,true);
    rotate_joint->actToAngle(angle_rotate,true);
    backforward_joint->actToAngle(angle_backforward,true);
}
void Arm::act(){
    //Serial.println("Arm act");
    grab_joint->act();
    rotate_joint->act();

    //由于购买的机械臂 上下轴 与 前后轴 相互限制，所有使用以下代码控制
    int lift_direction=lift_joint->getDirection();
    int backforward_direction=backforward_joint->getDirection();
    float lift_angle=lift_joint->getAngle();
    float backforward_angle=backforward_joint->getAngle();
    float included_angle=lift_angle+backforward_angle-90;//两轴夹角度数
    if(lift_direction<0||backforward_direction<0){
        //两轴夹角正在变小
        if(included_angle>80){
            lift_joint->act();
            backforward_joint->act();
        }
    }
    if(lift_direction>0||backforward_direction>0){
        //两轴夹角正在变大
        if(included_angle<130){
            lift_joint->act();
            backforward_joint->act();
        }
    }
    
}
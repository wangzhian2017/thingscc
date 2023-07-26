
#ifndef Arm_h
#define Arm_h

#include "IJoint.h"

class Arm
{
private:
    IJoint* grab_joint;
    IJoint* lift_joint;
    IJoint* backforward_joint;
    IJoint* rotate_joint;
public:
    Arm(/* args */);
    ~Arm();

    float grab(float angle_ratio);
    float lift(float angle_ratio);
    float backforward(float angle_ratio);
    float rotate(float angle_ratio);
    float getGrabAngle();
    float getLiftAngle();
    float getBackforwardAngle();
    float getRotateAngle();

    void initialization(float angle_grab,float angle_lift,float angle_rotate,float angle_backforward);
    void act();
};


#endif
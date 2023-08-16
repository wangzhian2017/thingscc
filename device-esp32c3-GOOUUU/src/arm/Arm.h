
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

    float grab(float angle);
    float lift(float angle);
    float backforward(float angle);
    float rotate(float angle);
    float getGrabAngle();
    float getLiftAngle();
    float getBackforwardAngle();
    float getRotateAngle();
    bool stopAll();

    void initialization(float angle_grab,float angle_lift,float angle_rotate,float angle_backforward);
    void act();
};


#endif
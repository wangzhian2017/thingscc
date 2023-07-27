#ifndef SteppingJoint_h
#define SteppingJoint_h

#include "IJoint.h"

class SteppingJoint:public IJoint
{
private:
    /* data */
    int total_step=200; //转360度需要的总步数（即脉冲数）
    int speed=1000;//每分钟转多少次
    float angle=0;
    float expect_angle=0;

    //4相电机
    int pin1;
    int pin2;
    int pin3;
    int pin4;

    void setPin(int in1, int in2, int in3, int in4);
    void stepForward();
    void stepReverse();
public:
    SteppingJoint(int pin1,int pin2,int pin3,int pin4);
    ~SteppingJoint();

    float actToAngle(float angle,bool immediately=false);
    float execute();
    float getAngle();
    int   getDirection();
};




#endif
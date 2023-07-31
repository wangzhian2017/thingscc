#ifndef SteppingJoint_h
#define SteppingJoint_h

#include "IJoint.h"
#include <Stepper.h>

class SteppingJoint:public IJoint
{
private:
    /* data */
    int total_step=200; //转360度需要的总步数（即脉冲数）
    int speed=1000;//每分钟转多少次
    float angle=0;
    float expect_angle=0;
    float inc_angle=1;
    
    //4相电机
    //8拍情况下，电机是64步/圈，每步360° / 64 = 5.625°
    //4拍情况下，电机是32步/圈
    const int stepsPerRevolution = 32;  //步/圈 
    const long whatSpeed=250; //圈/分钟
    const int reduction_ratio=64; //减速比
    
    Stepper* m_Stepper;

    float calStep(float degree);
public:
    SteppingJoint(int pin1,int pin2,int pin3,int pin4);
    ~SteppingJoint();

    float actToAngle(float angle,bool immediately=false);
    float execute();
    float getAngle();
    int   getDirection();
    int   stop();
};




#endif
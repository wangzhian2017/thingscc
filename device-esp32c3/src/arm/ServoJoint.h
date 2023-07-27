#ifndef ServoJoint_h
#define ServoJoint_h

#include "IJoint.h"

class ServoJoint : public IJoint{
public:
    ServoJoint(const char *name,int pin,float minAngle=0,float maxAngle=180
                ,int resolution=10,int freq=50,float min_pulse_time=0.2,float max_pulse_time=2.5);
     ~ServoJoint();
    float execute();
    float actToAngle(float angle,bool immediately=false);
    float getAngle();
    int   getDirection();
    
private:
    float calculatePWM(float degree);
    static int total_servo;

    const char *name;
    int freq;//舵机频率
    int resolution;
    float min_pulse_time; //0度对应的脉冲时间(毫秒)
    float max_pulse_time; //180度对应的脉冲时间(毫秒)
    float total_pulse_time;  //一个脉冲总时间 (毫秒)
    float min_pulse; //0度对应的脉冲
    float max_pulse;//180度对应的脉冲
    int channel;
    int pin;
    float min_angle=0;
    float max_angle=180;
    float angle=0;
    float inc_angle=1;
    float expect_angle=0;

    
};
#endif
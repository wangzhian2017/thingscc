#ifndef IJoint_h
#define IJoint_h

class IJoint
{
public:
     virtual  float actToAngle(float angle,bool immediately);
     virtual  float actToRatio(float ratio);
     virtual  float act();
     virtual  float getAngle();
     //转动方向 0不转动 1正转 -1反转
     virtual  int   getDirection();
};

#endif
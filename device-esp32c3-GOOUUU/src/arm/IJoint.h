#ifndef IJoint_h
#define IJoint_h

class IJoint
{
public:
     virtual  float actToAngle(float angle,bool immediately=false);
     virtual  float execute();
     virtual  float getAngle();
     //转动方向 0不转动 1正转 -1反转
     virtual  int   getDirection();

     virtual  int   stop();
};

#endif
import cv2
from friut.pose_detector import posedetector
import mediapipe as mp

# https://github.com/google/mediapipe/blob/master/docs/solutions/pose.md
def main():
    print("pose")

    start_pos=""
    end_pos=""
    pd=posedetector()
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("摄像头读取出错.")
            # If loading a video, use 'break' instead of 'continue'.
            continue

        image = cv2.flip(image, flipCode=1) 
        attach_result=pd.attach(image,draw=True)
        image=pd.attach_image
        if attach_result:
            pos=pd.point(19)
            if start_pos=="":
                start_pos=pos
                end_pos=""
            elif pos[1]>start_pos[1]:
                end_pos=pos
            elif start_pos!="" and end_pos!="":
                cv2.line(image,start_pos,end_pos,(0,255,0),3)
                start_pos=""
                end_pos=""
            else:
                start_pos=""
                end_pos=""
        
        cv2.imshow('pose', image)
        if cv2.waitKey(1)>0 :  #关闭窗体
            break

    cap.release()
    cv2.destroyAllWindows()



if __name__ == '__main__':
    main()






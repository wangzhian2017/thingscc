import mediapipe as mp
import cv2

class PoseHelper():
    def __init__(self):
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.mp_pose=mp.solutions.pose

        self.pose= self.mp_pose.Pose( min_detection_confidence=0.5, min_tracking_confidence=0.5)

        self.attach_img=[]
        self.key_points = []

    def attach(self, image,draw=False):
        self.attach_img=image
        self.key_points = []

        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.pose.process(image)
        if results.pose_landmarks:
            for id, lm in enumerate(results.pose_landmarks.landmark):
                h, w, c = image.shape
                px, py,pz = int(lm.x * w), int(lm.y * h),lm.z
                self.key_points.append([px, py,pz])
        # Draw the pose annotation on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if draw:
            self.mp_drawing.draw_landmarks(
                image,
                results.pose_landmarks,
                self.mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=self.mp_drawing_styles.get_default_pose_landmarks_style())
            
        return (len(self.key_points)>0)
    
    def point(self,index):
        return (self.key_points[index][0],self.key_points[index][1])


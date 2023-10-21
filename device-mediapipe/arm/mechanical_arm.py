import requests
import numpy as np

class mechanical_arm:
    def __init__(self,base_url,product_id,device_name):
        print("mechanical arm init")
        self.base_url = base_url
        self.product_id = product_id
        self.device_name = device_name

    def call_service(self,identifier,json_param):
        try:
            print(identifier,json_param)
            url=self.base_url+"/service/"+self.product_id+"/"+self.device_name+"/"+identifier
            r = requests.post(url,json = json_param, headers= {'Content-Type':'application/json;charset=UTF-8'})
            # print(r.json())
        
            return r.json()
        except:
            print('mechanical_arm.call_service网络请求异常')

    def grab(self,angle):
        angle=np.round(angle,2)
        param={'angle':angle}
        return self.call_service('grab',param)

    def lift(self,angle):
        angle=np.round(angle,2)
        param={'angle':angle}
        return self.call_service('lift',param)
        
    def rotate(self,angle):
        angle=np.round(angle,2)
        param={'angle':angle}
        return self.call_service('rotate',param)

    def backforward(self,angle):
        angle=np.round(angle,2)
        param={'angle':angle}
        return self.call_service('backforward',param)

    def stop(self):
        param={}
        return self.call_service('stop',param)
    
    # 空间位置运动
    def position_move(self,angle1,angle2,angle3):
        angle1=np.round(angle1,2)
        angle2=np.round(angle2,2)
        angle3=np.round(angle3,2)
        param={'angle1':angle1,'angle2':angle2,'angle3':angle3}
        return self.call_service('position_move',param)
    

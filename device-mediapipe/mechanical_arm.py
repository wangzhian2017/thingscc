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
            url=self.base_url+"/device/onnet/service/"+self.product_id+"/"+self.device_name+"/"+identifier
            r = requests.post(url,json = json_param, headers= {'Content-Type':'application/json;charset=UTF-8'})
            # print(r.json())
        
            return r.json()
        except:
            print('call_service网络请求异常')

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

    

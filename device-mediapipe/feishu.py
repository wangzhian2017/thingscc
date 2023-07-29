import requests
import base64
import secrets

class feishu:
    def __init__(self):
        self.base_url="https://open.feishu.cn"
        self.app_id="cli_a269fa42f378500b"
        self.app_secret="OV3yK3PyyXuH6qqm4dFRLbYUksqTxKq3"

        self.tenant_access_token=self.get_tenant_access_token()

    def get_tenant_access_token(self):
        url=self.base_url+"/open-apis/auth/v3/tenant_access_token/internal"
        json={
            'app_id':self.app_id,
            'app_secret':self.app_secret
            }
        r=requests.post(url,json=json, headers= {'Content-Type':'application/json;charset=UTF-8'}).json()
        if(r["code"]==0):
            return r["tenant_access_token"]
        else:
            print("获取飞书tenant_access_token失败",r)

        return ""
    
    def speech_to_text(self,file):
        s=""
        with open(file, 'rb') as fp:
            s = fp.read()
        speech = base64.b64encode(s).decode()
        json={
            "speech": {"speech":speech},
            "config":{
                "stream_id":secrets.token_hex(8),
                "sequence_id":0,
                "action":2,
                "format":"pcm",
                "engine_type":"16k_auto"
            }
        }
        headers= {'Content-Type':'application/json;charset=UTF-8',"Authorization":"Bearer "+self.tenant_access_token}
        url=self.base_url+"/open-apis/speech_to_text/v1/speech/stream_recognize"
        r=requests.post(url,json=json, headers= headers).json()
        print(r)
        if(r["code"]==0):
            return r["data"]["recognition_text"]
        
        return ""



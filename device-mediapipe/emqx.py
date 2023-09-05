import paho.mqtt.client as mqtt
import cv2
import random
import re
import binascii
import numpy as np


# 连接成功回调
def on_connect(client, userdata, flags, rc):
    print('Connected with result code '+str(rc))
    client.subscribe("$sys/+/+/image/post")

# 消息接收回调  https://www.jianshu.com/p/29b8f179182c
def on_message(client, userdata, msg):
    print("userdata",userdata)
    print("topic",msg.topic)
    # print("payload",msg.payload)
    
    pattern=re.compile('sys/(.+)/(.+)/image/post')   #匹配ab与ef之间的内容
    match=pattern.findall(msg.topic)
    if match:
        print("productid",match[0][0])
        print("clientid",match[0][1])
        # with open("data/test.png","rb") as f:
        #     content=f.read()
        #     print(binascii.hexlify(content))

        # payload=msg.payload
        # frame =cv2.imread("data/test.png")
        # payload=frame.tobytes()
        # data=np.frombuffer(payload,dtype=np.uint8)
        # img = data.reshape(192, 192, 3)
        # # img=cv2.imdecode(data,cv2.IMREAD_COLOR)
        # cv2.imshow("esp32cam", img)
        # cv2.waitKey(1)

        data=msg.payload
        data=data.strip()
        data=data.replace(' ', '')
        data=data.replace('\n', '')
        data = binascii.a2b_hex(data)
        with open('data/image.jpg', 'wb') as f:
            f.write(data)
        img = cv2.imread('data/image.jpg')
        cv2.imshow("arm_camera", img)
        cv2.waitKey(1)

def main():
    client_id = f'python-mqtt-{random.randint(0, 1000)}'  # 客户端id不能重复
    username = "thingscc"
    password = "1qaz@WSX"
    client = mqtt.Client(client_id)
    client.username_pw_set(username, password)
    # 指定回调函数
    client.on_connect = on_connect
    client.on_message = on_message

    # 建立连接
    client.connect('emqx.thingscc.com', 1883, 60)
    # 发布消息
    client.publish('python-mqtt',payload='Hello World',qos=0)

    
   
    client.loop_forever()
    # 运行一个线程来自动调用loop()处理网络事件, 非阻塞
    # client.loop_start()


if __name__ == '__main__':
    main()




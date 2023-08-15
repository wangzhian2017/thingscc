import paho.mqtt.client as mqtt
import cv2
import random

# 连接成功回调
def on_connect(client, userdata, flags, rc):
    print('Connected with result code '+str(rc))
    client.subscribe('testtopic/#')

# 消息接收回调
def on_message(client, userdata, msg):
    print(userdata)
    print(msg.topic+" "+str(msg.payload))

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

    # client.loop_forever()
    # 运行一个线程来自动调用loop()处理网络事件, 非阻塞
    client.loop_start()


if __name__ == '__main__':
    main()




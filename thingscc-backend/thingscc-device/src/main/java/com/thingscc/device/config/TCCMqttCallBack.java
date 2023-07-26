package com.thingscc.device.config;

import org.eclipse.paho.client.mqttv3.IMqttAsyncClient;
import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.MqttCallback;
import org.eclipse.paho.client.mqttv3.MqttMessage;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;

@Configuration
public class TCCMqttCallBack implements MqttCallback {

    @Value("${spring.mqtt.client.id}")
    private String clientId;

    /**
     * 与服务器断开连接的回调
     * @author xct
     * @param throwable
     * @return void
     * @date 2021/7/30 16:19
     */
    @Override
    public void connectionLost(Throwable throwable) {
        System.out.println(clientId + "与服务器断开连接");
    }

    /**
     * 消息到达的回调
     * @author xct
     * @param topic
     * @param message
     * @return void
     * @date 2021/7/30 16:19
     */
    @Override
    public void messageArrived(String topic, MqttMessage message) throws Exception {
        System.out.println(String.format("接收消息主题 : %s",topic));
        System.out.println(String.format("接收消息Qos : %d",message.getQos()));
        System.out.println(String.format("接收消息内容 : %s",new String(message.getPayload())));
        System.out.println(String.format("接收消息retained : %b",message.isRetained()));
    }

    /**
     * 消息发布成功的回调
     * @author xct
     * @param iMqttDeliveryToken
     * @return void
     * @date 2021/7/30 16:20
     */
    @Override
    public void deliveryComplete(IMqttDeliveryToken iMqttDeliveryToken) {
        IMqttAsyncClient client = iMqttDeliveryToken.getClient();
        System.out.println(client.getClientId() + "发布消息成功！");
    }
}

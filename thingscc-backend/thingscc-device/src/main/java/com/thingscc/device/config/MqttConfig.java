package com.thingscc.device.config;

import org.eclipse.paho.client.mqttv3.*;
import org.eclipse.paho.client.mqttv3.persist.MemoryPersistence;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;

import javax.annotation.PostConstruct;

@Configuration
public class MqttConfig {
    @Value("${spring.mqtt.username}")
    private String username;

    @Value("${spring.mqtt.password}")
    private String password;

    @Value("${spring.mqtt.url}")
    private String hostUrl;

    @Value("${spring.mqtt.client.id}")
    private String clientId;

    @Value("${spring.mqtt.default.topic}")
    private String defaultTopic;

    /**
     * 客户端对象
     */
    private MqttClient client;

    /**
     * 客户端连接服务端
     * @author xct
     * @param
     * @return void
     * @date 2021/7/30 16:01
     */

    public void connect() throws MqttException {

            //创建MQTT客户端对象
            client = new MqttClient(hostUrl,clientId,new MemoryPersistence());
            //连接设置
            MqttConnectOptions options = new MqttConnectOptions();
            //是否清空session，设置为false表示服务器会保留客户端的连接记录（订阅主题，qos），客户端重连之后能获取到服务器在客户端断开连接期间推送的消息
            //设置为true表示每次连接到服务端都是以新的身份
            options.setCleanSession(true);
            //设置连接用户名
            options.setUserName(username);
            //设置连接密码
            options.setPassword(password.toCharArray());
            //设置超时时间，单位为秒
            options.setConnectionTimeout(100);
            //设置心跳时间 单位为秒，表示服务器每隔1.5*20秒的时间向客户端发送心跳判断客户端是否在线
            options.setKeepAliveInterval(20);
            //设置遗嘱消息的话题，若客户端和服务器之间的连接意外断开，服务器将发布客户端的遗嘱信息
            options.setWill("willTopic",(clientId + "与服务器断开连接").getBytes(),0,false);
            //设置回调
            client.setCallback(new TCCMqttCallBack());
            client.connect(options);

    }

    public void publish(int qos,boolean retained,String topic,String message) throws MqttException {
        MqttMessage mqttMessage = new MqttMessage();
        mqttMessage.setQos(qos);
        mqttMessage.setRetained(retained);
        mqttMessage.setPayload(message.getBytes());
        //主题目的地，用于发布/订阅消息
        MqttTopic mqttTopic = client.getTopic(topic);
        //提供一种机制来跟踪消息的传递进度。
        //用于在以非阻塞方式（在后台运行）执行发布时跟踪消息的传递进度
        MqttDeliveryToken token;

            //将指定消息发布到主题，但不等待消息传递完成。返回的token可用于跟踪消息的传递状态。
            //一旦此方法干净地返回，消息就已被客户端接受发布。当连接可用时，将在后台完成消息传递。
            token = mqttTopic.publish(mqttMessage);
            token.waitForCompletion();

    }

    /**
     * 断开连接
     * @author xct
     * @param
     * @return void
     * @date 2021/8/2 09:30
     */
    public void disConnect(){
        try {
            client.disconnect();
        } catch (MqttException e) {
            e.printStackTrace();
        }
    }


    /**
     * 订阅主题
     * @author xct
     * @param topic
     * @param qos
     * @return void
     * @date 2021/7/30 17:12
     */
    public void subscribe(String topic,int qos){
        try {
            client.subscribe(topic,qos);
        } catch (MqttException e) {
            e.printStackTrace();
        }
    }

    /**
     * 在bean初始化后连接到服务器
     * @author xct
     * @param
     * @return void
     * @date 2021/7/30 16:48
     */
    @PostConstruct
    public void init(){
        try {
            connect();
            subscribe(clientId+"/#",0);

        } catch (MqttException e) {
            e.printStackTrace();
        }

    }
}

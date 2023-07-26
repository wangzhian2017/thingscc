#ifndef OneNET_h
#define OneNET_h

#include <WiFi.h>
#include <PubSubClient.h>
#include "arm/Arm.h"

//设备上传数据的post主题
#define ONENET_TOPIC_PROP_POST "$sys/%s/%s/thing/property/post"
//接收下发属性设置主题
#define ONENET_TOPIC_PROP_SET "$sys/%s/%s/thing/property/set"
//接收下发属性设置成功的回复主题
#define ONENET_TOPIC_PROP_SET_REPLY "$sys/%s/%s/thing/property/set_reply"
//接收设备属性获取命令主题
#define ONENET_TOPIC_PROP_GET "$sys/%s/%s/thing/property/get"
//接收设备属性获取命令成功的回复主题
#define ONENET_TOPIC_PROP_GET_REPLY "$sys/%s/%s/thing/property/get_reply"
//设备期望值获取请求主题
#define ONENET_TOPIC_DESIRED_GET "$sys/%s/%s/thing/property/desired/get"
//设备期望值获取响应主题
#define ONENET_TOPIC_DESIRED_GET_RE "$sys/%s/%s/thing/property/desired/get/reply"
//设备期望值删除请求主题
#define ONENET_TOPIC_DESIRED_DEL "$sys/%s/%s/thing/property/desired/delete"
//设备期望值删除响应主题
#define ONENET_TOPIC_DESIRED_DEL_RE "$sys/%s/%s/thing/property/desired/delete/reply"
//抓住  平台调用直连设备服务(下发数据并期望设备执行完成后给出响应)
#define ONENET_TOPIC_SERVICE_GRAB "$sys/%s/%s/thing/service/grab/invoke"
#define ONENET_TOPIC_SERVICE_GRAB_RE "$sys/%s/%s/thing/service/grab/invoke_reply"
//上抬
#define ONENET_TOPIC_SERVICE_UPLIFT "$sys/%s/%s/thing/service/uplift/invoke"
#define ONENET_TOPIC_SERVICE_UPLIFT_RE "$sys/%s/%s/thing/service/uplift/invoke_reply"
//下放
#define ONENET_TOPIC_SERVICE_PUTDOWN "$sys/%s/%s/thing/service/putdown/invoke"
#define ONENET_TOPIC_SERVICE_PUTDOWN_RE "$sys/%s/%s/thing/service/putdown/invoke_reply"
//左转
#define ONENET_TOPIC_SERVICE_TURNLEFT "$sys/%s/%s/thing/service/turnleft/invoke"
#define ONENET_TOPIC_SERVICE_TURNLEFT_RE "$sys/%s/%s/thing/service/turnleft/invoke_reply"
//左转
#define ONENET_TOPIC_SERVICE_TURNRIGHT "$sys/%s/%s/thing/service/turnright/invoke"
#define ONENET_TOPIC_SERVICE_TURNRIGHT_RE "$sys/%s/%s/thing/service/turnright/invoke_reply"
//前倾
#define ONENET_TOPIC_SERVICE_FORERAKE "$sys/%s/%s/thing/service/forerake/invoke"
#define ONENET_TOPIC_SERVICE_FORERAKE_RE "$sys/%s/%s/thing/service/forerake/invoke_reply"
//后仰
#define ONENET_TOPIC_SERVICE_TILTBACK "$sys/%s/%s/thing/service/tiltback/invoke"
#define ONENET_TOPIC_SERVICE_TILTBACK_RE "$sys/%s/%s/thing/service/tiltback/invoke_reply"

//这是post上传数据使用的模板
#define ONENET_POST_BODY_FORMAT "{\"id\":\"%u\",\"version\":\"1.0\",\"params\":%s}"

class OneNET
{
private:
    const char *mqtt_server = "mqtts.heclouds.com"; //onenet 的 IP地址
    const int mqtt_port = 1883;// port of MQTT over TCP
    const char *client_id;
    const char *user_name;
    const char *token;
    PubSubClient mqtt_client;
    int postMsgId = 0;
public:
    OneNET(const char *client_id,const char *user_name,const char *token,WiFiClient& wifi);
    ~OneNET();

    bool isConnected();
    void connect();
    void subscribe();
    
    void setMQTTCallback(MQTT_CALLBACK_SIGNATURE);
    void callback(char *topic, byte *payload, unsigned int length,Arm arm);

    void sendArmReport(Arm arm);
    void getDesired();
    
    void loop();
};






#endif
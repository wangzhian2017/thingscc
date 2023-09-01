#ifndef MQTT_h
#define MQTT_h

#include <WiFi.h>
#include <PubSubClient.h>

//设备上传图片数据的post主题
#define TOPIC_IMAGE_POST "$sys/%s/%s/image/post"

class MQTT{
private:
    const char *mqtt_server = "emqx.thingscc.com"; //mqtt服务 的 IP地址
    const int mqtt_port = 1883;// port of MQTT over TCP
    const char *client_id;
    const char *user_name;
    const char *password;
    PubSubClient mqtt_client;
    WiFiClient espClient;
public:
    MQTT(const char *client_id,const char *user_name,const char *password);
    ~MQTT();

    bool isConnected();
    void connect();
    void subscribe();
    void publish(const char* topic, String msg);

    void sendImage(String content);
    void sendImage(uint8_t * buf,size_t len);
};



#endif
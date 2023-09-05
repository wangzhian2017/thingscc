#include "mqtt.h"


MQTT::MQTT(const char *client_id,const char *user_name,const char *password){
    this->client_id=client_id;
    this->user_name=user_name;
    this->password=password;

    this->mqtt_client.setClient(espClient);
    this->mqtt_client.setServer(this->mqtt_server, this->mqtt_port);                   //设置客户端连接的服务器,连接MQTT服务器
    this->mqtt_client.connect(this->client_id, this->user_name, this->password); //客户端连接到指定的产品的指定设备.同时输入鉴权信息
    if (this->mqtt_client.connected())
    {
        Serial.println("MQTT is connected!"); //判断以下是不是连好了.
    }else{
        Serial.println("MQTT connect failed!"); 
        Serial1.println(this->mqtt_client.state());
    }
}

MQTT::~MQTT()
{
   
}

bool MQTT::isConnected(){
    return mqtt_client.connected();
}

void MQTT::connect(){
    while (!(this->mqtt_client.connected())) //再重连客户端
    {
        Serial.println("reconnect MQTT...");
        
        if ( this->mqtt_client.connect(this->client_id, this->user_name, this->password))
        {
            Serial.println("mqtt connected");
        }
        else
        {
            Serial.println("mqtt connect failed");
            Serial.println(this->mqtt_client.state());
            Serial.println("try again in 5 sec");
            delay(5000);
        }
    }
}

void MQTT::subscribe(){
    Serial.println("subscribe topics:");

}

void MQTT::publish(const char* topic, String msg){
    // this->mqtt_client.publish(topic,payload);
    this->mqtt_client.beginPublish(topic,msg.length(),0);
    this->mqtt_client.print(msg);
    this->mqtt_client.endPublish();
}

void MQTT::sendImage(String content){
    char topic[300];
    sprintf(topic, TOPIC_IMAGE_POST, this->user_name, this->client_id);
    
    int content_len=content.length();
    int pkg_size=200;
    int pkg_num=content_len/pkg_size;
    this->mqtt_client.beginPublish(topic,content_len,true);
    for(int i=0;i<pkg_num;i++){
        this->mqtt_client.print(content.substring(i*pkg_size,(i+1)*pkg_size));
    }
    this->mqtt_client.print(content.substring(pkg_num*pkg_size));
    this->mqtt_client.endPublish();
}

void MQTT::sendImage(uint8_t * buf,size_t len){
    char topic[300];
    sprintf(topic, TOPIC_IMAGE_POST, this->user_name, this->client_id);
    int pkg_size=200;
    int pkg_total=len/pkg_size;
    if(len%pkg_size>0){
        pkg_total+=1;
    }
    char msg[300];
    sprintf(msg, "{'pkg_size':%d,'pkg_total':%d}",pkg_size, pkg_total);
    this->mqtt_client.publish(topic,msg);

    int sent_len=0;
    while (len>sent_len)
    {
        buf+=sent_len;
        if(len-sent_len>pkg_size){
            this->mqtt_client.publish(topic,buf,pkg_size);
        }else{
            this->mqtt_client.publish(topic,buf,len-sent_len);
        }
        sent_len+=pkg_size;
    }
    this->mqtt_client.publish(topic,"end");
    
    Serial.println(topic);
}



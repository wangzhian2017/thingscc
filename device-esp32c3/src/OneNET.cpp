#include "OneNET.h"
#include "ArduinoJson.h"


OneNET::OneNET(const char *client_id,const char *user_name,const char *token,WiFiClient& wifi)
{
    this->client_id=client_id;
    this->user_name=user_name;
    this->token=token;

    this->mqtt_client.setClient(wifi);
    this->mqtt_client.setServer(this->mqtt_server, this->mqtt_port);                   //设置客户端连接的服务器,连接Onenet服务器, 使用6002端口
    this->mqtt_client.connect(this->client_id, this->user_name, this->token); //客户端连接到指定的产品的指定设备.同时输入鉴权信息
    if (this->mqtt_client.connected())
    {
        Serial.println("MQTT is connected!"); //判断以下是不是连好了.
    }else{
        Serial.println("MQTT connect failed!"); 
        Serial1.println(this->mqtt_client.state());
    }
}

OneNET::~OneNET()
{
}

bool OneNET::isConnected(){
    return mqtt_client.connected();
}

void OneNET::connect(){
    while (!(this->mqtt_client.connected())) //再重连客户端
    {
        Serial.println("reconnect MQTT...");
        
        if ( this->mqtt_client.connect(this->client_id, this->user_name, this->token))
        {
        Serial.println("connected");
        }
        else
        {
        Serial.println("failed");
        Serial.println(this->mqtt_client.state());
        Serial.println("try again in 5 sec");
        delay(5000);
        }
    }
}
void OneNET::subscribe(){
    Serial.println("subscribe topics:");
    char topic[300];
    sprintf(topic, ONENET_TOPIC_PROP_SET, this->user_name, this->client_id);
    Serial.println(topic);
    this->mqtt_client.subscribe(topic);
    sprintf(topic, ONENET_TOPIC_PROP_GET, this->user_name, this->client_id);
    Serial.println(topic);
    this->mqtt_client.subscribe(topic);
    sprintf(topic, ONENET_TOPIC_SERVICE_GRAB, this->user_name, this->client_id);
    Serial.println(topic);
    this->mqtt_client.subscribe(topic);
    sprintf(topic, ONENET_TOPIC_SERVICE_LIFT, this->user_name, this->client_id);
    Serial.println(topic);
    this->mqtt_client.subscribe(topic);
    sprintf(topic, ONENET_TOPIC_SERVICE_ROTATE, this->user_name, this->client_id);
    Serial.println(topic);
    this->mqtt_client.subscribe(topic);
    sprintf(topic, ONENET_TOPIC_SERVICE_BACKFORWARD, this->user_name, this->client_id);
    Serial.println(topic);
    this->mqtt_client.subscribe(topic);
}
void OneNET::setMQTTCallback(MQTT_CALLBACK_SIGNATURE){
    Serial.println("setMQTTCallback begin");
    this->mqtt_client.setCallback(callback);
    Serial.println("setMQTTCallback end");
}
void OneNET::callback(char *topic, byte *payload, unsigned int length,Arm arm){
    Serial.println("message rev:");
    Serial.println(topic);
    for (size_t i = 0; i < length; i++)
    {
        Serial.print((char)payload[i]);
    }
    Serial.println("");

    //解析回调数据 josn
    DynamicJsonDocument doc(100);
    DeserializationError error = deserializeJson(doc, payload);
    if (error)
    {
        Serial.println("parse json failed");
        return;
    }
    JsonObject objJSON = doc.as<JsonObject>();
    serializeJsonPretty(objJSON, Serial);

    char target[300];
    char re[300];
    sprintf(target, ONENET_TOPIC_PROP_SET, this->user_name, this->client_id);
    if (strstr(topic, target)){
        String id = objJSON["id"];
        Serial.println(id);
        char sendbuf[100];
        sprintf(sendbuf, "{\"id\": \"%s\",\"code\":200,\"msg\":\"success\"}", id.c_str());
        Serial.println(sendbuf);
        sprintf(re, ONENET_TOPIC_PROP_SET_REPLY, this->user_name, this->client_id);
        this->mqtt_client.publish(re, sendbuf);
    }
    sprintf(target, ONENET_TOPIC_PROP_GET, this->user_name, this->client_id);
    if (strstr(topic, target))
    {
        String id = objJSON["id"];
        Serial.println(id);
        char sendbuf[100];
        sprintf(sendbuf, "{\"id\": \"%s\",\"code\":200,\"msg\":\"success\",\"data\":{\"motor_num\":%d}}", id.c_str(), 4);
        Serial.println(sendbuf);
        sprintf(re, ONENET_TOPIC_PROP_GET_REPLY, this->user_name, this->client_id);
        this->mqtt_client.publish(re, sendbuf);
    }
    sprintf(target, ONENET_TOPIC_DESIRED_GET, this->user_name, this->client_id);
    if (strstr(topic, target))
    {
        String str = objJSON["data"]["motor_num"]["value"];
        Serial.println(str);
    }
    sprintf(target, ONENET_TOPIC_SERVICE_GRAB, this->user_name, this->client_id);
    if (strstr(topic, target))
    {
        String id = objJSON["id"];
        Serial.println(id);
        String s=objJSON["params"]["angle"];
        float angle=s.toFloat();
        float ret=arm.grab(angle);
        
        char sendbuf[100];
        sprintf(sendbuf, "{\"id\": \"%s\",\"code\":200,\"msg\":\"success\",\"data\":{\"result\":%s}}", id.c_str(), "true");
        Serial.println(sendbuf);
        sprintf(re, ONENET_TOPIC_SERVICE_GRAB_RE, this->user_name, this->client_id);
        this->mqtt_client.publish(re, sendbuf);
    }
    sprintf(target, ONENET_TOPIC_SERVICE_LIFT, this->user_name, this->client_id);
    if (strstr(topic, target))
    {
        String id = objJSON["id"];
        Serial.println(id);
        String s=objJSON["params"]["angle"];
        float angle=s.toFloat();
        float ret=arm.lift(angle);

        char sendbuf[100];
        sprintf(sendbuf, "{\"id\": \"%s\",\"code\":200,\"msg\":\"success\",\"data\":{\"result\":%f}}", id.c_str(), ret);
        Serial.println(sendbuf);
        sprintf(re, ONENET_TOPIC_SERVICE_LIFT_RE, this->user_name, this->client_id);
        this->mqtt_client.publish(re, sendbuf);
    }
    sprintf(target, ONENET_TOPIC_SERVICE_ROTATE, this->user_name, this->client_id);
    if (strstr(topic, target))
    {
        String id = objJSON["id"];
        Serial.println(id);
        String s=objJSON["params"]["angle"];
        float angle=s.toFloat();
        float ret=arm.rotate(angle);
        
        char sendbuf[100];
        sprintf(sendbuf, "{\"id\": \"%s\",\"code\":200,\"msg\":\"success\",\"data\":{\"result\":%f}}", id.c_str(), ret);
        Serial.println(sendbuf);
        sprintf(re, ONENET_TOPIC_SERVICE_ROTATE_RE, this->user_name, this->client_id);
        this->mqtt_client.publish(re, sendbuf);
    }
    sprintf(target, ONENET_TOPIC_SERVICE_BACKFORWARD, this->user_name, this->client_id);
    if (strstr(topic, target))
    {
        String id = objJSON["id"];
        Serial.println(id);
        String s=objJSON["params"]["angle"];
        float angle=s.toFloat();
        float ret=arm.backforward(angle);

        char sendbuf[100];
        sprintf(sendbuf, "{\"id\": \"%s\",\"code\":200,\"msg\":\"success\",\"data\":{\"result\":%f}}", id.c_str(), ret);
        Serial.println(sendbuf);
        sprintf(re, ONENET_TOPIC_SERVICE_BACKFORWARD_RE, this->user_name, this->client_id);
        this->mqtt_client.publish(re, sendbuf);
    }
}

void OneNET::sendArmReport(Arm arm){
    if (this->mqtt_client.connected())
    {
        //先拼接出json字符串
        char param[255];
        char jsonBuf[255];
        sprintf(param, "{\"motor_num\":{\"value\":%d},\"angle_grab\":{\"value\":%.2f},\"angle_lift\":{\"value\":%.2f},\"angle_backforward\":{\"value\":%.2f},\"angle_rotate\":{\"value\":%.2f}}", 
                        4,
                        arm.getGrabAngle(),
                        arm.getLiftAngle(),
                        arm.getBackforwardAngle(),
                        arm.getRotateAngle()); //我们把要上传的数据写在param里
        postMsgId += 1;
        sprintf(jsonBuf, ONENET_POST_BODY_FORMAT, postMsgId, param);
        Serial.println("Post message to cloud: ");
        Serial.println(ONENET_TOPIC_PROP_POST);
        Serial.println(jsonBuf);
        //再从mqtt客户端中发布post消息
        char topic[300];
        sprintf(topic, ONENET_TOPIC_PROP_POST, this->user_name, this->client_id);
        if (this->mqtt_client.publish(topic, jsonBuf))
        {
        Serial.println("Publish message to cloud success!");
        }
        else
        {
        Serial.println("Publish message to cloud failed!");
        }
    }
}

void OneNET::getDesired()
{
    if (this->mqtt_client.connected())
    {
        //先拼接出json字符串
        char param[82];
        char jsonBuf[178];
        sprintf(param, "[\"motor_model\",\"motor_num\"]"); //我们把要上传的数据写在param里
        postMsgId += 1;
        sprintf(jsonBuf, ONENET_POST_BODY_FORMAT, postMsgId, param);
        //再从mqtt客户端中发布post消息
        char topic[300];
        sprintf(topic, ONENET_TOPIC_DESIRED_GET, this->user_name, this->client_id);
        if (this->mqtt_client.publish(topic, jsonBuf))
        {
        Serial.print("Post message to cloud: ");
        Serial.println(jsonBuf);
        }
        else
        {
        Serial.println("Publish message to cloud failed!");
        }
    }
}

void OneNET::loop(){
    this->mqtt_client.loop();
}

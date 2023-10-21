#include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include "Ticker.h"
#include "arm/Arm.h"
#include "OneNET.h"

const char *ssid = "DI-WANGZHIAN";    //wifi名
const char *password = "13580416614";      //wifi密码

#define mqtt_clientid "esp32c3" //设备名称
#define mqtt_username "iqDUVzCjyD"    //产品ID

//鉴权信息
//#define mqtt_password "version=2018-10-31&res=products%2FiqDUVzCjyD%2Fdevices%2Fesp32c3&et=1697727629&method=sha1&sign=kI1W4UKGFq8B10XejD%2BpYDWsh4c%3D" //鉴权信息
#define device_key "V1pqR1doaXpKTjRTbVFkWW5mcXRCUTZXMkZmeHdxVmQ="
// #define token_url "http://master.thingscc.com:8080/device/onnet/token/" mqtt_username "/" mqtt_clientid "/" device_key
#define token_url "https://ncoa-dev.cmhktry.com/gateway/smallfeat/OneNet/token/" mqtt_username "/" mqtt_clientid "/" device_key


WiFiClient espClient;

Ticker tim1;                    //定时器,用来循环上传数据


int angle_grab=90;
int angle_lift=90;
int angle_rotate=90;
int angle_backforward=90;
int speed=1;

OneNET *oneNET;
Arm arm;

// 连接WIFI相关函数
void setupWifi()
{
    Serial.print("WIFI connecting");
    WiFi.begin(ssid, password);
    while (!WiFi.isConnected())
    {
        Serial.print(".");
        delay(1000);
    }
    Serial.println();
    Serial.print("Wifi connected!");
    Serial.println(WiFi.localIP());
}

String getOneNetToken(){
    String response;
    HTTPClient http;
    if (http.begin(token_url))
    {
        if(http.GET()==HTTP_CODE_OK){
            response=http.getString();
            Serial.println("get onnet token:"+response);
        }else{
             Serial.println("get onnet token failed");
        }
    }
    http.end();


    DynamicJsonDocument doc(1000);
    DeserializationError error = deserializeJson(doc, response);
    if (error)
    {
        Serial.println("parse token json failed");
        return "";
    }
    JsonObject obj = doc.as<JsonObject>();
    serializeJsonPretty(obj, Serial);
    String str = obj["msg"];
    
    return str;
}

void callback(char *topic, byte *payload, unsigned int length) {
    oneNET->callback(topic,payload,length,arm);
}

void getDesired()
{
  oneNET->getDesired();
}

//向主题发送数据
void sendMotorInfo()
{
    oneNET->sendArmReport(arm);
}

// the setup function runs once when you press reset or power the board
void setup() {
    Serial.begin(115200);
    setupWifi();

    arm.initialization(angle_grab,angle_lift,angle_rotate,angle_backforward);
    
    String oneNetToken=getOneNetToken();
    Serial.println(oneNetToken);
    oneNET = new OneNET(mqtt_clientid,mqtt_username,oneNetToken.c_str(),espClient);
    oneNET->subscribe();
    oneNET->setMQTTCallback(callback);

    tim1.attach(60, sendMotorInfo); //定时每60秒调用一次发送数据函数sendMotorInfo
    //tim1.attach(20, getDesired); //定时每20秒调用一次
}

// the loop function runs over and over again forever
void loop() {
    if (!WiFi.isConnected()) //先看WIFI是否还在连接
    {
        setupWifi();
    }
    if (!(oneNET->isConnected())) //如果客户端没连接ONENET, 重新连接
    {
        Serial.println("oneNET connect");
        oneNET->connect();
        delay(1000);
    }

    arm.act();
    delay(50);
    oneNET->loop(); //客户端循环检测
}


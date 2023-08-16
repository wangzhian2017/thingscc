#include <Arduino.h>
#include <WiFi.h>
#include <esp_camera.h>
#include "mqtt.h"


const char *ssid = "DI-WANGZHIAN";    //wifi名
const char *password = "13580416614";      //wifi密码

#define mqtt_clientid "esp32cam" //设备名称
#define mqtt_username "thingscc"    
#define mqtt_password "1qaz@WSX"    

#define CAM_PIN_PWDN 32
#define CAM_PIN_RESET -1 //software reset will be performed
#define CAM_PIN_XCLK 0
#define CAM_PIN_SIOD 26
#define CAM_PIN_SIOC 27
#define CAM_PIN_D7 35
#define CAM_PIN_D6 34
#define CAM_PIN_D5 39
#define CAM_PIN_D4 36
#define CAM_PIN_D3 21
#define CAM_PIN_D2 19
#define CAM_PIN_D1 18
#define CAM_PIN_D0 5
#define CAM_PIN_VSYNC 25
#define CAM_PIN_HREF 23
#define CAM_PIN_PCLK 22

WiFiClient espClient;
MQTT *mqtt;

// 连接WIFI相关函数
void wifi_connnet()
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

void camera_init() {
  // OV2640 camera module
  camera_config_t config{
    .pin_pwdn = CAM_PIN_PWDN,
    .pin_reset = CAM_PIN_RESET,
    .pin_xclk = CAM_PIN_XCLK,
    .pin_sccb_sda = CAM_PIN_SIOD,
    .pin_sccb_scl = CAM_PIN_SIOC,
    .pin_d7 = CAM_PIN_D7,
    .pin_d6 = CAM_PIN_D6,
    .pin_d5 = CAM_PIN_D5,
    .pin_d4 = CAM_PIN_D4,
    .pin_d3 = CAM_PIN_D3,
    .pin_d2 = CAM_PIN_D2,
    .pin_d1 = CAM_PIN_D1,
    .pin_d0 = CAM_PIN_D0,
    .pin_vsync = CAM_PIN_VSYNC,
    .pin_href = CAM_PIN_HREF,
    .pin_pclk = CAM_PIN_PCLK,
    //XCLK 20MHz or 10MHz for OV2640 double FPS (Experimental)
    .xclk_freq_hz = 20000000,
    .ledc_timer = LEDC_TIMER_0,
    .ledc_channel = LEDC_CHANNEL_0,
    .pixel_format = PIXFORMAT_RGB565, //YUV422,GRAYSCALE,RGB565,JPEG
    .frame_size = FRAMESIZE_QVGA,    //QQVGA-UXGA, For ESP32, do not use sizes above QVGA when not JPEG. The performance of the ESP32-S series has improved a lot, but JPEG mode always gives better frame rates.
    .jpeg_quality = 12, //0-63, for OV series camera sensors, lower number means higher quality
    .fb_count = 1,       //When jpeg mode is used, if fb_count more than one, the driver will work in continuous mode.
    .grab_mode = CAMERA_GRAB_WHEN_EMPTY,
  };
  esp_err_t err = esp_camera_init(&config);
  Serial.printf("esp_camera_init: 0x%x\n", err);


  // sensor_t *s = esp_camera_sensor_get();
  // s->set_framesize(s, FRAMESIZE_QVGA);
}


void snap(){
  camera_fb_t *pic = esp_camera_fb_get();
  if (pic){
    Serial.printf("width: %d, height: %d, buf: 0x%x, len: %d\n", pic->width, pic->height, pic->buf, pic->len);
    String msg="";
    for (int i = 0; i < pic->len; i++){
        char data[4104];
        sprintf(data, "%02X", *((pic->buf + i)));
        msg += data;
    }
    if (msg.length() > 0){
        mqtt->sendImage(msg);
    }
    esp_camera_fb_return(pic);
  }
}

void setup() {
    Serial.begin(115200);
    wifi_connnet();
    mqtt = new MQTT(mqtt_clientid,mqtt_username,mqtt_password,espClient);

    camera_init();
}

void loop() {
  if (!WiFi.isConnected()) //先看WIFI是否还在连接
  {
      wifi_connnet();
  }
  if (!(mqtt->isConnected())) //如果客户端没连接MQTT, 重新连接
  {
      Serial.println("oneNET connect");
      mqtt->connect();
      delay(1000);
  }

  snap();

  delay(1000); 
}

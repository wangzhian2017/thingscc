package com.thingscc.device.controller;

import com.thingscc.common.core.domain.AjaxResult;
import com.thingscc.device.config.MqttConfig;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import static com.thingscc.common.core.domain.AjaxResult.success;

@RestController
@RequestMapping("/device/mqtt")
public class MqttController {

    @Autowired
    private MqttConfig providerClient;

    @RequestMapping("/sendMessage")
    public AjaxResult sendMessage(String topic, String message,int qos, boolean retained) throws MqttException {
        providerClient.publish(qos, retained, topic, message);
        return success("发送成功");
    }


}

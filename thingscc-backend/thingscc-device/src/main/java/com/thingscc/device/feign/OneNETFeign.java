package com.thingscc.device.feign;

import com.thingscc.device.domain.*;
import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.stereotype.Component;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@Component
@FeignClient(name = "oneNETClient",url = "https://iot-api.heclouds.com")
public interface OneNETFeign {
    @GetMapping("/device/detail")
    OneNETResponse<OneNETDevice> GetDeviceInfo(@RequestHeader("authorization") String token,
                                                      @RequestParam(value = "product_id") String product_id,
                                                      @RequestParam(value = "device_name") String device_name);

    @PostMapping(value="/thingmodel/call-service")
    OneNETResponse<Map> CallService(@RequestHeader("authorization") String token,
                                                                @RequestBody OneNETServiceRequest<Map> request);
}

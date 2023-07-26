package com.thingscc.device.controller;

import com.thingscc.common.core.domain.AjaxResult;
import com.thingscc.device.domain.*;
import com.thingscc.device.feign.OneNETFeign;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.*;

import javax.annotation.Resource;
import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;
import java.io.UnsupportedEncodingException;
import java.net.URLEncoder;
import java.security.InvalidKeyException;
import java.security.NoSuchAlgorithmException;
import java.util.Base64;
import java.util.Map;

import static com.thingscc.common.core.domain.AjaxResult.error;
import static com.thingscc.common.core.domain.AjaxResult.success;

@RestController
@RequestMapping("/device/onnet")
public class OneNetController {

    @Resource
    private OneNETFeign oneNETFeign;

    @Value("${onnet.userid}")
    private String userid;
    @Value("${onnet.method}")
    private String method;
    @Value("${onnet.accessKey}")
    private String accessKey;


    @RequestMapping("/token/{product_id}/{device_name}/{key}")
    public AjaxResult getToken(@PathVariable String product_id
            ,@PathVariable String device_name
            ,@PathVariable String key)
            throws MqttException, UnsupportedEncodingException, NoSuchAlgorithmException, InvalidKeyException {
        String resource="products/"+product_id+"/devices/"+device_name;
        String expirationTime = System.currentTimeMillis() / 1000 + 100 * 24 * 60 * 60 + "";
        String version="2018-10-31";
        String token = assembleToken(version, resource, expirationTime, method.toLowerCase(), key);

        return success(token);
    }


    private String assembleToken(String version, String resourceName, String expirationTime, String signatureMethod, String accessKey)
            throws UnsupportedEncodingException, NoSuchAlgorithmException, InvalidKeyException {
        StringBuilder sb = new StringBuilder();
        String res = URLEncoder.encode(resourceName, "UTF-8");
        String sig = URLEncoder.encode(generatorSignature(version, resourceName, expirationTime, accessKey, signatureMethod), "UTF-8");
        sb.append("version=")
                .append(version)
                .append("&res=")
                .append(res)
                .append("&et=")
                .append(expirationTime)
                .append("&method=")
                .append(signatureMethod)
                .append("&sign=")
                .append(sig);
        return sb.toString();
    }

    private String generatorSignature(String version, String resourceName, String expirationTime, String accessKey, String signatureMethod)
            throws NoSuchAlgorithmException, InvalidKeyException {
        String encryptText = expirationTime + "\n" + signatureMethod + "\n" + resourceName + "\n" + version;
        String signature;
        byte[] bytes = HmacEncrypt(encryptText, accessKey, signatureMethod);
        signature = Base64.getEncoder().encodeToString(bytes);
        return signature;
    }

    private byte[] HmacEncrypt(String data, String key, String signatureMethod)
            throws NoSuchAlgorithmException, InvalidKeyException {
        //根据给定的字节数组构造一个密钥,第二参数指定一个密钥算法的名称
        SecretKeySpec signinKey = null;
        signinKey = new SecretKeySpec(Base64.getDecoder().decode(key),
                "Hmac" + signatureMethod.toUpperCase());

        //生成一个指定 Mac 算法 的 Mac 对象
        Mac mac = null;
        mac = Mac.getInstance("Hmac" + signatureMethod.toUpperCase());

        //用给定密钥初始化 Mac 对象
        mac.init(signinKey);

        //完成 Mac 操作
        return mac.doFinal(data.getBytes());
    }

    public enum SignatureMethod {
        SHA1, MD5, SHA256;
    }

    @RequestMapping("/info")
    public AjaxResult GetDeviceInfo(String product_id,String device_name) throws UnsupportedEncodingException, NoSuchAlgorithmException, InvalidKeyException {
        String expirationTime = System.currentTimeMillis() / 1000 + 100 * 24 * 60 * 60 + "";
        String token = assembleToken("2022-05-01", "userid/"+userid, expirationTime, method.toLowerCase(), accessKey);
        OneNETResponse<OneNETDevice> objOneNETResponse= oneNETFeign.GetDeviceInfo(token,product_id,device_name);
        if(objOneNETResponse.getCode()==0){
            return success(objOneNETResponse.getData());
        }

        return error(objOneNETResponse.getMsg()+objOneNETResponse.getCode());
    }

    @PostMapping("/service/{product_id}/{device_name}/{identifier}")
    public AjaxResult CallService(
            @PathVariable String product_id
            ,@PathVariable String device_name
            ,@PathVariable String identifier
            ,@RequestBody Map params)
            throws UnsupportedEncodingException, NoSuchAlgorithmException, InvalidKeyException {
        OneNETServiceRequest<Map> request=new OneNETServiceRequest<>();
        request.setProduct_id(product_id);
        request.setDevice_name(device_name);
        request.setIdentifier(identifier);
        request.setParams(params);

        String expirationTime = System.currentTimeMillis() / 1000 + 100 * 24 * 60 * 60 + "";
        String token = assembleToken("2022-05-01", "userid/"+userid, expirationTime, method.toLowerCase(), accessKey);
        OneNETResponse<Map> objOneNETResponse= oneNETFeign.CallService(token,request);
        if(objOneNETResponse.getCode()==0){
            return success(objOneNETResponse.getData());
        }

        return error(objOneNETResponse.getMsg()+objOneNETResponse.getCode());
    }
}

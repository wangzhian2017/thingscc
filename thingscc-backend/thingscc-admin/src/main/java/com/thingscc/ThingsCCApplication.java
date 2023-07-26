package com.thingscc;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.jdbc.DataSourceAutoConfiguration;
import org.springframework.cloud.openfeign.EnableFeignClients;

/**
 * 启动程序
 *
 * @author ruoyi
 */
@SpringBootApplication(exclude = { DataSourceAutoConfiguration.class })
@EnableFeignClients //启用OpenFeign
public class ThingsCCApplication {
    public static void main(String[] args)
    {
        // System.setProperty("spring.devtools.restart.enabled", "false");
        SpringApplication.run(ThingsCCApplication.class, args);
        System.out.println("(♥◠‿◠)ﾉﾞ  物联网控制中心启动成功   ლ(´ڡ`ლ)ﾞ " );
    }
}

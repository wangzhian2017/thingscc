package com.thingscc.device.domain;

import lombok.Data;

@Data
public class OneNETServiceRequest<T>  {
    private String product_id;

    private String device_name;

    private String identifier;

    private  T params;
}

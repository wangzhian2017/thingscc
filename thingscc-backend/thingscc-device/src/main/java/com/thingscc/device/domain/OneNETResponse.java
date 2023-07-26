package com.thingscc.device.domain;

import lombok.Data;

@Data
public class OneNETResponse<T> {
    private int code;

    private String msg;

    private String request_id;

    private  T data;
}

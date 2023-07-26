package com.thingscc.device.domain;

import lombok.Data;

import java.util.Date;
import java.util.List;

@Data
public class OneNETDevice {
    private String did;

    private String pid;

    private int access_pt;

    private int data_pt;

    private String name;

    private String desc;

    private int status;

    private Date create_time;

    private Date activate_time;

    private Date last_time;

    private String sec_key;

    private String imei;

    private String imsi;

    private String psk;

    private String auth_code;

    private int intelligent_way;

    private String group_id;

    private boolean enable_status;

    private List<String> tags;

    private String lon;

    private String lat;

    private boolean obsv;

    private boolean obsv_st;

    //private boolean private;

    private List<String> imsi_old;

    private Date imsi_mt;
}

package com.thingscc.device.domain;

import java.util.Date;
import com.fasterxml.jackson.annotation.JsonFormat;
import org.apache.commons.lang3.builder.ToStringBuilder;
import org.apache.commons.lang3.builder.ToStringStyle;
import com.thingscc.common.annotation.Excel;
import com.thingscc.common.core.domain.BaseEntity;

/**
 * 设备列表对象 iot_device
 * 
 * @author thingscc
 * @date 2023-07-05
 */
public class IotDevice extends BaseEntity
{
    private static final long serialVersionUID = 1L;

    /** 设置ID */
    private Long deviceId;

    /** 设备编号 */
    @Excel(name = "设备编号")
    private String deviceCode;

    /** 设备名称 */
    @Excel(name = "设备名称")
    private String deviceName;

    /** 分类 */
    @Excel(name = "分类")
    private Long catalogId;

    /** 接入时间 */
    @JsonFormat(pattern = "yyyy-MM-dd")
    @Excel(name = "接入时间", width = 30, dateFormat = "yyyy-MM-dd")
    private Date joinTime;

    /** 状态 */
    @Excel(name = "状态")
    private String status;

    public void setDeviceId(Long deviceId) 
    {
        this.deviceId = deviceId;
    }

    public Long getDeviceId() 
    {
        return deviceId;
    }
    public void setDeviceCode(String deviceCode) 
    {
        this.deviceCode = deviceCode;
    }

    public String getDeviceCode() 
    {
        return deviceCode;
    }
    public void setDeviceName(String deviceName) 
    {
        this.deviceName = deviceName;
    }

    public String getDeviceName() 
    {
        return deviceName;
    }
    public void setCatalogId(Long catalogId) 
    {
        this.catalogId = catalogId;
    }

    public Long getCatalogId() 
    {
        return catalogId;
    }
    public void setJoinTime(Date joinTime) 
    {
        this.joinTime = joinTime;
    }

    public Date getJoinTime() 
    {
        return joinTime;
    }
    public void setStatus(String status) 
    {
        this.status = status;
    }

    public String getStatus() 
    {
        return status;
    }

    @Override
    public String toString() {
        return new ToStringBuilder(this,ToStringStyle.MULTI_LINE_STYLE)
            .append("deviceId", getDeviceId())
            .append("deviceCode", getDeviceCode())
            .append("deviceName", getDeviceName())
            .append("catalogId", getCatalogId())
            .append("joinTime", getJoinTime())
            .append("status", getStatus())
            .toString();
    }
}

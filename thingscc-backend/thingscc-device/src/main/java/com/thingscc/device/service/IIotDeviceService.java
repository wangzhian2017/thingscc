package com.thingscc.device.service;

import java.util.List;
import com.thingscc.device.domain.IotDevice;

/**
 * 设备列表Service接口
 * 
 * @author thingscc
 * @date 2023-07-05
 */
public interface IIotDeviceService 
{
    /**
     * 查询设备列表
     * 
     * @param deviceId 设备列表主键
     * @return 设备列表
     */
    public IotDevice selectIotDeviceByDeviceId(Long deviceId);

    /**
     * 查询设备列表列表
     * 
     * @param iotDevice 设备列表
     * @return 设备列表集合
     */
    public List<IotDevice> selectIotDeviceList(IotDevice iotDevice);

    /**
     * 新增设备列表
     * 
     * @param iotDevice 设备列表
     * @return 结果
     */
    public int insertIotDevice(IotDevice iotDevice);

    /**
     * 修改设备列表
     * 
     * @param iotDevice 设备列表
     * @return 结果
     */
    public int updateIotDevice(IotDevice iotDevice);

    /**
     * 批量删除设备列表
     * 
     * @param deviceIds 需要删除的设备列表主键集合
     * @return 结果
     */
    public int deleteIotDeviceByDeviceIds(Long[] deviceIds);

    /**
     * 删除设备列表信息
     * 
     * @param deviceId 设备列表主键
     * @return 结果
     */
    public int deleteIotDeviceByDeviceId(Long deviceId);
}

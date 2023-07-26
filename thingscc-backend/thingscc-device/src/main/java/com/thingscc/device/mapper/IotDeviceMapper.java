package com.thingscc.device.mapper;

import java.util.List;
import com.thingscc.device.domain.IotDevice;

/**
 * 设备列表Mapper接口
 * 
 * @author thingscc
 * @date 2023-07-05
 */
public interface IotDeviceMapper 
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
     * 删除设备列表
     * 
     * @param deviceId 设备列表主键
     * @return 结果
     */
    public int deleteIotDeviceByDeviceId(Long deviceId);

    /**
     * 批量删除设备列表
     * 
     * @param deviceIds 需要删除的数据主键集合
     * @return 结果
     */
    public int deleteIotDeviceByDeviceIds(Long[] deviceIds);
}

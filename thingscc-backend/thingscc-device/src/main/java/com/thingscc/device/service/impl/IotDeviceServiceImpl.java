package com.thingscc.device.service.impl;

import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.thingscc.device.mapper.IotDeviceMapper;
import com.thingscc.device.domain.IotDevice;
import com.thingscc.device.service.IIotDeviceService;

/**
 * 设备列表Service业务层处理
 * 
 * @author thingscc
 * @date 2023-07-05
 */
@Service
public class IotDeviceServiceImpl implements IIotDeviceService 
{
    @Autowired
    private IotDeviceMapper iotDeviceMapper;

    /**
     * 查询设备列表
     * 
     * @param deviceId 设备列表主键
     * @return 设备列表
     */
    @Override
    public IotDevice selectIotDeviceByDeviceId(Long deviceId)
    {
        return iotDeviceMapper.selectIotDeviceByDeviceId(deviceId);
    }

    /**
     * 查询设备列表列表
     * 
     * @param iotDevice 设备列表
     * @return 设备列表
     */
    @Override
    public List<IotDevice> selectIotDeviceList(IotDevice iotDevice)
    {
        return iotDeviceMapper.selectIotDeviceList(iotDevice);
    }

    /**
     * 新增设备列表
     * 
     * @param iotDevice 设备列表
     * @return 结果
     */
    @Override
    public int insertIotDevice(IotDevice iotDevice)
    {
        return iotDeviceMapper.insertIotDevice(iotDevice);
    }

    /**
     * 修改设备列表
     * 
     * @param iotDevice 设备列表
     * @return 结果
     */
    @Override
    public int updateIotDevice(IotDevice iotDevice)
    {
        return iotDeviceMapper.updateIotDevice(iotDevice);
    }

    /**
     * 批量删除设备列表
     * 
     * @param deviceIds 需要删除的设备列表主键
     * @return 结果
     */
    @Override
    public int deleteIotDeviceByDeviceIds(Long[] deviceIds)
    {
        return iotDeviceMapper.deleteIotDeviceByDeviceIds(deviceIds);
    }

    /**
     * 删除设备列表信息
     * 
     * @param deviceId 设备列表主键
     * @return 结果
     */
    @Override
    public int deleteIotDeviceByDeviceId(Long deviceId)
    {
        return iotDeviceMapper.deleteIotDeviceByDeviceId(deviceId);
    }
}

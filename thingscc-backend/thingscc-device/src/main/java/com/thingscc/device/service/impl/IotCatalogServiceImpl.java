package com.thingscc.device.service.impl;

import java.util.List;
import com.thingscc.common.utils.DateUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.thingscc.device.mapper.IotCatalogMapper;
import com.thingscc.device.domain.IotCatalog;
import com.thingscc.device.service.IIotCatalogService;

/**
 * 设备分类Service业务层处理
 * 
 * @author thingscc
 * @date 2023-07-05
 */
@Service
public class IotCatalogServiceImpl implements IIotCatalogService 
{
    @Autowired
    private IotCatalogMapper iotCatalogMapper;

    /**
     * 查询设备分类
     * 
     * @param catalogId 设备分类主键
     * @return 设备分类
     */
    @Override
    public IotCatalog selectIotCatalogByCatalogId(Long catalogId)
    {
        return iotCatalogMapper.selectIotCatalogByCatalogId(catalogId);
    }

    /**
     * 查询设备分类列表
     * 
     * @param iotCatalog 设备分类
     * @return 设备分类
     */
    @Override
    public List<IotCatalog> selectIotCatalogList(IotCatalog iotCatalog)
    {
        return iotCatalogMapper.selectIotCatalogList(iotCatalog);
    }

    /**
     * 新增设备分类
     * 
     * @param iotCatalog 设备分类
     * @return 结果
     */
    @Override
    public int insertIotCatalog(IotCatalog iotCatalog)
    {
        iotCatalog.setCreateTime(DateUtils.getNowDate());
        return iotCatalogMapper.insertIotCatalog(iotCatalog);
    }

    /**
     * 修改设备分类
     * 
     * @param iotCatalog 设备分类
     * @return 结果
     */
    @Override
    public int updateIotCatalog(IotCatalog iotCatalog)
    {
        iotCatalog.setUpdateTime(DateUtils.getNowDate());
        return iotCatalogMapper.updateIotCatalog(iotCatalog);
    }

    /**
     * 批量删除设备分类
     * 
     * @param catalogIds 需要删除的设备分类主键
     * @return 结果
     */
    @Override
    public int deleteIotCatalogByCatalogIds(Long[] catalogIds)
    {
        return iotCatalogMapper.deleteIotCatalogByCatalogIds(catalogIds);
    }

    /**
     * 删除设备分类信息
     * 
     * @param catalogId 设备分类主键
     * @return 结果
     */
    @Override
    public int deleteIotCatalogByCatalogId(Long catalogId)
    {
        return iotCatalogMapper.deleteIotCatalogByCatalogId(catalogId);
    }
}

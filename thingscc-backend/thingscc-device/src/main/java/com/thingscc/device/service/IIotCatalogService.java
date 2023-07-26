package com.thingscc.device.service;

import java.util.List;
import com.thingscc.device.domain.IotCatalog;

/**
 * 设备分类Service接口
 * 
 * @author thingscc
 * @date 2023-07-05
 */
public interface IIotCatalogService 
{
    /**
     * 查询设备分类
     * 
     * @param catalogId 设备分类主键
     * @return 设备分类
     */
    public IotCatalog selectIotCatalogByCatalogId(Long catalogId);

    /**
     * 查询设备分类列表
     * 
     * @param iotCatalog 设备分类
     * @return 设备分类集合
     */
    public List<IotCatalog> selectIotCatalogList(IotCatalog iotCatalog);

    /**
     * 新增设备分类
     * 
     * @param iotCatalog 设备分类
     * @return 结果
     */
    public int insertIotCatalog(IotCatalog iotCatalog);

    /**
     * 修改设备分类
     * 
     * @param iotCatalog 设备分类
     * @return 结果
     */
    public int updateIotCatalog(IotCatalog iotCatalog);

    /**
     * 批量删除设备分类
     * 
     * @param catalogIds 需要删除的设备分类主键集合
     * @return 结果
     */
    public int deleteIotCatalogByCatalogIds(Long[] catalogIds);

    /**
     * 删除设备分类信息
     * 
     * @param catalogId 设备分类主键
     * @return 结果
     */
    public int deleteIotCatalogByCatalogId(Long catalogId);
}

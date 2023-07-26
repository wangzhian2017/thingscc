package com.thingscc.device.domain;

import org.apache.commons.lang3.builder.ToStringBuilder;
import org.apache.commons.lang3.builder.ToStringStyle;
import com.thingscc.common.annotation.Excel;
import com.thingscc.common.core.domain.BaseEntity;

/**
 * 设备分类对象 iot_catalog
 * 
 * @author thingscc
 * @date 2023-07-05
 */
public class IotCatalog extends BaseEntity
{
    private static final long serialVersionUID = 1L;

    /** 分类ID */
    private Long catalogId;

    /** 分类名称 */
    @Excel(name = "分类名称")
    private String catalogName;

    /** 父分类ID */
    @Excel(name = "父分类ID")
    private Long parentId;

    public void setCatalogId(Long catalogId) 
    {
        this.catalogId = catalogId;
    }

    public Long getCatalogId() 
    {
        return catalogId;
    }
    public void setCatalogName(String catalogName) 
    {
        this.catalogName = catalogName;
    }

    public String getCatalogName() 
    {
        return catalogName;
    }
    public void setParentId(Long parentId) 
    {
        this.parentId = parentId;
    }

    public Long getParentId() 
    {
        return parentId;
    }

    @Override
    public String toString() {
        return new ToStringBuilder(this,ToStringStyle.MULTI_LINE_STYLE)
            .append("catalogId", getCatalogId())
            .append("catalogName", getCatalogName())
            .append("parentId", getParentId())
            .append("createBy", getCreateBy())
            .append("createTime", getCreateTime())
            .append("updateBy", getUpdateBy())
            .append("updateTime", getUpdateTime())
            .append("remark", getRemark())
            .toString();
    }
}

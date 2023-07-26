package com.thingscc.device.controller;

import java.util.List;
import javax.servlet.http.HttpServletResponse;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import com.thingscc.common.annotation.Log;
import com.thingscc.common.core.controller.BaseController;
import com.thingscc.common.core.domain.AjaxResult;
import com.thingscc.common.enums.BusinessType;
import com.thingscc.device.domain.IotCatalog;
import com.thingscc.device.service.IIotCatalogService;
import com.thingscc.common.utils.poi.ExcelUtil;
import com.thingscc.common.core.page.TableDataInfo;

/**
 * 设备分类Controller
 * 
 * @author thingscc
 * @date 2023-07-05
 */
@RestController
@RequestMapping("/device/catalog")
public class IotCatalogController extends BaseController
{
    @Autowired
    private IIotCatalogService iotCatalogService;

    /**
     * 查询设备分类列表
     */
    @PreAuthorize("@ss.hasPermi('device:catalog:list')")
    @GetMapping("/list")
    public TableDataInfo list(IotCatalog iotCatalog)
    {
        startPage();
        List<IotCatalog> list = iotCatalogService.selectIotCatalogList(iotCatalog);
        return getDataTable(list);
    }

    /**
     * 导出设备分类列表
     */
    @PreAuthorize("@ss.hasPermi('device:catalog:export')")
    @Log(title = "设备分类", businessType = BusinessType.EXPORT)
    @PostMapping("/export")
    public void export(HttpServletResponse response, IotCatalog iotCatalog)
    {
        List<IotCatalog> list = iotCatalogService.selectIotCatalogList(iotCatalog);
        ExcelUtil<IotCatalog> util = new ExcelUtil<IotCatalog>(IotCatalog.class);
        util.exportExcel(response, list, "设备分类数据");
    }

    /**
     * 获取设备分类详细信息
     */
    @PreAuthorize("@ss.hasPermi('device:catalog:query')")
    @GetMapping(value = "/{catalogId}")
    public AjaxResult getInfo(@PathVariable("catalogId") Long catalogId)
    {
        return success(iotCatalogService.selectIotCatalogByCatalogId(catalogId));
    }

    /**
     * 新增设备分类
     */
    @PreAuthorize("@ss.hasPermi('device:catalog:add')")
    @Log(title = "设备分类", businessType = BusinessType.INSERT)
    @PostMapping
    public AjaxResult add(@RequestBody IotCatalog iotCatalog)
    {
        iotCatalog.setCreateBy(getUsername());
        return toAjax(iotCatalogService.insertIotCatalog(iotCatalog));
    }

    /**
     * 修改设备分类
     */
    @PreAuthorize("@ss.hasPermi('device:catalog:edit')")
    @Log(title = "设备分类", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@RequestBody IotCatalog iotCatalog)
    {
        iotCatalog.setUpdateBy(getUsername());
        return toAjax(iotCatalogService.updateIotCatalog(iotCatalog));
    }

    /**
     * 删除设备分类
     */
    @PreAuthorize("@ss.hasPermi('device:catalog:remove')")
    @Log(title = "设备分类", businessType = BusinessType.DELETE)
	@DeleteMapping("/{catalogIds}")
    public AjaxResult remove(@PathVariable Long[] catalogIds)
    {
        return toAjax(iotCatalogService.deleteIotCatalogByCatalogIds(catalogIds));
    }
}

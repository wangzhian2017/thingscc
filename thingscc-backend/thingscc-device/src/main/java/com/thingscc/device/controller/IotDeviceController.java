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
import com.thingscc.device.domain.IotDevice;
import com.thingscc.device.service.IIotDeviceService;
import com.thingscc.common.utils.poi.ExcelUtil;
import com.thingscc.common.core.page.TableDataInfo;

/**
 * 设备列表Controller
 * 
 * @author thingscc
 * @date 2023-07-05
 */
@RestController
@RequestMapping("/device/list")
public class IotDeviceController extends BaseController
{
    @Autowired
    private IIotDeviceService iotDeviceService;

    /**
     * 查询设备列表列表
     */
    @PreAuthorize("@ss.hasPermi('device:list:list')")
    @GetMapping("/list")
    public TableDataInfo list(IotDevice iotDevice)
    {
        startPage();
        List<IotDevice> list = iotDeviceService.selectIotDeviceList(iotDevice);
        return getDataTable(list);
    }

    /**
     * 导出设备列表列表
     */
    @PreAuthorize("@ss.hasPermi('device:list:export')")
    @Log(title = "设备列表", businessType = BusinessType.EXPORT)
    @PostMapping("/export")
    public void export(HttpServletResponse response, IotDevice iotDevice)
    {
        List<IotDevice> list = iotDeviceService.selectIotDeviceList(iotDevice);
        ExcelUtil<IotDevice> util = new ExcelUtil<IotDevice>(IotDevice.class);
        util.exportExcel(response, list, "设备列表数据");
    }

    /**
     * 获取设备列表详细信息
     */
    @PreAuthorize("@ss.hasPermi('device:list:query')")
    @GetMapping(value = "/{deviceId}")
    public AjaxResult getInfo(@PathVariable("deviceId") Long deviceId)
    {
        return success(iotDeviceService.selectIotDeviceByDeviceId(deviceId));
    }

    /**
     * 新增设备列表
     */
    @PreAuthorize("@ss.hasPermi('device:list:add')")
    @Log(title = "设备列表", businessType = BusinessType.INSERT)
    @PostMapping
    public AjaxResult add(@RequestBody IotDevice iotDevice)
    {
        return toAjax(iotDeviceService.insertIotDevice(iotDevice));
    }

    /**
     * 修改设备列表
     */
    @PreAuthorize("@ss.hasPermi('device:list:edit')")
    @Log(title = "设备列表", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@RequestBody IotDevice iotDevice)
    {
        return toAjax(iotDeviceService.updateIotDevice(iotDevice));
    }

    /**
     * 删除设备列表
     */
    @PreAuthorize("@ss.hasPermi('device:list:remove')")
    @Log(title = "设备列表", businessType = BusinessType.DELETE)
	@DeleteMapping("/{deviceIds}")
    public AjaxResult remove(@PathVariable Long[] deviceIds)
    {
        return toAjax(iotDeviceService.deleteIotDeviceByDeviceIds(deviceIds));
    }
}

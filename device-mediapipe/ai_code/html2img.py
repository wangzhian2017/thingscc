from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import time
import re
from PIL import Image 
import io
import base64

def main():
    # response=requests.get('https://www.runoob.com/cssref/css-reference.html',verify=False)
    # with open(r"C:\\bak\\test.txt","w",encoding="utf-8") as f:
    #     f.write(response.text)

    driver=webdriver.Chrome()
    driver.maximize_window()
    driver.get('https://www.runoob.com/cssref/css-reference.html')
    time.sleep(2)
    element=driver.find_element(By.CLASS_NAME,"article")
    # element.screenshot('C:\\bak\\test.png')

    title=re.sub(r'[^\w\s]', '', driver.title)
    with open("C:\\bak\\%s.html" % title,"w",encoding="utf-8") as f:
        f.write(element.get_attribute("innerHTML"))
    
    # 获取网页高度  
    height = element.size["height"] # driver.execute_script("return document.body.scrollHeight") 
    width= element.size["width"]
    # 执行滚动操作
    screenshot = Image.new('RGB', (width, height), (255, 255, 255))  
    page_y=element.location["y"]
    paste_position_y=0
    while paste_position_y<height:
        driver.execute_script("window.scrollTo(0, %d)" % page_y)  
        time.sleep(1)  
        element=driver.find_element(By.CLASS_NAME,"article")
        base64html=element.screenshot_as_base64
        screenshot_part=Image.open(io.BytesIO(base64.b64decode(base64html))).convert("RGB")
        screenshot.paste(screenshot_part, (0, paste_position_y)) 
        
        if screenshot_part.height<=0:
            break
        paste_position_y+=screenshot_part.height
        page_y+=screenshot_part.height
       

        
    # 保存截图 
    screenshot.save("C:\\bak\\%s.png" % title)  
    driver.quit()
  



if __name__ == '__main__':
    main()

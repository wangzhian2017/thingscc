from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import time
from PIL import Image 
import io
import base64

def main():
    response=requests.get('https://www.runoob.com/cssref/css-reference.html',verify=False)
   
    with open(r"C:\\bak\\test.txt","w",encoding="utf-8") as f:
        f.write(response.text)

    driver=webdriver.Chrome()
    driver.maximize_window()
    driver.get('https://www.runoob.com/cssref/css-reference.html')
    time.sleep(2)
    # element=driver.find_element(By.CLASS_NAME,"main")
    # element.screenshot('C:\\bak\\test.png')

    # 获取网页高度  
    height = driver.execute_script("return document.body.scrollHeight")  
    window_size = driver.get_window_size()
    # 执行滚动操作
    screenshot = Image.new('RGB', (window_size["width"], height), (255, 255, 255))  
    scroll_pixels = window_size['height'] # 每次向下滚动的像素数量
    for i in range(0, height, scroll_pixels):  
        driver.execute_script("window.scrollTo(0, %d)" % i)  
        time.sleep(2)  
        # element=driver.find_element(By.ID,"section-content")
        # base64html=element.screenshot_as_base64
        base64html=driver.get_screenshot_as_base64()
        screenshot_part=Image.open(io.BytesIO(base64.b64decode(base64html))).convert("RGB")
        screenshot.paste(screenshot_part, (0, i)) 
        break
    # 保存截图 
    screenshot.save("C:\\bak\\test.png")  
    driver.quit()
  



if __name__ == '__main__':
    main()

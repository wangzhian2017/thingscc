import time
from pywinauto.application import Application
from pywinauto import Desktop,keyboard



def main():
    app = Application(backend="uia").start(r"C:\Program Files\Google\Chrome\Application\chrome.exe --force-renderer-accessibility") 
    app = Application(backend="uia").connect(title='New Tab - Google Chrome',timeout=5)
    win=app.NewTabGoogleChrome
    win.type_keys('chrome://dino/')
    win.type_keys('{ENTER}')


    win=app['chrome://dino/ - Network error - Google ChromePane']
    while(True):
        time.sleep(3)
        win.capture_as_image().save('test.png')
        win.type_keys('{SPACE}')
    

if __name__ == '__main__':
    main()
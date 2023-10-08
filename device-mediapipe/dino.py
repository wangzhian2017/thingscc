import time
from pywinauto.application import Application
from pywinauto import Desktop,keyboard



def main():
    app = Application(backend="uia").start(r"C:\Program Files\Google\Chrome\Application\chrome.exe --force-renderer-accessibility") 
    app = Application(backend="uia").connect(title='New Tab - Google Chrome',timeout=5)
    win=app.NewTabGoogleChrome
    win.type_keys('chrome://dino/')
    win.type_keys('{ENTER}')

    time.sleep(1)
    win=app['chrome://dino/ - Network error - Google ChromePane']
    win.type_keys('{SPACE}')

    while(True):
        time.sleep(3)
        win.type_keys('{SPACE}')


if __name__ == '__main__':
    main()
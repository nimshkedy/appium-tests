import os
from time import sleep

from appium import webdriver

"""
REQUIREMENTS to run this file:
$ pip install Appium-Python-Client
$ npm install -g appium

# run appium:
$ appium

# use this module:
>>> import tmz
>>> t = tmz.Tmz()
>>> t.open_webview()
>>> t.driver.find_elements_by_xpath("//div")
# when done
>>> t.driver.quit()

"""


# PLATFORM_VERSION = '4.4'
PLATFORM_VERSION = '4.2'

driver = None

class Tmz:
    def __init__(self):
        # app = os.path.abspath(
        #         os.path.join(os.path.dirname(__file__),
        #                      '../../apps/trivial-drive-app-debug.apk'))

        app = os.path.abspath(
                os.path.join(os.path.dirname(__file__),
                             '../../apps/android-debug.apk'))

        desired_caps = {
            # this line may be commented out if trivial drive is already installed:
            'app': app,
            'appPackage': 'com.ionicframework.portrait139981',
            'appActivity': '.MainActivity',
            # 'appActivity': '.ThumzapActivity',
            'platformName': 'Android',
            'platformVersion': PLATFORM_VERSION,
            # 'deviceName': 'Android Emulator'
            'deviceName': 'HT449W900974'
            # 'deviceName': '067201e40ac6cff5'
        }

        # if True:
        if (PLATFORM_VERSION != '4.4'):
            desired_caps['automationName'] = 'selendroid'
            desired_caps['app'] = app

        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

    def open_webview(self):
        buttons = self.driver.find_elements_by_class_name("android.widget.Button")
        # buttons[0].click()
        buttons[1].click()
        sleep(3)
        self.driver.switch_to.context(self.driver.contexts[-1])

    def take_screenshot(self):
        directory = '%s/' % os.getcwd()
        file_name = 'screenshot.png'
        full_path = directory + file_name
        if self.driver.save_screenshot(full_path):
            return full_path
        return None


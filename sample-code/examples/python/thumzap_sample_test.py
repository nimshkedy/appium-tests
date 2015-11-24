import os
import glob
import unittest
from time import sleep

from appium import webdriver



class AndroidWebViewTests(unittest.TestCase):

    def setUp(self):
        app = os.path.abspath(
                os.path.join(os.path.dirname(__file__),
                             '../../apps/selendroid-test-app-debug.apk'))

        desired_caps = {
            'app': app,
            'appPackage': 'io.selendroid.testapp',
            'appActivity': '.HomeScreenActivity',
            'platformName': 'Android',
            'platformVersion': '4.2',
            'deviceName': 'Android Emulator',
            'automationName': 'selendroid'
        }

        self.driver = webdriver.Remote('http://localhost:4723/wd/hub',
                                       desired_caps)

    def take_screenshot(self, file_name):
        directory = '%s/screenshots/' % os.getcwd()
        full_path = directory + file_name
        if self.driver.save_screenshot(full_path):
            return full_path
        return None


    def test_webview_portrait(self):

        button = self.driver.find_element_by_name('portraitButtonCD')
        button.click()
        sleep(2)

        self.driver.switch_to.context('WEBVIEW_0')
        sleep(2)

        self.driver.get("http://10.0.0.15:8888/www/index.html")
        sleep(15)

        self.take_screenshot('portrait.png')


    def test_webview_landscape(self):


        button = self.driver.find_element_by_name('landscapeButtonCD')
        button.click()
        sleep(2)

        self.driver.switch_to.context('WEBVIEW_0')
        sleep(2)

        self.driver.get("http://10.0.0.15:8888/www/index.html")
        sleep(15)

        self.take_screenshot('landscape.png')


    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(AndroidWebViewTests)
    unittest.TextTestRunner(verbosity=2).run(suite)

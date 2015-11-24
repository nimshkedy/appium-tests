import re
import os
import glob
import unittest
from time import sleep

from appium import webdriver

class ParametrizedTestCase(unittest.TestCase):
    """ TestCase classes that want to be parametrized should
        inherit from this class.
    """
    def __init__(self, methodName='runTest', host=None, url_file=None, locale_file=None):
        super(ParametrizedTestCase, self).__init__(methodName)
        self.host = host
        self.url_file = url_file
        self.locale_file = locale_file

    @staticmethod
    def parametrize(testcase_klass, host=None, url_file=None, locale_file=None):
        """ Create a suite containing all tests taken from the given
            subclass, passing them the parameters
        """
        testloader = unittest.TestLoader()
        testnames = testloader.getTestCaseNames(testcase_klass)
        suite = unittest.TestSuite()
        for name in testnames:
            suite.addTest(testcase_klass(name, host=host, url_file=url_file, locale_file=locale_file))
        return suite

class AndroidWebViewTests(ParametrizedTestCase):
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

        with open(self.locale_file) as f:
            self.locales = f.readlines()

        with open(self.url_file) as f:
            self.urls = f.readlines()

        self.sdks = [ 2004 ]

    def build_webapp_url(self, host, relative_url, locale, sdk_version):
        webapp_url_path = '%s/%s?locale=%s&sdk=%s' % ( host, relative_url, locale, sdk_version )
        return webapp_url_path

    def take_screenshot(self, sdk_version, orientation, locale, filename):
        safe_filename = re.sub('[^\w\-_\. ]', '_', filename)

        full_path = '%s/screenshots/%s/%s/%s/%s' % ( os.getcwd(), sdk_version, orientation, locale, safe_filename )
        if self.driver.save_screenshot(full_path):
            return full_path
        return None

    def take_url_screenshots(self, orientation):
        self.driver.switch_to.context('WEBVIEW_0')
        sleep(2)

        for sdk in self.sdks:
            for locale in self.locales:
                for url in self.urls:
                    path = self.build_webapp_url(self.host, url, locale, sdk)
                    print 'Processing URL = [%s], orientation = [%s]' % ( path, orientation )
                    self.driver.get(path)
                    sleep(5)
                    self.take_screenshot(sdk, orientation, locale, url)


    def test_webview_portrait(self):
        button = self.driver.find_element_by_name('portraitButtonCD')
        button.click()
        sleep(2)

        self.take_url_screenshots('portrait')


    def test_webview_landscape(self):
        button = self.driver.find_element_by_name('landscapeButtonCD')
        button.click()
        sleep(2)

        self.take_url_screenshots('landscape')

    def tearDown(self):
        self.driver.quit()

def main(argv):
    host = ''
    url_file = ''
    locale_file = ''

    try:
        opts, args = getopt.getopt(argv,"h:u:l",["host=","url-file=","locale-file="])
    except getopt.GetoptError:
        print 'usage: -h <host> -u <url_file> -l <locale_file>'
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--host"):
            host = arg
        elif opt in ("-u", "--url-file"):
            url_file = arg
        elif opt in ("-l", "--locale-file"):
            locale_file = arg

    suite = unittest.TestSuite()
    suite.addTest(ParametrizedTestCase.parametrize(AndroidWebViewTests, host=host, url_file=url_file, locale_file=locale_file))
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == '__main__':
    main(sys.argv[1:])
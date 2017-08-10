from BB import Login

desired_cap = {'browser': 'Chrome', 'browser_version': '59.0', 'os': 'OS X', 'os_version': 'Sierra', 'resolution': '1920x1080'}
driver = webdriver.Remote(
command_executor='http://patrickanderson2:Z39oMKMLFiyYJ88GWosk@hub.browserstack.com:80/wd/hub',
desired_capabilities=desired_cap)

def test_hi(self):

    l= Login()
    l.staging_login(driver)

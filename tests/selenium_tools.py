from selenium import webdriver
# ref: http://stackoverflow.com/questions/12698843/how-do-i-pass-options-to-the-selenium-chrome-driver-using-python
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# START decorators
def set_class_drivers(drivers, default=None, conveniences=False):
    def modify_class(cls):
        cls.drivers = drivers

        if default:
            default_driver = drivers.get(default)
            cls.driver = default_driver

            if conveniences:
                cls.d = default_driver.find_element_by_id
                cls.q = default_driver.find_elements_by_css_selector

        return cls
    return modify_class

def method_use_drivers(*keys):
    return lambda func: _apply_drivers(func, *keys)
# END decorators

def _apply_drivers(func, *keys):
    def wrapper(ctx):
        if hasattr(ctx, 'driver'):
            old_driver = ctx.driver

        drivers = [ctx.drivers.get(key) for key in keys]

        for driver in drivers:
            ctx.driver = driver
            func(ctx)

        if old_driver:
            ctx.driver = old_driver
    return wrapper

class SeleniumDriverHolder():
    grid_url = 'http://127.0.0.1:4444/wd/hub'

    def __init__(self, remote=True, grid_url=None):
        self.grid_url = grid_url or self.grid_url
        self.drivers_container = {}

    def get(self, key):
        return self.drivers_container[key]

    def close(self, key=None):
        '''
        Close the browser window in all drivers.
        Note this is *not* the same as quitting the drivers.
        '''
        if key:
            drivers = [self.drivers_container[key]]
        else:
            drivers = self.drivers_container.values()

        for driver in drivers:
            driver.close()

    def quit(self, key=None):
        '''
        Quit all drivers and free their slots on the Selenium remote node.
        '''
        if key:
            drivers = [self.drivers_container[key]]
        else:
            drivers = self.drivers_container.values()

        for driver in drivers:
            driver.quit()

    def add_firefox(self, key, remote=True, **desired_capabilities):
        if key in self.drivers_container:
            raise ValueError('Key "{}" already in {}'.format(key, self.__class__))

        capabilities = DesiredCapabilities.FIREFOX.copy()
        capabilities.update(desired_capabilities)

        if remote:
            driver = webdriver.Remote(desired_capabilities=capabilities, command_executor=self.grid_url)
        else:
            driver = webdriver.Firefox(capabilities=capabilities)

        self.drivers_container[key] = driver

    def add_chrome(self, key, remote=True, **desired_capabilities):
        if key in self.drivers_container:
            raise ValueError('Key "{}" already in {}'.format(key, self.__class__))

        chrome_options = ChromeOptions()
        chrome_options.add_argument('--disable-extensions')
        capabilities = chrome_options.to_capabilities()
        capabilities.update(desired_capabilities)

        if remote:
            driver = webdriver.Remote(desired_capabilities=capabilities, command_executor=self.grid_url)
        else:
            driver = webdriver.Chrome(desired_capabilities=capabilities)

        self.drivers_container[key] = driver

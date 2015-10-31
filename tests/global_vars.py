import os
import tests.selenium_tools as selenium_tools
from pyvirtualdisplay import Display

if os.environ.get('REMOTE_SELENIUM') == 'True':
    remote_selenium = True
    grid_url = os.environ['REMOTE_SELENIUM_URL']
    drivers = selenium_tools.SeleniumDriverHolder(grid_url=grid_url)
else:
    remote_selenium = False
    # a headless display allows Selenium to work in the tox environment.
    # otherwise you need tox to passenv the DISPLAY and XAUTHORITY vars.
    # see: http://stackoverflow.com/questions/6183276/how-do-i-run-selenium-in-xvfb
    display = Display(visible=0, size=(800, 600))
    display.start()
    drivers = selenium_tools.SeleniumDriverHolder()

drivers.add_firefox('ff', remote=remote_selenium, platform='LINUX')
drivers.add_chrome('ch',  remote=remote_selenium, platform='LINUX')

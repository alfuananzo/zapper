from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep

zap_host = "localhost"
zap_port = 8080

profile = webdriver.FirefoxProfile()
profile.set_preference("network.proxy.type", 1)
profile.set_preference("network.proxy.http", zap_host)
profile.set_preference("network.proxy.http_port", zap_port)
profile.set_preference("network.proxy.ssl", zap_host)
profile.set_preference("network.proxy.ssl_port", zap_port)
profile.update_preferences()

driver = webdriver.Firefox(profile)

driver.get('https://cloud.fonsmijnen.nl')
assert 'Nextcloud' in driver.title

elem = driver.find_element_by_name('user')  # Find the login name
elem.send_keys('fons' + Keys.TAB + 'not my actual passwod' + Keys.ENTER)
sleep(5)
driver.get('https://cloud.fonsmijnen.nl/apps/files/')
assert 'Files - Nextcloud' in driver.title

driver.quit()

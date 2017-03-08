# from selenium import webdriver
#  
# driver = webdriver.Chrome(service_log_path="/docs/github/Opal/src/selenium_download")
# driver.get("http://www.google.com")
# driver.close()

# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# 
# browser = webdriver.Firefox()
# 
# browser.get('http://www.yahoo.com')
# assert 'Yahoo' in browser.title
# 
# elem = browser.find_element_by_name('p')  # Find the search box
# elem.send_keys('seleniumhq' + Keys.RETURN)
# 
# browser.quit()
from selenium import webdriver
# from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
# 
# binary = FirefoxBinary('path/to/binary')
# driver = webdriver.Firefox(firefox_binary=binary)

from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

binary = FirefoxBinary('/docs/python_projects/firefox/firefox')
binary = FirefoxBinary('/docs/python_projects/firefox/firefox')
print '1'
driver = webdriver.Firefox(firefox_binary=binary)
print '1'
driver.get('http://www.google.com')
print '1'
driver.quit()
import urllib2
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

class PacktpubCrawl:
    def __init__(self):
        self.baseUrl = "https://www.packtpub.com/"

    def findBookUrl(self):
        directory_name='.'
        binary = FirefoxBinary('/docs/python_projects/firefox/firefox')

        fp = webdriver.FirefoxProfile()

        fp.set_preference("webdriver.log.file", "/tmp/firefox_console");
        fp.set_preference("browser.download.folderList", 2)
        fp.set_preference('browser.download.manager.showWhenStarting', False)
        fp.set_preference('browser.download.manager.focusWhenStarting', False)
        fp.set_preference("browser.download.dir", directory_name)
        fp.set_preference("browser.download.manager.scanWhenDone", False)
        fp.set_preference("browser.download.manager.useWindow", False)
#             fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")
        fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream,application/xml,application/pdf,text/plain,text/xml,image/jpeg,text/csv,application/zip,application/x-rar-compressed");
        fp.set_preference("browser.helperApps.alwaysAsk.force", False);
        fp.set_preference("browser.popups.showPopupBlocker", False);
        fp.update_preferences()
        driver = webdriver.Firefox(firefox_profile=fp, firefox_binary=binary)
        # driver.find_element_by_xpath("html/body/table/tbody/tr[2]/td/div/table/tbody/tr/td[1]/img")
        driver.get(self.baseUrl)
        efd_link = driver.find_element_by_css_selector(".login-popup > div:nth-child(1)")
        efd_link.click()
        try:
            emailEl=driver.find_element_by_css_selector('#packt-user-login-form > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > input:nth-child(1)')
#             emailEl = driver.find_element_by_name("email")
            emailEl.send_keys('view7677@gmail.com')
            passwordEl = driver.find_element_by_css_selector("#packt-user-login-form > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)")
            passwordEl.send_keys('default')
            loginEl=driver.find_element_by_css_selector("#packt-user-login-form > div:nth-child(1) > div:nth-child(1) > div:nth-child(3) > input:nth-child(1)")
            loginEl.click()
            
            if True:
                myAccountEl=driver.find_element_by_css_selector('#account-bar-logged-in > a:nth-child(1) > div:nth-child(1) > strong:nth-child(1)')
                myAccountEl.click()
                
                myEbook=driver.get(self.baseUrl+'account/my-ebooks')
                productListEls=driver.find_elements_by_css_selector('div.product-line')
                print productListEls
            
            driver.get('https://www.packtpub.com/packt/offers/free-learning')
            try:
                claimFreeEbookEl=driver.find_element_by_css_selector('.book-claim-token-inner > input:nth-child(3)')
                claimFreeEbookEl.click()
            except Exception as e:
                print e
                
#             myEbook.click()
            
        except Exception as e:
            print e
        finally:
            print 'completed'
        print 'hi'


if __name__ == "__main__":
    PacktpubCrawl().findBookUrl()
    print 'pass'

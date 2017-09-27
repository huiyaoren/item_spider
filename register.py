from selenium import webdriver
import os
import time


# option = webdriver.ChromeOptions()
# option.add_extension('d:\crx\AdBlock_v2.17.crx') #自己下载的crx路径
# option.add_argument('--user-data-dir=C:\Users\Administrator\AppData\Local\Google\Chrome\User Data')
# driver = webdriver.Chrome(chrome_options=option)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


def run(username=''):
    # 请求连接
    req_url = "https://developer.ebay.com/signin"
    # 打开浏览器
    print("Opening chrome ...")
    browser = webdriver.Chrome()
    print('Visit {0} ...'.format(req_url))
    browser.get(req_url)
    print('Click ...')
    browser.find_element_by_xpath('//*[@id="w4-0[1]"]').click()
    print('Insert data ...')
    browser.find_element_by_xpath('//*[@id="w4-w1-registration-username"]').click()
    browser.find_element_by_xpath('//*[@id="w4-w1-registration-username"]').send_keys(username)
    browser.find_element_by_xpath('//*[@id="w4-w1-w1-password"]').send_keys('1234qwer$')
    browser.find_element_by_xpath('//*[@id="w4-w1-registration-email"]').send_keys('{0}@sina.com'.format(username))
    browser.find_element_by_xpath('//*[@id="w4-w1-registration-reenter-email"]').send_keys('{0}@sina.com'.format(username))
    browser.find_element_by_xpath('//*[@id="w4-w1-w2-phone"]').send_keys('12341234')
    browser.find_element_by_xpath('//*[@id="w4-w1-checkbox-user-agreement"]').click()
    captcha = input('Insert Captcha :\n')
    browser.find_element_by_xpath('//*[@id="w4-w1-w3-captcha-response-field"]').send_keys(captcha)
    print('Sent register data ...')
    browser.find_element_by_xpath('//*[@id="w4-w1-join-button"]').click()
    print('Write app name ...')
    try:
        element = WebDriverWait(browser, 10).until(
            expected_conditions.presence_of_element_located((By.XPATH, '//*[@id="_ip_wth_cntr"]'))
        )
    finally:
        pass
    element.send_keys('qwer')
    print('Create product app')
    browser.find_element_by_xpath('//*[@id="w6"]/div[2]/div[2]/div/a').click()
    print('Insert app data')
    try:
        element = WebDriverWait(browser, 10).until(
            expected_conditions.presence_of_element_located((By.XPATH, '//*[@id="w4-w0-first-name"]'))
        )
    finally:
        pass
    element.send_keys('qwer')
    # browser.find_element_by_xpath('//*[@id="w4-w0-first-name"]').send_keys('qwer')
    browser.find_element_by_xpath('//*[@id="w4-w0-last-name"]').send_keys('qwer')
    browser.find_element_by_xpath('//*[@id="w4-w0-continue"]').click()


    while 1:
        time.sleep(10)


if __name__ == '__main__':
    run('qwerasdip7')

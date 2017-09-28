from selenium import webdriver
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class Register():
    def __init__(self):
        option = webdriver.ChromeOptions()
        option.add_argument('--user-data-dir=~/.config/google-chrome')
        option.add_extension('/host/DL/92jiasu.crx')
        self.browser = webdriver.Chrome(chrome_options=option)

    def element_loaded(self, pattern, time=10):
        element = WebDriverWait(self.browser, time).until(
            expected_conditions.presence_of_element_located((By.XPATH, pattern)))
        return element

    def switch_window(self, now):
        all_handles = self.browser.window_handles  # 得到当前开启的所有窗口的句柄
        for handle in all_handles:
            if handle != now:  # 获取到与当前窗口不一样的窗口
                self.browser.switch_to_window(handle)

    def run(self, username='qwe'):
        # 请求连接
        req_url = "https://developer.ebay.com/signin"
        # 打开浏览器
        print("Opening chrome ...")
        browser = self.browser
        # 打开注册页面
        print('Visit {0} ...'.format(req_url))
        browser.get(req_url)
        print('Click ...')
        self.element_loaded('//*[@id="w4-0[1]"]').click()

        # 填写注册资料
        print('Insert data ...')
        continue_ = input('Continue')
        browser.find_element_by_xpath('//*[@id="w4-w1-registration-username"]').click()
        browser.find_element_by_xpath('//*[@id="w4-w1-registration-username"]').send_keys(username)
        browser.find_element_by_xpath('//*[@id="w4-w1-w1-password"]').send_keys('1234qwer$')
        browser.find_element_by_xpath('//*[@id="w4-w1-registration-email"]').send_keys('{0}@sina.com'.format(username))
        browser.find_element_by_xpath('//*[@id="w4-w1-registration-reenter-email"]').send_keys(
            '{0}@sina.com'.format(username))
        browser.find_element_by_xpath('//*[@id="w4-w1-w2-phone"]').send_keys('12341234')
        browser.find_element_by_xpath('//*[@id="w4-w1-checkbox-user-agreement"]').click()

        # 输入验证码
        captcha = input('Insert Captcha :\n')
        browser.find_element_by_xpath('//*[@id="w4-w1-w3-captcha-response-field"]').send_keys(captcha)
        # browser.find_element_by_xpath('//*[@id="w4-w1-join-button"]').click()
        continue_ = input('Continue')
        return

        # 提交注册信息
        print('Sent register data ...')
        browser.find_element_by_xpath('//*[@id="w4-w1-join-button"]').click()
        print('Write app name ...')
        self.element_loaded('//*[@id="_ip_wth_cntr"]', 20).send_keys('qwer')

        print('Create product app')
        browser.find_element_by_xpath('//*[@id="w6"]/div[2]/div[2]/div/a').click()
        print('Insert app data')

        self.element_loaded('//*[@id="w4-w0-first-name"]').send_keys('qwer')

        # browser.find_element_by_xpath('//*[@id="w4-w0-first-name"]').send_keys('qwer')
        browser.find_element_by_xpath('//*[@id="w4-w0-last-name"]').send_keys('qwer')
        browser.find_element_by_xpath('//*[@id="w4-w0-continue"]').click()

        # cnhdled - sale
        # Huo520Ding

        while 1:
            time.sleep(10)


if __name__ == '__main__':
    register = Register()
    register.run('wslshanlin69')
    # for i in range(64, 71):
    #     register.run('wslshanlin{0}'.format(i))

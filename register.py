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

    def element_loaded(self, pattern, time=60):
        element = WebDriverWait(self.browser, time).until(
            expected_conditions.presence_of_element_located((By.XPATH, pattern)))
        return element

    def element_visible(self, pattern, time=60):
        element = WebDriverWait(self.browser, time).until(
            expected_conditions.visibility_of_element_located((By.XPATH, pattern)))
        return element

    def switch_window(self, now):
        all_handles = self.browser.window_handles  # 得到当前开启的所有窗口的句柄
        for handle in all_handles:
            if handle != now:  # 获取到与当前窗口不一样的窗口
                # self.browser.switch_to_window(handle)
                self.browser.switch_to.window(handle)

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
        browser.find_element_by_xpath('//*[@id="w4-w1-registration-username"]').click()
        browser.find_element_by_xpath('//*[@id="w4-w1-registration-username"]').send_keys(username)
        browser.find_element_by_xpath('//*[@id="w4-w1-w1-password"]').send_keys('1234qwer$')
        browser.find_element_by_xpath('//*[@id="w4-w1-registration-email"]').send_keys('{0}@sina.com'.format(username))
        browser.find_element_by_xpath('//*[@id="w4-w1-registration-reenter-email"]').send_keys(
            '{0}@sina.com'.format(username))
        browser.find_element_by_xpath('//*[@id="w4-w1-w2-phone"]').send_keys('12341234')
        browser.find_element_by_xpath('//*[@id="w4-w1-checkbox-user-agreement"]').click()

        # 输入验证码
        # captcha = input('Insert Captcha :\n')
        # browser.find_element_by_xpath('//*[@id="w4-w1-w3-captcha-response-field"]').send_keys(captcha)

        # 提交注册信息
        print('Sent register data ...')
        # browser.find_element_by_xpath('//*[@id="w4-w1-join-button"]').click()

        # 新建应用
        print('Write app name ...')
        self.element_loaded('//*[@id="_ip_wth_cntr"]').send_keys('qwer')
        print('Create product app ...')
        browser.find_element_by_xpath('//*[@id="w6"]/div[2]/div[2]/div/a').click()
        print('Insert app data ...')
        self.element_visible('//*[@id="w4-w0-first-name"]').send_keys('qwer')
        browser.find_element_by_xpath('//*[@id="w4-w0-last-name"]').send_keys('qwer')
        browser.find_element_by_xpath('//*[@id="w4-w0-continue"]').click()

        # 获取应用信息
        print('Get app msg ...')
        app_id = self.element_visible('//*[@id="w6"]/div[2]/div[2]/div/div/section/div/div/div[1]/span[2]').text
        dev_id = browser.find_element_by_xpath(
            '//*[@id="w6"]/div[2]/div[2]/div/div/section/div/div/div[2]/span[2]').text
        cert_id = browser.find_element_by_xpath(
            '//*[@id="w6"]/div[2]/div[2]/div/div/section/div/div/div[3]/span[2]').text
        print('app_id: {0}'.format(app_id))
        print('dev_id: {0}'.format(dev_id))
        print('cert_id: {0}'.format(cert_id))

        # 跳转应用详情页
        print('Turn to appp detail ...')
        self.element_visible('//*[@id="w0"]/div/span').click()
        self.element_visible('//*[@id="w2"]/ul/li[1]/a').click()
        browser.find_element_by_xpath('//*[@id="w2"]/ul/li[1]/div/a[3]').click()

        # 补充应用信息
        print('Turn to production')
        self.element_visible('//*[@id="w5-w0"]/div/fieldset/span[2]/label').click()
        self.element_visible('//*[@id="w6-w1-signin"]').click()
        self.element_visible('//*[@id="w4-w0-street1"]').send_keys('qwer')
        browser.find_element_by_xpath('//*[@id="w4-w0-state"]').send_keys('qwer')
        browser.find_element_by_xpath('//*[@id="w4-w0-city"]').send_keys('qwer')
        browser.find_element_by_xpath('//*[@id="w4-w0-postal"]').send_keys('qwer')
        browser.find_element_by_xpath('//*[@id="w4-w0-country"]/option[7]').click()
        browser.find_element_by_xpath('//*[@id="w4-w0-continue-to-get-token"]').click()

        # 填写用户账号
        print('Insert user account ...')
        self.element_loaded('//*[@id="userid"]').clear()
        browser.find_element_by_xpath('//*[@id="userid"]').send_keys('cnhdled - sale')
        browser.find_element_by_xpath('//*[@id="pass"]').clear()
        browser.find_element_by_xpath('//*[@id="pass"]').send_keys('Huo520Ding')
        browser.find_element_by_xpath('//*[@id="sgnBt"]').click()

        # 同意协议
        print('Agree ...')
        self.element_loaded('//*[@id="frmAuth"]/div/div[2]/div[1]/input').click()

        # 获取 token
        print('Get token ...')
        token = self.element_visible('//*[@id="w6-w1-devToken"]').text
        print(token)
        assert len(token) > 50
        # todo-1 Insert token and app data to mysql or other database

        # 注销
        print('Sign out ...')
        self.element_visible('//*[@id="w0"]/div/span').click()
        self.element_visible('//*[@id="edp-headername"]').click()
        self.element_visible('//*[@id="w2"]/ul/li[1]/div/a[7]').click()

        return
        while 1:
            time.sleep(10)


if __name__ == '__main__':
    register = Register()
    register.run('wslshanlin89')
    # for i in range(88, 90):
    #     register.run('wslshanlin{0}'.format(i))

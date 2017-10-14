import time
from multiprocessing.pool import Pool

from pymongo.errors import DuplicateKeyError
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from ebay.ebay.utils.data import db_mongodb


class Register():
    def __init__(self, browser):
        self.browser = browser
        self.mongodb = db_mongodb()
        self.collection = self.mongodb['tokens']
        self.collection.ensure_index('username', unique=True)

    def element_loaded(self, pattern, time=1800):
        element = WebDriverWait(self.browser, time).until(
            expected_conditions.presence_of_element_located((By.XPATH, pattern)))
        return element

    def element_visible(self, pattern, time=1800):
        element = WebDriverWait(self.browser, time).until(
            expected_conditions.visibility_of_element_located((By.XPATH, pattern)))
        return element

    def switch_window(self, now):
        all_handles = self.browser.window_handles  # 得到当前开启的所有窗口的句柄
        for handle in all_handles:
            if handle != now:  # 获取到与当前窗口不一样的窗口
                # self.browser.switch_to_window(handle)
                self.browser.switch_to.window(handle)

    def save_tokens(self, data):
        c = self.collection
        try:
            c.insert_one(data)
        except DuplicateKeyError:
            print('DuplicateKeyError: {0}'.format(data))

    def run(self, username='qwe', password='1234qwer$'):
        # 请求连接
        req_url = "https://developer.ebay.com/signin"

        # 打开浏览器
        print("Opening chrome ...")
        browser = self.browser

        # 打开注册页面
        print('Visit {0} ...'.format(req_url))
        browser.get(req_url)
        print('Click Register...')
        self.element_loaded('//*[@id="w4-0[1]"]').click()

        # 填写注册资料
        print('Insert data ...')
        print('username: {0}'.format(username))
        browser.find_element_by_xpath('//*[@id="w4-w1-registration-username"]').click()
        browser.find_element_by_xpath('//*[@id="w4-w1-registration-username"]').send_keys(username)
        browser.find_element_by_xpath('//*[@id="w4-w1-w1-password"]').send_keys(password)
        browser.find_element_by_xpath('//*[@id="w4-w1-registration-email"]').send_keys('{0}@sina.com'.format(username))
        browser.find_element_by_xpath('//*[@id="w4-w1-registration-reenter-email"]').send_keys(
            '{0}@sina.com'.format(username))
        browser.find_element_by_xpath('//*[@id="w4-w1-w2-phone"]').send_keys('12341234')
        browser.find_element_by_xpath('//*[@id="w4-w1-checkbox-user-agreement"]').click()
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        browser.find_element_by_xpath('//*[@id="w4-w1-w3-captcha-response-field"]').click()

        # 输入验证码
        # captcha = input('Insert Captcha :\n')
        # browser.find_element_by_xpath('//*[@id="w4-w1-w3-captcha-response-field"]').send_keys(captcha)

        # 提交注册信息
        print('Sent register data ...')
        # browser.find_element_by_xpath('//*[@id="w4-w1-join-button"]').click()

        # 新建应用
        print('Write app name ...')  # todo 因未知原因返回登录页面
        self.element_loaded('//*[@id="_ip_wth_cntr"]').send_keys('qwer')
        print('Create product app ...')
        browser.find_element_by_xpath('//*[@id="w6"]/div[2]/div[2]/div/a').click()
        print('Insert app data ...')
        self.element_visible('//*[@id="w4-w0-first-name"]').send_keys('qwer')
        browser.find_element_by_xpath('//*[@id="w4-w0-last-name"]').send_keys('qwer')
        browser.find_element_by_xpath('//*[@id="w4-w0-continue"]').click()

        # 获取应用信息
        print('Get app msg ...')  # todo 因未知原因定在此处
        app_id = self.element_loaded(
            '//*[@id="w6"]/div[2]/div[2]/div/div/section/div/div/div[1]/span[2]').text
        dev_id = browser.find_element_by_xpath(
            '//*[@id="w6"]/div[2]/div[2]/div/div/section/div/div/div[2]/span[2]').text
        cert_id = browser.find_element_by_xpath(
            '//*[@id="w6"]/div[2]/div[2]/div/div/section/div/div/div[3]/span[2]').text
        print('app_id: {0}'.format(app_id))
        print('dev_id: {0}'.format(dev_id))
        print('cert_id: {0}'.format(cert_id))

        # 跳转应用详情页
        print('Turn to app detail ...')
        self.element_visible('//*[@id="w0"]/div/span')
        browser.execute_script("document.querySelector('#w2 > ul > li:nth-child(1) > a').click()")
        browser.execute_script("document.querySelector('#w2 > ul > li:nth-child(1) > div > a:nth-child(3)').click()")
        # browser.find_element_by_xpath('//*[@id="w2"]/ul/li[1]/div/a[3]').click()

        # 补充应用信息
        print('Turn to production ...')
        self.element_visible('//*[@id="w5-w0"]/div/fieldset/span[2]/label').click()
        self.element_visible('//*[@id="w6-w1-signin"]').click()
        self.element_visible('//*[@id="w4-w0-street1"]').send_keys('qwer')
        browser.find_element_by_xpath('//*[@id="w4-w0-state"]').send_keys('qwer')
        browser.find_element_by_xpath('//*[@id="w4-w0-city"]').send_keys('qwer')
        browser.find_element_by_xpath('//*[@id="w4-w0-postal"]').send_keys('qwer')
        browser.find_element_by_xpath('//*[@id="w4-w0-country"]/option[7]').click()
        browser.find_element_by_xpath('//*[@id="w4-w0-continue-to-get-token"]').click()

        # 填写用户账号
        print('Insert user account ...')  # fixme 此处等待时间过长 可作优化
        self.element_visible('//*[@id="userid"]').clear()
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
        assert (len(token) > 50), 'Bad token. :p'

        # 获取 runame
        browser.find_element_by_xpath('//*[@id="w6-getTokenApp"]').click()
        try:
            browser.execute_script("document.querySelector('#w6-w2-add-redirect-url-callout').click()")
        except WebDriverException:
            pass
        runame = self.element_visible('//*[@id="w6-w2-ruNames"]/ul/li/div/span[1]').text
        print('runame: {0}'.format(runame))

        # Insert token and app data to mysql or other database
        data = {}
        data['token'] = token
        data['app_id'] = app_id
        data['dev_id'] = dev_id
        data['cert_id'] = cert_id
        data['runame'] = runame
        data['username'] = username
        data['password'] = password
        self.save_tokens(data)

        # 注销
        print('Sign out ...')  # todo 因未知原因定在此处
        self.element_visible('//*[@id="w0"]/div/span')
        browser.execute_script("document.querySelector('#edp-headername').click()")
        browser.execute_script("document.querySelector('#w2 > ul > li:nth-child(1) > div > a:nth-child(7)').click()")

        print('Account: <{0}>, Done.'.format(username))
        return
        while 1:
            time.sleep(10)

    def close(self):
        self.browser.close()

    def run_circle(self, start, end):
        for i in range(start, end):
            self.run('srd_token_{0}'.format(i))
        print('Run Circle Done.')
        self.close()


def main(start, end):
    option = webdriver.ChromeOptions()
    # option.add_argument('--user-data-dir=~/.config/google-chrome')
    # option.add_extension('/host/DL/92jiasu.crx')
    browser = webdriver.Chrome(chrome_options=option)
    register = Register(browser)
    register.run_circle(start, end)


if __name__ == '__main__':
    p = Pool()
    p.apply_async(main, args=(512, 600,))
    p.close()
    p.join()

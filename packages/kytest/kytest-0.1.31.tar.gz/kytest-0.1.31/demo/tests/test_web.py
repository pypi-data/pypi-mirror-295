"""
@Author: kang.yang
@Date: 2023/11/16 17:50
"""
import kytest
from kytest.web import TC, Page, Elem


# ===========================页面定义============================================================
class IndexPage(Page):
    """首页"""
    url = "https://www-test.qizhidao.com/"
    loginBtn = Elem(xpath='(//div[text()="登录/注册"])[1]')
    patentText = Elem(xpath='//*[text()="查专利"]')


class LoginPage(Page):
    """登录页"""
    pwdTab = Elem(xpath='//*[text()="密码登录"]')
    userInput = Elem(xpath='//input[@placeholder="请输入手机号码"]')
    pwdInput = Elem(xpath='//input[@placeholder="请输入密码"]')
    accept = Elem(css=".agreeCheckbox .el-checkbox__inner")
    loginBtn = Elem(xpath='//*[text()="立即登录"]')
    firstItem = Elem(xpath="(//img[@class='right-icon'])[1]")


# 公共方法放在这个公共方法中
class CommonPage:
    """登录模块公共方法"""

    def __init__(self, driver):
        self.ip = IndexPage(driver)
        self.lp = LoginPage(driver)

    def login(self):
        """从首页进行登录"""
        username = "13652435335"
        password = 'wz123456@QZD'

        self.ip.open()
        self.ip.sleep(5)
        self.ip.loginBtn.click()
        self.ip.sleep(5)
        self.lp.pwdTab.click()
        self.lp.userInput.input(username)
        self.lp.pwdInput.input(password)
        self.lp.accept.click()
        self.lp.loginBtn.click()
        self.lp.firstItem.click()
# ============少的话就放用例中，多的话可以单独拆一个页面定义的模块========================================


# ===========================用例内容============================================================
@kytest.story('登录模块')
class TestWebDemo(TC):
    def start(self):
        self.common_page = CommonPage(self.dr)

    @kytest.title("登录")
    def test_login(self):
        self.common_page.login()
        self.assert_url()
        self.sleep(3)
        self.screenshot('登陆成功后的首页')
# ======可以用这种po模式，也可以直接使用self.elem(xpath='xxx').click的方式调用=============================




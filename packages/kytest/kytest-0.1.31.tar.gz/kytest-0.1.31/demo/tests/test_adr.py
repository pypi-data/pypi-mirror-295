import kytest
from kytest.adr import TC, Page, Elem


# ===========================页面定义============================================================
class AdrPage(Page):
    adBtn = Elem(rid='com.qizhidao.clientapp:id/bottom_btn')
    myTab = Elem(xpath='//android.widget.FrameLayout[4]')
    spaceTab = Elem(text='科创空间')
    setBtn = Elem(rid='com.qizhidao.clientapp:id/me_top_bar_setting_iv')
    title = Elem(rid='com.qizhidao.clientapp:id/tv_actionbar_title')
    agreeText = Elem(rid='com.qizhidao.clientapp:id/agreement_tv_2')
    moreService = Elem(xpath='//*[@resource-id="com.qizhidao.clientapp:id/layout_top_content"]'
                             '/android.view.ViewGroup[3]/android.view.View[10]')
# ============少的话就放用例中，多的话可以单独拆一个页面定义的模块========================================


# ===========================用例内容============================================================
@kytest.story('测试demo')
class TestAdrDemo(TC):
    def start(self):
        self.dp = AdrPage(self.dr)

    @kytest.title('进入设置页')
    def test_go_setting(self):
        self.start_app()
        self.dp.adBtn.click_exists()
        self.dp.myTab.click()
        self.dp.setBtn.click()
        self.screenshot("设置页")
        self.sleep(5)
        self.stop_app()
# ======可以用这种po模式，也可以直接使用self.elem(rid='xxx').click的方式调用=============================




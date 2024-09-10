"""
@Author: kang.yang
@Date: 2024/7/12 17:10
"""
import kytest
from data.login_data import get_headers


if __name__ == '__main__':
    kytest.kconfig['browser'] = 'firefox'
    kytest.main(
        proj="平台项目自动化测试报告",
        # path="tests/test_adr.py",
        # path="tests/test_web.py",
        # path="tests/test_api.py",
        path="tests",
        pkg="com.qizhidao.clientapp",  # 针对IOS和安卓
        host="https://app-test.qizhidao.com/",  # 接口常用，如果没有web_host设置，也使用这个
        web_host="https://www-test.qizhidao.com/",  # 针对接口和web测试并存的情况，web测试使用该参数
        headers=get_headers()
    )


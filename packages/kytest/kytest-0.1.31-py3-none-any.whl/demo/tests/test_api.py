"""
@Author: kang.yang
@Date: 2023/11/16 17:52
"""
import kytest
from requests_toolbelt import MultipartEncoder


@kytest.story('pc首页')
class TestApiDemo(kytest.TC):

    @kytest.title('金刚位')
    def test_normal_req(self):
        url = '/qzd-bff-app/qzd/v1/home/getToolCardListForPc'
        params = {"type": 2}
        self.post(url, json=params)
        self.assertEq('data[*].showType', 2)

    @kytest.title("文件上传")
    def test_upload_file(self):
        path = '/qzd-bff-patent/patent/batch/statistics/upload'
        m = MultipartEncoder(
            fields={
                'file': ('号码上传模板.xlsx', open("data/号码上传模板.xlsx", "rb"),
                         "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            }
        )
        self.post(path, data=m, headers={'Content-Type': m.content_type})
        self.assertEq('code', 0)

    @kytest.title("form请求")
    def test_form_req(self):
        url = '/qzd-bff-patent/image-search/images'

        m = MultipartEncoder(
            fields={
                # 'key1': 'value1',
                'imageFile': (
                    'logo.png', open('data/logo.png', 'rb'), 'image/png'
                )
            }
        )
        headers = {'Content-Type': m.content_type}
        self.post(url, data=m, headers=headers)
        self.assertEq("code", 0)

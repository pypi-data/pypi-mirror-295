import asyncio
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
import json
import aiohttp


class SMS阿里云:
    userID = 'sms@.onaliyun.com'

    def __init__(self, accessKeyId, accessSecret):
        self.client = AcsClient(accessKeyId, accessSecret, 'cn-hangzhou')

    async def 发送短信验证码SMS(self, 手机号: str,
                                验证码: str,
                                短信模板: str = "SMS_168725021",
                                短信签名: str = "景募"):
        request = CommonRequest()
        # ... 设置请求参数 ...
        request.add_query_param('TemplateParam', "{\"code\":%s}" % 验证码)

        async with aiohttp.ClientSession() as session:
            async with session.post(url='https://dysmsapi.aliyuncs.com',
                                    data=request.get_body_params(),
                                    headers=request.get_headers()) as response:
                content = await response.text()
                return json.loads(content)


async def main():
    sms = SMS阿里云('...', '...')
    re = await sms.发送短信验证码SMS('17512541044', "12345")
    print(re)


if __name__ == '__main__':
    asyncio.run(main())

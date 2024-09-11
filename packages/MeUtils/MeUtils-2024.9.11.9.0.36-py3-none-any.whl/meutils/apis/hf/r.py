#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : r
# @Time         : 2024/9/2 14:39
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : https://swanhub.co/cunyue/person-modnet/demo
from meutils.pipe import *
from meutils.request_utils import create_request

from meutils.io.image import image_to_base64

url = "https://cunyue-person-modnet.demo.swanhub.co/run/predict"
image_url = "https://cunyue-person-modnet.demo.swanhub.co/file=/app/image/image04.jpg"

payload = {
    "data": [image_to_base64(image_url)],
}


if __name__ == '__main__':


    arun(create_request(url, payload))
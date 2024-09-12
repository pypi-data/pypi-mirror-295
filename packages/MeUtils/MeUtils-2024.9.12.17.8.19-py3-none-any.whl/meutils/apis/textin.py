#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : textin
# @Time         : 2024/6/26 08:22
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : todo: 重构

from meutils.pipe import *
from meutils.io.image import base64_to_file


@alru_cache(ttl=3600 * 24)
async def textin_fileparser(data: bytes, page_count: int = 1000, service: str = "pdf_to_markdown"):
    params = {
        "service": service,
        "page_count": page_count,
        # "get_image": "objects"
        "apply_document_tree": 0
    }

    base_url = f"https://api.textin.com/home/user_trial_ocr?service={service}&page_count={page_count}"
    async with httpx.AsyncClient(base_url=base_url, timeout=120) as client:
        response = await client.post('/', content=data)

        if response.is_success:
            return response.json()

        response.raise_for_status()


if __name__ == '__main__':
    data = open("/Users/betterme/PycharmProjects/AI/11.jpg", 'rb').read()
    # data = open("/Users/betterme/PycharmProjects/AI/蚂蚁集团招股书.pdf", 'rb').read()
    # with timer("解析"):
    #     # arun(textin_fileparser(data))
    #     print(arun(textin_fileparser(data)))

    # response = requests.request("POST", url, data=data)
    # data = open("/Users/betterme/PycharmProjects/AI/watermark.png", 'rb').read()

    data = open("/Users/betterme/PycharmProjects/AI/doc_watermark.jpg", 'rb').read()
    from meutils.schemas.task_types import Purpose

    service = 'watermark-remove'
    service = Purpose.watermark_remove
    with timer("解析"):
        # arun(textin_fileparser(data))
        data = arun(textin_fileparser(data, service=service))

        b64 = data['data']['result']['image']

        base64_to_file(b64, "demo.png")

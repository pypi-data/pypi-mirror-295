#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : kolors
# @Time         : 2024/7/25 08:42
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : https://huggingface.co/spaces/gokaygokay/KolorsPlusPlus
# https://huggingface.co/spaces/Kwai-Kolors/Kolors-Virtual-Try-On

from meutils.pipe import *
from meutils.schemas.openai_types import ImageRequest, ImagesResponse
from meutils.async_utils import sync_to_async
from meutils.decorators.retry import retrying

from gradio_client import Client as _Client, handle_file
from meutils.io.image import image_to_base64

from gradio_client import Client

client = Client("https://cunyue-person-modnet.demo.swanhub.co/")


url = "https://cunyue-person-modnet.demo.swanhub.co/file=/app/image/image04.jpg"
result = client.predict(
    data=[image_to_base64(url)],
    # str (filepath or URL to image) in 'Image' Image component
    api_name="/predict"
)
print(result)


print(client.view_api())


hivisionidphotos
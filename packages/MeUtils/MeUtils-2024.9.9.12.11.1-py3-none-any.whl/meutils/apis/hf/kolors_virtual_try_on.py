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

Client = lru_cache(_Client)

ENDPOINT = "Kwai-Kolors/Kolors-Virtual-Try-On"


@sync_to_async(thread_sensitive=False)
@retrying()
def create():
    token = None
    # token = os.getenv("HF_TOKEN")

    client = Client(ENDPOINT, download_files=False, hf_token=token)

    result = client.predict(
        person_img=handle_file('https://kwai-kolors-kolors-virtual-try-on.hf.space/file=/tmp/gradio/e0de58607c53358c8199c23ecf808eebdfcc8f19/model2.png'),
        garment_img=handle_file('https://kwai-kolors-kolors-virtual-try-on.hf.space/file=/tmp/gradio/261a026192b36b29a328374701b69218c773eb65/11_upper.png'),
        seed=0,
        randomize_seed=True,
        api_name="/tryon"
    )

    return result


if __name__ == '__main__':

    with timer():
        arun(create())

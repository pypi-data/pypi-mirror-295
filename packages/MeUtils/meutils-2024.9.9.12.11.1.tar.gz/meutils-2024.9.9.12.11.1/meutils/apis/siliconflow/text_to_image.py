#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : text_to_image
# @Time         : 2024/7/8 12:19
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : https://docs.siliconflow.cn/reference/stabilityaistable-diffusion-3-medium_text-to-image

from meutils.pipe import *
from meutils.pipe import storage_to_cookie
from meutils.config_utils.lark_utils import get_spreadsheet_values, get_next_token_for_polling
from meutils.schemas.openai_types import ImageRequest, ImagesResponse
from meutils.apis.translator import deeplx
from meutils.schemas.translator_types import DeeplxRequest
from meutils.decorators.retry import retrying
from meutils.schemas.image_types import ASPECT_RATIOS

BASE_URL = "https://cloud.siliconflow.cn"
FEISHU_URL = "https://xchatllm.feishu.cn/sheets/Bmjtst2f6hfMqFttbhLcdfRJnNf?sheet=InxiCF"
FEISHU_URL_TOKEN = "https://xchatllm.feishu.cn/sheets/Bmjtst2f6hfMqFttbhLcdfRJnNf?sheet=xlvlrH"


# https://cloud.siliconflow.cn/api/redirect/model?modelName=black-forest-labs/FLUX.1-schnell&modelSubType=text-to-image

@retrying(max_retries=3, title=__name__)
async def create_image(request: ImageRequest):
    cookie = await get_next_token_for_polling(feishu_url=FEISHU_URL_TOKEN)

    prompt = (await deeplx.translate(DeeplxRequest(text=request.prompt, target_lang="EN"))).get("data")

    params = {
        "modelName": request.model,  # stabilityai/stable-diffusion-3-medium
        "modelSubType": "text-to-image"
    }

    data = f'{{"image_size":"{request.size}","batch_size":{request.n},' \
           f'"num_inference_steps":{request.num_inference_steps},"guidance_scale":{request.guidance_scale},'

    if request.negative_prompt:
        data += f'"negative_prompt":"{request.negative_prompt}",'

    if request.seed:
        data += f'"seed":{request.seed},'

    data += f'"prompt":"{prompt}"}}'

    headers = {
        'Cookie': cookie,
    }

    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=100, follow_redirects=True) as client:
        response = await client.post("/api/redirect/model", params=params, content=data)
        if response.is_success:
            data = response.json().get('images', [])
            return ImagesResponse(data=data)

        response.raise_for_status()


@retrying(max_retries=5, title=__name__)
async def create(request: ImageRequest, api_key: Optional[str] = None):  # SD3
    api_key = api_key or await get_next_token_for_polling(feishu_url=FEISHU_URL)

    base_url = "https://api.siliconflow.cn/v1"

    request.prompt = (await deeplx.translate(DeeplxRequest(text=request.prompt, target_lang="EN"))).get("data")

    # if not request.prompt_enhancement:
    #     request.prompt = (await deeplx.translate(DeeplxRequest(text=request.prompt, target_lang="EN"))).get("data")
    payload = {
        "prompt": request.prompt.replace("(", "[").replace(")", "]"),
        "image_size": ASPECT_RATIOS.get(request.size, request.size),
        "batch_size": request.n,
        "num_inference_steps": request.num_inference_steps,
        "guidance_scale": request.guidance_scale,
    }
    if request.model.startswith(("ByteDance", "stabilityai")):
        payload['num_inference_steps'] = 4
        payload['guidance_scale'] = 1

    headers = {
        "Authorization": f"Bearer {api_key}",
    }

    async with httpx.AsyncClient(base_url=base_url, headers=headers, timeout=100) as client:
        response = await client.post(f"{request.model}/text-to-image", json=payload)

        if response.is_success:
            data = response.json().get('images', [])
            return ImagesResponse(data=data)
        raise response.raise_for_status()  # 451
        # from fastapi import HTTPException, status

        # raise HTTPException(status_code=response.status_code, detail=response.text) from response.raise_for_status()


if __name__ == '__main__':
    # cookie = await get_next_token_for_polling(feishu_url="https://xchatllm.feishu.cn/sheets/Bmjtst2f6hfMqFttbhLcdfRJnNf?sheet=xlvlrH")
    # api_key = storage_to_cookie(cookie)

    # storage_state = get_spreadsheet_values(feishu_url="https://xchatllm.feishu.cn/sheets/Bmjtst2f6hfMqFttbhLcdfRJnNf?sheet=xlvlrH",
    #                            to_dataframe=True)[0]

    # cookie = storage_to_cookie(storage_state[0])

    # request = ImageRequest(
    #     # model="stabilityai/stable-diffusion-3-medium",
    #     # model="black-forest-labs/FLUX.1-schnell",
    #     model="black-forest-labs/FLUX.1-dev",
    #
    #     prompt="一条可爱的狗"
    # )
    # print(arun(create_image(request)))

    # arun(get_next_token_for_polling(feishu_url=FEISHU_URL_TOKEN))
    # request = ImageRequest(
    #     prompt="画条狗",
    #     model="stabilityai/stable-diffusion-3-medium"
    # )
    #
    # with timer():
    #     arun(
    #         api_create_image(
    #             request
    #         )
    #     )
    #
    # 内容审核测试
    prompt = """
    画条狗
    """
    request = ImageRequest(
        prompt=prompt,
        # model="black-forest-labs/FLUX.1-dev",
        # model="black-forest-labs/FLUX.1-schnell",
        model="ByteDance/SDXL-Lightning",

        # size='1366x1366',
        n=1
    )

    with timer():

        try:
            arun(
                create(
                    request,
                )
            )
        except Exception as e:
            print(e)
    # request = ImageRequest(
    #     prompt=prompt,
    #     model="black-forest-labs/FLUX.1-dev"
    # )
    #
    # with timer():
    #     arun(
    #         api_create_image(
    #             request
    #         )
    #     )

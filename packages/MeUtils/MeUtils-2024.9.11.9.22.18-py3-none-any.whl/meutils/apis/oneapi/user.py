#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : user
# @Time         : 2024/7/19 14:58
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import json
import os

from meutils.pipe import *
from meutils.schemas.oneapi_types import BASE_URL

# https://api.chatfire.cn/api/user/814

token = os.environ.get("CHATFIRE_ONEAPI_TOKEN")

headers = {
    "Authorization": f"Bearer {token}",
}


# https://api.chatfire.cn/api/user/token 刷新token
# https://api.chatfire.cn/api/user/1
# async def get_user(user_id):
#     async with httpx.AsyncClient(base_url=BASE_URL, headers=headers) as client:
#         response = await client.get(f"/api/user/{user_id}")
#         logger.debug(response.text)
#
#         if response.is_success:
#             data = response.json()
#             return data
@alru_cache()
async def get_api_key_log(api_key: str):
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=30) as client:
        response = await client.get("/api/log/token", params={"key": api_key})

        # logger.debug(response.text)

        if response.is_success:
            data = response.json()['data']
            return data and data[:1]


async def get_user(user_id):
    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=30) as client:
        response = await client.get(f"/api/user/{user_id}")
        # logger.debug(response.text)

        if response.is_success:
            data = response.json()
            return data


async def get_user_money(api_key):
    data = await get_api_key_log(api_key)
    if data:
        user_id = data[0]['user_id']
        data = await get_user(user_id)
        logger.debug(data)
        if data:
            username = data['data']['username']
            quota = data['data']['quota']
            return quota / 500000  # money


async def put_user(payload, add_money: float = 0):
    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers) as client:
        payload['quota'] = max(payload['quota'] + add_money * 500000, 0)  # 1块钱对应50万

        response = await client.put("/api/user/", json=payload)
        # logger.debug(response.text)
        # logger.debug(response.status_code)

        return response.json()


if __name__ == '__main__':
    # api-key => get_one_log => get_user => put_user
    # arun(get_user(814))
    # payload = arun(get_user(814))['data']
    # print(payload)
    # arun(put_user(payload, -1))

    arun(get_api_key_log('sk-WEmN6rbcmEu5jRUT5c6b2d672119435c999d308bCc124009'))
    arun(get_user_money("sk-HqdUIjaV3r2QeqpTEeE7Ef6605C94809Ab1761858f96E565"))

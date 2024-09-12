#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : video
# @Time         : 2024/7/26 12:03
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from meutils.schemas.chatglm_types import VideoRequest, Parameter, BASE_URL, VIDEO_BASE_URL, EXAMPLES
from meutils.schemas.task_types import Task, FileTask

from meutils.decorators.retry import retrying
from meutils.notice.feishu import send_message as _send_message
from meutils.config_utils.lark_utils import get_next_token_for_polling

FEISHU_URL = "https://xchatllm.feishu.cn/sheets/Bmjtst2f6hfMqFttbhLcdfRJnNf?sheet=siLmTk"
send_message = partial(
    _send_message,
    title=__name__,
    url="https://open.feishu.cn/open-apis/bot/v2/hook/dc1eda96-348e-4cb5-9c7c-2d87d584ca18"
)


@alru_cache(ttl=1 * 3600)
@retrying()
async def get_access_token(refresh_token: str):
    logger.debug(refresh_token)

    headers = {
        "Authorization": f"Bearer {refresh_token}",
    }
    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers) as client:
        response = await client.post('/user/refresh')
        logger.debug(response.status_code)
        logger.debug(response.text)

        return response.json()['result']['accessToken']


async def upload(file: bytes, token: Optional[str] = None):
    token = token or await get_next_token_for_polling(FEISHU_URL)
    access_token = await get_access_token(token)

    headers = {
        'Authorization': f'Bearer {access_token}',
    }

    files = [('file', ('x.png', file, 'image/png'))]

    async with httpx.AsyncClient(base_url=VIDEO_BASE_URL, headers=headers, timeout=60) as client:
        response = await client.post('/static/upload', files=files)

        logger.debug(response.text)
        logger.debug(response.status_code)

        if response.is_success:
            data = response.json()
            if data['status'] == 0:
                return data, token
            raise Exception(data)

        response.raise_for_status()

        # {'message': 'success',
        #  'result': {'source_id': '66a8aa225d5f1682b2a07b5c',
        #             'source_url': 'https://sfile.chatglm.cn/chatglm-videoserver/image/50/5049bae9.png'},
        #  'rid': '6068cc37fd6348728386d15418c438a2',
        #  'status': 0}


async def upload_task(file: bytes, token: Optional[str] = None):
    token = token or await get_next_token_for_polling(FEISHU_URL)
    access_token = await get_access_token(token)

    headers = {
        'Authorization': f'Bearer {access_token}',
    }

    files = [('file', ('x.png', file, 'image/png'))]

    async with httpx.AsyncClient(base_url=VIDEO_BASE_URL, headers=headers, timeout=60) as client:
        response = await client.post('/static/upload', files=files)

        logger.debug(response.text)
        logger.debug(response.status_code)

        if response.is_success:
            data = response.json()
            if data['status'] == 0:
                return FileTask(
                    id=data['result']['source_id'],
                    url=data['result']['source_url'],
                    data=data,
                    system_fingerprint=token
                )
        response.raise_for_status()


@retrying(max_retries=8, max=8, predicate=lambda r: r is True, title=__name__)
async def create_task(request: VideoRequest, token: Optional[str] = None):
    token = token or await get_next_token_for_polling(FEISHU_URL)
    access_token = await get_access_token(token)

    headers = {
        'Authorization': f'Bearer {access_token}',
    }
    payload = request.model_dump()
    async with httpx.AsyncClient(base_url=VIDEO_BASE_URL, headers=headers, timeout=30) as client:
        response = await client.post('/chat', json=payload)

        logger.debug(response.text)
        logger.debug(response.status_code)

        if response.is_success:
            data = response.json()

            if any(i in str(data) for i in {"请稍后再试", }):  # 重试
                return True

            task_id = f"cogvideox-{data['result']['chat_id']}"
            return Task(id=task_id, data=data, system_fingerprint=token)

        response.raise_for_status()


async def get_task(task_id: str, token: str):
    task_id = isinstance(task_id, str) and task_id.split("-", 1)[-1]
    access_token = await get_access_token(token)

    headers = {
        'Authorization': f'Bearer {access_token}',
    }
    async with httpx.AsyncClient(base_url=VIDEO_BASE_URL, headers=headers, timeout=30) as client:
        response = await client.get(f"/chat/status/{task_id}")

        logger.debug(response.text)
        logger.debug(response.status_code)

        if response.is_success:
            data = response.json()
            return data

        response.raise_for_status()


async def composite_video(task_id: str, token: str = None):
    access_token = await get_access_token(token)

    headers = {
        'Authorization': f'Bearer {access_token}',
    }
    payload = {
        "chat_id": task_id,
        "key": "quiet",
        "audio_id": "669b799d7a9ebbe698de2102"
    }
    # 669b790d7a9ebbe698de20f6 回忆老照片 todo:
    # {chat_id: "66a325cbf66684c40b362a30", key: "epic", audio_id: "669b809d3915c1ddbb3d6705"} 灵感迸发

    async with httpx.AsyncClient(base_url=VIDEO_BASE_URL, headers=headers) as client:
        response = await client.post('/static/composite_video', json=payload)

        logger.debug(response.text)
        logger.debug(response.status_code)

        if response.is_success:
            data = response.json()
            return data
        response.raise_for_status()


# https://chatglm.cn/chatglm/video-api/v1/trial/apply post申请
# https://chatglm.cn/chatglm/video-api/v1/trial/status check权限

async def check_token(refresh_token: str):
    access_token = await get_access_token(refresh_token)

    headers = {
        'Authorization': f'Bearer {access_token}',
    }
    url = "https://chatglm.cn/chatglm/video-api/v1/trial/status"
    return httpx.get(url, headers=headers).json()


if __name__ == '__main__':
    refresh_oken = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMDdlZDVkMDhlY2M0YzFmOGQ1NGU4OGQyMzVmMDYxZCIsImV4cCI6MTczNzg3NzYwNiwibmJmIjoxNzIyMzI1NjA2LCJpYXQiOjE3MjIzMjU2MDYsImp0aSI6ImQxNGNkZTk1ODg2NTRjZjJhZmMzMTYyYzhkOGU3YWZhIiwidWlkIjoiNjYxMTdjNGI1NGIwOTE2NjFjMDZmZWFlIiwidHlwZSI6InJlZnJlc2gifQ.4puphxxCPi5zXIsb1CxuuoJthILYgs9b31Hacq5BePg"

    # token = arun(get_access_token(refresh_oken))
    #     # request = VideoRequest(**EXAMPLES[0])
    #     # arun(create_task(request))
    #     # token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3YmFmYWQzYTRmZDU0OTk3YjNmYmNmYjExMjY5NThmZiIsImV4cCI6MTcyMjA1OTYyOSwibmJmIjoxNzIxOTczMjI5LCJpYXQiOjE3MjE5NzMyMjksImp0aSI6ImU3ZTQzNmFiY2IzMDQ2M2M4NTU2M2EzMDI0ODhiYmExIiwidWlkIjoiNjVmMDc1Y2E4NWM3NDFiOGU2ZmRjYjEyIiwidHlwZSI6ImFjY2VzcyJ9.ToOESTWv-EJmhneE14czdAv59OulpuA-FLcB8f190zU"
    #
    # request = VideoRequest(**EXAMPLES[0])
    # arun(create_task(request, refresh_oken))
    # arun(create_task(request))

    # arun(get_task('cogvideox-66ab320d18dd2553920bd664', refresh_oken))
    file = Path("/Users/betterme/PycharmProjects/AI/cover.jpeg").read_bytes()
    arun(upload_for_openai(file))

    # arun(refresh_token(refresh_oken))

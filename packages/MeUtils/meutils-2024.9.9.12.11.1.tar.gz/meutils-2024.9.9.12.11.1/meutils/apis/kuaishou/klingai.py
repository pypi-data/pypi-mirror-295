#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : klingai
# @Time         : 2024/7/9 13:23
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import jsonpath

from meutils.pipe import *
from meutils.decorators.retry import retrying
from meutils.schemas.kuaishou_types import BASE_URL, UPLOAD_BASE_URL, KlingaiImageRequest, FEISHU_URL, FEISHU_URL_VIP
from meutils.notice.feishu import send_message as _send_message
from meutils.config_utils.lark_utils import get_next_token_for_polling
from meutils.schemas.task_types import Task, FileTask

send_message = partial(
    _send_message,
    title=__name__,
    url="https://open.feishu.cn/open-apis/bot/v2/hook/dc1eda96-348e-4cb5-9c7c-2d87d584ca18"
)


@retrying(max_retries=3, title=__name__)  # 触发重试
async def upload(file: bytes, filename: Optional[str] = None, cookie: Optional[str] = None,
                 vip: bool = False):  # 应该不绑定cookie

    vip = True  # 上传强制走 vip 保证稳定性

    cookie = cookie or await get_next_token_for_polling(FEISHU_URL_VIP if vip else FEISHU_URL, check_token=check_token)

    filename = filename or f"{shortuuid.random()}.png"

    headers = {
        'Cookie': cookie,
        'Content-Type': 'application/json;charset=UTF-8'
    }

    async with httpx.AsyncClient(base_url=UPLOAD_BASE_URL, headers=headers, timeout=100) as client:
        # 文件名生成token
        response = await client.get(f"{BASE_URL}/api/upload/issue/token", params={"filename": filename})
        logger.debug(response.json())

        token = jsonpath.jsonpath(response.json(), "$.data.token")[0]  ####### bool[0]

        # 判断是否存在
        response = await client.get("/api/upload/resume", params={"upload_token": token})
        # {"result":1,"existed":true,"fragment_index":-1,"fragment_list":[],"endpoint":[{"protocol":"KTP","host":"103.107.217.16","port":6666},{"protocol":"KTP","host":"103.102.202.156","port":6666},{"protocol":"TCP","host":"103.107.217.16","port":6666}],"fragment_index_bytes":0,"token_id":"d36ce45c09ce9b84","prefer_http":false}
        logger.debug(response.json())

        # 上传
        response = await client.post(
            "/api/upload/fragment",
            params={"fragment_id": 0, "upload_token": token},
            content=file
        )
        logger.debug(response.json())

        # 校验
        response = await client.post(
            "api/upload/complete",
            params={"fragment_count": 1, "upload_token": token},
        )
        logger.debug(response.json())

        # 最终
        response = await client.get(f"{BASE_URL}/api/upload/verify/token", params={"token": token})
        if response.is_success:
            data = response.json()
            # logger.debug(data)
            # send_message(data)
            # {'status': 200, 'message': '成功', 'data': {'status': 8, 'url': '', 'message': '上传图片包含敏感信息'}, 'timestamp': [2024, 8, 30, 17, 32, 37, 964976000]}

            url = data['data']['url']
            return FileTask(url=url, data=data, system_fingerprint=token)

        response.raise_for_status()


@retrying(max_retries=5, predicate=lambda r: not r, title=__name__)
async def create_task(request: KlingaiImageRequest, token: Optional[str] = None, vip: bool = False):
    cookie = token or await get_next_token_for_polling(FEISHU_URL_VIP if vip else FEISHU_URL, check_token=check_token)

    headers = {
        'Cookie': cookie,
        'Content-Type': 'application/json;charset=UTF-8'
    }

    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=60) as client:
        response = await client.post("/api/task/submit", json=request.payload)

        logger.debug(response.status_code)
        logger.debug(response.text)

        if response.is_success:
            data = response.json()
            send_message(data)

            # 触发重试 404 429 520
            if any(i in str(data) for i in {"页面未找到", "请求超限", "配额耗尽", "积分消费失败"}):
                send_message(f"{data}\n\n{cookie}")
                return

            try:
                task_ids = jsonpath.jsonpath(data, "$..task.id")  # $..task..[id,arguments]
                if task_ids:
                    task_id = task_ids[0]
                    return Task(id=task_id, data=data, system_fingerprint=cookie)
                else:
                    return Task(status=0, data=data)

            except Exception as e:
                logger.error(e)
                send_message(f"未知错误：{e}")


@retrying(max_retries=16, exp_base=1.1, predicate=lambda r: r == "RETRYING")  # 触发重试
async def get_task(task_id, cookie: str):
    headers = {
        'Cookie': cookie,
        'Content-Type': 'application/json;charset=UTF-8'
    }

    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=60) as client:
        response = await client.get("/api/task/status", params={"taskId": task_id, "withWatermark": False})
        if response.is_success:
            data = response.json()

            logger.debug(data)

            if not task_id or "failed," in str(data): return "TASK_FAILED"  # 跳出条件

            urls = jsonpath.jsonpath(data, '$..resource.resource')
            if urls and all(urls):
                images = [{"url": url} for url in urls]
                return images
            else:
                return "RETRYING"  # 重试


@retrying(max_retries=3)
async def create_image(request: KlingaiImageRequest):
    vip = True
    task = await create_task(request, vip=vip)

    logger.debug(task)

    data = await get_task(task.id, task.system_fingerprint)

    return data


@alru_cache(ttl=30)
@retrying()
async def get_reward(cookie: str):
    headers = {
        'Cookie': cookie,
        'Content-Type': 'application/json;charset=UTF-8'
    }
    params = {"activity": "login_bonus_daily"}
    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers) as client:
        response = await client.get("/api/pay/reward", params=params)
        if response.is_success:
            data = response.json()
            return data


@alru_cache(ttl=30)
@retrying()
async def get_point(cookie: str):
    headers = {
        'Cookie': cookie,
        'Content-Type': 'application/json;charset=UTF-8'
    }
    await get_reward(cookie)

    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=15) as client:
        response = await client.get("/api/account/point")
        if response.is_success:
            data = response.json()
            return data
        # response.raise_for_status()


async def check_token(token, threshold=10):
    try:
        data = await get_point(token)
        # logger.debug(data['data']['total'])

        return data['data']['total'] >= threshold * 100  # 视频
    except Exception as e:
        logger.error(f"{e}\n无效{token}")
        return False


if __name__ == '__main__':
    # token="weblogger_did=web_9665177505014D12; _gcl_au=1.1.961392860.1725442018; did=web_d77db05423a7f37445a28355351bf2736bf0; userId=5138238; ksi18n.ai.portal_st=ChNrc2kxOG4uYWkucG9ydGFsLnN0EqABqRUW14ibaB-hwLGxZAlwhkzCKaSz-D2KvRfHtYKdqyOyowP5a5Dg2caDxFhL8r6FY0FhWtGh21qSzpxuVfVRLd3JSt43pp9O8IN-8q-d5YyDcaIyIhWfrAxKe_4Pk-Myb-lp1l7T2oUuwhH4ULkhpYgleh2FW6PgkxmlxKyWtDOA3c0q8d3YG7KtxPTQnoV175iPFhfi2Px7RChec3GhCBoSSEjmKhUuRI7OeXOQ1U6phkEJIiCOLbZNE8-xbaRn8agXQX1y2jB025mS9Rn31D3Vxm934SgFMAE; ksi18n.ai.portal_ph=462580e5c345322c372722c3ccccfb28f17e"
    # arun(check_token(token))

    # 存活率
    # arun(get_next_token_for_polling(feishu_url=FEISHU_URL, check_token=check_token))

    # arun(get_next_token_for_polling(feishu_url=FEISHU_URL_VIP, check_token=check_token))

    # https://xchatllm.feishu.cn/sheets/Bmjtst2f6hfMqFttbhLcdfRJnNf?sheet=v8vcZY
    # url = "https://s22-def.ap4r.com/bs2/upload-ylab-stunt-sgp/ai_portal/1724806149/rXWnzc3Dhv/x.png"
    #
    request = KlingaiImageRequest(
        prompt="笑起来", imageCount=1,
        # url=url
    )  # 27638649
    # token = "monetization-ads-shown-count-xx=T;_gcl_au=1.1.1994862793.1723432037;did=web_b11919c67a1966b83eaef4a19fb2de266cba;ksi18n.ai.portal_ph=4ab564ff72d22ac3c25c0dacd35cbd5d68ca;ksi18n.ai.portal_st=ChNrc2kxOG4uYWkucG9ydGFsLnN0EqABlvpmXr2OeS7mUSuMO-KL1sVJfy5GcuzNso0ZdOKIlmXj42dZqAjU_14VrJV-e2Yrp4OODrbKy-ZioGBZg1pnU0PKbgK_okknTNnVhujftS8xQoIBvwuIQYoErKr6NNrcIgPnwLvZMYZc4oQLCrs0xNlkm_S4ZET44R3T7PJntudwzNuoIT_5QOn0HMja6Q80eon0o4Zw2-ivZevLwNsWghoSp94kUOm9gCAed8BLne8huz5PIiAM29axw-J1X8AUXudFsw-ZaBZY83v2XfR1d6CAz3roaygFMAE;monetization-ads-shown-count-xxx=T;userId=3426808;weblogger_did=web_8897873009A74F8"
    # token = "_gcl_au=1.1.2117561676.1724226781;did=web_219408fbb50842a98d7b2d6bdb6549fa98f9;ksi18n.ai.portal_ph=b597d7d5856b3c29e0b279defe349b0fc88a;ksi18n.ai.portal_st=ChNrc2kxOG4uYWkucG9ydGFsLnN0EqABdJQ_kVVXVCqIczbfFLJT5Swq6ibgU2mkEOe0njB-ElJnZWI1_Ukw3xikycgE9WLxak5tQpCv8YdEBEiTbcu-YxCs8ntqJkrTpAxcP7a-j216wxvUwzlNcmmK12OlXLaXBRRLgsul9XLnff-d91eCjDnY27y0nb7PizdWdgdbJ39G7xuiTnvZar6TH4nAScGrXSFM5fhVCNJJT1f_yT79bRoSn4p1S_AmSvxx8MBv-fWXfBXKIiBNx-fSmLqe0EJl_zEozwLjbzirH0CJj_lqibAoDmUXHygFMAE;userId=3626555;weblogger_did=web_4557277593AC34F7"

    # arun(get_point(token))
    # cookie = "weblogger_did=web_47164250171DB527; did=web_e022fde52721456f43cb66d90a7d6f14e462; userId=742626779; kuaishou.ai.portal_st=ChVrdWFpc2hvdS5haS5wb3J0YWwuc3QSoAGAEPOivL4BJ2Y8y48CvR-t25o44Sj_5G9LnZI8BJbV_Inkqd4qxPMJy4OqZCf0VHZnr8EcgMHOzuj_fw5-x0OF3UtrXrU2ZBe6G_bnD1umPIAL6DVtv6ERJ9uLpa7asCBgIUvMXk6K345vc5okzhoTPw69b1GsXY777qwuOwGoUrP9eyJc6Z4TeQPYDEW2wdazss7Dn2osIhObsW9izb1yGhJaTSf_z6v_i70Q1ZuLG30vAZsiIGMXZhr3i8pOgOICzAXA0T6fJZZk3hFRsxn3MDQzIeiKKAUwAQ; kuaishou.ai.portal_ph=fe74c1e2fb91142f838c4b3d435d6153ccf3"
    # cookie = "did=web_bd7da66e83ea345fac39694d32d4672b9e07;ksi18n.ai.portal_st=ChNrc2kxOG4uYWkucG9ydGFsLnN0EqAB1Xjdnlyrc7pKORRU-g10oEUbejZbRSGuv4CKK6_colUDfWdfBysqENjMM11prWCVJqKCLUKgy9U3XxPD7KVtgd_nEom9gS1TnzFWDYjgnnULYyszQ9C9DPylj9glH_xThIuy9rN6gpLxPnRtTwj2fh7f1Uy_cSzkOQx_Th3ePnpauTOw-KhCE25G6eXteybcjjotKgd2JWKcKd_3QqRIDhoSBRHAf_JILfM_YhcnxIVtU2YmIiBzb2VMb2UCDTac51ufmB9GzIPUXMNvgrqbKQr8GigFpigFMAE;userId=3431862"
    # task = arun(create_task(request))
    #
    # arun(get_task(task.id, task.system_fingerprint))

    # pprint(arun(get_task(46578557)))
    #
    # pprint())

    # file = open("/Users/betterme/PycharmProjects/AI/kling_watermark.png", "rb").read()
    # file = open("/Users/betterme/PycharmProjects/AI/MeUtils/examples/apis/lzp.jpg", "rb").read()
    #
    # arun(upload(file))

    # print(request)
    #
    arun(create_image(request))

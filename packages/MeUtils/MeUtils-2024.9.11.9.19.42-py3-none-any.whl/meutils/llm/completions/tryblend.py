#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : tryblend
# @Time         : 2024/9/4 09:22
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :


from meutils.pipe import *
from meutils.notice.feishu import send_message as _send_message
from meutils.db.redis_db import redis_client, redis_aclient
from meutils.config_utils.lark_utils import aget_spreadsheet_values, get_next_token_for_polling
from meutils.schemas.tryblend_types import BASE_URL, FEISHU_URL, FEISHU_URL_VIP
from meutils.schemas.tryblend_types import GPT_4O_MINI, GPT_4O
from meutils.schemas.tryblend_types import CLAUDE_3_HAIKU, CLAUDE_3_SONNET, CLAUDE_3_OPUS, CLAUDE_35_SONNET
from meutils.schemas.tryblend_types import PERPLEXITY_SONAR_SMALL, PERPLEXITY_SONAR_LARGE, PERPLEXITY_SONAR_HUGE

from meutils.llm.openai_utils import to_openai_completion_params, token_encoder, token_encoder_with_cache
from meutils.schemas.openai_types import chat_completion, chat_completion_chunk, ChatCompletionRequest, CompletionUsage
from openai import OpenAI, AsyncOpenAI, APIStatusError

# from meutils.llm.openai_utils import create_chat_completion_chunk, create_chat_completion

send_message = partial(
    _send_message,
    url="https://open.feishu.cn/open-apis/bot/v2/hook/e0db85db-0daf-4250-9131-a98d19b909a9",
    title=__name__
)


class Completions(object):

    def __init__(self, api_key: Optional[str] = None, vip: bool = False):
        self.api_key = api_key or await get_next_token_for_polling(feishu_url=FEISHU_URL_VIP if vip else FEISHU_URL)

    async def create(self, request: ChatCompletionRequest):
        if request.stream:
            return self.stream(request)
        else:
            content = ""
            completion_tokens = 0
            prompt_tokens = len(str(request.messages))
            async for chunk in self.stream(request):
                content += chunk
                completion_tokens += 1
            logger.debug(content)
            chat_completion.choices[0].message.content = content
            chat_completion.usage = CompletionUsage(
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                total_tokens=prompt_tokens + completion_tokens
            )
            return chat_completion

    async def stream(self, request: ChatCompletionRequest):

        if request.model.startswith("gpt-4o-mini"):
            payload = GPT_4O_MINI
        elif request.model.startswith("gpt-4"):
            payload = GPT_4O

        elif request.model.startswith("claude-3-5-sonnet"):
            payload = CLAUDE_35_SONNET
        elif request.model.__contains__("haiku"):
            logger.debug(request.model)
            payload = CLAUDE_3_HAIKU
        elif request.model.__contains__("sonnet"):
            payload = CLAUDE_3_SONNET
        elif request.model.__contains__("opus"):
            payload = CLAUDE_3_OPUS

        elif request.model.startswith(("perplexity-sonar-huge",)):
            payload = PERPLEXITY_SONAR_HUGE
        elif request.model.startswith(("perplexity-sonar-large", "net-gpt-4",)):
            payload = PERPLEXITY_SONAR_LARGE
        elif request.model.startswith(("perplexity-sonar-small", "perplexity", "net", "meta",)):
            payload = PERPLEXITY_SONAR_SMALL

        else:
            payload = GPT_4O_MINI

        payload[0]['messages'] = request.messages

        headers = {
            'Cookie': token,
            'next-action': 'ca5ce500ddee37bddc3c986bee81b599f41e3efb',
        }

        async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=6) as client:
            async with client.stream(method="POST", url="", json=payload) as response:
                yield " "  # 提升首字速度

                async for chunk in response.aiter_lines():
                    # logger.debug(chunk)
                    if chunk and (chunk := chunk.split(":", maxsplit=1)[-1]).strip() and chunk.startswith("{"):
                        try:
                            chunk = json.loads(chunk)
                            chunk = chunk.get('diff', [""])[-1] or chunk.get('curr', "")
                            yield chunk

                        except Exception as e:
                            _ = f"{e}\n{chunk}"
                            logger.error(_)
                            send_message(_)


if __name__ == '__main__':
    # token="_gcl_au=1.1.1862027067.1725453508.1422004205.1725453530.1725453532; session=eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjp7ImVtYWlsIjoiMTBAY2hhdGx1ZmVpLmNvbSJ9LCJleHBpcmVzIjoiMjAyNC0xMi0xM1QxMjozOToxOS43MzJaIiwiaWF0IjoxNzI1NDUzNTU5LCJleHAiOjE3MzQwOTM1NTl9.cxidfpCGmTl3JTH3QSixzl_mGAPuOti2-R_MDDn-LoE"
    # token1="__Host-next-auth.csrf-token=f5dec3278f4e3b090ece20cc6fc5e76a746f0206b8c4ff8dcef2404afb4072e0%7C1a6c45d36f9da3db31738737687a8d3516e9555e2988e37a3c6c194b794e0215; __Secure-next-auth.callback-url=https%3A%2F%2Fwww.tryblend.ai%2F; _gcl_au=1.1.1862027067.1725453508.1506235828.1725877352.1725877846; session=eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjp7ImVtYWlsIjoiMTIzYWJjQGNoYXRsdWZlaS5jb20ifSwiZXhwaXJlcyI6IjIwMjQtMTItMThUMTA6MzE6MDIuNTM1WiIsImlhdCI6MTcyNTg3Nzg2MiwiZXhwIjoxNzM0NTE3ODYyfQ.BCwQqY9QOG0AzgbThBgcBQqpgrSs3ASvVsnpiz7_pec"
    # token2="__Host-next-auth.csrf-token=f5dec3278f4e3b090ece20cc6fc5e76a746f0206b8c4ff8dcef2404afb4072e0%7C1a6c45d36f9da3db31738737687a8d3516e9555e2988e37a3c6c194b794e0215; __Secure-next-auth.callback-url=https%3A%2F%2Fwww.tryblend.ai%2F; _gcl_au=1.1.1862027067.1725453508.1506235828.1725877352.1725877937; session=eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjp7ImVtYWlsIjoiMTBAY2hhdGx1ZmVpLmNvbSJ9LCJleHBpcmVzIjoiMjAyNC0xMi0xOFQxMDozMjozNC41NDFaIiwiaWF0IjoxNzI1ODc3OTU0LCJleHAiOjE3MzQ1MTc5NTR9.9kbC3NO2Trg-HuAXQdsGyAq1W1hj7dKKAD6NT7cQ2bg"
    # token3="__Host-next-auth.csrf-token=f5dec3278f4e3b090ece20cc6fc5e76a746f0206b8c4ff8dcef2404afb4072e0%7C1a6c45d36f9da3db31738737687a8d3516e9555e2988e37a3c6c194b794e0215; __Secure-next-auth.callback-url=https%3A%2F%2Fwww.tryblend.ai%2F; _gcl_au=1.1.1862027067.1725453508.1506235828.1725877352.1725877937; __Secure-next-auth.session-token=eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..r56dN51z69Xm6cbF.xKKVi0In7tqsSdT7yYzmz0ybd7yfNKGpmFnrKE1T6PML5hpmqnrjewSwupmENDm1XxukcJZWFWDQoXt89-q3YQuFCD0HG37BKdxjmMh0IKA1xFie5SfjcYOIkok-qqdR4uuLkSa59dIhXOJHMnfh3FgrSxvGRe2VDvTHujcP_wSpDZ2iFOJ-oI07QnqydGvpMHU26RGR_TcXJUxm_oLuabNNj9TpSrJadfddXNyNhw1lU9QxVtFR97aG3JOqgfHjtOnE9FP5gOEjATMjOiitGSO8o5HeIBN-eEhqEQF1IKSwpnk2yTpdQ2d47sLIThPOJEecH0i0g99nYEMeTUL_mSdu3AbJkFCi1h_ek1Lh4M9qiA4pwPVyGnm3LykR.Hj570agEKEPR_OXN1VjGzg"
    # token4="__Host-next-auth.csrf-token=f5dec3278f4e3b090ece20cc6fc5e76a746f0206b8c4ff8dcef2404afb4072e0%7C1a6c45d36f9da3db31738737687a8d3516e9555e2988e37a3c6c194b794e0215; __Secure-next-auth.callback-url=https%3A%2F%2Fwww.tryblend.ai%2F; _gcl_au=1.1.1862027067.1725453508.1506235828.1725877352.1725877937; __Secure-next-auth.session-token=eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..kj4RtzbMZQ4oLgw-.2T5uSfI-Pv4n-TdsmJtl9B0XRzTe5Z_WQuKWxaBN3Vv19nUwpmpuEU7agUpogU53T0ILVxlkhjmSxA2xjD3wXVDU2hROypvkD3byDBZYQfBfn9a0KpoC95yKMNdG7gepuBkif_ZTXdSkZhfKCjlGa4q4NbW9LsLX87Q-yD18dzemW6hxVZ9AS2-mAGQVeH-i8mtw7FgI9Q0u7Ee4od9ImrctxcPtOgseomkyyTJ8vjMesgMFF3xmtqkIRl3HwNWAXJ_8IOFU8NQKPi5WHeJPayM6VzSy_od2YRkqHDgwxLZd0telUNl-zpVB6pctUdCXjZ0FwbJAsmDnsAZsL6bo0uLCqlFuW6EZM_KsFNuTbYCEK56kJWtMOOE.iVtK2G3FkgLzhjVQIT_ehg"
    # token5="__Host-next-auth.csrf-token=f5dec3278f4e3b090ece20cc6fc5e76a746f0206b8c4ff8dcef2404afb4072e0%7C1a6c45d36f9da3db31738737687a8d3516e9555e2988e37a3c6c194b794e0215; __Secure-next-auth.callback-url=https%3A%2F%2Fwww.tryblend.ai%2F; _gcl_au=1.1.1862027067.1725453508.1506235828.1725877352.1725877937; session=eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjp7ImVtYWlsIjoiMTBAY2hhdGx1ZmVpLmNvbSJ9LCJleHBpcmVzIjoiMjAyNC0xMi0xOFQxMDozMjozNC41NDFaIiwiaWF0IjoxNzI1ODc3OTU0LCJleHAiOjE3MzQ1MTc5NTR9.9kbC3NO2Trg-HuAXQdsGyAq1W1hj7dKKAD6NT7cQ2bg"
    df = arun(aget_spreadsheet_values(feishu_url=FEISHU_URL_VIP, to_dataframe=True))
    df = arun(aget_spreadsheet_values(feishu_url=FEISHU_URL, to_dataframe=True))

    api_keys = df[0]
    for i, token in enumerate(filter(None, api_keys)):
        logger.debug(i)
        if token:

            # token = None

            c = Completions(token)
            request = ChatCompletionRequest(
                # model="claude-3-haiku-20240307",
                # model="claude-3-5-sonnet",
                model="perplexity-sonar-small",
                # messages=[{'role': 'user', 'content': '南京天气怎么样'}],
                messages=[{'role': 'user', 'content': '南京天气怎么样'}],
                stream=False,

            )


            async def main():
                if request.stream:
                    async for i in await c.create(request):
                        print(i, end='')
                else:
                    for i in await c.create(request):
                        print(i, end='')


            arun(main())

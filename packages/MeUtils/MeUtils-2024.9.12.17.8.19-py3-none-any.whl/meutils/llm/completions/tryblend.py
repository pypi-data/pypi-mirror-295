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
        self.api_key = api_key
        self.vip = vip

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
            # logger.debug(content)
            chat_completion.choices[0].message.content = content
            chat_completion.usage = CompletionUsage(
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                total_tokens=prompt_tokens + completion_tokens
            )
            return chat_completion

    async def stream(self, request: ChatCompletionRequest):
        token = self.api_key or await get_next_token_for_polling(feishu_url=FEISHU_URL_VIP if self.vip else FEISHU_URL)

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
                yield "\n"  # 提升首字速度

                async for chunk in response.aiter_lines():
                    # logger.debug(chunk)

                    if 'Please add more credits to use this model' in chunk:
                        # send_message("tryblend 余额不足")
                        logger.debug(chunk)
                        break
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
    token = "HMACCOUNT_BFESS=2A2062EF2FE81046; io=4gPrU0FUQr5w60EmAdXS; Hm_lvt_a3c8711bce1795293b1793d35916c067=1726115406; Hm_lpvt_a3c8711bce1795293b1793d35916c067=1726115406; HMACCOUNT=2A2062EF2FE81046; _gcl_au=1.1.112315428.1726115409.331920663.1726115409.1726115409; id=221988a1d5f300f3||t=1726115409|et=730|cs=002213fd481785fd77a9cb7651; session=eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjp7ImVtYWlsIjoiZjk5Y241ZGJhQG1haWwueGl1dmkuY24ifSwiZXhwaXJlcyI6IjIwMjQtMTItMjFUMDQ6MzA6MTcuMTQ5WiIsImlhdCI6MTcyNjExNTQxNywiZXhwIjoxNzM0NzU1NDE3fQ.G7MvMcx_96aHeVZV7I28Fssl14MqbhTyAkHIM8ZgwOk; __cf_bm=rAWQ3zYw5tpAvJSeP3uD8Sd0mZir3NbcJdqiLg3YHlE-1726115419-1.0.1.1-pPoQZFTpwqS1eGcSfxmSoGYOCHkxEVhPl8LVig05cFf.Ri3smhoG5KCzCcupGTtQOM0To5WwGbPLX24mP3rEpw"
    df = arun(aget_spreadsheet_values(feishu_url=FEISHU_URL_VIP, to_dataframe=True))
    df = arun(aget_spreadsheet_values(feishu_url=FEISHU_URL, to_dataframe=True))

    api_keys = df[0]
    api_keys = [token]
    for i, token in enumerate(filter(None, api_keys)):
        logger.debug(i)
        if token:

            # token = None

            c = Completions(token)
            request = ChatCompletionRequest(
                # model="claude-3-haiku-20240307",
                # model="claude-3-5-sonnet",
                # model="perplexity-sonar-small",
                model="gpt-4o-mini",

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

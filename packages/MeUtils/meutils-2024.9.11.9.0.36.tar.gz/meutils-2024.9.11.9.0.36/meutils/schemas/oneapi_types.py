#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : oneapi_types
# @Time         : 2024/6/28 10:13
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *

BASE_URL = "https://api.chatfire.cn"

MODEL_PRICE = {
    # chatfire
    "ppu-0001": 0.0001,
    "ppu-001": 0.001,
    "ppu-01": 0.01,
    "ppu-1": 0.1,
    "chatfire-translator": 0.01,
    "chatfire-all": 0.0001,

    # 图片 音频 视频
    "step-1x-medium": 0.1 / 3,

    "kolors": 0.02,
    "kling": 0.02,

    "flux": 0.01,
    "flux-schnell": 0.01,
    "flux-dev": 0.03,
    "flux-pro": 0.05,
    "flux-pro-max": 0.1,

    "chat-step-1x-medium": 0.1 / 3,

    "chat-flux-schnell": 0.01,
    "chat-flux-dev": 0.03,
    "chat-flux-pro": 0.05,
    "chat-flux-pro-max": 0.1,

    "chat-kolors": 0.02,
    "chat-kling": 0.02,
    "chat-video": 0.1,
    "chat-video-kling": 0.1,
    "chat-video-gen3": 0.1,
    "chat-video-vidu": 0.1,
    "chat-video-vidu-vip": 0.3,

    # api
    "api-watermark-remove": 0.01,
    "api-idphotos": 0.01,
    "api-pcedit": 0.007,
    "api-faceswap": 0.01,

    "api-kling": 0.1,
    "api-kling-vip": 0.4,

    "api-vidu": 0.07,
    "api-vidu-vip": 0.3,

    "api-runwayml-gen3": 0.1,
    "api-sunoai-chirp": 0.1,
    "api-sunoai-audio": 0.01,  # file
    "api-sunoai-lyrics": 0.01,
    "api-translator": 0.0001,
    "api-voice-clone": 0.01,
    "api-cogvideox": 0.1,

    "api-reranker": 0.01,

    "suno-v3": 0.1,
    "suno-v3.5": 0.1,
    "suno-chat": 0.1,
    "chirp-v3": 0.1,
    "chirp-v3.5": 0.1,

    # all
    "gpt-4-all": 0.1,
    "gpt-4-mobile": 0.1,
    "gpt-4-gizmo-*": 0.1,
    "net-gpt-3.5-turbo": 0.01,
    "net-gpt-4": 0.1,
    "perplexity": 0.01,

    # 逆向
    "cogview-3": 0.01,
    "cogview-3-plus": 0.01,

    "spark-all": 0.005,
    "glm-4-all": 0.005,
    "step-1-all": 0.005,
    "step-all": 0.005,
    "hunyuan-all": 0.005,

    "kimi-all": 0.01,
    "minicpm-v": 0.01,
    "minicpm-v2.6": 0.01,

    "dreamshaper-8-lcm": 0.01,
    "stable-diffusion": 0.01,
    "stable-diffusion-v1-5-img2img": 0.01,
    "stable-diffusion-v1-5-inpainting": 0.01,
    "stable-diffusion-xl-base-1.0": 0.01,
    "stable-diffusion-xl-lightning": 0.01,
    "stable-diffusion-3": 0.02,
    "stable-diffusion-3-medium": 0.02,
    "chat-stable-diffusion-3": 0.02,

    "midjourney": 0.14,  # chat

    "mj_imagine": 0.1 * 0.6,
    "mj_variation": 0.1 * 0.6,
    "mj_high_variation": 0.1 * 0.6,
    "mj_low_variation": 0.1 * 0.6,
    "mj_pan": 0.1 * 0.6,
    "mj_blend": 0.1 * 0.6,
    "mj_inpaint": 0,
    "mj_reroll": 0.1 * 0.6,

    "mj_upscale": 0.05 * 0.6,
    "mj_custom_zoom": 0,
    "mj_describe": 0.05 * 0.6,
    "mj_modal": 0.1 * 0.6,
    "mj_shorten": 0.1 * 0.6,
    "mj_zoom": 0.1 * 0.6,
    "swap_face": 0.05 * 0.6,

}

MODEL_RATIO = {
    # 定制
    "lingxi-all": 1,

    "kimi": 5,
    "kimi-128k": 5,

    # 智谱
    'glm-4-9b-chat': 0.05,  # 特价
    "glm-3-turbo": 0.05,  # 特价
    "glm-4-flash": 0.05,  # 特价
    "glm-4-air": 0.05,  # 特价

    "glm-4": 2.5,
    "glm-4-0520": 2.5,
    "glm-4-airx": 10,
    "glm-4v": 2.5,

    # 月之暗面 https://platform.moonshot.cn/docs/price/chat#%E4%BA%A7%E5%93%81%E5%AE%9A%E4%BB%B7
    "moonshot-v1-8k": 6 / 5,  # 特价
    "moonshot-v1-32k": 12 / 5,  # 特价
    "moonshot-v1-128k": 60 / 5,  # 特价

    # 阿里千问 https://dashscope.console.aliyun.com/billing
    "qwen-long": 0.25,
    "qwen-turbo": 1,
    "qwen-plus": 2,
    "qwen-max": 20,
    "qwen-max-longcontext": 20,

    "qwen1.5-7b-chat": 0.05,  # 特价
    'Qwen/Qwen1.5-7B-Chat': 0.05,  # 特价
    "qwen1.5-14b-chat": 0.7,
    "Qwen/Qwen1.5-14B-Chat": 0.7,
    "qwen1.5-32b-chat": 1.75,
    'Qwen/Qwen1.5-32B-Chat': 1.75,
    "qwen1.5-110b-chat": 3.5,
    "Qwen/Qwen1.5-110B-Chat": 3.5,

    "qwen2-1.5b-instruct": 0.05,  # 特价
    'Qwen/Qwen2-1.5B-Instruct': 0.05,  # 特价
    "qwen2-7b-instruct": 0.05,  # 特价
    "Qwen/Qwen2-7B-Instruct": 0.05,  # 特价
    "qwen2-57b-a14b-instruct": 1.26,
    'Qwen/Qwen2-57B-A14B-Instruct': 1.26,
    "qwen2-72b-instruct": 4.13,
    'Qwen/Qwen2-72B-Instruct': 4.13,
    "farui-plus": 10,  # 法律大模型
    'qwen2-math-72b-instruct': 4.13,

    # 讯飞 https://xinghuo.xfyun.cn/sparkapi?scr=price
    'spark-lite': 0.05,  # 特价
    'spark-pro': 15 / 5,  # 特价
    'spark-max': 15,
    'spark-ultra': 50,

    # 阶跃星辰 https://platform.stepfun.com/docs/pricing/details
    "step-1-8k": 2.5,
    "step-1-32k": 7.5,
    "step-1v-8k": 2.5,
    "step-1v-32k": 7.5,

    # 零一万物 https://platform.lingyiwanwu.com/docs#%E8%AE%A1%E8%B4%B9%E5%8D%95%E5%85%83
    "yi-spark": 0.05,  # 特价
    "yi-1.5-6b-chat": 0.05,  # 特价
    "yi-1.5-9b-chat-16k": 0.05,  # 特价
    "yi-34b-chat": 0.63,
    "yi-34b-chat-0205": 0.63,
    "yi-1.5-34b-chat-16k": 0.63,

    "yi-large": 10,
    "yi-large-turbo": 6,
    "yi-large-rag": 12.5,
    "yi-medium": 1.25,
    "yi-medium-200k": 6,
    "yi-vision": 3,

    # minimax https://platform.minimaxi.com/document/price?id=6433f32294878d408fc8293e
    "abab6.5-chat": 15 / 7.5,
    "abab6.5s-chat": 5,
    "abab6.5t-chat": 2.5,
    "abab6.5g-chat": 2.5,
    "abab5.5-chat": 7.5,
    "abab5.5s-chat": 2.5,

    # deepseek
    "deepseek-chat": 0.5,
    "deepseek-coder": 0.5,
    'deepseek-coder-v2-instruct': 0.5,
    'deepseek-v2-chat': 0.5,
    'deepseek-llm-67b-chat': 0.5,

    # 豆包
    "doubao-lite-128k": 0.4,
    "doubao-lite-32k": 0.15,
    "doubao-lite-4k": 0.15,
    "doubao-pro-128k": 2.5,
    "doubao-pro-32k": 0.4,
    "doubao-pro-4k": 0.4,

    # 商汤 https://platform.sensenova.cn/pricing
    # https://platform.sensenova.cn/doc?path=/pricingdoc/pricing.md
    "SenseChat-Turbo": 1 / 5,  # 特价
    "SenseChat": 6 / 5,  # 特价
    "SenseChat-32K": 18 / 5,  # 特价
    "SenseChat-128K": 30 / 5,  # 特价
    "SenseChat-5": 20 / 5,  # 最新版本#  特价
    "SenseChat-Vision": 50 / 5,  # 图生文#  特价
    "SenseChat-5-Cantonese": 13.5 / 5,  # 粤语大模型#  特价

    # 腾讯混元
    "hunyuan": 7.143,
    "hunyuan-lite": 4,
    "hunyuan-pro": 50,
    "hunyuan-standard": 5,
    "hunyuan-standard-256k": 60,

    # 百度文心
    "ERNIE-Speed-8K": 0.2858,
    "ERNIE-Speed-128K": 0.2858,

    "ERNIE-3.5-8K": 2,
    "ERNIE-3.5-128K": 4,

    "ERNIE-4.0-Turbo-8K": 15,
    "ERNIE-4.0-8K": 20,

    "text-ada-001": 0.2,
    "text-babbage-001": 0.25,
    "text-davinci-edit-001": 10,
    "text-embedding-3-large": 1,
    "text-embedding-3-small": 1,
    "text-embedding-ada-002": 1,
    "text-embedding-v1": 1,
    "text-moderation-latest": 0.1,
    "text-moderation-stable": 0.1,
    "tts-1": 7.5,
    "tts-1-1106": 7.5,
    "tts-1-hd": 15,
    "tts-1-hd-1106": 15,
    "whisper-1": 15,

    "bing": 5,

    "PaLM-2": 1,
    "360gpt-pro": 0.8572,
    "360gpt-turbo": 0.0858,
    "360gpt-turbo-responsibility-8k": 0.8572,
    "360GPT_S2_V9": 0.8572,
    "ada": 10,
    "babbage": 10,
    "babbage-002": 0.2,
    "baichuan2-turbo": 4,
    "baichuan2-turbo-192k": 8,
    "baichuan3-turbo": 6,
    "baichuan3-turbo-128k": 12,
    "baichuan4": 50,

    "claude-2.0": 4,
    "claude-2.1": 4,
    "claude-instant-1": 0.4,

    "claude-3-haiku-20240307": 0.125,
    "claude-3-sonnet-20240229": 1.5 * 5,
    "claude-3-opus-20240229": 7.5,

    "claude-3-5-sonnet-20240620": 1.5,

    "code-davinci-edit-001": 10,
    "command": 0.5,
    "command-light": 0.5,
    "command-light-nightly": 0.5,
    "command-nightly": 0.5,
    "command-r": 0.25,
    "command-r-plus": 1.5,
    "curie": 10,
    "dall-e-3": 16,
    "davinci": 10,
    "davinci-002": 1,

    "embedding-bert-512-v1": 0.0715,
    "Embedding-V1": 0.1429,
    "embedding_s1_v1": 0.0715,

    "gemini-1.0-pro-001": 1,
    "gemini-1.0-pro-latest": 1,
    "gemini-1.0-pro-vision-001": 1,
    "gemini-1.0-pro-vision-latest": 1,
    "gemini-1.5-flash-latest": 2,
    "gemini-1.5-pro-latest": 2,
    "gemini-1.5-pro": 2,
    "gemini-1.5-flash": 2,
    "gemini-pro": 1,
    "gemini-pro-vision": 1,
    "gemini-ultra": 1,

    "gpt-3.5-turbo": 0.75,
    "gpt-3.5-turbo-0125": 0.25,
    "gpt-3.5-turbo-0613": 0.75,
    "gpt-3.5-turbo-1106": 0.5,
    "gpt-3.5-turbo-16k": 1.5,
    "gpt-3.5-turbo-16k-0613": 1.5,
    "gpt-3.5-turbo-instruct": 0.75,
    "gpt-4": 15,
    "gpt-4-0125-preview": 5,
    "gpt-4-0613": 15,
    "gpt-4-1106-preview": 5,
    "gpt-4-1106-vision-preview": 5,
    "gpt-4-32k": 30,
    "gpt-4-32k-0613": 30,
    "gpt-4-all": 15,
    "gpt-4-gizmo-*": 15,
    "gpt-4-turbo": 5,
    "gpt-4-turbo-2024-04-09": 5,
    "gpt-4-turbo-preview": 5,
    "gpt-4-vision-preview": 5,
    "chatgpt-4o-latest": 2.5,

    "gpt-4o": 2.5,
    "gpt-4o-all": 2.5,  # 逆向
    "gpt-4o-2024-05-13": 2.5,
    "gpt-4o-mini": 0.075,
    "gpt-4o-mini-2024-07-18": 0.075,
    "gpt-4o-2024-08-06": 1.25,

    # 硅基
    "llama-3.1-8b-instruct": 0.01,
    "llama-3.1-70b-instruct": 0.21,
    "llama-3.1-405b-instruct": 10.5,

    # groq https://console.groq.com/docs/models
    "llama3-8b-8192": 0.01,
    "llama3-70b-8192": 0.01,
    "mixtral-8x7b-32768": 0.01,
    "gemma-7b-it": 0.01,
    "llama-3.1-8b-instant": 0.01,
    "llama-3.1-70b-versatile": 0.5,

    # sili
    "gemma2-9b-it": 0.01,
    "gemma2-27b-it": 0.63,
    "google/gemma-2-27b-it": 0.09,

    "internlm2_5-7b-chat": 0.01,
    'internlm2_5-20b-chat': 0.5,

    # embedding
    "bge-large-zh-v1.5": 1,
    "bge-large-en-v1.5": 1,
    "BAAI/bge-large-zh-v1.5": 1,
    "BAAI/bge-large-en-V1.5": 1,
    "BAAI/bge-m3": 1,
    "bge-large-zh-v1.5-q4": 1,
    "bge-small-zh-v1.5-q4": 1,
    "chatfire/bge-m3:q8_0": 1,

    "acge_text_embedding": 1,
    "dmeta-embedding-zh-q4": 1,

}

COMPLETION_RATIO = {
    "gpt-4-all": 2,
    "gpt-4-gizmo-*": 2,
    "gpt-4o": 3,
    "gpt-4o-vision": 3,
    "gpt-4o-all": 3,
    "bing": 5
}

GROUP_RATIO = {
    "chatfire": 1,
    "default": 1,

    "vip": 2.5,
    "svip": 1,
    "ssvip": 1,
    "2B": 4,
    "35": 1,
    "国产": 0.5
}

REDIRECT_MODEL = {
    # https://docs.siliconflow.cn/docs/4-api%E8%B0%83%E7%94%A8
    "gpt-3.5-turbo": "THUDM/glm-4-9b-chat",  # 永久免费
    "chatfire-translator": "THUDM/glm-4-9b-chat",  # 永久免费
    "internlm2_5-7b-chat": "internlm/internlm2_5-7b-chat",  # 永久免费

    "glm-3-turbo": "THUDM/glm-4-9b-chat",  # 永久免费
    "glm-4-air": "THUDM/glm-4-9b-chat",  # 永久免费
    "glm-4-flash": "THUDM/glm-4-9b-chat",  # 永久免费
    'glm-4-9b-chat': 'THUDM/glm-4-9b-chat',  # 永久免费
    'chatglm3-6b': 'THUDM/chatglm3-6b',  # 永久免费

    "doubao-pro-128k": "deepseek-ai/DeepSeek-V2-Chat",
    "deepseek-chat": "deepseek-ai/DeepSeek-V2-Chat",
    "deepseek-coder": "deepseek-ai/DeepSeek-Coder-V2-Instruct",
    'deepseek-coder-v2-instruct': 'deepseek-ai/DeepSeek-Coder-V2-Instruct',
    'deepseek-v2-chat': 'deepseek-ai/DeepSeek-V2-Chat',
    'deepseek-llm-67b-chat': 'deepseek-ai/deepseek-llm-67b-chat',

    "yi-spark": "01-ai/Yi-1.5-9B-Chat-16K",  # 永久免费
    'yi-1.5-6b-chat': '01-ai/Yi-1.5-6B-Chat',  # 永久免费
    'yi-1.5-9b-chat-16k': '01-ai/Yi-1.5-9B-Chat-16K',  # 永久免费
    'yi-34b-chat': '01-ai/Yi-1.5-9B-Chat-16K',  # 永久免费
    'yi-34b-chat-0205': '01-ai/Yi-1.5-9B-Chat-16K',  # 永久免费
    'yi-1.5-34b-chat-16k': '01-ai/Yi-1.5-9B-Chat-16K',  # 永久免费
    # 'yi-1.5-34b-chat-16k': '01-ai/Yi-1.5-34B-Chat-16K',

    "qwen-turbo": "Qwen/Qwen2-7B-Instruct",
    'qwen2-1.5b-instruct': 'Qwen/Qwen2-1.5B-Instruct',
    'qwen2-7b-instruct': 'Qwen/Qwen2-7B-Instruct',
    'qwen2-72b-instruct': 'Qwen/Qwen2-72B-Instruct',
    'qwen2-math-72b-instruct': 'Qwen/Qwen2-Math-72B-Instruct',

    'qwen2-57b-a14b-instruct': 'Qwen/Qwen2-57B-A14B-Instruct',
    'qwen1.5-7b-chat': 'Qwen/Qwen1.5-7B-Chat',
    'qwen1.5-14b-chat': 'Qwen/Qwen1.5-14B-Chat',
    'qwen1.5-32b-chat': 'Qwen/Qwen1.5-32B-Chat',
    'qwen1.5-110b-chat': 'Qwen/Qwen1.5-110B-Chat',

    'internlm2_5-20b-chat': 'internlm/internlm2_5-20b-chat',

    # 千问兜底
    "qwen-max": 'Qwen/Qwen2-72B-Instruct',
    "qwen-plus": 'Qwen/Qwen2-72B-Instruct',

    # 国外开源
    "gemma2-9b-it": "google/gemma-2-9b-it",  # 永久免费
    "gemma2-27b-it": "google/gemma-2-27b-it",
    "gemini": "google/gemma-2-9b-it",  # todo
    "gemini-1.5": "google/gemma-2-27b-it",

    "meta-llama-3-8b-instruct": "meta-llama/Meta-Llama-3-8B-Instruct",  # 永久免费
    "mistral-7b-instruct": "mistralai/Mistral-7B-Instruct-v0.2",  # 永久免费

    "mixtral-8x7b-instruct-v0.1": "mistralai/Mixtral-8x7B-Instruct-v0.1",

    "meta-llama-3-70b-instruct": "meta-llama/Meta-Llama-3-70B-Instruct",
    "llama-3-70b-instruct": "meta-llama/Meta-Llama-3-70B-Instruct",
    "llama-3.1-8b-instruct": "meta-llama/Meta-Llama-3.1-8B-Instruct",
    "llama-3.1-70b-instruct": "meta-llama/Meta-Llama-3.1-70B-Instruct",
    "llama-3.1-405b-instruct": "meta-llama/Meta-Llama-3.1-405B-Instruct",

    # https://xinghuo.xfyun.cn/sparkapi
    # spark-lite,spark-pro,spark-max,spark-ultra
    # 'spark-lite': "general",  # 实名免费
    'spark-lite': "generalv3.5",  # 实名免费
    'spark-pro': "generalv3.5",
    'spark-pro-128k': "generalv3.5",
    'spark-max': "generalv3.5",
    'spark-ultra': "generalv3.5",

    # 硅基
    "stable-diffusion": "stabilityai/stable-diffusion-3-medium",
    "stable-diffusion-3-medium": "stabilityai/stable-diffusion-3-medium",

    "stable-diffusion-turbo": "stabilityai/sd-turbo",
    "stable-diffusion-xl-turbo": "stabilityai/sdxl-turbo",
    "dreamshaper-8-lcm": "ByteDance/SDXL-Lightning",

    "stable-diffusion-v1-5-img2img": "ByteDance/SDXL-Lightning",
    "stable-diffusion-2-1": "stabilityai/stable-diffusion-2-1",
    "stable-diffusion-xl-base-1.0": "stabilityai/stable-diffusion-xl-base-1.0",
    "stable-diffusion-xl-lightning": "ByteDance/SDXL-Lightning",
    "stable-diffusion-3": "stabilityai/stable-diffusion-3-medium",

    "photomaker": "TencentARC/PhotoMaker",

    "flux.1-schnell": "black-forest-labs/FLUX.1-schnell",
    "flux.1-dev": "black-forest-labs/FLUX.1-dev",

    # groq
    # "llama3-8b": "llama3-8b-8192",
    # "mixtral-8x7b": "mixtral-8x7b-32768",
    # "gemma-7b": "gemma-7b-it",
    # "gemma2-9b": "gemma2-9b-it"

    "todo": "gpt-4-vision-preview"

}

# class User(BaseModel):
#     id: int
#     username: str
#     password: str
#     display_name: str
#     role: int
#     status: int
#     email: datetime
#     github_id: datetime
#     wechat_id
#     telegram_id
#     verification_code
#     access_token
#     quota
#     used_quota
#     request_count
#
#     is_active: bool
#     created_at: datetime
#     updated_at:  datetime
#     email: str
#     password: str
#     created_at: datetime
#     updated_at: datetime
#
#     name: str
#     email: str
#     password: str
#     is_active: bool
#     is_superuser: bool
#     created_at: datetime
#     updated_at: datetime
#     deleted_at: Optional[datetime]

# {
#         "id": 814,
#         "username": "yqfy2020",
#         "password": "",
#         "display_name": "yqfy2020",
#         "role": 1,
#         "status": 1,
#         "email": "yqfy2020@qq.com",
#         "github_id": "",
#         "wechat_id": "",
#         "telegram_id": "",
#         "verification_code": "",
#         "access_token": "acb03c337e1b4a6a88d02e0146576cdf",
#         "quota": 11111,
#         "used_quota": 0,
#         "request_count": 0,
#         "group": "default",
#         "aff_code": "dvwc",
#         "aff_count": 0,
#         "aff_quota": 0,
#         "aff_history_quota": 0,
#         "inviter_id": 0,
#         "DeletedAt": None
#     }
if __name__ == '__main__':
    # print(','.join(REDIRECT_MODEL.keys()))
    from meutils.apis.oneapi import option

    option()

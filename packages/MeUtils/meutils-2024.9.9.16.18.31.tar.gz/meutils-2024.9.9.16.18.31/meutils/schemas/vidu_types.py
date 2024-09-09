#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : vidu_types
# @Time         : 2024/7/31 08:58
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *

BASE_URL = "https://api.vidu.studio/vidu/v1"
UPLOAD_BASE_URL = "https://api.vidu.studio/tools/v1"  # /files/uploads

EXAMPLES = [
    {
        "input": {
            "prompts": [
                {
                    "type": "text",
                    "content": "两个人举起茶杯小口抿了一口。左边的人轻抿双唇后微笑，右边的人专注于他们的茶，形成一种静雅和微妙互动的场景。布景精致，淡雅的颜色、花卉布置和古典家具增强了优雅氛围。",
                    "enhance": True
                }
            ]
        },
        "type": "text2video",
        "settings": {
            "style": "general",
            "aspect_ratio": "16:9",
            "duration": 4,
            "model": "vidu-1"
        }
    },
    {
        "input": {
            "prompts": [
                {
                    "type": "text",
                    "content": "开花吧",
                    "enhance": True
                },
                {
                    "type": "image",
                    "content": "ssupload:?id=2368323193735387",
                    "enhance": True
                }
            ]
        },
        "type": "img2video",
        "settings": {
            "style": "general",
            "aspect_ratio": "16:9",
            "duration": 4,
            "model": "vidu-1"
        }
    }
]


class ViduRequest(BaseModel):
    prompt: Optional[str] = None
    url: Optional[str] = None  # ssupload:?id=
    style: str = "general"  # anime
    aspect_ratio: str = "16:9"
    duration: int = 4

    type: Optional[str] = None  # text2video img2video character2video

    payload: dict = {}

    def __init__(self, **data):
        super().__init__(**data)

        if self.duration > 4:
            self.duration = 8
        else:
            self.duration = 4

        input = {
            "prompts": []
        }

        if self.prompt:
            input['prompts'].append(
                {
                    "type": "text",
                    "content": self.prompt,
                    "enhance": True
                }
            )
        type = "text2video"
        if self.url:
            input['prompts'].append({
                "type": "image",
                "content": self.url,
                "enhance": True
            })
            type = "img2video"  # character2video

        self.payload = {
            "input": input,
            "type": self.type or type,
            "settings": {
                "style": self.style,
                "aspect_ratio": self.aspect_ratio,
                "duration": self.duration,
                "model": "vidu-1"
            }
        }

    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "prompt": "一只可爱的黑白边境牧羊犬，头伸出车窗，毛发被风吹动，微笑着伸出舌头。",
                }
            ]
        }


class ViduUpscaleRequest(BaseModel):
    task_id: str  # vip
    creation_id: str

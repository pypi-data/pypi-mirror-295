#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : baidu_types
# @Time         : 2024/8/29 09:55
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *

TYPES = {
    "变清晰": "3",
    "去水印": "1",
    "提取线稿": "15",
    "智能抠图": "9",
    # "涂抹消除": "10",
    "涂抹消除": "8",

    "背景替换": "12",  # text: 大雪纷飞，落叶凋零的景象

    "AI扩图": "4",  # ext_ratio: 3:4
    "AI重绘": "6",  # # create_level=2
    "AI相似图": "7",  # create_level=5
    "风格转换": "14",  # style：miyazaki宫崎骏风 clay橡皮泥风  monet油画风
}


class BDAITPZSRequest(BaseModel):
    query: str = 'bdaitpzs百度AI图片助手bdaitpzs'
    image_source: str = '1'

    picInfo: str = ''  # base64
    picInfo2: str = ''

    text: str = ''
    ext_ratio: str = ''
    expand_zoom: str = ''

    clid: str = ''
    front_display: str = '2'  # front_display
    create_level: str = '0'

    type: str = '1'
    style: str = ''

    original_url: str = ''
    thumb_url: str = ''

    is_first: bool = True


if __name__ == '__main__':
    pprint(list(TYPES.keys()))
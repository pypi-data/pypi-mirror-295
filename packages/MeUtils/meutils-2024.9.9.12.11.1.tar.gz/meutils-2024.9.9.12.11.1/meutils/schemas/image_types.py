#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : image_types
# @Time         : 2024/8/21 14:18
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 


ASPECT_RATIOS = {
    "1:1": "1024x1024",

    "1:2": "512x1024",
    "2:1": "1024x512",

    '2:3': "768x512",
    '3:2': "512x768",

    "4:3": "1280x960",  # "1024x768"
    "3:4": "960x1280",

    "5:4": "1280x960",
    "4:5": "960x1280",

    "16:9": "1366x768",  # "1024x576"
    "9:16": "768x1366",

    "21:9": "1344x576",
}


if __name__ == '__main__':
    print(ASPECT_RATIOS.items())
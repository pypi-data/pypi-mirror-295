#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : demo
# @Time         : 2024/9/11 15:18
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
import ell
from openai import OpenAI

@ell.simple(model="gpt-4o", client=OpenAI())
def hello(world: str):
    """You are a helpful assistant that writes in lower case."""  # System Message
    return f"Say hello to {world[::-1]} with a poem."  # User Message


hello("sama")

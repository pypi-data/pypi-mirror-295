#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : file
# @Time         : 2022/7/5 下午3:31
# @Author       : yuanjie
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
# from fastapi import UploadFile 有点区别
from starlette.datastructures import UploadFile


def file_append_firstline(line):
    with open('untitled.txt', "r+") as f:
        old = f.read()

        f.seek(0)
        f.write(line)
        f.write(old)


def base64_to_bytes(base64_image_string):
    """
    # 将字节数据写入图片文件
    image_data = base64_to_bytes(...)
    with open(filename, 'wb') as file:
        file.write(image_data)
    """
    return base64.b64decode(base64_image_string.split(",", 1)[-1])


async def to_bytes(file: Union[UploadFile, str]):  # plus
    """

    :param file: 文件对象、路径、base64、url
    :return: todo: bytes、filepath、io.BytesIO
    """
    logger.debug(type(file))

    file_bytes = None
    from starlette.datastructures import UploadFile as _UploadFile
    if isinstance(file, _UploadFile):
        file_bytes = await file.read()

    elif isinstance(file, str) and file.startswith('http'):
        resp = await httpx.AsyncClient(timeout=100).get(file)
        file_bytes = resp.content

    elif isinstance(file, str) and len(file) > 256:
        file_bytes = base64_to_bytes(file)

    elif isinstance(file, str) and len(file) < 256 and Path(file).is_file():
        file_bytes = Path(file).read_bytes()

    return file_bytes


if __name__ == '__main__':

    import tempfile

    # 使用上下文管理器自动处理文件的关闭和删除
    with tempfile.NamedTemporaryFile(mode='wb+') as temp:
        temp.write("This is a temporary file.")
        temp.seek(0)
        print(f"文件内容: {temp.read()}")
        print(f"临时文件名: {temp.name}")
    # 文件在这里自动关闭和删除

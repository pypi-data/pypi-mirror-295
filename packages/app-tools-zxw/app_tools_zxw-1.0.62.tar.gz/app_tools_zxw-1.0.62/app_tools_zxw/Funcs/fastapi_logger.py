"""
# File       : 初始化logger.py
# Time       ：2024/8/28 下午1:13
# Author     ：xuewei zhang
# Email      ：shuiheyangguang@gmail.com
# version    ：python 3.12
# Description：在 FastAPI 中初始化 logger，在其他的路由文件中引用 logger
            例如：在main.py中，引用logger ,用作初始化
                            from app_tools_zxw.FUNCs_支付相关.初始化logger import logger
                在apis/支付_支付宝_二维码/api_支付_支付宝_二维码.py中，引用logger：
                            from app_tools_zxw.FUNCs_支付相关.初始化logger import logger
"""
import logging
from logging.handlers import RotatingFileHandler
import os
from fastapi.logger import logger as fastapi_logger


def setup_logger(log_level=logging.INFO):
    # 创建 logs 目录（如果不存在）
    if not os.path.exists("logs"):
        os.makedirs("logs")

    # 配置根日志记录器
    logging.basicConfig(level=log_level)

    # 创建一个 RotatingFileHandler
    file_handler = RotatingFileHandler(
        "logs/app.log", maxBytes=10 * 1024 * 1024, backupCount=5
    )
    file_handler.setLevel(log_level)

    # 创建一个格式化器
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # 将处理器添加到根日志记录器
    logging.getLogger().addHandler(file_handler)

    # 配置 FastAPI 的日志记录器
    fastapi_logger.handlers = logging.getLogger().handlers

    return logging.getLogger(__name__)


# 创建并配置 logger
logger = setup_logger()

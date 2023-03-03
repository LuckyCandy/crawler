import os.path
import sys

from utils.decorator import singleton
import logging
import logging.handlers
import common.settings as st


@singleton
class Logger:
    def __init__(self, name):
        self.log = logging.getLogger(name)
        # 设置日志的打印目录
        log_path = os.path.abspath(os.path.join(os.getcwd(), st.LOG_PATH))
        if not os.path.exists(log_path):
            os.makedirs(log_path)
        # 日志的打印格式
        print_formatter = logging.Formatter('[%(asctime)s]-[%(levelname)s]-[%(filename)s]-[line:%(lineno)d]: %('
                                            'message)s')
        # 增加按大小分片的文件日志处理器
        rotating_file_handler = logging.handlers.RotatingFileHandler(
            os.path.join(log_path, st.LOG_FILE_NAME),
            maxBytes=st.LOG_FILE_MAX_BYTES,
            backupCount=st.LOF_FILE_BACKUP_CNT,
            encoding='utf-8'
        )
        rotating_file_handler.setLevel(logging.WARNING)
        rotating_file_handler.setFormatter(print_formatter)
        self.log.addHandler(rotating_file_handler)
        # 增加控制台输出
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(print_formatter)
        console_handler.setLevel(logging.DEBUG)
        self.log.addHandler(console_handler)
        self.log.setLevel(logging.DEBUG)

    def info(self, msg, *args) -> None:
        self.log.info(msg, *args)
        return

    def warning(self, msg, *args) -> None:
        self.log.warning(msg, *args)
        return

    def error(self, msg, *args) -> None:
        self.log.error(msg, *args)
        return

    def debug(self, msg, *args) -> None:
        self.log.debug(msg, *args)
        return


# 快速使用
def get_logger(name=None) -> Logger:
    return Logger(name)

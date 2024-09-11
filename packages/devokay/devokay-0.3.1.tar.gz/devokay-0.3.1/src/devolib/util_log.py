# -*- coding: UTF-8 -*-
# python3

import inspect
import logging
import os

'''
日志模块
'''
#################################################################
## 常规日志对象
# 获取 debug logger
logger = logging.getLogger("debug_logger")
logger.setLevel(logging.DEBUG)

# 创建流式句柄
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# 创建格式化器
formatter = logging.Formatter(
    '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
)

# 配置 logger
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

#########################################################################
## 动态日志对象
# 创建动态 logger 适配器，解决 logger 封装带来的文件信息缺失问题
class DynamicLoggerAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        stack = inspect.stack()
        try:
            outer_frames = inspect.getouterframes(stack[0].frame)
            caller_frame_ = outer_frames[4]
            filename = caller_frame_.filename
            lineno = caller_frame_.lineno

            filename = os.path.basename(filename)

            kwargs['extra'] = {'custom_lineno': lineno, 'custom_pathname': filename}
        finally:
            del outer_frames
            del stack
        return msg, kwargs

dyn_logger = logging.getLogger("dyn_debug_logger")
dyn_logger.setLevel(logging.DEBUG)
dyn_console_handler = logging.StreamHandler()
dyn_console_handler.setLevel(logging.DEBUG)
dyn_formatter = logging.Formatter(
    '%(asctime)s %(levelname)s [%(custom_pathname)s:%(custom_lineno)d] %(message)s'
)
dyn_console_handler.setFormatter(dyn_formatter)
dyn_logger.addHandler(dyn_console_handler)
dyn_logger = DynamicLoggerAdapter(dyn_logger, {})

'''
@brief 级别封装
'''
def LOG_D(str):
    dyn_logger.debug(str)

def LOG_I(str):
    dyn_logger.info(str)

def LOG_W(str):
    dyn_logger.warning(str)

def LOG_E(str):
    dyn_logger.error(str)

def LOG_F(str):
    dyn_logger.error(str)
    raise Exception(str)

'''
@brief 打印主流程
'''
def LOG_MAIN(str):
    dyn_logger.warning(f'====> {str}')


'''
@brief 打印子流程
'''
def LOG_SUB(str):
    dyn_logger.info(f'----> {str}')


def LOG_CONSOLE(str):
    print(f'>> {str}')

# 测试例程

if __name__ == '__main__':
    LOG_D('debug log')
    LOG_MAIN('main log')
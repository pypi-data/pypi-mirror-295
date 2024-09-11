# -*- coding: UTF-8 -*-
# python3

import os
import shutil
import subprocess

from devolib.util_fs import path_join_one, path_exists
from devolib.util_log import LOG_D

##################################################################
# Export vcxproj from CMakeLists.txt

CMAKE_CONFIG_FILE='CMakeLists.txt'

def export_vcxproj(args):
    if args.cmake_export_vcxproj is not None:
        LOG_D(f'cmake export vcxproj started')

        # validate params

#         cmake -G "Visual Studio 17 2022" -A x64 -B build
# -G "Visual Studio 17 2022" 指定了 Visual Studio 2022。
# -A x64 指定了目标平台架构（可以选择 Win32 或 x64）。
# -B build 指定了构建目录，这里会将生成的 Visual Studio 工程文件放在 build 目录中。

cmake -G "Visual Studio 16 2019" -A x64 .



# 设置构建输出目录
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

# 设置不同构建配置下的输出目录
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY_DEBUG ${CMAKE_BINARY_DIR}/lib/Debug)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY_DEBUG ${CMAKE_BINARY_DIR}/bin/Debug)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY_DEBUG ${CMAKE_BINARY_DIR}/bin/Debug)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY_RELEASE ${CMAKE_BINARY_DIR}/lib/Release)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY_RELEASE ${CMAKE_BINARY_DIR}/bin/Release)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY_RELEASE ${CMAKE_BINARY_DIR}/bin/Release)
    


        # cmake -G "Visual Studio 17 2022" -A x64 -B build -D CMAKE_ARCHIVE_OUTPUT_DIRECTORY=path/to/output/lib -D CMAKE_LIBRARY_OUTPUT_DIRECTORY=path/to/output/bin -D CMAKE_RUNTIME_OUTPUT_DIRECTORY=path/to/output/bin



'''
@brief CMake 助手
'''
def cmd_regist(subparsers):
    parser = subparsers.add_parser('cmake_export_vcxproj', help='CMake导出VS子工程')
    parser.add_argument('-v', '--version', type=str, default='2022', help='2019,2022')
    parser.add_argument('-o', '--output-path', type=str, default='EXPORT', help='导出路径')
    parser.set_defaults(handle=export_vcxproj)
    
# -*- coding: UTF-8 -*-
# python3

import platform
from enum import Enum

class OSEnum(Enum):
    WIN = "Windows"
    MAC = "macOS"
    UBU = "Ubuntu"
    CEN = "CentOS"
    LIN = "Linux"

def operating_system():
    system = platform.system()
    if system == "Windows":
        return OSEnum.WIN
    elif system == "Darwin":
        return OSEnum.MAC
    elif system == "Linux":
        distribution = platform.linux_distribution()
        if distribution[0] == "Ubuntu":
            return OSEnum.UBU
        elif distribution[0] == "CentOS Linux":
            return OSEnum.CEN
        else:
            return OSEnum.LIN
    else:
        return system  # 其他操作系统名称

def is_ubuntu():
    return operating_system() == OSEnum.UBU
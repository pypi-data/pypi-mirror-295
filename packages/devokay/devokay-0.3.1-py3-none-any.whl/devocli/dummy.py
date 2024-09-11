# -*- coding: UTF-8 -*-
# python3

import argparse
from devocli.pcsdk import regist_pcsdk
from devocli.find_big_files import FindBigFilesCmd
from devocli.omni import OmniCmd
from devocli.remote import RemoteCmd
from devocli.utf8bom import cmd_regist as utf8bom_cmd_reg
from devocli.nginx import cmd_regist as nginx_cmd_reg
from devocli.fir import cmd_regist as fir_cmd_reg

def cli():
    parser = argparse.ArgumentParser(description='CLI描述')
    subparsers = parser.add_subparsers(metavar='子命令')

    find_big_files_cmd = FindBigFilesCmd()
    find_big_files_cmd.regist(subparsers)

    regist_pcsdk(subparsers)

    omni_cmd = OmniCmd()
    omni_cmd.regist(subparsers)

    remote_cmd = RemoteCmd()
    remote_cmd.regist(subparsers)

    utf8bom_cmd_reg(subparsers)
    nginx_cmd_reg(subparsers)
    fir_cmd_reg(subparsers)

    args = parser.parse_args()      # 解析命令
    if hasattr(args, 'handle'):     # 1.第一个命令会解析成handle，使用args.handle()就能够调用
        args.handle(args)           # 1.1.其他参数会被解析成args的属性，以命令全称为属性名
    else:                           # 2.如果没有handle属性，则表示未输入子命令
        parser.print_help()


# python cli.py one
# python cli.py two
# python cli.py two -h
# python src/devocli/dummy.py find_big_files
# python src/devocli/dummy.py find_big_files -s 10
# python src/devocli/dummy.py pcsdk upload -
        
# python src/devocli/dummy.py omni --account_unbind_all 111 --token xxxx
# python src/devocli/dummy.py omni --account_register fengzilijie@qq.com
# python src/devocli/dummy.py omni --account_delete 1059
        
# python src/devocli/dummy.py remote --dir_copy lxlogs --date 2024-04-10

# python src/devocli/dummy.py fir.upload --token ece538a6e01af06934a621c36f699536 --file /Users/fallenink/Desktop/Developer/y8-assist-android/build/outputs/apk/debug/y8-assist-android-debug.apk --name 韵动场馆 --version 3.2.14 --build 84 --app_id 653762cd23389f6010122e43
# python src/devocli/dummy.py fir.latest --token ece538a6e01af06934a621c36f699536 --app_id 653762cd23389f6010122e43
if __name__ == '__main__':
    cli()

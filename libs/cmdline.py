# /usr/bin/env python
# coding=utf-8

import sys
import argparse
from IPy import IP

def get_args():
    """
    :return: 返回参数信息
    """
    parser = argparse.ArgumentParser(description="CDN Bypass Explotion Tools")
    parser.add_argument("--domain", help="Input the domain u want to find the true IP")
    parser.add_argument("--network", help="The network to scan,network[,network[,network]]")
    parser.add_argument("--file", help="The network file to scan")
    parser.add_argument("--keyword", help="The keyword U wanna filter")
    parser.add_argument("--browser", help="Scaned then browser it,default No", action="store_true")
    if len(sys.argv) == 1:
        sys.argv.append("-h")
    args = parser.parse_args()  # 增加-h参数之后，最后就会exit
    check_args(args)
    return args

def check_args(args):
    """
    检测参数的格式是否正确，并进行处理
    :param args:
    :return:
    """
    if not args.domain or (not args.network and not args.file):
        msg = "Please input 'Python cndx.py -h for help'"
        raise Exception(msg)


    args.ip = []            # IP列表保存的地方

    if args.network:        # 处理network
        network = args.network.split(",")
        for net in network:
            net = IP(net)
            for ip in net:
                args.ip.append(ip.strNormal(0))

    if args.file:           # 处理存在于文件中的nerwork
        with open(args.file, "r") as f:
            network = f.readlines()
            for net in network:
                net = IP(net.strip())
                for ip in net:
                    args.ip.append(ip.strNormal(0))    #

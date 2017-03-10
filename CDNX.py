# /usr/bin/env python
# coding=utf-8

import os
import sys
import socket
import threading
import webbrowser
from Queue import Queue
from httplib import HTTPResponse

from libs.report import *
from libs.log import logInit
from libs.cmdline import get_args
from libs.FakeSocket import FakeSocket



mutex = threading.Lock()
timeout = 10
socket.setdefaulttimeout(timeout)

class CDNX:
    def __init__(self):
        self.args = get_args()
        self.threads = 30
        self.log = logInit(log_name="res.log")
        self.result = []
        self.setTask()
        self.saveResult()

    def sendData(self, ip):
        """
        套接字通信
        :param ip:
        :return:
        """
        addr = (ip, 80)
        data = "GET / HTTP/1.1\r\nHost: " + self.args.domain + "\r\n" + "Connection: close" + "\r\n\r\n"
        recvdata = ""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        res = {}
        res.setdefault("ip", ip)
        res.setdefault("status")
        res.setdefault("body")
        res.setdefault("server_header")
        res.setdefault("x_powered_by_header")
        res.setdefault("success")
        try:
            sock.connect(addr)
            sock.send(data)
            while True:
                buffer = sock.recv(1024)
                if not buffer:
                    break
                recvdata += buffer
            response = HTTPResponse(FakeSocket(recvdata))
            response.begin()                                    # begin有什么用???
            res["status"] = response.status
            if response.status == 200:                          # 这里就可以保存为html文件了
                msg = ip + " seems done!!!"
                self.log.info(msg)
            res["body"] = response.read()
            res["server"] = response.getheader("Server", default="Known")
            res["x_powered_by"] = response.getheader("X-Powered-By", default="Known")
            if self.args.keyword:
                if self.args.keyword in res["body"]:
                    res["success"] = True
                else:
                    res["success"] = False
            else:
                res["success"] = True
            self.result.append(res)
        except Exception as err:
            self.log.error(err)
            res["success"] = False

    def setTask(self):
        """
        设置任务队列
        :return:
        """
        thread_list = []
        qsize = (len(self.args.ip)/1024+1)*1024
        self.queue = Queue(qsize)
        for ip in self.args.ip:
            self.queue.put(ip)
        for i in range(self.threads):
            thread_list.append(threading.Thread(target=self.run))
        for t in thread_list:
            t.start()
        for t in thread_list:
            t.join()

    def run(self):
        while True:
            if not self.queue.empty():
                ip = self.queue.get()
                self.sendData(ip)
            else:
                break
        pass

    def saveResult(self):
        """
        创建单独的目录,expmaple_com/result.html
        将self.result的结果存储进文件保存
        :return:
        """
        html = html_template.replace("{domain}", self.args.domain)
        content = ""
        if not self.result:
            msg = "No result....Scan Complished"
            self.log.warning(msg)
        else:
            dir = self.args.domain.replace(".", "_")
            path = sys.path[0] + "\\report\\" + dir
            if not os.path.exists(path):
                os.mkdir(path, 0755)
            for res in self.result:
                if res["success"] and res["status"]:
                    filename = path + "\\" + res["ip"].replace(".", "_") + ".html"
                    tmp_content = content_template
                    tmp_content = tmp_content.replace("{status}", str(res["status"]))
                    tmp_content = tmp_content.replace("{ip}", res["ip"])
                    tmp_content = tmp_content.replace("{x_powered_by}", res["x_powered_by"])
                    tmp_content = tmp_content.replace("{server}", res["server"])
                    tmp_content = tmp_content.replace("{href}", "file:///" + filename)
                    content += tmp_content
                    with open(filename, "w") as f:
                        f.write(res["body"])
            html = html.replace("{content_template}", content)
            with open(path + "\\result.html", "w") as f:
                f.write(html)
            msg = "Scan Complished"
            self.log.warning(msg)
            msg = "Saved in " + path + "\\result.html"
            self.log.warning(msg)
            if self.args.browser:
                webbrowser.open(path + "\\result.html")

if __name__ == "__main__":
    test = CDNX()

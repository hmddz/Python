"""
 !/usr/bin/env python3.6
 -*- coding: utf-8 -*-
 --------------------------------
 Description : 获取随机可以用IP
 --------------------------------
 @Time    : 19-2-28 上午11:28
 @File    : randomIp.py
 @Software: PyCharm
 --------------------------------
 @Author  : lixj
 @contact : lixj_zj@163.com
"""

import requests
from bs4 import BeautifulSoup as bs
import userAgent
import logging
import os
import random
import traceback

# logging.basicConfig函数对日志的输出格式及方式做相关配置
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')


class RandomIp():
    def __init__(self):
        self.XICI_URL = "https://www.xicidaili.com/nn/"
        self.BAIDU_URL = "https://www.baidu.com/"
        self.IP_POOL_FILE = "ipPool.txt"
        self.MAX_PAGE_OF_XICI = 3614  # 西刺网站总页数
        self.NUM_OF_PAGES = 3  # 爬取的目标页数
        # 获取随机的headers
        self.headers = userAgent.UserAgent().getRandomHeaders()  # userAgent.UserAgent() 类实例化()括号就相当于self参数

    def getIpPool(self):
        """
        获取IP池
        :return:
        """
        resultIpPool = []
        maxPage = self.MAX_PAGE_OF_XICI
        # 获取随机的NUM_OF_PAGES页
        targetPages = random.sample(range(1, maxPage), self.NUM_OF_PAGES)
        for onePage in targetPages:
            onePageUrl = self.XICI_URL + str(onePage)
            req = requests.get(onePageUrl, headers=self.headers, timeout=10)
            #
            if (req.status_code == 200):
                soup = bs(req.text, "lxml")
                ips = soup.find_all("tr")
                # 遍历当页的每条记录
                for i in range(1, len(ips)):
                    try:
                        ip = ips[i]
                        tds = ip.find_all("td")
                        tempIp = str(tds[5].contents[0]).lower() + "://" + tds[1].contents[0] + ":" + tds[2].contents[0]
                        speed = float(tds[6].div.get("title")[:-1])
                        connectTime = float(tds[7].div.get("title")[:-1])
                        #
                        if speed < 0.5 and connectTime < 0.5:
                            resultIpPool.append(tempIp)
                    except Exception as e:
                        logging.error("解析IP参数异常！")
                        traceback.format_exc(e)
            else:
                logging.error("连接异常！异常url:", onePageUrl)
        return resultIpPool

    def reviewIp(self):
        """
        重新验证IP池
        :return: ipPool
        """
        ipPool = self.getIpPool()
        try:
            for ip in ipPool[:10]:
                proxy = {ip.split("://")[0]: ip.split("://")[1]}
                req = requests.get(self.BAIDU_URL, proxies=proxy, headers=self.headers, timeout=10)
                if req.status_code != 200:
                    ipPool.remove(ip)
            return ipPool
        except Exception as e:
            logging.error("重新验证IP池异常！异常信息：", e)
            traceback.format_exc(e)

    def writeIpToFile(self):
        """
        IP写入文件
        :return:
        """
        try:
            module_path = os.path.dirname(__file__)
            fileName = module_path + '\\' + self.IP_POOL_FILE
            with open(fileName, "a+", encoding="utf-8") as f:
                f.write(str(self.getIpPool()))
                logging.info("写入IP {} 个结束！".format(len(self.getIpPool())))
        except Exception as e:
            logging.error("IP写入文件异常！异常信息：", e)
            traceback.format_exc(e)

    def getOneIp(self):
        """
        获取随机的一个IP地址
        :return:
        """
        try:
            module_path = os.path.dirname(__file__)
            fileName = module_path + '\\' + self.IP_POOL_FILE
            with open(fileName, "r", encoding="utf-8") as f:
                content = f.read()
                contList = content.split("', '")
                ipList = contList[1:len(contList) - 1]
                randomIp = random.choice(ipList)  # choice()获取一个
                logging.info("randomIp: %s", randomIp)
            return randomIp
        except Exception as e:
            logging.error("IP读入文件异常！异常信息：", e)
            traceback.format_exc(e)

    def getOneProxies(self):
        """
        获取随机的一个Proxies
        :return:
        """
        try:
            module_path = os.path.dirname(__file__)
            fileName = module_path + '\\' + self.IP_POOL_FILE
            with open(fileName, "r", encoding="utf-8") as f:
                content = f.read()
                contList = content.split("', '")
                ipList = contList[1:len(contList) - 1]
                randomIp = random.choice(ipList)  # choice()获取一个
                proxies = {"http": randomIp}
                logging.info("proxies: %s", str(proxies))
            return proxies
        except Exception as e:
            logging.error("IP读入文件异常！异常信息：", e)
            traceback.format_exc(e)

    def getNumOfIp(self, numOfIp):
        """
        获取指定数量的IP
        :return:
        """
        try:
            module_path = os.path.dirname(__file__)
            fileName = module_path + '\\' + self.IP_POOL_FILE
            with open(fileName, "r", encoding="utf-8") as f:
                content = f.read()
                contList = content.split("', '")
                ipList = contList[1:len(contList) - 1]
                randomIpList = random.sample(ipList, numOfIp)  # sample()获取多个
                logging.info("randomIpList: %s", randomIpList)
            return randomIpList
        except Exception as e:
            logging.error("IP读入文件异常！异常信息：", e)
            traceback.format_exc(e)
        pass


if __name__ == '__main__':
    RandomIp().writeIpToFile()

#! /usr/bin/python
# -*- coding: UTF-8 -*-
import requests
from mark_proxy import get_ipdeal_proxy
from loguru import logger

class Req():

    def __init__(self):
        ...

    @classmethod
    def do_get_req(cls,headers,url,timeout=5):
        ...

    @classmethod
    def do_post_req(cls,headers,url,data,timeout=5):
        ...

    @classmethod
    def do_json_req(cls,headers,url,json_data,timeout=5):
        for _ in range(3):
            try:
                proxies = get_ipdeal_proxy()
                rsp = requests.post(url=url,headers=headers,json=json_data,timeout=timeout,proxies=proxies)
                if rsp.status_code == 200:
                    return rsp
            except Exception as e:
                logger.info(e)


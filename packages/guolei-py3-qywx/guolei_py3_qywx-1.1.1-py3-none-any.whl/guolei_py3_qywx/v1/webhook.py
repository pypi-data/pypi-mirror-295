#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
=================================================
qywx Webhook Class Library
-------------------------------------------------
作者：[郭磊]
手机：[15210720528]
Email：[174000902@qq.com]
Github：https://github.com/guolei19850528/guolei_py3_qywx
=================================================
"""
from typing import Callable
from jsonschema import validate, Draft202012Validator
import requests
from addict import Dict


class Api(object):
    """
    企业微信 群机器人 Webhook Api Class
    @see https://developer.work.weixin.qq.com/document/path/91770
    """

    def __init__(
            self,
            base_url: str = "https://qyapi.weixin.qq.com/cgi-bin/webhook",
            key: str = "",
            mentioned_list: list = [],
            mentioned_mobile_list: list = []
    ):
        """
        @see https://developer.work.weixin.qq.com/document/path/91770
        :param base_url: base url
        :param key: key
        :param mentioned_list:
        :param mentioned_mobile_list:
        """
        validate(instance=base_url, schema={"type": "string", "minLength": 1, "format": "uri", })
        validate(instance=key, schema={"type": "string", "minLength": 1, })
        self._base_url = base_url
        self._key = key
        self._mentioned_list = mentioned_list
        self._mentioned_mobile_list = mentioned_mobile_list

    @property
    def base_url(self):
        return self._base_url[:-1] if self._base_url.endswith("/") else self._base_url

    @base_url.setter
    def base_url(self, value):
        self._base_url = value

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, value):
        self._key = value

    @property
    def mentioned_list(self):
        return self._mentioned_list

    @mentioned_list.setter
    def mentioned_list(self, value):
        self._mentioned_list = value

    @property
    def mentioned_mobile_list(self):
        return self._mentioned_mobile_list

    def send(
            self,
            request_func_kwargs: dict = {},
            request_func_response_callable: Callable = None
    ):
        """
        @see https://developer.work.weixin.qq.com/document/path/91770#%E6%B6%88%E6%81%AF%E7%B1%BB%E5%9E%8B%E5%8F%8A%E6%95%B0%E6%8D%AE%E6%A0%BC%E5%BC%8F
        :param request_func_kwargs:
        :param request_func_response_callable:
        :return:
        """
        if not Draft202012Validator({"type": "boolean", "const": True}).is_valid(isinstance(request_func_kwargs, dict)):
            request_func_kwargs = {}
        request_func_kwargs = Dict(request_func_kwargs)
        request_func_kwargs.setdefault("url", f"{self.base_url}/send")
        request_func_kwargs.setdefault("method", f"POST")
        request_func_kwargs.setdefault("params", {})
        request_func_kwargs.params.setdefault("key", self.key)
        request_func_kwargs.setdefault("json", {})
        response = requests.request(**request_func_kwargs.to_dict())
        if Draft202012Validator({"type": "boolean", "const": True}).is_valid(
                isinstance(request_func_response_callable, Callable)):
            return request_func_response_callable(response, request_func_kwargs)
        if response.status_code == 200:
            if Draft202012Validator({
                "type": "object",
                "properties": {
                    "errcode": {"type": "integer", "const": 0},
                    "errmsg": {"type": "string", "const": "ok"},
                },
                "required": ["errcode", "errmsg"]
            }).is_valid(response.json()):
                return True
        return False

    def send_text(
            self,
            content: str = "",
            mentioned_list: list = [],
            mentioned_mobile_list: list = [],
            send_func_kwargs: dict = {}
    ):
        """
        @see https://developer.work.weixin.qq.com/document/path/91770#%E6%96%87%E6%9C%AC%E7%B1%BB%E5%9E%8B
        :param content:
        :param mentioned_list:
        :param mentioned_mobile_list:
        :param send_func_kwargs:
        :return:
        """
        if not isinstance(self.mentioned_list, list):
            self.mentioned_list = []
        if not isinstance(self.mentioned_mobile_list, list):
            self.mentioned_mobile_list = []
        send_func_kwargs = Dict(send_func_kwargs)
        send_func_kwargs.request_func_kwargs = {
            "json": {
                "msgtype": "text",
                "text": {
                    "content": content,
                    "mentioned_list": self.mentioned_list + mentioned_list,
                    "mentioned_mobile_list": self.mentioned_mobile_list + mentioned_mobile_list,
                }
            },
        }
        return self.send(**send_func_kwargs.to_dict())

    def send_markdown(
            self,
            content: str = "",
            mentioned_list: list = [],
            mentioned_mobile_list: list = [],
            send_func_kwargs: dict = {}
    ):
        """
        https://developer.work.weixin.qq.com/document/path/91770#markdown%E7%B1%BB%E5%9E%8B
        :param content:
        :param mentioned_list:
        :param mentioned_mobile_list:
        :param send_func_kwargs:
        :return:
        """
        if not isinstance(self.mentioned_list, list):
            self.mentioned_list = []
        if not isinstance(self.mentioned_mobile_list, list):
            self.mentioned_mobile_list = []
        send_func_kwargs = Dict(send_func_kwargs)
        send_func_kwargs.request_func_kwargs = {
            "json": {
                "msgtype": "markdown",
                "markdown": {
                    "content": content,
                    "mentioned_list": self.mentioned_list + mentioned_list,
                    "mentioned_mobile_list": self.mentioned_mobile_list + mentioned_mobile_list,
                }
            },
        }
        return self.send(**send_func_kwargs.to_dict())

    def send_file(
            self,
            media_id: str = "",
            mentioned_list: list = [],
            mentioned_mobile_list: list = [],
            send_func_kwargs: dict = {}
    ):
        """
        @see https://developer.work.weixin.qq.com/document/path/91770#%E6%96%87%E4%BB%B6%E7%B1%BB%E5%9E%8B
        :param media_id:
        :param mentioned_list:
        :param mentioned_mobile_list:
        :param send_func_kwargs:
        :return:
        """
        if not isinstance(self.mentioned_list, list):
            self.mentioned_list = []
        if not isinstance(self.mentioned_mobile_list, list):
            self.mentioned_mobile_list = []
        send_func_kwargs = Dict(send_func_kwargs)
        send_func_kwargs.request_func_kwargs = {
            "json": {
                "msgtype": "file",
                "file": {
                    "media_id": media_id,
                    "mentioned_list": self.mentioned_list + mentioned_list,
                    "mentioned_mobile_list": self.mentioned_mobile_list + mentioned_mobile_list,
                }
            },
        }
        return self.send(**send_func_kwargs.to_dict())

    def send_voice(
            self,
            media_id: str = "",
            mentioned_list: list = [],
            mentioned_mobile_list: list = [],
            send_func_kwargs: dict = {}
    ):
        """
        @see https://developer.work.weixin.qq.com/document/path/91770#%E8%AF%AD%E9%9F%B3%E7%B1%BB%E5%9E%8B
        :param media_id:
        :param mentioned_list:
        :param mentioned_mobile_list:
        :param send_func_kwargs:
        :return:
        """
        if not isinstance(self.mentioned_list, list):
            self.mentioned_list = []
        if not isinstance(self.mentioned_mobile_list, list):
            self.mentioned_mobile_list = []
        send_func_kwargs = Dict(send_func_kwargs)
        send_func_kwargs.request_func_kwargs = {
            "json": {
                "msgtype": "voice",
                "file": {
                    "media_id": media_id,
                    "mentioned_list": self.mentioned_list + mentioned_list,
                    "mentioned_mobile_list": self.mentioned_mobile_list + mentioned_mobile_list,
                }
            },
        }
        return self.send(**send_func_kwargs.to_dict())

    def upload_media(
            self,
            request_func_kwargs: dict = {},
            request_func_response_callable: Callable = None
    ):
        """
        @see https://developer.work.weixin.qq.com/document/path/91770#%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0%E6%8E%A5%E5%8F%A3
        :param request_func_kwargs:
        :param request_func_response_callable:
        :return:
        """

        if not Draft202012Validator({"type": "boolean", "const": True}).is_valid(isinstance(request_func_kwargs, dict)):
            request_func_kwargs = {}
        request_func_kwargs = Dict(request_func_kwargs)
        request_func_kwargs.setdefault("url", f"{self.base_url}/upload_media")
        request_func_kwargs.setdefault("method", f"POST")
        request_func_kwargs.setdefault("params", {})
        request_func_kwargs.params.setdefault("key", self.key)
        request_func_kwargs.params.setdefault("type", "file")
        request_func_kwargs.setdefault("files", {})
        response = requests.request(**request_func_kwargs.to_dict())
        if Draft202012Validator({"type": "boolean", "const": True}).is_valid(
                isinstance(request_func_response_callable, Callable)):
            return request_func_response_callable(response, request_func_kwargs)
        if response.status_code == 200:
            if Draft202012Validator({
                "type": "object",
                "properties": {
                    "errcode": {"type": "integer", "const": 0},
                    "errmsg": {"type": "string", "const": "ok"},
                    "media_id": {"type": "string", "minLength": 1},
                },
                "required": ["errcode", "errmsg", "media_id"]
            }).is_valid(response.json()):
                return Dict(response.json()).media_id
        return None

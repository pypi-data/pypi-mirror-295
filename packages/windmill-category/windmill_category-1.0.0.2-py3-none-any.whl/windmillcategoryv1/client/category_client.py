#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright(C) 2023 baidu, Inc. All Rights Reserved

# @Time : 2024/3/20 19:38
# @Author : zhangzhijun06
# @Email: zhangzhijun06@baidu.com
# @File : category_client.py
# @Software: PyCharm
"""
import json
from typing import Optional
from baidubce.http import http_methods
from baidubce.http import http_content_types
from baidubce.bce_client_configuration import BceClientConfiguration

from bceinternalsdk.client.bce_internal_client import BceInternalClient
from bceinternalsdk.client.paging import PagingRequest


class CategoryClient(BceInternalClient):
    """
    A client class for interacting with the Category service. Initializes with default configuration.

    This client provides an interface to interact with the Category service using BCE (Baidu Cloud Engine) API.
    It supports operations related to creating and retrieving category within a specified workspace.
    """

    def create_category(self, workspace_id: str, local_name: str, category: str,
                        object_type: str, object_name: str):
        """
        Create a new category.

        Args:
            workspace_id (str): Workspace ID.
            local_name (str): 本地名称, example: "cate01"
            category (str): 分类, example: "firstCate/secondCate"
            object_type (str): 数据类型, example: "model"
            object_name (str): 数据完整名称, example:"workspaces/ws01/categories/cate01"

        Returns:
            dict: The response containing information about the created category.
        """
        body = {"workspaceID": workspace_id,
                "localName": local_name,
                "category": category,
                "objectType": object_type,
                "objectName": object_name}
        return self._send_request(http_method=http_methods.POST,
                                  headers={b"Content-Type": http_content_types.JSON},
                                  path=bytes("/v1/workspaces/" + workspace_id +
                                             "/categories", encoding="utf-8"),
                                  body=json.dumps(body))

    def get_category(self, workspace_id: str, local_name: str):
        """
        Get details of a category.

        Args:
            workspace_id (str): Workspace ID.
            local_name (str): 本地名称, example: "cate01"

        Returns:
            dict: The response containing details of the requested category.
        """
        return self._send_request(http_method=http_methods.GET,
                                  path=bytes("/v1/workspaces/" + workspace_id +
                                             "/categories/" + local_name, encoding="utf-8"))

    def list_category(self, workspace_id: str, categories: Optional[list] = None,
                      object_type: Optional[str] = "", object_name: Optional[str] = "",
                      object_names: Optional[list] = None, is_distinct: Optional[bool] = None,
                      filter_param: Optional[str] = "",
                      page_request: Optional[PagingRequest] = PagingRequest()):
        """
        List categories based on the specified parameters.

        Args:
            workspace_id (str): Workspace ID.
            categories (Optional[list]): 分类, example: ["firstCate/secondCate"]
            object_type (Optional[str]): 数据类型, example: "model"
            object_name (Optional[str]): 数据完整名称, example:"workspaces/ws01/categories/cate01"
            object_names (Optional[list]): 数据完整名称列表, example: ["workspaces/ws01/categories/cate01"]
            is_distinct (Optional[bool]): 是否返回唯一值, example: True
            filter_param (Optional[str]): 过滤条件, example: "{\"key\":\"value\"}"
            page_request: 分页请求参数
        Returns:
            dict: Response from the service containing a list of categories.
        """
        params = {"pageNo": str(page_request.get_page_no()),
                  "pageSize": str(page_request.get_page_size()),
                  "order": page_request.order,
                  "orderBy": page_request.orderby,
                  "filter": filter_param}

        if categories:
            params["categories"] = categories
        if object_type != "":
            params["objectType"] = object_type
        if object_name != "":
            params["objectName"] = object_name
        if object_names:
            params["objectNames"] = object_names
        if is_distinct:
            params["isDistinct"] = is_distinct
        return self._send_request(http_method=http_methods.GET,
                                  path=bytes("/v1/workspaces/" + workspace_id +
                                             "/categories", encoding="utf-8"),
                                  body=json.dumps(params))


    def update_category(self, workspace_id: str, local_name: str, category: str):
        """
        Update details of a category.

        Args:
            workspace_id (str): Workspace ID.
            local_name (str): 本地名称, example: "cate01"
            category (str): 分类, example: "firstCate/secondCate"

        Returns:
            dict: The response containing information about the updated category.
        """
        body = {"workspaceID": workspace_id,
                "localName": local_name,
                "category": category}
        return self._send_request(http_method=http_methods.PUT,
                                  headers={b"Content-Type": http_content_types.JSON},
                                  path=bytes("/v1/workspaces/" + workspace_id +
                                             "/categories/" + local_name,
                                             encoding="utf-8"),
                                  body=json.dumps(body))

    def delete_category(self, workspace_id: str, local_name: str):
        """
        Delete a category.

        Args:
            workspace_id (str): Workspace ID.
            local_name (str): 本地名称, example: "cate01"

        Returns:
            dict: The response indicating the success of the deletion.
        """
        return self._send_request(http_method=http_methods.DELETE,
                                  path=bytes("/v1/workspaces/" + workspace_id +
                                             "/categories/" + local_name, encoding="utf-8"))

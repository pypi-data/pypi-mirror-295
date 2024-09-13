#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright(C) 2023 baidu, Inc. All Rights Reserved

# @Time : 2024/3/20 19:38
# @Author : zhangzhijun06
# @Email: zhangzhijun06@baidu.com
# @File : category_api.py
# @Software: PyCharm
"""
import re
from typing import Optional
from pydantic import BaseModel
from bceinternalsdk.client.validator import check as validator
from bceinternalsdk.client.validator import Naming

category_name_regex = re.compile("^workspaces/(?P<workspace_id>.+?)/categories/(?P<local_name>.+?)$")


class Category(BaseModel):
    """
    Category.
    """

    name: str
    local_name: str
    category: str
    create_at: str
    update_at: str
    naming: Naming

    def check(self):
        """
        Check the category.
        """
        if self.category is None or self.category == "":
            raise ValueError("category can not be empty.")

        m = category_name_regex.match(self.category)
        if m is None:
            raise ValueError("Parameter category is invalid.")

        return validator(self.category)

    def get_levels(self):
        """
        Get the levels of category.
        """
        levels = split_category(self.category)
        for i, level in enumerate(levels):
            if level == "":
                levels[i] = "*"

        return levels


class CategoryName(BaseModel):
    """
    The name of category.
    """

    workspace_id: str
    local_name: str

    def get_name(self):
        """
        get name
        """
        return f"workspaces/{self.workspace_id}/categories/{self.local_name}"


def parse_category_name(name: str) -> Optional[CategoryName]:
    """
    Get Category。
    """
    m = category_name_regex.match(name)
    if m is None:
        return None
    return CategoryName(
        workspace_id=m.group("workspace_id"),
        local_name=m.group("local_name"),
    )


def split_category(category: str):
    """
    Split category.
    """
    category = category.strip().lstrip("/").rstrip("/")
    return category.split("/")


def match(category1: str, category2: str):
    """
    Check if two categories is matched.
    """
    c1 = split_category(category1)
    c2 = split_category(category2)
    if len(c1) == 0 or len(c2) == 0:
        return False

    for i, value in enumerate(c1):
        if i > len(c2) - 1:
            return True

        if value != c2[i] and value != "*" and c2[i] != "*":
            return False

    return True
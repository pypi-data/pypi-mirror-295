#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: GPL-2.0-only
import os
from funnylog import logger


def check_git_installed():
    if not os.popen("git --version").read().startswith("git version"):
        logger.info("git 没有安装，我们将尝试安装")
        os.system("echo '1' | sudo -S apt install git -y")
        logger.error("git 没有安装，尝试安装 git 失败，请先安装 git")
        raise Exception("git 没有安装，请先安装 git")

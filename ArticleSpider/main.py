# -*- coding: utf-8 -*-
__author__ = 'bobby'

from scrapy.cmdline import execute

import sys
import os
# 报错module 'OpenSSL.SSL' has no attribute 'TLS_METHOD'
# 执行pip install pyopenssl --upgrade

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# execute(["scrapy", "crawl", "jobbole"])
# execute(["scrapy", "crawl", "zhihu"])

execute(["scrapy", "crawl", "lagou"])
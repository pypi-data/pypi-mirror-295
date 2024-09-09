#!/usr/bin/env python
#  -*- coding: utf-8 -*-
__author__ = 'chenli'

from pathlib import Path


def get_zq_otg_path():
    return Path(__file__, "../zq_otg").resolve()

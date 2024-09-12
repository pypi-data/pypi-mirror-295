#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Andreas Mussgiller
"""

from datetime import datetime, timedelta

def DateTimeFromDecimalYear(year):
    y = int(year)
    rem = year - y
    base = datetime(y, 1, 1)
    result = base + timedelta(seconds=(base.replace(year=base.year + 1) - base).total_seconds() * rem)
    return result

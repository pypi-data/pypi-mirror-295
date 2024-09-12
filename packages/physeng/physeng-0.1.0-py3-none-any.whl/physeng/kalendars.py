#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Andreas Mussgiller
"""

from datetime import date, timedelta
from workalendar.europe import Germany, Hamburg, LowerSaxony

class CalDESY(Hamburg):
    FIXED_HOLIDAYS = Hamburg.FIXED_HOLIDAYS

    def __init__(self, XMasStartDay=21, XMasEndDay=4, **kwargs):
        super().__init__(**kwargs)
        self.XMasStartDay = XMasStartDay
        self.XMasEndDay = XMasEndDay

    def get_variable_days(self, year):
        # usual variable days
        days = super().get_variable_days(year)

        if self.XMasStartDay<25:
            for d in range(self.XMasStartDay, 25, 1):
                if date(year, 12, d).weekday()<5:
                    days.append((date(year, 12, d), 'XMas Shutdown'))

        for d in range(27, 32):
            if date(year, 12, d).weekday()<5:
                days.append((date(year, 12, d), 'XMas Shutdown'))

        if self.XMasEndDay>1:
            for d in range(2, self.XMasEndDay+1):
                if date(year, 1, d).weekday()<5:
                    days.append((date(year, 1, d), 'XMas Shutdown'))

        return days

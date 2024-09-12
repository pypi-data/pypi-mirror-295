import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Andreas Mussgiller
"""

import pandas as pd

################################################################
# intitial version of function (c) Andreas Nuernberg (DESY)
################################################################
def DustMeter_xml_to_pandas(filename, cumulative=False):
    tree = ET.parse(filename)
    root = tree.getroot()
    
    if cumulative:
        ChannelDataString = "ChannelDataCumulative"
    else:
        ChannelDataString = "ChannelDataDiff"


    df = None

    for child in root:
        if child.attrib.get("WorksheetType")=="Data":
            # print(child.tag, child.attrib)
            for row in child[0]:
                if row.attrib.get("RowType")=="SampleRecord":
                    # print(row.tag, row.attrib)
                    tmp = dict()
                    for c in row:
                        cell = c[0]
                        # print(cell.tag, cell.attrib, cell.text)
                        # size = -1
                        if cell.attrib.get("DataType")=="SampleDate":
                            dat = datetime.fromisoformat(cell.text)
                            # print(dat)
                            tmp["DateTime"]=dat
                        if cell.attrib.get("DataType")=="ChannelSize":
                            # print(cell.attrib, cell.text)
                            size = f"{float(cell.text)} um"
                        if cell.attrib.get("DataType")==ChannelDataString:
                            count = int(cell.text) #int(cell.attrib.get("Count"))
                            # print(f"{size}um: {count}")
                            tmp[size]=count
                    # print(tmp)
                    if df is None:
                        df = pd.DataFrame(tmp, index=[dat])
                        #df = pd.DataFrame(tmp)
                    else:
                        df = pd.concat([df, pd.DataFrame(tmp, index=[dat])])
                        #df = pd.concat([df, pd.DataFrame(tmp)])
                    # print(df)

    return df

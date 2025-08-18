from fastapi import Query, HTTPException
from typing import Optional
from models import *


async def query_boss_data(industry=None, district=None, position=None):
    # 动态构建查询条件
    filters = {}
    if industry is not None:
        filters["industryName"] = industry
    if district is not None:
        filters["areaDistrict"] = district
    if position is not None:
        filters["positionName"] = position

    # 执行查询
    data = await BossData.filter(**filters)
    data_list = list(data)  # 转为列表（如果 data 是异步生成器）
    data_len = len(data_list)

    return {
        "sum": data_len,
        "data": data_list
    }
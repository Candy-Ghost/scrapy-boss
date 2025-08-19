from models import *


async def scale_salary_analyze(position=None):
    # 动态构建查询条件
    filters = {}
    if position is not None:
        filters["positionName"] = position

    # 执行查询
    data = await BossData.filter(**filters)
    salary = await BossData.filter(**filters).only("")


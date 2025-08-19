import ast
from models import *
from collections import Counter

async def job_labels_tags(district=None, position=None):
    # 初始化过滤条件字典
    filters = {}

    # 根据传入的参数构建过滤条件
    if district is not None:
        filters["areaDistrict"] = district  # 添加地区过滤条件
    if position is not None:
        filters["positionName"] = position  # 添加职位过滤条件

    # 从数据库中获取符合过滤条件的记录，只选择salaryDesc和scaleName字段
    data = await BossData.filter(**filters).only("labels")

    labels_counter = Counter()

    # 处理每条数据的技能
    for item in data:
        try:

            labels = ast.literal_eval(item.labels.lower()) if item.labels else []
            labels_counter.update(labels)  # 更新计数器
        except (ValueError, SyntaxError):
            # 如果数据格式有问题就跳过
            continue

    # 获取出现次数最多的前5个福利
    top_labels = labels_counter.most_common(5)


    result = [{"labels": labels, "count": count} for labels, count in top_labels]

    return result


async def job_qualification_tags(industry=None,district=None, position=None):
    # 初始化过滤条件字典
    filters = {}

    if industry is not None:
        filters["industryName"] = industry  # 添加地区过滤条件
    if district is not None:
        filters["areaDistrict"] = district  # 添加地区过滤条件
    if position is not None:
        filters["positionName"] = position  # 添加职位过滤条件

    # 从数据库中获取符合过滤条件的记录，只选择salaryDesc和scaleName字段
    degree_names = await BossData.filter(**filters).values_list("degreeName", flat=True)

    # 使用 Counter 统计每个 degreeName 的数量
    degree_counts = Counter(degree_names)

    return dict(degree_counts)
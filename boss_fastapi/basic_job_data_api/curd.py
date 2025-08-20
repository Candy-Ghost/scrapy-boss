import re
from collections import Counter  # 用于计数
import ast  # 用于安全地解析字符串形式的列表
from fastapi import Query, HTTPException
from typing import Optional
from models import *

#判断其中行业、区域、岗位条件输出相应内容
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

#计算薪资分位值
async def tantile_data(industry=None, district=None, position=None, experience=None,tantiles=[25, 50, 75]):
    filters = {}
    if industry is not None:
        filters["industryName"] = industry
    if district is not None:
        filters["areaDistrict"] = district
    if position is not None:
        filters["positionName"] = position
    if experience is not None:
        filters["experienceName"] = experience

    # 执行查询
    data = await BossData.filter(**filters).only("salaryDesc")

    if not data:
        return None  # 如果没有数据，返回None

    monthly_salaries = []
    annual_salaries = []

    for item in data:
        salary_desc = item.salaryDesc.strip()  # 去除前后空格
        if not salary_desc:
            continue  # 跳过空数据

        # 解析薪资范围（如 "28-35K·14薪"、"30W-50W/年"、"1.5M-2M"）
        match = re.match(r"(\d+\.?\d*)([KWMkwm]?)-(\d+\.?\d*)([KWMkwm]?)(?:\·(\d+)薪)?|(\d+)-(\d+)万/年",
                         salary_desc.lower())
        if not match:
            continue  # 如果格式不匹配，跳过

        # 解析薪资值、单位和结构
        if match.group(6):  # 处理"X万-Y万/年"格式
            min_val = float(match.group(6)) * 10  # 万转换为千
            max_val = float(match.group(7)) * 10
            months = 12
        else:  # 处理其他格式
            min_val = float(match.group(1))
            max_val = float(match.group(3))
            unit = (match.group(2) or match.group(4) or 'k').lower()
            months = int(match.group(5)) if match.group(5) else 12

            # 统一转换为千元(K)为单位
            if unit == 'w':  # 万转换为千
                min_val *= 10
                max_val *= 10
            elif unit == 'm':  # 百万转换为千
                min_val *= 1000
                max_val *= 1000

        # 计算平均月薪和年薪
        avg_monthly = (min_val + max_val) / 2
        avg_annual = avg_monthly * months

        monthly_salaries.append(avg_monthly)
        annual_salaries.append(avg_annual)

    if not monthly_salaries:
        return None  # 如果没有有效数据，返回None

    # 对薪资数据进行排序
    monthly_salaries.sort()
    annual_salaries.sort()

    # 计算分位值
    def calculate_tantiles(sorted_data, tantiles):
        n = len(sorted_data)
        results = {}
        for tantile in tantiles:
            if tantile < 0 or tantile > 100:
                continue
            index = (n - 1) * tantile / 100
            lower = int(index)
            upper = lower + 1
            weight = index - lower

            if upper >= n:
                value = sorted_data[lower]
            else:
                value = sorted_data[lower] * (1 - weight) + sorted_data[upper] * weight

            results[f"p{tantile}"] = round(value, 2)
        return results

    monthly_tantiles = calculate_tantiles(monthly_salaries, tantiles)
    annual_tantiles = calculate_tantiles(annual_salaries, tantiles)

    return {
        "monthly": monthly_tantiles,
        "annual": annual_tantiles,
        "count": len(monthly_salaries),
        "unit": "K"  # 明确标注所有数据已统一为千元
    }

#统计行业技能
async def skill_analyze(industry=None, position=None, experience=None, degree=None, scale=None):

    # 构建查询条件
    filters = {}
    if industry is not None:
        filters["industryName"] = industry
    if position is not None:
        filters["positionName"] = position
    if experience is not None:
        filters["experienceName"] = experience
    if degree is not None:
        filters["degreeName"] = degree
    if scale is not None:
        filters["scaleName"] = scale

    # 执行数据库查询，只获取showSkills字段
    data = await BossData.filter(**filters).only("showSkills")

    # 初始化技能计数器
    skill_counter = Counter()

    # 处理每条数据的技能
    for item in data:
        try:
            # 把字符串形式的列表(如'[java,python]')转为真正的列表
            # 统一转小写避免大小写差异造成的重复计数
            skills = ast.literal_eval(item.showSkills.lower()) if item.showSkills else []
            skill_counter.update(skills)  # 更新计数器
        except (ValueError, SyntaxError):
            # 如果数据格式有问题就跳过
            continue

    # 获取出现次数最多的前3个技能
    top_skills = skill_counter.most_common()

    # 格式化结果：返回[{"skill": "java", "count": 10}, ...]这样的形式
    result = [{"skill": skill, "count": count} for skill, count in top_skills]

    return result

#统计一个岗位前3出现的次数
async def position_statistics_data(position):
    # 查询该岗位的所有记录，只获取区域信息
    records = await BossData.filter(positionName = position).only("areaDistrict")

    # 统计各区域出现次数
    area_counts = {}
    for record in records:
        district = record.areaDistrict
        area_counts[district] = area_counts.get(district, 0) + 1

    # 按出现次数降序排序并取前3，转换为字典格式
    top_areas = dict(sorted(area_counts.items(), key=lambda x: x[1], reverse=True)[:3])

    return top_areas


import re
from typing import Optional, List, Dict

from fastapi import HTTPException
from models import *
import numpy as np



async def keywords_analyze(keywords, industry=None, district=None, experience=None, degree=None, scale=None):
    # 1. 动态构建查询条件
    keywords_lower = keywords.lower()

    # 1. 动态构建查询条件（所有字符串条件转为小写）
    filters = {}
    if industry is not None:
        filters["industryName__iexact"] = industry.lower()
    if district is not None:
        filters["areaDistrict__iexact"] = district.lower()
    if experience is not None:
        filters["experienceName__iexact"] = experience.lower()
    if degree is not None:
        filters["degreeName__iexact"] = degree.lower()
    if scale is not None:
        filters["scaleName__iexact"] = scale.lower()

    # 2. 查询数据库（使用不敏感匹配）
    positions = await BossData.filter(**filters).only(
        "positionName", "jobName", "showSkills", "postDescription", "salaryDesc"
    )

    # 3. 关键词分析（大小写不敏感匹配）
    salary_list = []
    for position in positions:  # 关键修复：遍历positions列表
        # 检查关键词匹配
        if keywords_lower == position.positionName.lower() :
            avg_monthly = calculate_salary_midpoint(position.salaryDesc)
            if avg_monthly is not None:
                salary_list.append(avg_monthly)
        elif  re.search(keywords_lower,position.jobName.lower()):
            avg_monthly = calculate_salary_midpoint(position.salaryDesc)
            if avg_monthly is not None:
                salary_list.append(avg_monthly)
        elif position.showSkills is not None and re.search(keywords_lower, position.showSkills.lower()):
             avg_monthly = calculate_salary_midpoint(position.salaryDesc)
             if avg_monthly is not None:
                salary_list.append(avg_monthly)

        elif position.postDescription is not None and re.search(keywords_lower,position.postDescription.lower()):
             avg_monthly = calculate_salary_midpoint(position.salaryDesc)
             if avg_monthly is not None:
                salary_list.append(avg_monthly)
    print(salary_list)
    retain = round_list_elements(salary_list)
    return analyze_salary_distribution(retain)


def calculate_salary_midpoint(salary_str: str) -> Optional[float]:
    """
    解析多种薪资格式并计算中间值（返回纯数值）

    支持的格式：
    - 固定月薪：6000元/月 → 6000
    - 月薪范围：10-13K·13薪 → (10+13)/2 * 1000 * 13/12
    - 月薪单值：15K → 15 * 1000
    - 时薪：100-120元/时 → (100+120)/2 * 8 * 22
    - 日薪：100-800元/天 → (100+800)/2 * 22
    - 周薪：4000元/周 → 4000 * 52 / 12
    - 年薪：30万/年 → 300000 / 12

    参数:
    salary_str: 薪资字符串

    返回:
    float: 薪资中间值，无法解析时返回None
    """
    if not salary_str:
        return None

    try:
        salary_lower = salary_str.lower()

        if "元/月" in salary_lower or "/month" in salary_lower:
            return float(re.search(r"\d+", salary_lower).group())

        if "·" in salary_lower:
            monthly_part, annual_part = salary_lower.split("·")
            annual_months = int(re.search(r"\d+", annual_part).group())
            monthly_mid = parse_monthly_salary(monthly_part)
            return monthly_mid * annual_months / 12 if monthly_mid else None

        if "元/时" in salary_lower or "/h" in salary_lower:
            hourly_range = re.search(r"(\d+)-?(\d*)", salary_lower.replace(" ", ""))
            min_h = float(hourly_range.group(1))
            max_h = float(hourly_range.group(2)) if hourly_range.group(2) else min_h
            return (min_h + max_h) / 2 * 8 * 22

        if "元/天" in salary_lower or "/d" in salary_lower:
            daily_range = re.search(r"(\d+)-?(\d*)", salary_lower.replace(" ", ""))
            min_d = float(daily_range.group(1))
            max_d = float(daily_range.group(2)) if daily_range.group(2) else min_d
            return (min_d + max_d) / 2 * 22

        if "元/周" in salary_lower or "/w" in salary_lower:
            weekly_range = re.search(r"(\d+)-?(\d*)", salary_lower.replace(" ", ""))
            min_w = float(weekly_range.group(1))
            max_w = float(weekly_range.group(2)) if weekly_range.group(2) else min_w
            return (min_w + max_w) / 2 * 52 / 12

        return parse_monthly_salary(salary_lower)

    except (ValueError, AttributeError):
        return None


def parse_monthly_salary(salary_str: str) -> Optional[float]:
    """解析月薪部分（10-13K 或 1-1.5万）"""
    salary_str = salary_str.replace(" ", "").lower()

    if "万" in salary_str:
        salary_str = salary_str.replace("万", "*10000")
    elif "k" in salary_str:
        salary_str = salary_str.replace("k", "*1000")

    if "-" in salary_str:
        parts = salary_str.split("-")
        min_val = eval(parts[0])
        max_val = eval(parts[1])
    else:
        min_val = max_val = eval(salary_str)

    return (min_val + max_val) / 2


def analyze_salary_distribution(salary_list: List[float]) -> Dict[str, Optional[float]]:

    if not salary_list:
        return {
            'count': 0,
            'min': None,
            '25%': None,
            'median': None,
            '75%': None,
            'max': None,
            'mean': None,
            'std': None
        }

    salary_array = np.array(salary_list)

    return {
        'count': len(salary_list),
        'min': float(np.min(salary_array)),
        '25%': float(np.percentile(salary_array, 25)),
        'median': float(np.median(salary_array)),
        '75%': float(np.percentile(salary_array, 75)),
        'max': float(np.max(salary_array)),
        'mean': float(np.mean(salary_array)),
        'std': float(np.std(salary_array)) if len(salary_list) > 1 else 0.0
    }

def round_list_elements(lst, decimals=2):
    """将列表中的每个数值保留指定小数位数"""
    return [round(num, decimals) for num in lst]
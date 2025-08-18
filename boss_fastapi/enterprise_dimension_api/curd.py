from models import *
from collections import defaultdict # 用于创建默认字典
import numpy as np


async def scale_salary_contact(industry=None, position=None, experience=None, degree=None, district=None):
    # 初始化过滤条件字典
    filters = {}

    # 根据传入的参数构建过滤条件
    if industry is not None:
        filters["industryName"] = industry  # 添加行业过滤条件
    if position is not None:
        filters["positionName"] = position  # 添加职位过滤条件
    if experience is not None:
        filters["experienceName"] = experience  # 添加经验要求过滤条件
    if degree is not None:
        filters["degreeName"] = degree  # 添加学历要求过滤条件
    if district is not None:
        filters["areaDistrict"] = district  # 添加地区过滤条件

    # 从数据库中获取符合过滤条件的记录，只选择salaryDesc和scaleName字段
    records = await BossData.filter(**filters).only("salaryDesc", "scaleName")

    # 定义薪资解析函数，将薪资描述转换为数值
    def parse_salary(salary_desc):
        # 如果薪资描述为空，返回None
        if not salary_desc:
            return None

        try:
            # 处理类似 "28-35K·14薪" 或 "15-30K" 的格式
            # 1. 去除字符串中的所有空格
            salary_str = salary_desc.replace(" ", "")

            # 2. 分离薪资部分和薪数部分（如果有）
            if "·" in salary_str:
                # 如果有·分隔符，分割薪资部分和薪数部分（我们只需要薪资部分）
                salary_part, _ = salary_str.split("·", 1)
            else:
                # 如果没有·分隔符，整个字符串都是薪资部分
                salary_part = salary_str

            # 3. 处理K单位（表示千元）
            if "K" in salary_part:
                # 如果有K单位，转换为小写并去掉K，然后分割上下限
                lower, upper = salary_part.lower().replace('k', '').split('-')
                # 计算平均值并转换为月薪数值（乘以1000）
                return (float(lower) + float(upper)) / 2 * 1000
            else:
                # 如果没有K单位，假设是人民币数值，直接分割计算平均值
                lower, upper = salary_part.split('-')
                return (float(lower) + float(upper)) / 2
        except:
            # 如果解析过程中出现任何错误，返回None
            return None

    # 创建按scaleName分组的字典，值为薪资列表
    grouped_data = defaultdict(list)

    # 遍历所有记录，解析薪资并按scaleName分组
    for record in records:
        # 解析当前记录的薪资
        salary = parse_salary(record.salaryDesc)
        # 如果解析成功，添加到对应scaleName的分组中
        if salary is not None:
            grouped_data[record.scaleName].append(salary)

    # 初始化结果列表
    result = []

    # 遍历每个scaleName分组，计算统计量
    for scale_name, salaries in grouped_data.items():
        # 确保该分组至少有1个有效薪资数据
        if len(salaries) >= 1:
            # 计算各种分位值和统计量
            quantiles = {
                'scaleName': scale_name,  # 公司规模名称
                'count': len(salaries),  # 该规模下的数据点数量
                'p25': round(np.percentile(salaries, 25), 2),  # 25分位数
                'p50': round(np.percentile(salaries, 50), 2),  # 中位数（50分位数）
                'p75': round(np.percentile(salaries, 75), 2),  # 75分位数
                'min': round(min(salaries), 2),  # 最小值
                'max': round(max(salaries), 2),  # 最大值
                'avg': round(np.mean(salaries), 2)  # 平均值
            }
            # 将计算结果添加到结果列表
            result.append(quantiles)

    # 按scaleName对结果进行排序
    result.sort(key=lambda x: x['scaleName'])

    # 返回最终结果
    return result
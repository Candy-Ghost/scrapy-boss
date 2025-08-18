from fastapi import APIRouter, Form, Depends, HTTPException
from models import *
from boss_fastapi.basic_job_data_api.curd import query_boss_data, tantile_data, skill_analyze, position_statistics_data
from boss_fastapi.basic_job_data_api.data_models import JobQueryParams, SalaryDistributionStatistics, SkillAnalyze, \
    PositionStatistics

basic_job_data = APIRouter()


@basic_job_data.get('/basic/job/data/',summary="职位数量统计")
async def basic_data(params : JobQueryParams = Depends()):
    industry = params.industry
    district = params.district
    position = params.position

    data = await query_boss_data(industry,district,position)
    return data

@basic_job_data.get('/salary/distribution/data/',summary="薪资分布分析")
async def salary_distribution(params : SalaryDistributionStatistics = Depends()):
    industry = params.industry
    district = params.district
    position = params.position
    experience = params.experience

    data = await tantile_data(industry, district, position,experience)
    return data

@basic_job_data.get('/job/skill/analysis/',summary="职位技能分析")
async def skill_analysis(params : SkillAnalyze = Depends()):
    industry = params.industry
    position = params.position
    experience = params.experience
    degree = params.degree
    scale = params.scale

    data = await skill_analyze(industry, degree, position, experience,scale)
    return data

@basic_job_data.get('/position/statistics',summary="岗位统计分析")
async def position_statistics(params : PositionStatistics = Depends()):
    position = params.position

    data = await position_statistics_data(position)
    return data

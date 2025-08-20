from fastapi import APIRouter, Form, Depends, HTTPException
from models import *
from boss_fastapi.competitive_analysis_api.curd import keywords_analyze
from boss_fastapi.competitive_analysis_api.data_models import KeywordsAnalyze

competitive_analysis = APIRouter()


@competitive_analysis.get('/position/salary/analysis',summary="根据输入的关键词（行业、经验、学历、规模）统计各项数据")
async def keywords_statistics(params : KeywordsAnalyze = Depends()):
    keywords = params.keywords
    industry = params.industry
    district = params.district
    experience = params.experience
    degree = params.degree
    scale = params.scale

    data = await keywords_analyze(keywords,industry, district, experience, degree, scale)
    return data


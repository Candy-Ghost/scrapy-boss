from fastapi import APIRouter, Form, Depends
from models import *

from boss_fastapi.competitive_analysis_api.data_models import ScaleSalary

competitive_analysis = APIRouter()


@competitive_analysis.get('/position/salary/analysis',summary="同岗位不同企业薪资对比")
async def salary_analysis(params : ScaleSalary = Depends()):
    position = params.position
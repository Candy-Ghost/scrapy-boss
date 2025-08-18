from fastapi import APIRouter, Form, Depends, HTTPException
from models import *
from boss_fastapi.basic_job_data_api.curd import  query_boss_data
from boss_fastapi.basic_job_data_api.data_models import JobQueryParams
basic_job_data = APIRouter()


@basic_job_data.get('/basic/job/data/',summary="职位数量统计")
async def basic_data(params : JobQueryParams = Depends()):
    industry = params.industry
    district = params.district
    position = params.position

    data = await query_boss_data(industry,district,position)
    return data


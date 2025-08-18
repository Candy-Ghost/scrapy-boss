from fastapi import APIRouter, Form, Depends
from models import *
from boss_fastapi.enterprise_dimension_api.curd import scale_salary_contact
from boss_fastapi.enterprise_dimension_api.data_models import PositionStatistics
enterprise_dimension = APIRouter()

@enterprise_dimension.get('/scale/salary',summary="企业的规模和薪资的相关性")
async def scale_salary(params : PositionStatistics = Depends()):
    industry= params.industry
    position= params.position
    experience= params.experience
    degree= params.degree
    district= params.district
    data = await scale_salary_contact(industry,position,experience,degree,district)
    return data
from fastapi import APIRouter, Form, Depends, HTTPException
from models import *

from boss_fastapi.basic_job_data_api.curd import ParamsValidator

basic_job_data = APIRouter()


@basic_job_data.get('/basic/job/data/',summary="职位数量统计")
async def basic_data(params: dict = Depends(ParamsValidator.validate_params))
    industry = params['industry']
    district = params['district']
    position = params['position']

    if industry is not None and district is None and position is None:
        data = await BossData.filter(industryName = industry)
        data_len = len(list(data))
        return {
                "sum":data_len,
                "data":data
        }
    elif industry is None and district is not None and position is None:
        data = await BossData.filter(areaDistrict = district)
        data_len = len(list(data))
        return {
            "sum": data_len,
            "data": data
        }
    elif industry is None and district is  None and position is  not None:
        data = await BossData.filter(positionName = position)
        data_len = len(list(data))
        return {
            "sum": data_len,
            "data": data
        }
    elif industry is not None and district is not None and position is None:
        data = await BossData.filter(industryName = industry,areaDistrict = district)
        data_len = len(list(data))
        return {
            "sum": data_len,
            "data": data
        }
    elif industry is not None and district is  None and position is not None:
        data = await BossData.filter(industryName=industry, positionName = position)
        data_len = len(list(data))
        return {
            "sum": data_len,
            "data": data
        }
    elif industry is  None and district is not None and position is not None:
        data = await BossData.filter(areaDistrict = district, positionName=position)
        data_len = len(list(data))
        return {
            "sum": data_len,
            "data": data
        }
    else :
        data = await BossData.filter(industryName=industry,areaDistrict=district, positionName=position)
        data_len = len(list(data))
        return {
            "sum": data_len,
            "data": data
        }
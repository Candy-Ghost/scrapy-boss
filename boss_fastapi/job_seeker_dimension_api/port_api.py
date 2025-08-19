from fastapi import APIRouter, Form, Depends
from models import *

from boss_fastapi.job_seeker_dimension_api.curd import job_labels_tags, job_qualification_tags
from boss_fastapi.job_seeker_dimension_api.data_models import LabelsTags, QualificationDistribution

job_seeker_dimension = APIRouter()

@job_seeker_dimension.get('/labels/tags',summary="求职者技能标签分布")
async def job_labels(params : LabelsTags = Depends()):
    district = params.district
    position = params.position

    data = await job_labels_tags(district,position)
    return data

@job_seeker_dimension.get('/qualification/distribution',summary="求职者学历标签比例")
async def qualification_distribution(params : QualificationDistribution = Depends()):
    industry = params.industry
    district = params.district
    position = params.position

    data = await job_qualification_tags(industry,district,position)
    return data
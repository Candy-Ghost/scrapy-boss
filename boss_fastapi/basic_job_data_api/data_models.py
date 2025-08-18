from pydantic import BaseModel, validator,field_validator,root_validator
from fastapi import Query, HTTPException
from typing import Optional

class JobQueryParams(BaseModel):
    industry: Optional[str] = Query(None)
    district: Optional[str] = Query(None)
    position: Optional[str] = Query(None)

    @root_validator(pre=True, allow_reuse=True)
    def check_at_least_one_param(cls, values):
        """确保至少提供一个查询参数"""
        if not any(v is not None for v in values.values()):
            raise HTTPException(
                status_code=400,
                detail="至少需要提供一个查询参数"
            )
        return values

class SalaryDistributionStatistics(BaseModel):
    industry: Optional[str] = Query(None)
    district: Optional[str] = Query(None)
    position: Optional[str] = Query(None)
    experience: Optional[str] = Query(None)

    @root_validator(pre=True, allow_reuse=True)
    def check_at_least_one_param(cls, values):
        """确保至少提供一个查询参数"""
        if not any(v is not None for v in values.values()):
            raise HTTPException(
                status_code=400,
                detail="至少需要提供一个查询参数"
            )
        return values

class SkillAnalyze(BaseModel):
    industry: Optional[str] = Query(None)
    position: Optional[str] = Query(None)
    experience:Optional[str] = Query(None)
    degree:Optional[str] = Query(None)
    scale:Optional[str] = Query(None)

    @root_validator(pre=True, allow_reuse=True)
    def check_at_least_one_param(cls, values):
        """确保至少提供一个查询参数"""
        if not any(v is not None for v in values.values()):
            raise HTTPException(
                status_code=400,
                detail="至少需要提供一个查询参数"
            )
        return values

class PositionStatistics(BaseModel):
    position: Optional[str] = Query(None)

    @root_validator(pre=True, allow_reuse=True)
    def check_at_least_one_param(cls, values):
        """确保至少提供一个查询参数"""
        if not any(v is not None for v in values.values()):
            raise HTTPException(
                status_code=400,
                detail="至少需要提供一个查询参数"
            )
        return values
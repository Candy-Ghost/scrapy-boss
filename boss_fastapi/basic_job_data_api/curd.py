from fastapi import Query, HTTPException
from typing import Optional

class ParamsValidator:
    @classmethod
    def validate_params(
        cls,
        industry: Optional[str] = Query(None),
        district: Optional[str] = Query(None),
        position: Optional[str] = Query(None)
    ):
        if not any([industry, district, position]):
            raise HTTPException(
                status_code=400,
                detail="至少需要提供一个查询参数（industry/district/position）"
            )
        return {"industry": industry, "district": district, "position": position}
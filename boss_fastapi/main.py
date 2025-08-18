from fastapi import FastAPI
import uvicorn
from settings import TORTOISE_ORM
from tortoise.contrib.fastapi import register_tortoise
from fastapi.middleware.cors import CORSMiddleware
from basic_job_data_api.port_api import basic_job_data
from enterprise_dimension_api.port_api import enterprise_dimension

app=FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # 可以根据需要替换为具体的域名
#     allow_credentials=True,
#     allow_methods=["*"],  # 允许所有方法，包括OPTIONS
#     allow_headers=["*"],
# )

app.include_router(basic_job_data,tags=['基础职位数据分析'],)
app.include_router(enterprise_dimension,tags=['企业维度分析'],)

# app.include_router(index_api,prefix="/user")

    #mysql
register_tortoise(
    app=app,
    config=TORTOISE_ORM,

)


if __name__ == '__main__':
    uvicorn.run("main:app",port=8050,reload=True)

    # aerich init -t settings.TORTOISE_ORM 初始化配置
    #aerich init-db  初始化数据库（一般只用一次）
    #aerich migrate[--name] 更改数据库
    #aerich upgrade 确定更改
    #aerich aerich upgrade 返回上一次更改


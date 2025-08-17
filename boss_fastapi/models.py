from tortoise.models import Model
from tortoise import fields


class BossData(Model):
    industryName = fields.CharField(max_length=500,null=True, description="行业")
    positionName = fields.CharField(max_length=500,null=True,  description="岗位名字")
    jobName = fields.CharField(max_length=500,null=True,description="职位名字")
    brandName = fields.CharField(max_length=500,null=True,description="公司名称")
    locationName = fields.CharField(max_length=500,null=True,description="工作地点")
    areaDistrict = fields.CharField(max_length=500,null=True,description="区域")
    businessDistrict = fields.CharField(max_length=500,null=True,description="商业区")
    experienceName = fields.CharField(max_length=500,null=True,description="工作经验")
    degreeName = fields.CharField(max_length=500,null=True,description="学历")
    salaryDesc = fields.CharField(max_length=500,null=True,description="薪资")
    showSkills = fields.CharField(max_length=1000,null=True,description="技能要求")
    postDescription = fields.TextField(null=True,description="职位描述")
    address = fields.CharField(max_length=500,null=True,description="公司具体地址")
    labels = fields.CharField(max_length=500,null=True,description="福利")
    scaleName = fields.CharField(max_length=500,null=True,description="规模")



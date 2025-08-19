from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `bossdata` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `industryName` VARCHAR(500) COMMENT '行业',
    `positionName` VARCHAR(500) COMMENT '岗位名字',
    `jobName` VARCHAR(500) COMMENT '职位名字',
    `brandName` VARCHAR(500) COMMENT '公司名称',
    `locationName` VARCHAR(500) COMMENT '工作地点',
    `areaDistrict` VARCHAR(500) COMMENT '区域',
    `experienceName` VARCHAR(500) COMMENT '工作经验',
    `degreeName` VARCHAR(500) COMMENT '学历',
    `salaryDesc` VARCHAR(500) COMMENT '薪资',
    `showSkills` VARCHAR(1000) COMMENT '技能要求',
    `postDescription` LONGTEXT COMMENT '职位描述',
    `address` VARCHAR(500) COMMENT '公司具体地址',
    `labels` VARCHAR(1000) COMMENT '福利',
    `scaleName` VARCHAR(500) COMMENT '规模'
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `aerich` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `version` VARCHAR(255) NOT NULL,
    `app` VARCHAR(100) NOT NULL,
    `content` JSON NOT NULL
) CHARACTER SET utf8mb4;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """

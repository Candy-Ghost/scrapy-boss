TORTOISE_ORM = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.mysql",
            "credentials": {
                "host": "localhost",      # 数据库主机地址
                "port": 3306,             # 端口（默认3306）
                "user": "root",            # 用户名
                "password": "123456",  # 密码
                "database": "fastapi-boss",     # 数据库名
                "charset": "utf8mb4",         # 字符集（推荐utf8mb4）
                "pool_recycle": 3600,          # 连接池回收时间（秒）
                "minsize": 5,                  # 最小连接数
                "maxsize": 20,                # 最大连接数
                "echo":True
            }
        }
    },
    "apps": {
        "models": {
            "models": ["models",'aerich.models'],  # 模型路径（包含aerich迁移表）
            "default_connection": "default",          # 默认连接名
        }
    },
    "use_tz": False,   # 是否使用时区（与数据库设置一致）
    "timezone": "Asia/shanghai", # 时区（若 use_tz=True 需指定）
}
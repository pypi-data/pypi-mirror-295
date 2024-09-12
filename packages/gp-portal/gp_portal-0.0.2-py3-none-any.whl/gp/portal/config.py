import os
import sys
from dotenv import load_dotenv

load_dotenv(".env")

class DefaultConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(16)
    STRAPI_URL = os.environ.get("STRAPI_URL", "http://gp-bench-3.hil:1337")
    NOCODB_URL = os.environ.get("NOCODB_URL", "http://gp-bench-3.hil:8083")
    NOCODB_API_TOKEN = os.environ.get("NOCODB_API_TOKEN")
    LOGURU_LEVEL = os.environ.get("LOGURU_LEVEL", "INFO")  # DEBUG, INFO, WARNING, ERROR, CRITICAL

    # loguru 配置
    # ref: https://loguru.readthedocs.io/en/stable/api/logger.html#loguru._logger.Logger.configure
    LOGURU_CONFIG = dict(
        handlers = [
            dict(sink = sys.stdout, level = LOGURU_LEVEL),
            dict(sink = "logs/gp_portal_{time:YYYY-MM-DD}.log", rotation = "1 day", retention = "5 days", level = "INFO"),
            dict(sink = "logs/gp_portal_{time:YYYY-MM-DD}_error.log", rotation = "1 day", retention = "5 days", level = "ERROR"),
        ],
        activation=[("gp.portal", True)],
    )

    # API 模块配置
    API = dict(
        strapi = dict(
            url = STRAPI_URL,
            endpoint = "endpoints",
            identifier = None,
            password = None
        )
    )

    # Flask-Caching 相关配置
    CACHE_TYPE = "SimpleCache"
    CACHE_DEFAULT_TIMEOUT = 300

    # NOCODB 配置
    NOCODB_CONFIG = dict(
        url = NOCODB_URL,
        api_token = NOCODB_API_TOKEN,
        project_id = "py64mim32384hzn",
        project = "台架",
        table_id = "mm9ydgsnc2516rj",
        blueprint = True    # 是否启用蓝图
    )

    MODULES = dict(
        ROOT = dict(
            package = "gp.portal.root",
        ),
        API = dict(
            package = "gp.portal.api",
        ),
        CACHE = dict(
            package = "gp.portal.cache",
        ),
        NOCODB = dict(
            package = "gp_flask_ext.flask_nocodb",
        ),
        OAUTH_GITLAB = dict(
            package = "gp_flask_ext.flask_gitlab_oauth",
            OAUTH_DOMAIN = "gitlab.carota.ai",
            # GITLAB_CLIENT_ID = "",        # 从环境变量中获取
            # GITLAB_CLIENT_SECRET = "",    # 从环境变量中获取
        )
	)
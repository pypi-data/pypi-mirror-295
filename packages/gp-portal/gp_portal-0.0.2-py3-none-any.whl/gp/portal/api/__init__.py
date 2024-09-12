from loguru import logger
from flask import Blueprint, Flask, current_app

bp = Blueprint("api", __name__) # 创建一个蓝图对象

def init_app(app: Flask, config=None):
    app.register_blueprint(bp, url_prefix="/api")  # 将蓝图注册到应用程序上

    # 根据config创建extension对象
    # config = app.config["API"]
    # strapi = Strapi(**config)
    # app.extensions["strapi"] = strapi

# def _get_strapi():
#    return current_app.extensions["strapi"]


@bp.route('/<endpoint>', methods=['GET', 'POST'])  # 定义接收请求的端点
def api_endpoint(endpoint):
    # 在这里编写处理请求的代码
    return {"message": f"Hello, World from {endpoint}"}

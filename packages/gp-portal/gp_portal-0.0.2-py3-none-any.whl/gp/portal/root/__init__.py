from loguru import logger
from flask import Blueprint, Flask, current_app, render_template, url_for

bp = Blueprint("root", __name__, template_folder="templates") # 创建一个蓝图对象

def init_app(app: Flask, config=None):
    app.register_blueprint(bp, url_prefix="/")  # 将蓝图注册到应用程序上

@bp.route('/')
def index():
    table_id = current_app.config["NOCODB_CONFIG"]["table_id"]
    record_url = url_for("nocodb.get", table_id=table_id)
    logger.debug(f"url: {record_url}")
    return render_template("index.html", record_url=record_url)
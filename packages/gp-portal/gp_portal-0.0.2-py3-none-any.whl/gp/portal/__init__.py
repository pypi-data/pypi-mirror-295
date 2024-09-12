import os

from loguru import logger
from flask import Flask
from .config import DefaultConfig

logger.disable("gp.portal")

def create_app(app_name=None, default_config=None, test_config=None, **kwargs):
    # create and configure the app
    app_name = app_name or __name__
    app = Flask(app_name, instance_relative_config=True, **kwargs)
    app.config.from_object(DefaultConfig)
    if default_config:
        app.config.from_object(default_config)

    if "LOGURU_CONFIG" in app.config:
        logger.configure(**app.config["LOGURU_CONFIG"])

    logger.debug("root_path: {}", app.root_path)
    logger.debug("instance_path: {}", app.instance_path)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        ret = app.config.from_pyfile('config.cfg', silent=True)
        if ret:
            logger.info("load config.cfg from {}", app.instance_path)
    else:
        # load the test config if passed in
        ret = app.config.from_mapping(test_config)
        if ret:
            logger.info("apply test config from {}", test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 注册其他模块
    for module, config in app.config.get("MODULES", dict()).items():
        logger.debug("Loading module: {}", module)
        package = config.get("package")
        if package:
            module = __import__(package, fromlist=["init_app"])
            module.init_app(app, config)

    return app
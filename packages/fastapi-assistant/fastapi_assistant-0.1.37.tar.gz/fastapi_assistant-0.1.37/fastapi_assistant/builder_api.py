import logging
import os
import copy
from typing import Union, Dict, Optional
from configparser import ConfigParser

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.openapi.docs import (
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
    get_redoc_html,
)

logging.basicConfig(format="%(asctime)s - %(levelname)s: %(message)s", level=logging.DEBUG)
logger = logging.getLogger(__name__)

FASTAPI_SETTINGS_MODULE = "FASTAPI_SETTINGS_MODULE"


def set_settings_module(module: str = "settings.ini"):
    os.environ.setdefault(FASTAPI_SETTINGS_MODULE, module)


def setup_routes(
    app: FastAPI,
    docs_url: str = "/docs",
    redoc_url: str = "/redoc",
):
    static_dir = os.path.join(os.path.dirname(__file__), "static")
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

    @app.get(docs_url, include_in_schema=False)
    async def custom_swagger_ui_html():
        return get_swagger_ui_html(
            openapi_url=app.openapi_url,
            title=f"{app.title} - Swagger UI",
            oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
            swagger_js_url="/static/swagger-ui-bundle.js",
            swagger_css_url="/static/swagger-ui.css",
        )

    @app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
    async def swagger_ui_redirect():
        return get_swagger_ui_oauth2_redirect_html()

    @app.get(redoc_url, include_in_schema=False)
    async def redoc_html():
        return get_redoc_html(
            openapi_url=app.openapi_url,
            title=f"{app.title} - ReDoc",
            redoc_js_url="/static/redoc.standalone.js",
        )


def builder_fastapi(deploy: Union[Dict, FastAPI, None] = None, fastapi_settings: Optional[Dict] = None) -> FastAPI:
    if isinstance(deploy, FastAPI):
        return deploy
    config = copy.deepcopy(deploy or fastapi_settings or {})

    docs_url = config.pop("docs_url", "/docs")
    redoc_url = config.pop("redoc_url", "/redoc")
    config.update({"docs_url": None, "redoc_url": None})

    _app = FastAPI(**config)

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 调用 setup_routes 函数，自动添加文档接口
    setup_routes(_app, docs_url, redoc_url)

    # 合并的异常处理器
    @_app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        logging.warning("Validation Error: %s", exc)
        return JSONResponse(
            content={"msg": "参数校验失败", "code": -1, "data": exc.errors()},
            status_code=400,
        )

    @_app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request, exc: StarletteHTTPException):
        return JSONResponse(
            content={"message": exc.detail},
            status_code=exc.status_code,
        )

    return _app


class BuilderSettings:
    def __init__(self, base_dir, default_setting):
        self.conf_path = os.path.join(base_dir, base_dir, default_setting)
        self.parser = ConfigParser()
        self.settings = self.mount_configuration()

    def mount_configuration(self):
        self.parser.read(self.conf_path, encoding="utf-8")

        class BaseSettings:
            class Service:
                section = "service"
                if self.parser.has_section(section):
                    app = self.parser.get(section, "app")
                    host = self.parser.get(section, "host")
                    port = self.parser.getint(section, "port")

            class Fastapi:
                config = {}
                section = "fastapi"
                if self.parser.has_section(section):
                    for option in self.parser.options(section):
                        value = self.parser.get(section, option)
                        if value in ["true", "false"]:
                            value = bool(value)
                        elif value == "null":
                            value = None
                        config[option] = value

            if self.parser.has_section("mysql"):

                class Mysql:
                    section = "mysql"
                    if self.parser.has_section(section):
                        username = self.parser.get(section, "username")
                        password = self.parser.get(section, "password")
                        host = self.parser.get(section, "host")
                        port = self.parser.getint(section, "port")
                        database = self.parser.get(section, "database")
            else:

                class Sqlit:
                    path = "/sqlit.db"
                    if self.parser.has_section("sqlit") and self.parser.has_option("sqlit", "path"):
                        path = self.parser.get("sqlit", "path")

        class Settings(BaseSettings): ...

        return Settings()

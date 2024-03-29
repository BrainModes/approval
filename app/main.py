from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from .config import ConfigClass
from .api_registry import api_registry
from app.resources.error_handler import APIException
from fastapi_sqlalchemy import DBSessionMiddleware
import os

def create_app():
    '''
    create app function
    '''
    app = FastAPI(
        title="Service Approval",
        description="Service Approval",
        docs_url="/v1/api-doc",
        version=ConfigClass.version
    )

    app.add_middleware(DBSessionMiddleware, db_url=ConfigClass.OPS_DB_URI)
    app.add_middleware(
        CORSMiddleware,
        allow_origins="*",
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # API registry
    # v1
    api_registry(app)

    @app.exception_handler(APIException)
    async def http_exception_handler(request: Request, exc: APIException):
        return JSONResponse(
            status_code=exc.status_code,
            content=exc.content,
        )

    return app

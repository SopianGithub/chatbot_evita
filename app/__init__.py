import time
from starlette.requests import Request
from fastapi import FastAPI
from mongoengine import connect
from starlette.testclient import TestClient
from fastapi.middleware.cors import CORSMiddleware

from app.logs import CustomizeLogger
from pathlib import Path
import logging

from app.routers import users, todos, ams, cc, segmen, employe, product, chat, login, conversation, report
from app.models.logs import Logs

logger = logging.getLogger(__name__)

config_path=Path(__file__).with_name("logging_config.json")

def create_app() -> FastAPI:
    app = FastAPI(title='CustomLogger', debug=False)
    logger = CustomizeLogger.make_logger(config_path)
    app.logger = logger

    return app

app = create_app()

@app.get('/custom-logger')
def customize_logger(request: Request):
    request.app.logger.info("Here Is Your Info Log")
    a = 1 / 0
    request.app.logger.error("Here Is Your Error Log")
    return {'data': "Successfully Implemented Custom Log"}

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

mongodb = connect('mongodb', host='mongodb://127.0.0.1:27017/evita')
client = TestClient(app)

app.include_router(users.router, prefix="/users", tags=["User Docs"], )
app.include_router(todos.router, prefix="/todo", tags=["Todo Docs!"], )
app.include_router(ams.router, prefix="/ams", tags=["AM Docs"], )
app.include_router(cc.router, prefix="/cc", tags=["CC Docs"], )
app.include_router(segmen.router, prefix="/segmen", tags=["Segmen Docs"], )
app.include_router(employe.router, prefix="/employe", tags=["Employe Docs"], )
app.include_router(product.router, prefix="/product", tags=["Product Docs"], )
app.include_router(chat.router, prefix="/hook", tags=["Webhook Docs"], )
app.include_router(login.router, prefix="/login", tags=["Login Docs"], )
app.include_router(conversation.router, prefix="/webhook", tags=["Webhook Docs"], )
app.include_router(report.router, prefix="/report", tags=["Report Docs"], )

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)

    log = Logs()
    log.loggerstr = str(process_time)
    log.save()

    return response
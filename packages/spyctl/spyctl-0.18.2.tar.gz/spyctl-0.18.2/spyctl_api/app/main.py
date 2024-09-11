import logging
from contextlib import asynccontextmanager

import spyctl.config.configs as cfg
from fastapi import FastAPI

from app import config
from app.api import create, diff, merge, report, validate


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger = logging.getLogger("uvicorn")
    logger.setLevel(logging.INFO)
    logger.info("Starting spyctl API server")
    await config.load_config()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/alive")
async def alive():
    return {"message": "Alive"}


@app.get("/")
async def root():
    return {"message": "Alive2"}


app.include_router(create.router)
app.include_router(diff.router)
app.include_router(merge.router)
app.include_router(validate.router)
app.include_router(report.router)
cfg.set_api_call()


if __name__ == "__main__":
    import uvicorn
    import uvicorn.config

    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"][
        "fmt"
    ] = "%(asctime)s %(levelname)s:  %(message)s"
    log_config["formatters"]["default"][
        "fmt"
    ] = "%(asctime)s %(levelname)s:  %(message)s"
    uvicorn.run(
        app,
    )

    uvicorn.run(
        app, host="0.0.0.0", port=8000, log_config=log_config, log_level="info"
    )

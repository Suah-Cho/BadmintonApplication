from contextlib import asynccontextmanager
import logging

import uvicorn
from fastapi import FastAPI, Request
from fastapi_cache import FastAPICache
from fastapi.responses import JSONResponse
from fastapi_cache.backends.inmemory import InMemoryBackend

from app.domains.user.exceptions import CustomException
from database.session import init_db, dispose_db
from app.api_router import router as api_router
from app.core.config import config

@asynccontextmanager
async def lifespan(app: FastAPI):
    print(config)
    init_db()
    FastAPICache.init(InMemoryBackend())

    yield  # lifespan 동안 애플리케이션 실행

    await dispose_db()

app = FastAPI(
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

origins = ["http://localhost:3000"]

@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    logging.info(str(exc))
    return JSONResponse(
        status_code=int(exc.status_code),
        content={
            "success": False,
            "message": str(exc.message),
        },
    )

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(api_router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
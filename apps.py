from fastapi import FastAPI
from app.api.main_router import router as main_router
from hypercorn.config import Config
from hypercorn.asyncio import serve
import asyncio

app = FastAPI()
app.include_router(main_router)

if __name__ == '__main__':
    hypercorn_config = Config()
    hypercorn_config.bind = ["0.0.0.0:8099"]

    asyncio.run(serve(app, hypercorn_config))

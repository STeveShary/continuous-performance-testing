import asyncio
from time import sleep

from fastapi import FastAPI
from starlette.responses import PlainTextResponse

app = FastAPI(title="API For Performance Testing")


@app.get("/fast")
async def get_fast_response():
    await asyncio.sleep(0.001)
    return PlainTextResponse("fast")


@app.get("/slow")
async def get_slow_response():
    await asyncio.sleep(0.8)
    return PlainTextResponse("slow")


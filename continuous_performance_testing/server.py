import asyncio

from fastapi import FastAPI
from starlette.responses import PlainTextResponse

# A simple FastAPI application to use as a testing example.
app = FastAPI(title="API For Performance Testing")


@app.get("/fast")
async def get_fast_response():
    """
    A simple "fast" response that will be run most of the time.
    """
    await asyncio.sleep(0.001)
    return PlainTextResponse("fast")


@app.get("/slow")
async def get_slow_response():
    """
    A simple "slow" response that will be run less often.
    :return:
    """
    await asyncio.sleep(0.8)
    return PlainTextResponse("slow")

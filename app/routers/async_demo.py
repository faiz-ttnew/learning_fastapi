import asyncio
import time

from fastapi import APIRouter


router = APIRouter(
    prefix="/async-demo",
    tags=["Async Learning"]
)


@router.get("/sync")
def sync_example():
    time.sleep(3)

    return {"message": "Sync wait completed"}


@router.get("/async")
async def async_example():
    await asyncio.sleep(3)

    return {"message": "Async wait completed"}


@router.get("/blocking")
async def blocking_example():
    time.sleep(3)

    return {"message": "Blocking wait completed"}
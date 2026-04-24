from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from routes.webhook import router as webhook_router
from routes.reports import router as reports_router
from database import get_pool, close_pool

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await get_pool()
    # scheduler.start()  # scheduler.py 구현 후 활성화
    yield
    await close_pool()
    # scheduler.shutdown()


app = FastAPI(title="unc-system", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(webhook_router)
app.include_router(reports_router)


@app.get("/health")
async def health():
    return {"status": "ok"}

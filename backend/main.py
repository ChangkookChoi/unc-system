from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from routes.webhook import router as webhook_router
from routes.reports import router as reports_router

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup: 스케줄러 시작 (scheduler.py 구현 후 활성화)
    # scheduler.start()
    yield
    # shutdown: 스케줄러 종료
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

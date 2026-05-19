from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import tasks, plans, ai_parser  # ← 加上 ai

app = FastAPI(title="每日计划 API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://你的netlify地址.netlify.app"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tasks.router, prefix="/tasks", tags=["任务"])
app.include_router(plans.router, prefix="/plans", tags=["每日计划"])
app.include_router(ai_parser.router, prefix="/ai", tags=["AI"])  # ← 加上这行

@app.get("/")
def root():
    return {"message": "后端运行正常 ✅"}
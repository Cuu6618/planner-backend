from fastapi import APIRouter
from database import supabase
from pydantic import BaseModel
from datetime import date

router = APIRouter()

class TaskCreate(BaseModel):
    title: str
    quadrant: str
    description: str = ""
    planned_date: date = None
    user_id: str

class TaskUpdate(BaseModel):
    status: str  # 'todo' 或 'done'

# 获取某天所有任务
@router.get("/")
def get_tasks(user_id: str, date: date = None):
    query = supabase.table("tasks").select("*").eq("user_id", user_id)
    if date:
        query = query.eq("planned_date", str(date))
    return query.execute().data

# 创建任务
@router.post("/")
def create_task(task: TaskCreate):
    data = task.dict()
    if data.get("planned_date"):
        data["planned_date"] = str(data["planned_date"])  # ← 加这行
    return supabase.table("tasks").insert(data).execute().data
# 完成任务（todo → done）
@router.patch("/{task_id}/complete")
def complete_task(task_id: str):
    from datetime import datetime
    return supabase.table("tasks").update({
        "status": "done",
        "completed_at": datetime.now().isoformat()
    }).eq("id", task_id).execute().data

# 删除任务
@router.delete("/{task_id}")
def delete_task(task_id: str):
    return supabase.table("tasks").delete().eq("id", task_id).execute().data
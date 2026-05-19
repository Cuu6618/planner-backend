from fastapi import APIRouter
from database import supabase
from pydantic import BaseModel
from datetime import date

router = APIRouter()

class DailyPlanCreate(BaseModel):
    user_id: str
    plan_date: date
    note: str = ""

class DailyPlanUpdate(BaseModel):
    note: str

# 获取某天的计划
@router.get("/")
def get_plan(user_id: str, plan_date: date):
    result = supabase.table("daily_plans") \
        .select("*") \
        .eq("user_id", user_id) \
        .eq("plan_date", str(plan_date)) \
        .execute()
    return result.data

# 创建每日计划
@router.post("/")
def create_plan(plan: DailyPlanCreate):
    result = supabase.table("daily_plans") \
        .insert(plan.dict()) \
        .execute()
    return result.data

# 更新每日计划备注
@router.patch("/{plan_id}")
def update_plan(plan_id: str, update: DailyPlanUpdate):
    result = supabase.table("daily_plans") \
        .update({"note": update.note}) \
        .eq("id", plan_id) \
        .execute()
    return result.data

# 删除每日计划
@router.delete("/{plan_id}")
def delete_plan(plan_id: str):
    result = supabase.table("daily_plans") \
        .delete() \
        .eq("id", plan_id) \
        .execute()
    return result.data
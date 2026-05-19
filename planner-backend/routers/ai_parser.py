from fastapi import APIRouter
from pydantic import BaseModel
from openai import OpenAI
import os
import json

router = APIRouter()

class AIRequest(BaseModel):
    text: str

@router.post("/classify")
def classify_tasks(req: AIRequest):
    client = OpenAI(
        api_key=os.getenv("DEEPSEEK_APIKEY"),
        base_url="https://api.deepseek.com"
    )
    
    prompt = f"""
你是一个任务管理助手。用户会输入一段话描述他要做的事情。
请根据艾森豪威尔四象限法则，将这些事情分类。

四个象限：
- urgent-important（重要且紧急）
- important-not-urgent（重要不紧急）
- urgent-not-important（紧急不重要）
- not-urgent-important（不重要不紧急）

用户输入：{req.text}

请严格按照以下 JSON 格式返回，不要有任何多余的文字：
{{
  "urgent-important": ["任务1", "任务2"],
  "important-not-urgent": ["任务3"],
  "urgent-not-important": [],
  "not-urgent-important": ["任务4"]
}}
"""
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )

    content = response.choices[0].message.content
    content = content.replace("```json", "").replace("```", "").strip()
    result = json.loads(content)
    return result

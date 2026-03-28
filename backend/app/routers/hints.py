from fastapi import APIRouter
from pydantic import BaseModel
from groq import Groq
import os

router = APIRouter()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

class HintRequest(BaseModel):
    question_title: str
    question_description: str
    user_code: str
    hint_level: int  # 1, 2, or 3
    attempts_so_far: int

class HintResponse(BaseModel):
    hint: str
    level: int

HINT_PROMPTS = {
    1: "Give a single directional question that points them toward the right approach. No code. No answer. Just one question.",
    2: "Describe the approach they should take in 1-2 sentences. No code yet.",
    3: "Give pseudocode only. No working Python. Just the logic structure."
}

@router.post("/hint", response_model=HintResponse)
async def get_hint(request: HintRequest):
    prompt = f"""
                You are a Socratic DSA tutor. A student is solving: {request.question_title}

                Problem: {request.question_description}

                Their current code:
                {request.user_code if request.user_code else "They haven't written anything yet."}

                They have attempted this {request.attempts_so_far} time(s).
                Hint level requested: {request.hint_level}

                Instructions: {HINT_PROMPTS[request.hint_level]}

                Be encouraging but don't give away the answer.
            """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
        temperature=0.7,
    )

    return HintResponse(
        hint=response.choices[0].message.content,
        level=request.hint_level
    )

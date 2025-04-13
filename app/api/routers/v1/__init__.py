from fastapi import APIRouter
from app.api.routers.v1.quiz import router as quiz_router

# v1 API 라우터 초기화
v1_router = APIRouter()

# 퀴즈 라우터 등록
v1_router.include_router(
    quiz_router,
    prefix="/quizzes",
    tags=["quizzes"],
    responses={404: {"description": "Not found"}},
)

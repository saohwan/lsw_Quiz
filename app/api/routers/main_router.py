from fastapi import APIRouter
from app.api.routers.user import user_router
from app.api.routers.v1 import v1_router

router = APIRouter()

# 사용자 라우터 등록
router.include_router(user_router)

# v1 API 라우터 등록
router.include_router(
    v1_router,
    prefix="/api/v1",
    tags=["v1"],
)



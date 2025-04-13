# fastapi
from fastapi import FastAPI
from app.core.modules import init_routers, make_middleware
from app.api.v1 import quiz
from app.core.cache import init_cache


def create_app() -> FastAPI:
    app_ = FastAPI(
        title="Quiz API",
        description="퀴즈 생성 및 응시를 위한 API",
        version="1.0.0",
        # dependencies=[Depends(Logging)],
        middleware=make_middleware(),
    )
    
    # 라우터 등록
    app_.include_router(quiz.router, prefix="/api/v1", tags=["quizzes"])
    init_routers(app_=app_)
    
    # 캐시 초기화
    @app_.on_event("startup")
    async def startup_event():
        await init_cache()
    
    return app_


app = create_app()

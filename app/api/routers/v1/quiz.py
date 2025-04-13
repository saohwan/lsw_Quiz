from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.auth import get_current_user, get_current_admin
from app.schemas.quiz import (
    QuizCreate, QuizUpdate, QuizInDB, QuizList,
    QuizAttemptCreate, QuizAttemptInDB
)
from app.models.quiz import Quiz, Question, QuizAttempt, Answer
from app.models.user import User
import random
from app.core.redis import get_from_cache, set_to_cache

router = APIRouter()


@router.post("", response_model=QuizInDB)
async def create_quiz(
    quiz: QuizCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """관리자만 퀴즈를 생성할 수 있습니다."""
    db_quiz = Quiz(
        title=quiz.title,
        description=quiz.description,
        total_questions=quiz.total_questions,
        is_random_questions=quiz.is_random_questions,
        is_random_choices=quiz.is_random_choices,
        created_by=current_user.id
    )
    db.add(db_quiz)
    db.flush()

    for question in quiz.questions:
        db_question = Question(
            quiz_id=db_quiz.id,
            content=question.content,
            choices=question.choices,
            correct_answer=question.correct_answer
        )
        db.add(db_question)

    db.commit()
    db.refresh(db_quiz)
    return db_quiz


@router.put("/{quiz_id}", response_model=QuizInDB)
async def update_quiz(
    quiz_id: int,
    quiz: QuizUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """관리자만 퀴즈를 수정할 수 있습니다."""
    db_quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not db_quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    for field, value in quiz.dict(exclude_unset=True).items():
        setattr(db_quiz, field, value)

    db.commit()
    db.refresh(db_quiz)
    return db_quiz


@router.delete("/{quiz_id}")
async def delete_quiz(
    quiz_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """관리자만 퀴즈를 삭제할 수 있습니다."""
    db_quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not db_quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    db.delete(db_quiz)
    db.commit()
    return {"message": "Quiz deleted successfully"}


@router.get("", response_model=List[QuizList])
async def list_quizzes(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """퀴즈 목록을 조회합니다. 관리자는 전체 목록을, 사용자는 응시 여부를 포함한 목록을 볼 수 있습니다."""
    cache_key = f"quizzes:list:{skip}:{limit}:{current_user.id}"
    cached_data = await get_from_cache(cache_key)
    if cached_data:
        return cached_data

    query = db.query(Quiz)
    
    if not current_user.is_admin:
        # 사용자의 경우 응시 여부를 포함한 목록을 반환
        attempts = db.query(QuizAttempt).filter(QuizAttempt.user_id == current_user.id).all()
        attempted_quiz_ids = {attempt.quiz_id for attempt in attempts}
        
        quizzes = query.offset(skip).limit(limit).all()
        result = [
            QuizList(
                **quiz.__dict__,
                is_completed=quiz.id in attempted_quiz_ids
            )
            for quiz in quizzes
        ]
    else:
        result = query.offset(skip).limit(limit).all()

    await set_to_cache(cache_key, result)
    return result


@router.get("/{quiz_id}", response_model=QuizInDB)
async def get_quiz(
    quiz_id: int,
    page: int = Query(1, ge=1),
    questions_per_page: int = Query(10, ge=1),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """퀴즈 상세 정보를 조회합니다. 문제는 페이징 처리됩니다."""
    cache_key = f"quiz:{quiz_id}:{page}:{questions_per_page}"
    cached_data = await get_from_cache(cache_key)
    if cached_data:
        return cached_data

    db_quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not db_quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    # 문제 랜덤 배치 여부에 따라 처리
    questions = db.query(Question).filter(Question.quiz_id == quiz_id).all()
    if db_quiz.is_random_questions:
        random.shuffle(questions)
    
    # 설정된 문제 수만큼만 선택
    questions = questions[:db_quiz.total_questions]
    
    # 페이징 처리
    start_idx = (page - 1) * questions_per_page
    end_idx = start_idx + questions_per_page
    paginated_questions = questions[start_idx:end_idx]
    
    db_quiz.questions = paginated_questions
    await set_to_cache(cache_key, db_quiz)
    return db_quiz


@router.post("/{quiz_id}/attempt", response_model=QuizAttemptInDB)
async def submit_quiz_attempt(
    quiz_id: int,
    attempt: QuizAttemptCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """퀴즈 응시를 제출합니다."""
    db_quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not db_quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    # 이미 응시한 경우 체크
    existing_attempt = db.query(QuizAttempt).filter(
        QuizAttempt.quiz_id == quiz_id,
        QuizAttempt.user_id == current_user.id
    ).first()
    if existing_attempt:
        raise HTTPException(status_code=400, detail="You have already attempted this quiz")

    # 새로운 응시 생성
    db_attempt = QuizAttempt(
        quiz_id=quiz_id,
        user_id=current_user.id,
        is_completed=True
    )
    db.add(db_attempt)
    db.flush()

    # 답안 저장 및 채점
    correct_count = 0
    for answer in attempt.answers:
        question = db.query(Question).filter(Question.id == answer.question_id).first()
        if not question:
            raise HTTPException(status_code=404, detail=f"Question {answer.question_id} not found")
        
        is_correct = question.correct_answer == answer.selected_answer
        if is_correct:
            correct_count += 1

        db_answer = Answer(
            attempt_id=db_attempt.id,
            question_id=answer.question_id,
            selected_answer=answer.selected_answer,
            is_correct=is_correct
        )
        db.add(db_answer)

    # 점수 계산 및 저장
    db_attempt.score = int((correct_count / len(attempt.answers)) * 100)
    db.commit()
    db.refresh(db_attempt)
    return db_attempt 
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class ChoiceBase(BaseModel):
    content: str
    order: int


class QuestionBase(BaseModel):
    content: str
    choices: List[ChoiceBase]
    correct_answer: int = Field(..., ge=0)


class QuestionCreate(QuestionBase):
    pass


class QuestionUpdate(QuestionBase):
    pass


class QuestionInDB(QuestionBase):
    id: int
    quiz_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class QuizBase(BaseModel):
    title: str
    description: Optional[str] = None
    total_questions: int = Field(..., gt=0)
    is_random_questions: bool = False
    is_random_choices: bool = False


class QuizCreate(QuizBase):
    questions: List[QuestionCreate]


class QuizUpdate(QuizBase):
    pass


class QuizInDB(QuizBase):
    id: int
    created_by: int
    created_at: datetime
    updated_at: datetime
    questions: List[QuestionInDB]

    class Config:
        from_attributes = True


class AnswerCreate(BaseModel):
    question_id: int
    selected_answer: int = Field(..., ge=0)


class AnswerInDB(AnswerCreate):
    id: int
    attempt_id: int
    is_correct: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class QuizAttemptCreate(BaseModel):
    quiz_id: int
    answers: List[AnswerCreate]


class QuizAttemptInDB(BaseModel):
    id: int
    quiz_id: int
    user_id: int
    score: int
    is_completed: bool
    created_at: datetime
    updated_at: datetime
    answers: List[AnswerInDB]

    class Config:
        from_attributes = True


class QuizList(BaseModel):
    id: int
    title: str
    description: Optional[str]
    total_questions: int
    is_completed: Optional[bool] = None
    created_at: datetime

    class Config:
        from_attributes = True 
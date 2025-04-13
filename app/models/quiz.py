from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.models.common import CommonModel
from app.core.database import Base


class Quiz(CommonModel):
    __tablename__ = "quizzes"

    title = Column(String, nullable=False)
    description = Column(String)
    total_questions = Column(Integer, nullable=False)  # 출제될 문제 수
    is_random_questions = Column(Boolean, default=False)  # 문제 랜덤 배치 여부
    is_random_choices = Column(Boolean, default=False)  # 선택지 랜덤 배치 여부
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relationships
    questions = relationship("Question", back_populates="quiz", cascade="all, delete-orphan")
    attempts = relationship("QuizAttempt", back_populates="quiz", cascade="all, delete-orphan")


class Question(CommonModel):
    __tablename__ = "questions"

    quiz_id = Column(Integer, ForeignKey("quizzes.id"), nullable=False)
    content = Column(String, nullable=False)
    choices = Column(JSON, nullable=False)  # 선택지와 정답 정보를 JSON으로 저장
    correct_answer = Column(Integer, nullable=False)  # 정답 번호
    
    # Relationships
    quiz = relationship("Quiz", back_populates="questions")
    answers = relationship("Answer", back_populates="question", cascade="all, delete-orphan")


class QuizAttempt(CommonModel):
    __tablename__ = "quiz_attempts"

    quiz_id = Column(Integer, ForeignKey("quizzes.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    score = Column(Integer, default=0)
    is_completed = Column(Boolean, default=False)
    
    # Relationships
    quiz = relationship("Quiz", back_populates="attempts")
    answers = relationship("Answer", back_populates="attempt", cascade="all, delete-orphan")


class Answer(CommonModel):
    __tablename__ = "answers"

    attempt_id = Column(Integer, ForeignKey("quiz_attempts.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    selected_answer = Column(Integer, nullable=False)  # 사용자가 선택한 답안
    is_correct = Column(Boolean, nullable=False)  # 정답 여부
    
    # Relationships
    attempt = relationship("QuizAttempt", back_populates="answers")
    question = relationship("Question", back_populates="answers") 
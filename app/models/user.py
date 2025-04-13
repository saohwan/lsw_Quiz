from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.models.common import CommonModel
from app.core.database import Base


class User(CommonModel):
	__tablename__ = "users"

	username = Column(String, unique=True, index=True, nullable=False)
	email = Column(String, unique=True, index=True, nullable=False)
	hashed_password = Column(String, nullable=False)
	first_name = Column(String)
	last_name = Column(String)
	role = Column(String, default='user')
	is_active = Column(Boolean, default=True)
	is_admin = Column(Boolean, default=False)
	created_at = Column(DateTime(timezone=True), server_default=func.now())
	updated_at = Column(DateTime(timezone=True), onupdate=func.now())

	def __repr__(self):
		return f"{self.email}"
	
metadata = Base.metadata


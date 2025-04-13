from sqlalchemy import Column, Integer, String, Boolean
from app.models.common import CommonModel
from app.core.database import Base


class User(CommonModel):
	__tablename__ = "users"

	username = Column(String, unique=True, index=True, nullable=False)
	email = Column(String, unique=True, index=True, nullable=False)
	hashed_password = Column(String, nullable=False)
	is_active = Column(Boolean, default=True)
	is_admin = Column(Boolean, default=False)

	def __repr__(self):
		return f"{self.email}"
	
metadata = Base.metadata


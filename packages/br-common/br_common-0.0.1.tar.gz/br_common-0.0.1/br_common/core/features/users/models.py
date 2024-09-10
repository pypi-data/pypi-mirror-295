from br_common.core.models import BaseModel
from enum import Enum
from sqlalchemy import Column, String, Enum as SQLEnum
from sqlalchemy.orm import validates


# Enum class for the role field
class UserRole(Enum):
    ADMIN = "admin"
    USER = "user"
    MODERATOR = "moderator"


class User(BaseModel):
    __tablename__ = 'users'

    name = Column(String(100), nullable=False)    
    mobile_number = Column(String(15), unique=True, nullable=False)    
    password = Column(String(255), nullable=True)    
    role = Column(SQLEnum(UserRole), nullable=False, default=UserRole.USER)
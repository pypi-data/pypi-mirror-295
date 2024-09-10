from br_common.core.models import BaseModel
from enum import Enum
from sqlalchemy import Column, String, Enum as SQLEnum
from sqlalchemy.orm import validates


# Enum class for the role field
class UserRole(Enum):
    PRE_SELLER = "pre-seller"
    SALES_MAN = "sales-man"
    DELIVERY_DRIVER = "delivery-driver"
    SUPERVISOR = "supervisor"


class User(BaseModel):
    __tablename__ = "users"

    name = Column(String(100), nullable=False)
    mobile_number = Column(String(15), unique=True, nullable=False)
    password = Column(String(255), nullable=True)
    # Use Enum with native_enum=False to store the actual string values
    role = Column(SQLEnum(UserRole, native_enum=False), nullable=False, default=UserRole.PRE_SELLER)

    def __repr__(self):
        return f"<User: [{self.id if self.id else 'Unsaved'}]>"
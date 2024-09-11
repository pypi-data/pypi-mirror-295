from br_common.core.models import BaseModel
from enum import Enum
from sqlalchemy import (
    Column,
    String,
    Enum as SQLEnum,
    Integer,
    DateTime,
    ForeignKey,
    func,
)
from sqlalchemy.orm import relationship


# Enum class for the role field
class UserRole(Enum):
    PRE_SELLER = "PRE_SELLER"
    SALES_MAN = "SALES_MAN"
    DELIVERY_DRIVER = "DELIVERY_DRIVER"
    SUPERVISOR = "SUPERVISOR"


class User(BaseModel):
    __tablename__ = "users"

    name = Column(String(100), nullable=False)
    mobile_number = Column(String(15), unique=True, nullable=False)
    password = Column(String(255), nullable=True)
    # Use Enum with native_enum=False to store the actual string values
    role = Column(
        SQLEnum(UserRole, native_enum=False),
        nullable=False,
        default=UserRole.PRE_SELLER,
    )

    otp_sessions = relationship("OtpSession", back_populates="user")

    def __repr__(self):
        return f"<User: [{self.id if self.id else 'Unsaved'}]>"


class OtpSession(BaseModel):
    __tablename__ = "otp_sessions"

    otp = Column(String(255), nullable=False)
    attempts = Column(Integer, default=0)
    otp_expires_at = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="otp_sessions")

    def __repr__(self):
        return f"<OtpSession: [{self.id if self.id else 'Unsaved'}]>"

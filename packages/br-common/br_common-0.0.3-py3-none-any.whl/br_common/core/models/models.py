from sqlalchemy import Column, Integer, DateTime, func
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import Session


@as_declarative()
class BaseModel:
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower() + "s"

    def save(self, db: Session):
        """Save the current instance to the database."""
        db.add(self)
        db.commit()
        db.refresh(self)  # Refresh the instance to reflect the changes

    def delete(self, db: Session):
        """Delete the current instance from the database."""
        db.delete(self)
        db.commit()

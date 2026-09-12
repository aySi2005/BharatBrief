"""Summary ORM model."""
import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, Text, Integer, Float, Boolean, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class Summary(Base):
    __tablename__ = "summaries"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    
    # Source info
    original_text: Mapped[str] = mapped_column(Text, nullable=False)
    source_url: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    source_type: Mapped[str] = mapped_column(String(20), nullable=False, default="text")  # text, url, pdf, docx, txt
    title: Mapped[str | None] = mapped_column(String(500), nullable=True)
    author: Mapped[str | None] = mapped_column(String(255), nullable=True)
    publish_date: Mapped[str | None] = mapped_column(String(100), nullable=True)
    
    # Summary output
    summary_text: Mapped[str] = mapped_column(Text, nullable=False)
    summary_length: Mapped[str] = mapped_column(String(20), nullable=False, default="medium")  # short, medium, detailed
    headline: Mapped[str | None] = mapped_column(String(500), nullable=True)
    key_points: Mapped[str | None] = mapped_column(JSON, nullable=True)
    bullet_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    # Analytics
    sentiment: Mapped[str | None] = mapped_column(String(20), nullable=True)
    sentiment_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    keywords: Mapped[str | None] = mapped_column(JSON, nullable=True)
    readability_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    original_word_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    summary_word_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    reading_time_saved: Mapped[int | None] = mapped_column(Integer, nullable=True)  # seconds
    confidence_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    
    # User interaction
    is_favorite: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="summaries")

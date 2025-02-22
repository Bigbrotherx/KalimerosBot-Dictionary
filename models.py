from sqlalchemy import String, TIMESTAMP, func, UniqueConstraint, ForeignKey

from database import Base
from sqlalchemy.orm import Mapped, mapped_column


class Word(Base):
    __tablename__ = "words"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    word: Mapped[str] = mapped_column(String, nullable=False)
    translation: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP, server_default=func.now())

    __table_args__ = (UniqueConstraint("word", "translation"),)


class UserWord(Base):
    __tablename__ = "user_words"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(String, nullable=False, index=True)
    word_id: Mapped[int] = mapped_column(
        ForeignKey(Word.id, ondelete="CASCADE"), nullable=False)
    added_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, server_default=func.now())

    __table_args__ = (UniqueConstraint("user_id", "word_id"),)

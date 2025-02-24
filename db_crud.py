import enum

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from models import Word, UserWord
from database import async_session
from deepl_api import translate_greek_to_russian


class CRUDStatus(enum.Enum):
    SUCCESS = "success"
    NO_RESULT = "no result"
    ERROR = "error"


async def _get_user_word(session: AsyncSession, word: str, user_id: str):
    query = select(UserWord).join(Word).where(
        UserWord.user_id == user_id,
        Word.word == word)
    result = await session.execute(query)
    return result.scalar_one_or_none()


async def get_word(word: str, translation: str):
    query = select(Word).where(
        Word.word == word, Word.translation == translation)
    async with async_session() as session:
        result = await session.execute(query)
    return result.scalar_one_or_none()


async def create_word(user_id: str, word: str, translation: str):
    if translation is None:
        translation = translate_greek_to_russian(word)
    async with async_session() as session:
        async with session.begin():
            db_word = await get_word(word=word, translation=translation)

            if db_word is None:
                db_word = Word(word=word, translation=translation)
                session.add(db_word)
                await session.flush()

        user_word = UserWord(user_id=user_id, word_id=db_word.id)
        session.add(user_word)

        try:
            await session.commit()
        except IntegrityError:
            await session.rollback()
            return {"message": "User already has this word",
                    "status": CRUDStatus.NO_RESULT}
    return {"message": "Word added", "status": CRUDStatus.SUCCESS}


async def update_word(user_id: str, word: str, new_translation: str):
    async with async_session() as session:
        async with session.begin():
            user_word = await _get_user_word(
                session=session, word=word, user_id=user_id)
            if user_word is None:
                return {"message": "Word not found for this user",
                        "status": CRUDStatus.ERROR}

            new_word_entry = await get_word(
                word=word, translation=new_translation)
            if new_word_entry is None:
                if new_translation is None:
                    new_translation = translate_greek_to_russian(word)
                new_word_entry = Word(word=word, translation=new_translation)
                session.add(new_word_entry)
                await session.flush()
            user_word.word_id = new_word_entry.id

            try:
                await session.commit()
            except IntegrityError as e:
                await session.rollback()
                return {"message": f"Failed to update word {e.detail}",
                        "status": CRUDStatus.ERROR}
            return {
                "message": "Word updated successfully",
                "status": CRUDStatus.SUCCESS
            }


async def delete_word(user_id: str, word: str):
    async with async_session() as session:
        async with session.begin():
            user_word = await _get_user_word(
                session=session, word=word, user_id=user_id)
            if user_word is None:
                return {"message": "Word not found for this user",
                        "status": CRUDStatus.NO_RESULT}
            await session.delete(user_word)

            word_query = select(UserWord).where(
                UserWord.word_id == user_word.word_id)
            word_result = await session.execute(word_query)
            remaining_users = word_result.scalar_one_or_none()
            if remaining_users is None:
                word_to_delete = await session.get(Word, user_word.word_id)
                if word_to_delete:
                    await session.delete(word_to_delete)
            try:
                await session.commit()
            except IntegrityError as e:
                await session.rollback()
                return {"message": f"Failed to delete word {e.detail}",
                        "status": CRUDStatus.ERROR}

            return {"message": "Word deleted successfully",
                    "status": CRUDStatus.SUCCESS}

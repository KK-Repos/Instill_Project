import logging
from datetime import datetime
from asyncio import gather, create_task
from fastapi import APIRouter, Body, Depends
from starlette.exceptions import HTTPException
from starlette.status import (
    HTTP_403_FORBIDDEN,
    HTTP_422_UNPROCESSABLE_ENTITY,
)

from app.models import DictionaryMeaning
from app.config import PASSWORD
from app.dictionary_service import DictionaryService
from app.api.dependencies import get_dictionary_service

logger = logging.getLogger()

router = APIRouter()

@router.post("/get-word-meaning", response_model=list[DictionaryMeaning])
async def def_word_meanings_from_dictionary(
    words: list[str] = Body(...),
    password: str = Body(...),
    dictionary_service:DictionaryService = Depends(get_dictionary_service),
):
    if password != PASSWORD:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Password is incorrect")
    try:
        start = datetime.now()
        
        # Sync approach
        # all_meanings = [await dictionary_service.get_dictionary_meaning(word) for word in words]
       
        unique_words = list(set(words))
        logger.info(f"getting word meaning for: {unique_words}")

        # Async Approach
        all_coroutines = [create_task(dictionary_service.get_dictionary_meaning_async(word)) for word in unique_words]
        all_meanings = await gather(*all_coroutines)
        
       
        end = datetime.now()
        logger.info(f"Time taken to serve: {end-start}")
        return all_meanings
    except Exception as ex:
        raise HTTPException(status_code=HTTP_422_UNPROCESSABLE_ENTITY, detail="Processing Failed")
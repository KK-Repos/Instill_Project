import requests
import logging
import httpx

from app.config import DICTIONARY_URL
from app.models import Meaning, DictionaryMeaning

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

httpx_logger = logging.getLogger("httpx")
httpx_logger.setLevel(logging.WARNING)

class DictionaryService:

    def __init__(self, database):
        self.database = database

    def insert_into_db(self, word_meaning):
        # this is just a network call that inserts the word meaning into database
        assert isinstance(word_meaning, DictionaryMeaning), "Insertion Failed"
        pass
    
    def get_dictionary_meaning(self, word:str) -> DictionaryMeaning:
        logger.info(f"getting word meaning for: {word}")
        url = f"{DICTIONARY_URL}/{word}"
        res = requests.get(url)
        if not res.ok:
            return None, None
        meanings = []
        source = []
    
        json_res = res.json()[0]
        source = json_res.get('sourceUrls', [])
        for meaning in json_res['meanings']:
            try:
                meaning_to_add = {}
                meaning_to_add['part_of_speech'] = meaning['partOfSpeech']
                meaning_to_add['definitions'] = list(map(lambda x: x['definition'], meaning['definitions']))
                meanings.append(Meaning(**meaning_to_add))
            except Exception:
                pass
        logger.info(f"got word meaning for: {word}")
        if meanings:
            word_meaning = DictionaryMeaning(meanings=meanings, source=source)
            self.insert_into_db(word_meaning)
            return word_meaning

        return meanings, source
    

    async def get_dictionary_meaning_async(self, word:str) -> DictionaryMeaning:
        logger.info(f"getting word meaning for: {word}")
        url = f"{DICTIONARY_URL}/{word}"
        res = {}
        async with httpx.AsyncClient() as client:
            res = await client.get(url)
            if res.status_code != httpx.codes.ok:
                return None, None
        
        meanings = []
        source = []
        
        json_res = res.json()[0]
        source = json_res.get('sourceUrls', [])
        for meaning in json_res['meanings']:
            try:
                meaning_to_add = {}
                meaning_to_add['part_of_speech'] = meaning['partOfSpeech']
                meaning_to_add['definitions'] = list(map(lambda x: x['definition'], meaning['definitions']))
                meanings.append(Meaning(**meaning_to_add))
            except Exception:
                pass
        logger.info(f"got word meaning for: {word}")
        if meanings:
            word_meaning = DictionaryMeaning(meanings=meanings, source=source)
            self.insert_into_db(word_meaning)
            return word_meaning

        return meanings, source
    

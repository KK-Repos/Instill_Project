from app.dictionary_service import DictionaryService

def get_database_service():
    return {}


def get_dictionary_service() -> DictionaryService:
    database = get_database_service()
    dictionary_service = DictionaryService(database = database)
    return dictionary_service
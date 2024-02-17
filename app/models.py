from pydantic import BaseModel

class Meaning(BaseModel):
    part_of_speech: str
    definitions: list[str]

class DictionaryMeaning(BaseModel):
    meanings: list[Meaning]
    source: list[str]
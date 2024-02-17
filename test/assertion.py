
def assert_status_code(response, expected_status_code):
    assert response.status_code == expected_status_code, f"Unexpected status code: {response.status_code}"

def assert_word_meaning(response_data):
    assert isinstance(response_data, list), "Expected a list in the response"
    assert len(response_data) == 1, "Expected exactly one item in the list"

    word_info = response_data[0]
    assert "meanings" in word_info, "Expected 'meanings' key in response"
    meanings = word_info["meanings"]

    assert isinstance(meanings, list), "Expected 'meanings' to be a list"
    assert len(meanings) == 1, "Expected exactly one meaning for the word 'car'"

    meaning_info = meanings[0]
    assert "part_of_speech" in meaning_info, "Expected 'part_of_speech' key in meaning"
    assert "definitions" in meaning_info, "Expected 'definitions' key in meaning"

    assert meaning_info["part_of_speech"] == "noun", "Expected part of speech to be 'noun'"
    assert len(meaning_info["definitions"]) == 12, "Expected 12 definitions for the word 'car'"

    source = "https://en.wiktionary.org/wiki/car"
    assert source in response_data[0].get("source", []), f"Expected source '{source}' not found in the response"
    

def assert_word_info(word_info, expected_meanings):
    assert "meanings" in word_info, "Expected 'meanings' key in response"
    meanings = word_info["meanings"]
    assert isinstance(meanings, list), "Expected 'meanings' to be a list"
    assert len(meanings) == expected_meanings, f"Expected exactly {expected_meanings} meaning(s)"

    for meaning_info in meanings:
        assert "part_of_speech" in meaning_info, "Expected 'part_of_speech' key in meaning"
        assert "definitions" in meaning_info, "Expected 'definitions' key in meaning"

        part_of_speech = meaning_info["part_of_speech"]
        assert part_of_speech in ["noun", "verb"], "Expected part of speech to be 'noun' or 'verb'"
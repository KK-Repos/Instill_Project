import requests
import pytest

from test.assertion import assert_status_code, assert_word_info, assert_word_meaning

from app.config import BASE_URL,HOST_PORT,API_V1_STR, PASSWORD


API_BASE_URL = f"{BASE_URL}:{HOST_PORT}{API_V1_STR}/get-word-meaning"


def test_wrong_password_post_api():
    payload = {
        "words": ["car"],
        "password": "wrong_password"
    }

    response = requests.post(API_BASE_URL, json=payload)

    assert_status_code(response,403)
    
    response_data = response.json()
    

    assert "detail" in response_data, "Expected 'detail' key in response"
    assert response_data["detail"] == "Password is incorrect", "Incorrect password error message"

def test_wrong_payload_post_api():
    payload = {
        "words": [0],
        "password": PASSWORD
    }

    response = requests.post(API_BASE_URL, json=payload)

    assert_status_code(response,422)
    
    response_data = response.json()
    error_message = response_data['detail'][0]['msg']
    expected_message = 'Input should be a valid string'
    assert error_message == expected_message, f"Expected error message: '{expected_message}', but got: '{error_message}'"

    print("[response_data]",error_message)


def test_valid_get_word_post_api():
    payload = {
        "words": ["car"],
        "password": PASSWORD
    }

    response = requests.post(API_BASE_URL, json=payload)

    assert_status_code(response,200)

    response_data = response.json()

    assert_word_meaning(response_data)


def test_duplicate_payload():
    payload = {
        "words": ["car","car"],
        "password": PASSWORD
    }

    response = requests.post(API_BASE_URL, json=payload)

    assert_status_code(response,200)

    response_data = response.json()

    assert_word_meaning(response_data)

def test_duplicate_payload():

    payload = {
        "words": ["car", "rocket"],
        "password": PASSWORD
    }
    try:
        response = requests.post(API_BASE_URL, json=payload)
        response.raise_for_status()
    except requests.RequestException as e:
        assert False, f"Request failed: {e}"

    assert_status_code(response,200)

    response_data = response.json()

    assert isinstance(response_data, list), "Expected a list in the response"
    assert len(response_data) == 2, "Expected exactly two items in the list"

    for word_info in response_data:
        txt = word_info.get("source", "")
        if "car" in txt:
            assert_word_info(word_info, expected_meanings=1)
        elif "rocket" in txt:
            assert_word_info(word_info, expected_meanings=2)


if __name__ == "__main__":
    pytest.main(["-v", "test/test_instill_qa.py"])

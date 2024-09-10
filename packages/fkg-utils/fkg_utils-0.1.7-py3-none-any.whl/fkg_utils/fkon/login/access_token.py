from fkg_utils.utils.utils import encode_md5_text
import requests
import json


def get_access_token(username, password) -> dict:
    '''
    Returns a dictionary with information about the access token.
    If an error occurs, a dictionary with the key "error" set to
    True and an error message will be returned.

    :return: A dictionary containing the following keys:
    - "error" (bool): True if there is an error, False otherwise.
    - "message" (str): A descriptive message about the result.
    - "data" (dict): A dictionary with additional information. If there is an
    error, this field will contain information about the error. Otherwise, this
    field will contain information from the server.
    - "token" (str): The access token returned by the server.
    '''
    try:

        password = encode_md5_text(password)

        payload_login = {
            "login": username,
            "password": password,
            "platform": 'fk-on'
        }

        payload_login = json.dumps(payload_login)

        headers_login = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36" # noqa E501
        }

        with requests.Session() as session:

            response = session.post(
                url="https://gateway.frisokar.com.br/auth/login",
                data=payload_login,
                headers=headers_login
            )

        status_code = response.status_code
        content_response = response.json()

        if status_code != 200:
            return {
                "error": True,
                "message": content_response,
                "data": status_code,
                "token": None
            }

        token = content_response["accessToken"]

    except Exception as e:
        return {
            "error": True,
            "message": "Unexpected error",
            "data": f"{e}",
            "token": None
        }

    return {
        "error": False,
        "message": "",
        "data": content_response,
        "token": token
    }

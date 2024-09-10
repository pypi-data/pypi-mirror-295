from fkg_utils.utils.utils import timestamp_to_datetime
from fkg_utils.utils.utils import encode_md5_text
from datetime import datetime
import requests
import tempfile
import json
import os


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

        today = datetime.now()

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

        temp_dir = tempfile.gettempdir()
        access_token_file = os.path.join(temp_dir, "access_token.json")

        if os.path.exists(access_token_file):

            with open(access_token_file, "r") as file:
                token_json = json.load(file)

            token = token_json["accessToken"]
            token_expire = token_json["tokenExpiry"]

            token_expire_date = timestamp_to_datetime(token_expire)

        if not os.path.exists(access_token_file) or token_expire_date <= today: # noqa E501

            with requests.Session() as session:

                response = session.post(
                    url="https://gateway.frisokar.com.br/auth/login",
                    data=payload_login,
                    headers=headers_login
                )

            status_code = response.status_code
            token_json = response.json()

            if status_code != 200:
                return {
                    "error": True,
                    "message": token_json,
                    "data": status_code,
                    "token": None
                }

            with open(access_token_file, "w") as file:
                json.dump(token_json, file, ensure_ascii=False, indent=4)

            token = token_json["accessToken"]

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
        "data": token_json,
        "token": token
    }

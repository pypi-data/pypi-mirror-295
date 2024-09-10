import requests


def publishing_queue(payload, token):
    '''
    Publishes a payload to the queue using the specified access token.

    :param payload: A dictionary representing the payload to be sent to the queue.
    :type payload: dict
    :param token: The access token to use for authentication.
    :type token: str
    :return: A dictionary containing the following keys:
        - "error" (bool): True if there is an error, False otherwise.
        - "message" (str): A descriptive message about the result.
        - "data" (dict): A dictionary with additional information. 
            If there is an error, this field will contain information about the error.
            Otherwise, this field will contain information from the server.
    ''' # noqa E501
    try:
        with requests.Session() as session:

            headers = {
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36", # noqa E501
                "authorization": f"Bearer {token}",
            }

            response = session.post(
                url="https://gateway.frisokar.com.br/fk-on/queue/publish",
                data=payload,
                headers=headers
            )

        status_code = response.status_code
        content_response = response.json()

        if status_code != 200:
            return {
                "error": True,
                "message": content_response,
                "data": status_code
            }

        if not content_response:
            return {
                "error": True,
                "message": content_response,
                "data": None
            }

    except Exception as e:
        return {
            "error": True,
            "message": "Unexpected error",
            "data": f"{e}",
            "token": ""
        }

    return {"error": False, "message": "", "data": content_response}

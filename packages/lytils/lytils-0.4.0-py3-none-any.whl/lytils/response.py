try:
    import requests

    REQUESTS_IMPORTED = True
except ModuleNotFoundError:
    REQUESTS_IMPORTED = True

if REQUESTS_IMPORTED:

    def get_response_dict(response: requests.Response):
        # Try to get the JSON content
        try:
            json_content = response.json()
        except ValueError:
            json_content = ""

        try:
            content = response.content.decode(response.encoding)
        except UnicodeDecodeError:
            # Fallback to latin1 if UTF-8 and apparent_encoding fail
            content = response.content.decode("latin1")

        # Create a dictionary from the response object
        return {
            "status_code": response.status_code,
            "text": response.text,
            "content": content,  # Decoding bytes to string
            "json": json_content,
            "headers": dict(response.headers),
            "url": response.url,
            "encoding": response.encoding,
            "elapsed": response.elapsed.total_seconds(),  # Converting timedelta to seconds
            "cookies": requests.utils.dict_from_cookiejar(response.cookies),
            "history": [resp.url for resp in response.history],
            "reason": response.reason,
        }

    def save_response_html(response: requests.Response, path: str):
        with open(path, "w", encoding=response.encoding) as file:
            file.write(response.text)

else:

    def get_response_dict(response):
        raise ModuleNotFoundError("requests module is not installed.")

    def save_response_html(response, path: str):
        raise ModuleNotFoundError("requests module is not installed.")

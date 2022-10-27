def paste_code_on_hastebin(code: str) -> str:
    """Return the hastebin url"""
    import requests
    return requests.post("https://hastebin.com/documents", data=code).json()["key"]

def get_url_to_code(code: str) -> str:
    """Return the raw url to the code using hastebin"""
    return f"https://hastebin.com/raw/{paste_code_on_hastebin(code)}"
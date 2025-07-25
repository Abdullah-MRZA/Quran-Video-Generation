from pathlib import Path
import requests
import hashlib
from pydantic import BaseModel
import json

CACHE_DIR = Path("caches")
CACHE_DIR.mkdir(parents=True, exist_ok=True)


# https://alquran.cloud/api


def fetch_and_cache(url: str) -> str:
    """
    Fetch JSON from `url` and write it to `cache_path`.
    Returns the parsed JSON as a Python dict.
    """

    # headers = {
    #     # "User-Agent": self.ua.random,
    #     "Accept": "application/json, text/plain, */*",
    #     "Accept-Language": "en-US,en;q=0.5",
    #     # "Referer": "https://quranwbw.com",
    #     "DNT": "1",
    #     "Connection": "keep-alive",
    #     "Accept-Encoding": "gzip, deflate, br",
    #     "Sec-Fetch-Site": "same-origin",
    #     "Sec-Fetch-Mode": "cors",
    #     "Sec-Fetch-Dest": "empty",
    # }

    hashname = hashlib.md5(url.encode("utf8")).hexdigest()
    filename = CACHE_DIR / Path(f"{hashname}.json")

    if filename.is_file():
        return filename.read_text()

    print(f"Requesting JSON from the internet… ({url})")
    response = requests.get(url)
    response.raise_for_status()

    _ = filename.write_text(response.text)
    return response.text


class translator(BaseModel):
    translation_name: str
    identifier: str


def get_translations() -> list[translator]:
    data = json.loads(
        fetch_and_cache("https://api.alquran.cloud/v1/edition/language/en")
    )
    translations = [
        translator(translation_name=x["name"], identifier=x["identifier"])
        for x in data["data"]
    ]
    return translations

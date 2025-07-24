import requests
from tqdm import tqdm
import json


def download_ayah_by_ayah():
    links = [f"https://api.alquran.cloud/v1/surah/{x}/1" for x in range(1, 114 + 1)]

    data = [json.loads(requests.get(link).text) for link in tqdm(links)]

    with open("download_ayah_by_ayah.json", "w") as f:
        _ = f.write(json.dumps(data))


# download_ayah_by_ayah()

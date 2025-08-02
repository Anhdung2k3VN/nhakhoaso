import requests
import random

# === Cấu hình API key ===
PEXELS_API_KEY = "UlGyLAQL2I186HmJK27g47a1Yr5JpLx20JU2tWCqBIHY26wlwtSUeme7"
UNSPLASH_ACCESS_KEY = "C4HYGPxckR-SqwTq90Fht4ibiYyc76HAJPNL5gAsZgA"

def get_from_pexels(query="nature", per_page=12, page=1):
    headers = {"Authorization": PEXELS_API_KEY}
    params = {
        "query": query,
        "per_page": per_page,
        "page": page
    }
    r = requests.get("https://api.pexels.com/v1/search", headers=headers, params=params)
    if r.status_code == 200:
        data = r.json()
        return [{"full": p['src']['original'], "thumb": p['src']['medium']} for p in data['photos']]
    return []

def get_from_unsplash(query="nature", per_page=12, page=1):
    url = "https://api.unsplash.com/search/photos"
    params = {
        "query": query,
        "per_page": per_page,
        "page": page,
        "client_id": UNSPLASH_ACCESS_KEY
    }
    r = requests.get(url, params=params)
    if r.status_code == 200:
        data = r.json()
        return [{"full": img['urls']['full'], "thumb": img['urls']['small']} for img in data['results']]
    return []

def get_wallpapers_combined(query="anime", total=24, page=1):
    n = total // 2  # chia đều cho 2 nguồn
    images = []
    images += get_from_pexels(query=query, per_page=n, page=page)
    images += get_from_unsplash(query=query, per_page=n, page=page)
    random.shuffle(images)  # trộn ngẫu nhiên
    return images

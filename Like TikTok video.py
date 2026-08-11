#@K_33_S
import requests
import time
import random
import re
import uuid
import binascii
import os
import secrets
import threading
import string
import webbrowser  
from typing import Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    import SignerPy
except ImportError:
    import subprocess, sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "SignerPy"])
    import SignerPy

class Config:
    REGIONS = ["AE", "IQ", "US", "FR", "DE", "EG", "SA"]
    DEVICE_TYPES = ["SM-S928B", "P40", "Mi 11", "iPhone12,1", "OnePlus9", "Pixel 6"]
    DEVICE_BRANDS = ["samsung", "huawei", "xiaomi", "apple", "oneplus", "google"]

success_count = 0
failed_count = 0
count_lock = threading.Lock()


session_file = input("ملف السيشنات (كل سطر sessionid) / Session file (one sessionid per line) : ")
with open(session_file, "r", encoding="utf-8") as f:
    SESSIONS = [line.strip() for line in f if line.strip()]

def extract_aweme_id(link: str) -> str:
   
    if link.isdigit():
        return link
    if "vt.tiktok.com" in link or "vm.tiktok.com" in link:
        try:
            resp = requests.head(link, allow_redirects=True, timeout=10)
            final = resp.url
        except:
            resp = requests.get(link, allow_redirects=True, timeout=10)
            final = resp.url
    else:
        final = link
    m = re.search(r'/video/(\d+)', final)
    if m:
        return m.group(1)
    raise ValueError(f"لم نتمكن من استخراج aweme_id من: / Could not extract aweme_id from: {final}")

def generate_mobile_ua() -> str:
    
    android_versions = ["10", "11", "12", "13", "14"]
    android_apis = ["29", "30", "31", "32", "33", "34"]
    models = [
        "SM-S908B", "SM-G991B", "M2011K2G", "ELS-NX9", "LE2123",
        "Pixel 6", "Pixel 7", "CPH2237", "V2045", "XQ-BC72",
        "LM-F100N", "SM-A536B", "2107113SG", "M2101K6G", "NE2213"
    ]
    app_versions = [
        "2022806050", "2022907000", "2023008001", "2023109002",
        "2023111003", "2023122004", "2024011005", "2024022006"
    ]
    ttnet_versions = ["6a8e8a4c", "7b9f9b5d", "8c0a0c6e", "9d1b1d7f"]
    quic_versions = ["5f23035d", "6g34146e", "7h45257f", "8i56368g"]
    
    model = random.choice(models)
    android_ver = random.choice(android_versions)
    api_level = random.choice(android_apis)
    build_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=random.randint(6, 10)))
    app_ver = random.choice(app_versions)
    ttnet_ver = random.choice(ttnet_versions)
    quic_ver = random.choice(quic_versions)
    
    return f"com.zhiliaoapp.musically/{app_ver} (Linux; U; Android {android_ver}; {api_level}; ar_EG; {model}; Build/{build_id}; Cronet/TTNetVersion:{ttnet_ver} QuicVersion:{quic_ver})"

def build_params() -> dict:
    
    return {
        'aweme_id': '',  
        'enter_from': random.choice(["homepage_hot", "homepage_follow", "homepage_fresh"]),
        'friends_upvote': "false",
        'type': "1",
        'channel_id': "0",
        'device_platform': "android",
        'os': "android",
        'ssmix': "a",
        'iid': str(random.randint(10**18, 10**19 - 1)),
        'device_id': str(random.randint(10**18, 10**19 - 1)),
        'ac': random.choice(["wifi", "4g", "5g"]),
        'channel': "googleplay",
        'aid': "1233",
        'app_name': "musical_ly",
        'version_code': str(random.randint(270000, 290000)),
        'version_name': f"{random.randint(27,29)}.{random.randint(0,9)}.{random.randint(0,9)}",
        'ab_version': "28.6.5",
        'device_type': random.choice(Config.DEVICE_TYPES),
        'device_brand': random.choice(Config.DEVICE_BRANDS),
        'language': "ar",
        'os_api': str(random.randint(28, 34)),
        'os_version': str(random.randint(10, 14)),
        'openudid': binascii.hexlify(os.urandom(8)).decode(),
        'manifest_version_code': str(random.randint(2022000000, 2024999999)),
        'resolution': random.choice(["1080*2400", "720*1600", "1440*3200"]),
        'dpi': str(random.choice([240, 320, 480])),
        'update_version_code': str(random.randint(2022000000, 2024999999)),
        '_rticket': str(int(time.time() * 1000)),
        'app_type': "normal",
        'sys_region': random.choice(Config.REGIONS),
        'mcc_mnc': str(random.randint(10000, 99999)),  
        'timezone_name': random.choice(["Africa/Cairo", "Asia/Baghdad", "Europe/Paris"]),
        'carrier_region_v2': str(random.randint(100, 999)),  
        'app_language': "ar",
        'carrier_region': random.choice(Config.REGIONS),  
        'ac2': random.choice(["wifi", "4g", "5g"]),
        'uoo': "0",
        'op_region': random.choice(Config.REGIONS),
        'timezone_offset': str(random.choice([7200, 10800, 3600])),
        'build_number': "28.6.5",
        'host_abi': "arm64-v8a",
        'locale': "ar",
        'region': random.choice(Config.REGIONS),
        'ts': int(time.time()),
        'cdid': str(uuid.uuid4()),
        'effect_sdk_version': "1.3.0",  
    }

def send_like(aweme_id: str, session_id: Optional[str] = None) -> None:

    global success_count, failed_count
    try:
        session = requests.Session()
        
      
        if SESSIONS:
            ss = random.choice(SESSIONS)
        else:
            ss = secrets.token_hex(16)
        
        secret = secrets.token_hex(16)
        session.cookies.update({
            "passport_csrf_token": secret,
            "passport_csrf_token_default": secret,
            "sessionid": ss,
            "sessionid_ss": ss,
            "sid_tt": ss,
        })
        
    
        host = random.choice(["22", "21", "16", "15", "19"])
        url = f"https://api{host}-normal-c-alisg.tiktokv.com/aweme/v1/commit/item/digg/"
        
   
        params = build_params()
        params['aweme_id'] = aweme_id
        payload = {'body': 'null'}
        
        
        headers = {'User-Agent': generate_mobile_ua()}
        sign_headers = SignerPy.sign(params=params, payload=payload, url=url)
        headers.update(sign_headers)
        
        response = session.post(url, params=params, data=payload, headers=headers, timeout=10)
        
        with count_lock:
            if response.status_code == 200 and '"status_code":0' in response.text:
                success_count += 1
            else:
                failed_count += 1
        
 
        print(f"\r[+] نجاح / Success: {success_count} | فشل / Failed: {failed_count}", end="", flush=True)
        
    except Exception:
        with count_lock:
            failed_count += 1
        print(f"\r[+] نجاح / Success: {success_count} | فشل / Failed: {failed_count}", end="", flush=True)

def main():
    
    print("=" * 50)
    print("قناة تليجرام / Telegram Channel: @tools_kretos")
    print("جارٍ فتح القناة تلقائياً / Opening channel automatically...")
    webbrowser.open("https://t.me/tools_kretos")  
    print("=" * 50)
    
 
    video_input = input("أدخل رابط الفيديو أو aweme_id / Enter video link or aweme_id: ")
    aweme_id = extract_aweme_id(video_input)

    print(f"[✓] تم استخراج / Extracted aweme_id: {aweme_id}")
    print("=" * 50)

    total = 10000
    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = []
        for _ in range(total):
            futures.append(executor.submit(send_like, aweme_id))
        for future in as_completed(futures):
            future.result()

    print(f"\n[✓] تم الانتهاء / Completed - نجاح / Success: {success_count} | فشل / Failed: {failed_count}")

if __name__ == "__main__":
    main()
import time
import uuid
import base64
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
import requests
from dotenv import load_dotenv
import os

load_dotenv()

API_BASE = "https://gmgn.ai"
API_KEY = os.getenv("GMGN_API_KEY")
PRIVATE_PEM = os.getenv("GMGN_PRIVATE_KEY")
WALLET = os.getenv("WALLET_ADDRESS")

def sign_message(path: str, query: dict, body: str = ""):
    timestamp = int(time.time())
    client_id = str(uuid.uuid4())
    query["timestamp"] = timestamp
    query["client_id"] = client_id
    sorted_qs = "&".join(f"{k}={v}" for k, v in sorted(query.items()))
    message = f"{path}:{sorted_qs}:{body}:{timestamp}"
    priv_key = serialization.load_pem_private_key(PRIVATE_PEM.encode(), password=None)
    signature = priv_key.sign(message.encode(), padding.PKCS1v15(), hashes.SHA256())
    return base64.b64encode(signature).decode(), timestamp, client_id

def gmgn_request(method: str, path: str, params=None, json_data=None):
    if params is None:
        params = {}
    headers = {"X-APIKEY": API_KEY}
    body_str = json_data if isinstance(json_data, str) else ""
    
    if method.upper() == "POST":
        sig, ts, cid = sign_message(path, params.copy(), body_str)
        headers["X-Signature"] = sig
        params["timestamp"] = ts
        params["client_id"] = cid
    
    url = f"{API_BASE}{path}"
    resp = requests.request(method, url, params=params, json=json_data, headers=headers)
    if resp.status_code != 200:
        print(f"❌ API Error: {resp.text}")
    return resp.json()

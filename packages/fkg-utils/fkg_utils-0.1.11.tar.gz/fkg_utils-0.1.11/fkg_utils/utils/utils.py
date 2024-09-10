from datetime import datetime
import hashlib


def encode_md5_text(text: str):
    sha1_hash = hashlib.sha1(text.encode()).digest()
    sha1_hex = sha1_hash.hex()
    md5_hash = hashlib.md5(sha1_hex.lower().encode()).digest()
    md5_hex = md5_hash.hex()
    return md5_hex.lower()


def timestamp_to_datetime(timestamp: int) -> datetime:
    return datetime.fromtimestamp(timestamp / 1000)

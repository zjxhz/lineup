import hashlib
from django.conf import settings

def check_signature(data):
    try:
        signature = data.get('signature')
        timestamp = data.get('timestamp')
        nonce = data.get('nonce')
        
        if not signature or not timestamp or not nonce:
            return False
        
        my_hash = hashlib.sha1(settings.SECRET_KEY+timestamp+nonce)
        return signature == my_hash 
    except Exception:
        return False
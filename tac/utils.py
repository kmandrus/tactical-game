from hashlib import md5
from datetime import datetime
from random import random


def new_id(name: str, creation_time: datetime = datetime.now(), salt: float = random()) -> str:
    unique_hash = md5()
    unique_hash.update(f"{name}_{creation_time}_{salt}".encode('utf8'))
    return f"{name}_{unique_hash.hexdigest()}"  

from random import randint
from config.database import SessionLocal,get_db
from models.url import Url
import sys
def base62_encode(deci: int):
    string = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    hash_str = ''
    while deci > 0 and len(hash_str)<7:
        hash_str = string[deci % 62] + hash_str
        deci //= 62
    return hash_str

def long_to_short(url: str):
    decimal = randint(1,sys.maxsize)
    short_url = base62_encode(decimal)
    short_url = short_url
    return short_url
    

    
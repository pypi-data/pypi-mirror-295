import os
import redis
import uuid
import json
import hashlib
from django.conf import settings
from cryptography.fernet import Fernet

class RedisHelper():
    def __init__(self):
        redis_host = settings.REDIS_HOST
        redis_port = settings.REDIS_PORT
        
        self.redis_client = redis.StrictRedis(host=redis_host, port=redis_port, db=0)

    # set the value in the redis
    def set_values(self, key, value):
        json_value = json.dumps(value)
        self.redis_client.set(key, json_value)

    # get the value from the redis
    def get_value(self, key):
        json_value = self.redis_client.get(key)
        if json_value:
            value = json.loads(json_value)
            return value
        else:
            return None
    
    # delete the key - value pair from the redis
    def delete_key(self, key):
        self.redis_client.delete(key)

    # generate the uuid that will be used as a key in the redis
    @classmethod
    def generate_uuid(self, data):
        # Use hashlib to create a stable hash based on the data
        has_string = hashlib.md5(data.encode("UTF-8")).hexdigest()

        # Generate UUID from the stable hash
        generated_uuid = uuid.UUID(hex=has_string)
        return generated_uuid
    
    @classmethod
    def encrypt_token(self, data):
        fernet = Fernet(os.getenv('ENCRYPT_DECRYPT_KEY'))
        encodedToken = fernet.encrypt(data.encode("UTF-8"))

        return encodedToken
    
    @classmethod
    def decrypt_token(self, data):
        fernet = Fernet(os.getenv('ENCRYPT_DECRYPT_KEY'))
        encodedToken = fernet.decrypt(data).decode("UTF-8")

        return encodedToken

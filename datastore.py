# Standard modules
import base64
import os

# Third-Party modules
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes
from Crypto.Util import Padding


def encrypt(key, data):
    block_size = 16

    key = SHA256.new(key.encode()).digest()
    nonce = get_random_bytes(block_size)

    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    padded_data = Padding.pad(data.encode(), block_size)

    ciphertext, tag = cipher.encrypt_and_digest(padded_data)
    bytes_result = b''.join([nonce, tag, ciphertext])

    return base64.encode(bytes_result).decode()


def get_client_secrets(key):
    result = {'gfycat': {}, 'streamable': {}}

    gfycat_secrets = get_gfycat_secrets()
    client_id = gfycat_secrets['client_id']
    client_secret = gfycat_secrets['client_secret']

    result['gfycat']['client_id'] = encrypt(key, client_id)
    result['gfycat']['client_secret'] = encrypt(key, client_secret)

    streamable_auth = get_streamable_secrets()
    result['streamable']['Authorization'] = encrypt(key,
                                                    streamable_auth)

    return result


def get_riot_api_key():
    return os.environ['RIOT_API_KEY']


def get_gfycat_secrets():
    client_id = os.environ['GFYCAT_CLIENT_ID']
    client_secret = os.environ['GFYCAT_CLIENT_SECRET']

    result = {'client_id': client_id, 'client_secret': client_secret}
    return result


def get_streamable_secrets():
    user_name = os.environ['STREAMABLE_USER_NAME']
    password = os.environ['STREAMABLE_PASSWORD']

    auth = f'{user_name}:{password}'.encode()
    authorization = base64.b64encode(auth).decode()

    return authorization

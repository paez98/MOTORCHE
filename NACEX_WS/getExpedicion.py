import os
import requests
import hashlib
from getExpeCodigo import getExpeCodigo


user = os.getenv('NACEX_USER')
pswd = os.getenv('NACEX_PASSWORD')

md5_pass = hashlib.md5(pswd.encode()).hexdigest()
base_url = os.getenv('NACEX_BASE_URL')

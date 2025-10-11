import os
import requests
from dotenv import load_dotenv

load_dotenv()


user = os.getenv('NACEX_USER')
pswd = os.getenv('NACEX_PASSWORD')

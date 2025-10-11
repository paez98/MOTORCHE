import os
from dotenv import  load_dotenv
request

data = load_dotenv(override=True)

password = os.getenv('PASSWORD')
USER = os.getenv('USER')
url = os.getenv('NACEX_BASE_URL')

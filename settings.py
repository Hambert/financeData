# settings.py
import os
from dotenv import load_dotenv

load_dotenv(verbose=True)

APIKEY = os.getenv("APIKEY")
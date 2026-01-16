import os
from dotenv import load_dotenv

load_dotenv()

DB_PATH = os.getenv("DB_PATH", "radioDevices.sqlite")

MIN_FREQ = 800
MAX_FREQ = 6000
DEFAULT_FREQUENCY = 2400
DEFAULT_POWER = 10

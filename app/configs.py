import os

from dotenv import load_dotenv

ENV = os.getenv("ENV", default="LOCAL")

if ENV == "TEST":
    load_dotenv(".env.test")
else:
    load_dotenv(".env")

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT")
DB_HOST = os.getenv("DB_HOST")

POSTGRESS_DB = os.getenv("POSTGRESS_DB")

APP_HOST = os.getenv("APP_HOST")
APP_PORT = int(os.getenv("APP_PORT", "5000"))
APP_DEBUG = bool(os.getenv("APP_DEBUG", 0))

ENGINE = os.getenv("ENGINE")

if ENGINE == "postgresql+psycopg2":
    BASE_URL = f"{ENGINE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}"
else:
    BASE_URL = ""

ECHO_OPTION = os.getenv("ECHO_OPTION", 1)
ENGINE_OPTIONS = {"echo": int(ECHO_OPTION)}

LOGGER_LEVEL = os.getenv("LOGGER_LEVEL")

GROUPS_AMOUNT = 10
STUDENTS_AMOUNT = 200

API_VERSION = "v1"
API_PREFIX = f"/api/{API_VERSION}"

# Importing necessary modules and packages
import os

# Defining environment variables
ROOT_PATH = os.getenv("ROOT_PATH", "fastapi")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PWD = os.getenv("DATABASE_PWD")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_PORT = os.getenv("DATABASE_PORT", 5432)
MAX_FILE_COUNT = os.getenv("MAX_FILE_COUNT", 10)
OLD_K_VALUE = os.getenv("OLD_K_VALUE", 20)
MAX_K_VALUE = os.getenv("MAX_K_VALUE", 80)

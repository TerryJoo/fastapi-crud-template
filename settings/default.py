import os

PROJECT_ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
DEBUG = os.getenv("DEBUG", False)
SQLITE3_DATABASE_URI: str = os.getenv("SQLITE3_DATABASE_URL", "sqlite:///./db.sqlite3")

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ─────────────────────────────────────────
# BASE PATHS
# ─────────────────────────────────────────
BASE_DIR     = Path(__file__).parent.parent
PROFILES_DIR = str(BASE_DIR / "profiles")
DATA_DIR     = str(BASE_DIR / "data")
TEMP_DIR     = str(BASE_DIR / "temp")
LOGS_DIR     = str(BASE_DIR / "logs")
MODELS_DIR   = str(BASE_DIR / "models")
ASSETS_DIR   = str(BASE_DIR / "assets")

# ─────────────────────────────────────────
# MODEL SETTINGS
# ─────────────────────────────────────────
OLLAMA_MODEL     = os.getenv("OLLAMA_MODEL", "llama3.1")
FACE_MODEL       = os.getenv("FACE_MODEL", "buffalo_l")
VECTOR_DIMENSION = int(os.getenv("VECTOR_DIMENSION", 512))
MATCH_THRESHOLD  = float(os.getenv("MATCH_THRESHOLD", 0.6))

# ─────────────────────────────────────────
# DATABASE PATHS
# ─────────────────────────────────────────
FAISS_INDEX_PATH = str(BASE_DIR / "data" / "face_index.bin")
METADATA_PATH    = str(BASE_DIR / "data" / "metadata.pkl")

# ─────────────────────────────────────────
# LOGGING
# ─────────────────────────────────────────
LOG_LEVEL    = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE     = str(BASE_DIR / "logs" / "ironclad.log")

# ─────────────────────────────────────────
# APP SETTINGS
# ─────────────────────────────────────────
APP_TITLE    = "🛡️ Ironclad - Face Detective"
APP_VERSION  = "1.0.0"
APP_AUTHOR   = "Ironclad Team"

# ─────────────────────────────────────────
# DETECTION SETTINGS
# ─────────────────────────────────────────
DET_SIZE     = (640, 640)
TOP_K        = 3              # Return top 3 matches
HNSW_M       = 32            # HNSW graph connections

# ─────────────────────────────────────────
# DEBUG PRINT (optional)
# ─────────────────────────────────────────
if __name__ == "__main__":
    print("=== Ironclad Settings ===")
    print(f"BASE_DIR         : {BASE_DIR}")
    print(f"OLLAMA_MODEL     : {OLLAMA_MODEL}")
    print(f"FACE_MODEL       : {FACE_MODEL}")
    print(f"VECTOR_DIMENSION : {VECTOR_DIMENSION}")
    print(f"MATCH_THRESHOLD  : {MATCH_THRESHOLD}")
    print(f"FAISS_INDEX_PATH : {FAISS_INDEX_PATH}")
    print(f"METADATA_PATH    : {METADATA_PATH}")

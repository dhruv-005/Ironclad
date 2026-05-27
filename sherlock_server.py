import cv2
import faiss
import pickle
import numpy as np
import sys
import os
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent))

from mcp.server.fastmcp import FastMCP
from insightface.app import FaceAnalysis
from langchain_community.tools import DuckDuckGoSearchRun
from config.settings import (
    FACE_MODEL,
    VECTOR_DIMENSION,
    MATCH_THRESHOLD,
    FAISS_INDEX_PATH,
    METADATA_PATH,
    LOGS_DIR
)

# ─────────────────────────────────────────
# INITIALIZE FASTMCP SERVER
# ─────────────────────────────────────────
mcp = FastMCP("Ironclad_Intelligence_Engine")

# ─────────────────────────────────────────
# LOAD VISION MODELS
# ─────────────────────────────────────────
print("[Ironclad] Loading InsightFace Vision Model...")
face_app = FaceAnalysis(
    name=FACE_MODEL,
    providers=['CPUExecutionProvider']
)
face_app.prepare(ctx_id=0, det_size=(640, 640))
print("[Ironclad] Vision Model Ready ✅")

# ─────────────────────────────────────────
# LOAD FAISS VECTOR DATABASE
# ─────────────────────────────────────────
def load_database():
    if not os.path.exists(FAISS_INDEX_PATH):
        print("[Ironclad] WARNING: No FAISS index found. Run init_db.py first.")
        return None, {}

    index = faiss.read_index(FAISS_INDEX_PATH)
    with open(METADATA_PATH, "rb") as f:
        metadata_store = pickle.load(f)

    print(f"[Ironclad] Database Loaded: {index.ntotal} identities indexed ✅")
    return index, metadata_store

index, metadata_store = load_database()

# ─────────────────────────────────────────
# LOGGING HELPER
# ─────────────────────────────────────────
def log_event(message: str):
    os.makedirs(LOGS_DIR, exist_ok=True)
    log_path = os.path.join(LOGS_DIR, "server_log.txt")
    with open(log_path, "a") as f:
        f.write(f"\n[LOG] {message}")
    print(f"[Ironclad LOG] {message}")

# ─────────────────────────────────────────
# TOOL A: FACE MATCHING ENGINE
# ─────────────────────────────────────────
@mcp.tool()
def match_face_by_image(image_path: str) -> str:
    """
    Scans the uploaded image using ArcFace biometric AI.
    Detects and aligns the face using RetinaFace.
    Generates a 512-dimension vector embedding.
    Searches the FAISS HNSW index for the closest match.
    Returns identity metadata if a confident match is found.
    """
    log_event(f"Face match requested for: {image_path}")

    # Validate image path
    if not os.path.exists(image_path):
        return f"ERROR: Image file not found at path: {image_path}"

    # Load image
    img = cv2.imread(image_path)
    if img is None:
        return "ERROR: Could not read image. File may be corrupted or unsupported format."

    # Detect faces
    faces = face_app.get(img)
    if not faces:
        return "ERROR: No human face detected in the image. Please use a clear frontal face photo."

    if len(faces) > 1:
        log_event(f"Multiple faces detected ({len(faces)}). Using the largest face.")

    # Use the largest detected face
    largest_face = max(faces, key=lambda f: (f.bbox[2] - f.bbox[0]) * (f.bbox[3] - f.bbox[1]))

    # Generate 512-D embedding
    query_vector = largest_face.embedding.reshape(1, -1).astype('float32')
    faiss.normalize_L2(query_vector)

    # Check if database is loaded
    if index is None or index.ntotal == 0:
        return "ERROR: Face database is empty. Please run init_db.py to populate the database first."

    # Search HNSW index
    distances, indices = index.search(query_vector, k=3)

    match_idx        = indices[0][0]
    confidence_score = float(distances[0][0])

    log_event(f"Match result - Index: {match_idx} | Confidence: {confidence_score:.4f}")

    # Apply threshold
    if match_idx in metadata_store and confidence_score > MATCH_THRESHOLD:
        match_data = metadata_store[match_idx]
        result = (
            f"MATCH CONFIRMED ✅\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"Name            : {match_data['name']}\n"
            f"Base Details    : {match_data['base_details']}\n"
            f"Confidence Score: {confidence_score:.4f} ({confidence_score*100:.1f}%)\n"
            f"Vector Distance : {confidence_score:.6f}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        )
        log_event(f"MATCH FOUND: {match_data['name']}")
        return result

    return (
        f"NO MATCH FOUND ❌\n"
        f"Best similarity score was {confidence_score:.4f} "
        f"which is below threshold {MATCH_THRESHOLD}.\n"
        f"The person is not in the local database."
    )


# ─────────────────────────────────────────
# TOOL B: WEB OSINT ENGINE
# ─────────────────────────────────────────
@mcp.tool()
def search_web_osint(name: str) -> str:
    """
    Performs live OSINT web intelligence gathering on a target name.
    Queries DuckDuckGo search engine for publicly available information.
    Returns scraped text data including professional background,
    social profiles, news mentions, and biography details.
    """
    log_event(f"OSINT search initiated for: {name}")

    if not name or name.strip() == "":
        return "ERROR: No name provided for OSINT search."

    search = DuckDuckGoSearchRun()

    results_collection = []

    # Query 1: Professional Background
    try:
        q1 = search.run(f"{name} professional background career biography")
        results_collection.append(f"📌 Professional Background:\n{q1}")
    except Exception as e:
        results_collection.append(f"📌 Professional Background: Search failed - {str(e)}")

    # Query 2: Social Media & Online Presence
    try:
        q2 = search.run(f"{name} LinkedIn Twitter social media profile")
        results_collection.append(f"📌 Social Media & Online Presence:\n{q2}")
    except Exception as e:
        results_collection.append(f"📌 Social Media: Search failed - {str(e)}")

    # Query 3: News & Mentions
    try:
        q3 = search.run(f"{name} news articles mentions recent")
        results_collection.append(f"📌 News & Public Mentions:\n{q3}")
    except Exception as e:
        results_collection.append(f"📌 News Mentions: Search failed - {str(e)}")

    # Combine all results
    full_report = f"\n🔍 OSINT Intelligence Report for: {name}\n"
    full_report += "━" * 50 + "\n"
    full_report += "\n\n".join(results_collection)
    full_report += "\n" + "━" * 50

    log_event(f"OSINT complete for: {name}")
    return full_report


# ─────────────────────────────────────────
# TOOL C: DATABASE STATUS CHECKER
# ─────────────────────────────────────────
@mcp.tool()
def check_database_status() -> str:
    """
    Returns the current status of the FAISS vector database.
    Shows how many identities are indexed and system health.
    """
    if index is None:
        return "DATABASE STATUS: ❌ Not initialized. Run init_db.py first."

    status = (
        f"DATABASE STATUS ✅\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"Total Identities Indexed : {index.ntotal}\n"
        f"Vector Dimensions        : {VECTOR_DIMENSION}\n"
        f"Match Threshold          : {MATCH_THRESHOLD}\n"
        f"Index File               : {FAISS_INDEX_PATH}\n"
        f"Metadata File            : {METADATA_PATH}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    )
    return status


# ─────────────────────────────────────────
# START MCP SERVER
# ─────────────────────────────────────────
if __name__ == "__main__":
    print("[Ironclad] Starting MCP Server Engine...")
    mcp.run(transport="stdio")

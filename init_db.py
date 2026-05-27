import os
import cv2
import sys
import faiss
import numpy as np
import pickle
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent))

from insightface.app import FaceAnalysis
from config.settings import (
    FACE_MODEL,
    VECTOR_DIMENSION,
    FAISS_INDEX_PATH,
    METADATA_PATH,
    PROFILES_DIR,
    DATA_DIR
)

print("=" * 60)
print("  🛡️  IRONCLAD - Database Initializer")
print("=" * 60)

# ─────────────────────────────────────────
# INITIALIZE FACE AI MODEL
# ─────────────────────────────────────────
print("\n[1/4] Loading InsightFace AI Model...")
face_app = FaceAnalysis(
    name=FACE_MODEL,
    providers=['CPUExecutionProvider']
)
face_app.prepare(ctx_id=0, det_size=(640, 640))
print("      ✅ ArcFace Model Loaded Successfully")

# ─────────────────────────────────────────
# INITIALIZE FAISS VECTOR DATABASE
# ─────────────────────────────────────────
print("\n[2/4] Initializing FAISS HNSW Vector Index...")
os.makedirs(DATA_DIR, exist_ok=True)

# Check if existing index exists
if os.path.exists(FAISS_INDEX_PATH) and os.path.getsize(FAISS_INDEX_PATH) > 0:
    print("      📂 Existing index found. Loading...")
    index = faiss.read_index(FAISS_INDEX_PATH)
    with open(METADATA_PATH, "rb") as f:
        metadata_store = pickle.load(f)
    print(f"      ✅ Loaded existing index with {index.ntotal} entries")
else:
    print("      🆕 Creating fresh HNSW index...")
    # HNSW Index - Ultra fast approximate nearest neighbor
    index = faiss.IndexHNSWFlat(VECTOR_DIMENSION, 32)
    metadata_store = {}
    print("      ✅ Fresh HNSW Index Created")

# ─────────────────────────────────────────
# CORE FUNCTION: ADD PERSON TO DATABASE
# ─────────────────────────────────────────
def add_person_to_db(image_path: str, name: str, details: str) -> bool:
    """
    Add a person's face to the vector database.

    Args:
        image_path : Path to the person's clear face image
        name       : Full name of the person
        details    : Background details / description

    Returns:
        bool: True if successfully added, False otherwise
    """
    print(f"\n  ➤ Processing: {name}")
    print(f"    Image: {image_path}")

    # Validate image exists
    if not os.path.exists(image_path):
        print(f"    ❌ SKIP: Image not found at {image_path}")
        return False

    # Read image
    img = cv2.imread(image_path)
    if img is None:
        print(f"    ❌ SKIP: Cannot read image file")
        return False

    # Detect faces with InsightFace
    faces = face_app.get(img)
    if not faces:
        print(f"    ❌ SKIP: No face detected in image")
        return False

    if len(faces) > 1:
        print(f"    ⚠️  Multiple faces ({len(faces)}) detected. Using largest.")

    # Use largest face
    target_face = max(
        faces,
        key=lambda f: (f.bbox[2] - f.bbox[0]) * (f.bbox[3] - f.bbox[1])
    )

    # Generate 512-D ArcFace embedding
    embedding = target_face.embedding.reshape(1, -1).astype('float32')
    faiss.normalize_L2(embedding)  # Normalize for cosine similarity

    # Add to FAISS index
    current_idx = index.ntotal
    index.add(embedding)

    # Store metadata
    metadata_store[current_idx] = {
        "name"        : name,
        "base_details": details,
        "image_path"  : image_path,
        "index_id"    : current_idx
    }

    print(f"    ✅ SUCCESS: {name} added at index [{current_idx}]")
    return True


# ─────────────────────────────────────────
# SAVE DATABASE FUNCTION
# ─────────────────────────────────────────
def save_database():
    """Save the FAISS index and metadata to disk."""
    faiss.write_index(index, FAISS_INDEX_PATH)
    with open(METADATA_PATH, "wb") as f:
        pickle.dump(metadata_store, f)
    print(f"\n[4/4] Database Saved:")
    print(f"      📁 Index    : {FAISS_INDEX_PATH}")
    print(f"      📁 Metadata : {METADATA_PATH}")
    print(f"      👥 Total Identities: {index.ntotal}")


# ─────────────────────────────────────────
# REMOVE PERSON FROM DATABASE
# ─────────────────────────────────────────
def remove_person(name: str) -> bool:
    """Remove a person from metadata (Note: FAISS does not support deletion natively)."""
    for idx, data in list(metadata_store.items()):
        if data["name"].lower() == name.lower():
            del metadata_store[idx]
            print(f"✅ Removed {name} from metadata store")
            return True
    print(f"❌ Person '{name}' not found in database")
    return False


# ─────────────────────────────────────────
# LIST ALL PEOPLE IN DATABASE
# ─────────────────────────────────────────
def list_all_people():
    """Print all indexed identities."""
    print("\n📋 Current Database Contents:")
    print("━" * 50)
    if not metadata_store:
        print("  (Empty - No identities indexed yet)")
    for idx, data in metadata_store.items():
        print(f"  [{idx}] {data['name']} - {data['base_details']}")
    print("━" * 50)
    print(f"  Total: {len(metadata_store)} identities")


# ─────────────────────────────────────────
# MAIN SEEDING SCRIPT
# ─────────────────────────────────────────
if __name__ == "__main__":
    print("\n[3/4] Seeding Database with Profile Data...")
    os.makedirs(PROFILES_DIR, exist_ok=True)

    # ──────────────────────────────────────
    # ADD YOUR PEOPLE HERE
    # Format: add_person_to_db("path/to/image.jpg", "Full Name", "Details")
    # ──────────────────────────────────────

    people_to_add = [
        {
            "image_path": os.path.join(PROFILES_DIR, "john_doe.jpg"),
            "name"      : "John Doe",
            "details"   : "Lead Security Architect at CyberCorp. Known aliases: JD, J.Doe"
        },
        {
            "image_path": os.path.join(PROFILES_DIR, "jane_smith.jpg"),
            "name"      : "Jane Smith",
            "details"   : "Data Scientist at TechLabs. PhD Computer Vision, MIT 2019"
        },
        # Add more people below:
        # {
        #     "image_path": os.path.join(PROFILES_DIR, "your_file.jpg"),
        #     "name"      : "Person Name",
        #     "details"   : "Their background details"
        # },
    ]

    success_count = 0
    skip_count    = 0

    for person in people_to_add:
        result = add_person_to_db(
            person["image_path"],
            person["name"],
            person["details"]
        )
        if result:
            success_count += 1
        else:
            skip_count += 1

    # Show results
    list_all_people()

    # Save to disk
    save_database()

    print("\n" + "=" * 60)
    print(f"  ✅ Done! Added: {success_count} | Skipped: {skip_count}")
    print("  🚀 Database is ready. Run: streamlit run app.py")
    print("=" * 60 + "\n")

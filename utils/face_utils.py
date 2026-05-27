

# ─────────────────────────────────────────
# GET FACE LANDMARKS
# ─────────────────────────────────────────
def get_face_landmarks(face_app, image_path: str) -> dict:
    """
    Extract facial landmark points from an image.
    Returns eye, nose, and mouth coordinates.
    """
    img   = cv2.imread(image_path)
    faces = face_app.get(img)

    if not faces:
        return {}

    face = faces[0]
    return {
        "landmarks": face.kps.tolist() if face.kps is not None else [],
        "bbox"     : face.bbox.tolist(),
        "det_score": float(face.det_score)
    }


# ─────────────────────────────────────────
# ESTIMATE AGE AND GENDER
# ─────────────────────────────────────────
def estimate_demographics(face_app, image_path: str) -> dict:
    """
    Estimate age and gender from face image.
    Uses InsightFace demographic analysis.
    """
    img   = cv2.imread(image_path)
    faces = face_app.get(img)

    if not faces:
        return {}

    face = faces[0]
    return {
        "age"   : int(face.age) if hasattr(face, 'age') else None,
        "gender": "Male" if face.gender == 1 else "Female"
        if hasattr(face, 'gender') else None
    }

import streamlit as st
import asyncio
import os
import sys
from pathlib import Path
from datetime import datetime

# Add project root to path
sys.path.append(str(Path(__file__).parent))

from config.settings import (
    OLLAMA_MODEL,
    TEMP_DIR,
    LOGS_DIR
)

# ─────────────────────────────────────────
# PAGE CONFIGURATION
# ─────────────────────────────────────────
st.set_page_config(
    layout="wide",
    page_title="🛡️ Ironclad - Face Detective",
    page_icon="🛡️",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────
with st.sidebar:
    st.title("🛡️ Ironclad")
    st.markdown("---")
    st.markdown("### ⚙️ Settings")
    match_threshold = st.slider(
        "🎯 Match Confidence Threshold",
        min_value=0.1,
        max_value=1.0,
        value=0.4,
        step=0.05
    )
    st.markdown("---")
    st.markdown("### 📊 System Status")
    try:
        import faiss
        st.success("✅ FAISS Vector DB")
    except:
        st.error("❌ FAISS Not Found")
    try:
        import insightface
        st.success("✅ InsightFace AI")
    except:
        st.error("❌ InsightFace Not Found")
    try:
        from duckduckgo_search import DDGS
        st.success("✅ OSINT Engine")
    except:
        st.error("❌ OSINT Engine")
    st.markdown("---")
    st.markdown("**🛡️ Ironclad v2.0.0**")
    st.markdown("*Deep Investigation Engine*")

# ─────────────────────────────────────────
# MAIN TITLE
# ─────────────────────────────────────────
st.markdown("""
    <div style='text-align: center; padding: 20px;'>
        <h1>🛡️ Project Ironclad</h1>
        <h3>Deep Face Investigation & OSINT Engine</h3>
        <p>Upload → Detect → Identify → Full Intelligence Report</p>
    </div>
""", unsafe_allow_html=True)
st.markdown("---")


# ─────────────────────────────────────────
# DEEP OSINT SEARCH ENGINE
# ─────────────────────────────────────────
def deep_osint_search(name: str) -> dict:
    """
    Perform comprehensive OSINT search on a person.
    Returns detailed intelligence from multiple sources.
    """
    from duckduckgo_search import DDGS

    results = {
        "social_media"      : {},
        "professional"      : {},
        "news"              : {},
        "images"            : {},
        "websites"          : {},
        "contact"           : {},
        "location"          : {},
        "other"             : {}
    }

    ddgs = DDGS()

    # ── 1. LinkedIn Profile ──
    try:
        r = list(ddgs.text(
            f"{name} site:linkedin.com",
            max_results=3
        ))
        if r:
            results["social_media"]["LinkedIn"] = r
    except Exception as e:
        results["social_media"]["LinkedIn"] = [{"error": str(e)}]

    # ── 2. Twitter / X Profile ──
    try:
        r = list(ddgs.text(
            f"{name} site:twitter.com OR site:x.com",
            max_results=3
        ))
        if r:
            results["social_media"]["Twitter/X"] = r
    except Exception as e:
        results["social_media"]["Twitter/X"] = [{"error": str(e)}]

    # ── 3. Facebook Profile ──
    try:
        r = list(ddgs.text(
            f"{name} site:facebook.com",
            max_results=3
        ))
        if r:
            results["social_media"]["Facebook"] = r
    except Exception as e:
        results["social_media"]["Facebook"] = [{"error": str(e)}]

    # ── 4. Instagram Profile ──
    try:
        r = list(ddgs.text(
            f"{name} site:instagram.com",
            max_results=3
        ))
        if r:
            results["social_media"]["Instagram"] = r
    except Exception as e:
        results["social_media"]["Instagram"] = [{"error": str(e)}]

    # ── 5. GitHub Profile ──
    try:
        r = list(ddgs.text(
            f"{name} site:github.com",
            max_results=3
        ))
        if r:
            results["social_media"]["GitHub"] = r
    except Exception as e:
        results["social_media"]["GitHub"] = [{"error": str(e)}]

    # ── 6. YouTube Profile ──
    try:
        r = list(ddgs.text(
            f"{name} site:youtube.com",
            max_results=2
        ))
        if r:
            results["social_media"]["YouTube"] = r
    except Exception as e:
        results["social_media"]["YouTube"] = [{"error": str(e)}]

    # ── 7. Reddit Profile ──
    try:
        r = list(ddgs.text(
            f"{name} site:reddit.com",
            max_results=2
        ))
        if r:
            results["social_media"]["Reddit"] = r
    except Exception as e:
        results["social_media"]["Reddit"] = [{"error": str(e)}]

    # ── 8. Professional Background ──
    try:
        r = list(ddgs.text(
            f"{name} professional career job title company",
            max_results=5
        ))
        results["professional"]["career"] = r
    except Exception as e:
        results["professional"]["career"] = [{"error": str(e)}]

    # ── 9. Education Background ──
    try:
        r = list(ddgs.text(
            f"{name} education university college degree",
            max_results=3
        ))
        results["professional"]["education"] = r
    except Exception as e:
        results["professional"]["education"] = [{"error": str(e)}]

    # ── 10. News Articles ──
    try:
        r = list(ddgs.text(
            f"{name} news article interview",
            max_results=5
        ))
        results["news"]["articles"] = r
    except Exception as e:
        results["news"]["articles"] = [{"error": str(e)}]

    # ── 11. Image Search - Where Photos Appear ──
    try:
        r = list(ddgs.images(
            f"{name} person photo",
            max_results=5
        ))
        results["images"]["photo_sources"] = r
    except Exception as e:
        results["images"]["photo_sources"] = [{"error": str(e)}]

    # ── 12. Personal Website ──
    try:
        r = list(ddgs.text(
            f"{name} personal website blog portfolio",
            max_results=3
        ))
        results["websites"]["personal"] = r
    except Exception as e:
        results["websites"]["personal"] = [{"error": str(e)}]

    # ── 13. Email / Contact Info ──
    try:
        r = list(ddgs.text(
            f"{name} email contact information",
            max_results=3
        ))
        results["contact"]["email_info"] = r
    except Exception as e:
        results["contact"]["email_info"] = [{"error": str(e)}]

    # ── 14. Location / Address ──
    try:
        r = list(ddgs.text(
            f"{name} location city country lives",
            max_results=3
        ))
        results["location"]["places"] = r
    except Exception as e:
        results["location"]["places"] = [{"error": str(e)}]

    # ── 15. Research Papers / Publications ──
    try:
        r = list(ddgs.text(
            f"{name} research paper publication author",
            max_results=3
        ))
        results["other"]["publications"] = r
    except Exception as e:
        results["other"]["publications"] = [{"error": str(e)}]

    # ── 16. General Web Presence ──
    try:
        r = list(ddgs.text(
            f'"{name}"',
            max_results=8
        ))
        results["websites"]["general_presence"] = r
    except Exception as e:
        results["websites"]["general_presence"] = [{"error": str(e)}]

    return results


# ─────────────────────────────────────────
# REVERSE IMAGE SEARCH
# ─────────────────────────────────────────
def reverse_image_search(image_path: str, name: str = "") -> list:
    """
    Search for where the image appears online.
    Uses DuckDuckGo image search with name as context.
    """
    from duckduckgo_search import DDGS
    ddgs    = DDGS()
    results = []

    try:
        # Search for person images across web
        search_queries = [
            f"{name} face photo profile picture",
            f"{name} image picture online",
            f"{name} photo appearance"
        ]

        for query in search_queries:
            r = list(ddgs.images(query, max_results=3))
            results.extend(r)

    except Exception as e:
        results.append({"error": str(e)})

    return results


# ─────────────────────────────────────────
# FORMAT DEEP REPORT
# ─────────────────────────────────────────
def format_deep_report(
    name          : str,
    details       : str,
    confidence    : float,
    osint_data    : dict,
    image_results : list
) -> str:
    """Format all gathered intelligence into a structured report."""

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conf_pct  = confidence * 100

    # Risk level
    if confidence >= 0.9:
        risk = "🔴 HIGH"
    elif confidence >= 0.7:
        risk = "🟠 MEDIUM-HIGH"
    elif confidence >= 0.5:
        risk = "🟡 MEDIUM"
    else:
        risk = "🟢 LOW"

    lines = []

    # ── HEADER ──
    lines.append("# 🛡️ IRONCLAD DEEP INVESTIGATION DOSSIER")
    lines.append("---")
    lines.append(f"**🕐 Generated:** {timestamp}")
    lines.append(f"**🔒 Classification:** CONFIDENTIAL")
    lines.append(f"**⚙️ Engine:** Ironclad v2.0.0 Deep OSINT")
    lines.append("")

    # ── IDENTITY ──
    lines.append("---")
    lines.append("## 👤 IDENTITY PROFILE")
    lines.append("")
    lines.append(f"| Field | Value |")
    lines.append(f"|-------|-------|")
    lines.append(f"| **Full Name** | {name} |")
    lines.append(f"| **Known Details** | {details} |")
    lines.append(f"| **Match Confidence** | {conf_pct:.1f}% |")
    lines.append(f"| **Risk Level** | {risk} |")
    lines.append(f"| **Report Time** | {timestamp} |")
    lines.append("")

    # ── SOCIAL MEDIA ──
    lines.append("---")
    lines.append("## 📱 SOCIAL MEDIA PROFILES")
    lines.append("")

    social = osint_data.get("social_media", {})
    if social:
        for platform, data in social.items():
            if data and not (len(data) == 1 and "error" in data[0]):
                lines.append(f"### 🔗 {platform}")
                for item in data[:3]:
                    if isinstance(item, dict):
                        title = item.get('title', 'No Title')
                        url   = item.get('href', item.get('url', 'No URL'))
                        body  = item.get('body', '')
                        lines.append(f"- **[{title}]({url})**")
                        if body:
                            lines.append(f"  > {body[:200]}...")
                lines.append("")
    else:
        lines.append("*No social media profiles found.*")
    lines.append("")

    # ── PROFESSIONAL ──
    lines.append("---")
    lines.append("## 💼 PROFESSIONAL BACKGROUND")
    lines.append("")

    prof = osint_data.get("professional", {})

    # Career
    career = prof.get("career", [])
    if career:
        lines.append("### 🏢 Career & Employment")
        for item in career[:5]:
            if isinstance(item, dict) and "error" not in item:
                title = item.get('title', '')
                url   = item.get('href', '')
                body  = item.get('body', '')
                lines.append(f"- **[{title}]({url})**")
                if body:
                    lines.append(f"  > {body[:250]}")
        lines.append("")

    # Education
    edu = prof.get("education", [])
    if edu:
        lines.append("### 🎓 Education & Academic Background")
        for item in edu[:3]:
            if isinstance(item, dict) and "error" not in item:
                title = item.get('title', '')
                url   = item.get('href', '')
                body  = item.get('body', '')
                lines.append(f"- **[{title}]({url})**")
                if body:
                    lines.append(f"  > {body[:200]}")
        lines.append("")

    # ── NEWS ──
    lines.append("---")
    lines.append("## 📰 NEWS & MEDIA MENTIONS")
    lines.append("")

    news = osint_data.get("news", {}).get("articles", [])
    if news:
        for item in news[:5]:
            if isinstance(item, dict) and "error" not in item:
                title = item.get('title', '')
                url   = item.get('href', '')
                body  = item.get('body', '')
                lines.append(f"- **[{title}]({url})**")
                if body:
                    lines.append(f"  > {body[:250]}")
        lines.append("")
    else:
        lines.append("*No news articles found.*")
        lines.append("")

    # ── IMAGE SOURCES ──
    lines.append("---")
    lines.append("## 🖼️ WHERE PHOTOS APPEAR ONLINE")
    lines.append("")

    img_sources = osint_data.get("images", {}).get("photo_sources", [])
    all_images  = img_sources + image_results

    if all_images:
        lines.append("| # | Source Website | Image URL | Title |")
        lines.append("|---|---------------|-----------|-------|")
        seen = set()
        count = 1
        for item in all_images[:10]:
            if isinstance(item, dict) and "error" not in item:
                img_url = item.get(
                    'image', item.get('src', item.get('url', ''))
                )
                source  = item.get(
                    'url', item.get('href', item.get('source', ''))
                )
                title   = item.get('title', 'Photo')

                # Extract domain
                try:
                    from urllib.parse import urlparse
                    domain = urlparse(source).netloc
                except:
                    domain = source[:30]

                if source not in seen and source:
                    seen.add(source)
                    lines.append(
                        f"| {count} | `{domain}` | "
                        f"[View Image]({img_url}) | {title[:50]} |"
                    )
                    count += 1
        lines.append("")
    else:
        lines.append("*No image sources found online.*")
        lines.append("")

    # ── WEBSITES ──
    lines.append("---")
    lines.append("## 🌐 WEB PRESENCE & WEBSITES")
    lines.append("")

    # Personal website
    personal = osint_data.get("websites", {}).get("personal", [])
    if personal:
        lines.append("### 🏠 Personal Websites & Portfolios")
        for item in personal[:3]:
            if isinstance(item, dict) and "error" not in item:
                title = item.get('title', '')
                url   = item.get('href', '')
                body  = item.get('body', '')
                lines.append(f"- **[{title}]({url})**")
                if body:
                    lines.append(f"  > {body[:200]}")
        lines.append("")

    # General presence
    general = osint_data.get("websites", {}).get("general_presence", [])
    if general:
        lines.append("### 🔍 General Web Mentions")
        lines.append("")
        lines.append("| Website | Title | Description |")
        lines.append("|---------|-------|-------------|")
        for item in general[:8]:
            if isinstance(item, dict) and "error" not in item:
                title  = item.get('title', '')[:50]
                url    = item.get('href', '')
                body   = item.get('body', '')[:100]
                try:
                    from urllib.parse import urlparse
                    domain = urlparse(url).netloc
                except:
                    domain = url[:30]
                lines.append(f"| `{domain}` | [{title}]({url}) | {body} |")
        lines.append("")

    # ── CONTACT INFO ──
    lines.append("---")
    lines.append("## 📧 CONTACT & LOCATION INTELLIGENCE")
    lines.append("")

    contact = osint_data.get("contact", {}).get("email_info", [])
    if contact:
        lines.append("### 📬 Contact Information Found")
        for item in contact[:3]:
            if isinstance(item, dict) and "error" not in item:
                title = item.get('title', '')
                url   = item.get('href', '')
                body  = item.get('body', '')
                lines.append(f"- **[{title}]({url})**")
                if body:
                    lines.append(f"  > {body[:200]}")
        lines.append("")

    location = osint_data.get("location", {}).get("places", [])
    if location:
        lines.append("### 📍 Location Information")
        for item in location[:3]:
            if isinstance(item, dict) and "error" not in item:
                title = item.get('title', '')
                url   = item.get('href', '')
                body  = item.get('body', '')
                lines.append(f"- **[{title}]({url})**")
                if body:
                    lines.append(f"  > {body[:200]}")
        lines.append("")

    # ── PUBLICATIONS ──
    pubs = osint_data.get("other", {}).get("publications", [])
    if pubs:
        lines.append("---")
        lines.append("## 📚 PUBLICATIONS & RESEARCH")
        lines.append("")
        for item in pubs[:3]:
            if isinstance(item, dict) and "error" not in item:
                title = item.get('title', '')
                url   = item.get('href', '')
                body  = item.get('body', '')
                lines.append(f"- **[{title}]({url})**")
                if body:
                    lines.append(f"  > {body[:200]}")
        lines.append("")

    # ── RISK ASSESSMENT ──
    lines.append("---")
    lines.append("## ⚠️ RISK ASSESSMENT")
    lines.append("")
    lines.append("| Category | Assessment |")
    lines.append("|----------|------------|")
    lines.append(f"| **Match Confidence** | {conf_pct:.1f}% |")
    lines.append(f"| **Risk Level** | {risk} |")

    social_count = sum(
        1 for v in social.values()
        if v and not (len(v) == 1 and "error" in v[0])
    )
    lines.append(f"| **Social Media Platforms Found** | {social_count} |")
    lines.append(
        f"| **Web Pages Mentioning Person** | "
        f"{len(general)} pages |"
    )
    lines.append(
        f"| **Image Sources Found** | "
        f"{len(all_images)} sources |"
    )
    lines.append(
        f"| **Data Reliability** | "
        f"{'High' if confidence > 0.8 else 'Medium' if confidence > 0.5 else 'Low'} |"
    )
    lines.append("")

    # ── SUMMARY ──
    lines.append("---")
    lines.append("## 📝 INVESTIGATION SUMMARY")
    lines.append("")
    lines.append(
        f"Target **{name}** was identified with **{conf_pct:.1f}%** "
        f"confidence using ArcFace biometric analysis."
    )
    lines.append("")
    lines.append("**Key Findings:**")

    if social_count > 0:
        platforms = [
            p for p, v in social.items()
            if v and not (len(v) == 1 and "error" in v[0])
        ]
        lines.append(
            f"- 📱 Found on **{social_count}** social media platforms: "
            f"{', '.join(platforms)}"
        )

    if len(general) > 0:
        lines.append(
            f"- 🌐 Found on **{len(general)}** websites across the internet"
        )

    if len(all_images) > 0:
        lines.append(
            f"- 🖼️ Photos found on **{len(all_images)}** online sources"
        )

    if career:
        lines.append(f"- 💼 Professional career information retrieved")

    if news:
        lines.append(f"- 📰 Found in **{len(news)}** news articles")

    lines.append("")
    lines.append("---")
    lines.append(
        "*🛡️ Ironclad v2.0.0 | Deep OSINT Engine | "
        "100% Local | Zero Cost | For Authorized Use Only*"
    )

    return "\n".join(lines)


# ─────────────────────────────────────────
# MAIN INVESTIGATION FUNCTION
# ─────────────────────────────────────────
def run_deep_investigation(img_path: str, threshold: float) -> str:
    """
    Complete deep investigation pipeline:
    1. Face Detection & Biometric Analysis
    2. Database Match
    3. Deep OSINT Search (15+ queries)
    4. Reverse Image Search
    5. Full Structured Report
    """
    import cv2
    import faiss
    import pickle
    import numpy as np
    from insightface.app import FaceAnalysis
    from config.settings import (
        FACE_MODEL,
        FAISS_INDEX_PATH,
        METADATA_PATH
    )

    identified_name    = None
    identified_details = ""
    confidence_score   = 0.0

    # ────────────────────────────────────
    # PHASE 1: FACE DETECTION
    # ────────────────────────────────────
    with st.status("🔬 Phase 1: Biometric Face Analysis...", expanded=True) as status:
        try:
            st.write("Loading ArcFace AI Model...")
            face_app = FaceAnalysis(
                name=FACE_MODEL,
                providers=['CPUExecutionProvider']
            )
            face_app.prepare(ctx_id=0, det_size=(640, 640))
            st.write("✅ ArcFace Model Loaded")

            st.write("Analyzing facial biometrics...")
            img   = cv2.imread(img_path)
            faces = face_app.get(img)

            if not faces:
                status.update(
                    label="❌ No face detected",
                    state="error"
                )
                return "❌ No face detected in image. Please use a clear frontal face photo."

            st.write(f"✅ Detected {len(faces)} face(s) in image")

            # Get largest face
            target_face  = max(
                faces,
                key=lambda f: (
                    f.bbox[2] - f.bbox[0]
                ) * (f.bbox[3] - f.bbox[1])
            )
            query_vector = target_face.embedding.reshape(
                1, -1
            ).astype('float32')
            faiss.normalize_L2(query_vector)
            st.write("✅ 512-D ArcFace embedding generated")

            # ── Database Search ──
            if os.path.exists(FAISS_INDEX_PATH) and \
               os.path.getsize(FAISS_INDEX_PATH) > 0:

                st.write("Searching FAISS vector database...")
                index = faiss.read_index(FAISS_INDEX_PATH)

                with open(METADATA_PATH, "rb") as f:
                    metadata_store = pickle.load(f)

                if index.ntotal > 0:
                    distances, indices = index.search(query_vector, k=3)
                    match_idx          = indices[0][0]
                    confidence_score   = float(distances[0][0])

                    if match_idx in metadata_store and \
                       confidence_score > threshold:
                        match              = metadata_store[match_idx]
                        identified_name    = match['name']
                        identified_details = match['base_details']
                        st.write(
                            f"✅ MATCH: **{identified_name}** "
                            f"({confidence_score*100:.1f}% confidence)"
                        )
                    else:
                        st.write(
                            f"⚠️ No confident match. "
                            f"Best score: {confidence_score:.4f}"
                        )
                else:
                    st.write("⚠️ Database is empty")
            else:
                st.write("⚠️ No database found. Add faces via init_db.py")

            status.update(label="✅ Phase 1 Complete", state="complete")

        except Exception as e:
            status.update(label=f"❌ Error: {str(e)}", state="error")
            return f"❌ Face analysis failed: {str(e)}"

    # ────────────────────────────────────
    # PHASE 2: DEEP OSINT
    # ────────────────────────────────────
    if not identified_name:
        st.warning(
            "⚠️ No match in local DB. "
            "Enter name manually for OSINT search."
        )
        identified_name    = st.text_input(
            "Enter person's name for OSINT search:",
            placeholder="e.g. John Doe"
        )
        identified_details = "Manually entered for OSINT"
        confidence_score   = 0.0

        if not identified_name:
            return "⚠️ Please enter a name to continue investigation."

    osint_data    = {}
    image_results = []

    with st.status(
        "🌐 Phase 2: Deep OSINT Intelligence Gathering...",
        expanded=True
    ) as status:
        try:
            st.write(f"Gathering intelligence on: **{identified_name}**")

            st.write("🔍 Searching LinkedIn...")
            st.write("🔍 Searching Twitter/X...")
            st.write("🔍 Searching Facebook...")
            st.write("🔍 Searching Instagram...")
            st.write("🔍 Searching GitHub...")
            st.write("🔍 Searching News Sources...")
            st.write("🔍 Searching Image Databases...")
            st.write("🔍 Searching Professional Records...")
            st.write("🔍 Searching Location Data...")

            osint_data = deep_osint_search(identified_name)
            st.write("✅ OSINT Data Collected")

            st.write("🖼️ Running Reverse Image Search...")
            image_results = reverse_image_search(
                img_path,
                identified_name
            )
            st.write(
                f"✅ Found {len(image_results)} image sources online"
            )

            status.update(
                label="✅ Phase 2 Complete - OSINT Gathered",
                state="complete"
            )

        except Exception as e:
            status.update(
                label=f"⚠️ OSINT Partial: {str(e)}",
                state="complete"
            )

    # ────────────────────────────────────
    # PHASE 3: GENERATE REPORT
    # ────────────────────────────────────
    with st.status(
        "📋 Phase 3: Generating Deep Dossier Report...",
        expanded=True
    ) as status:
        report = format_deep_report(
            name          = identified_name,
            details       = identified_details,
            confidence    = confidence_score,
            osint_data    = osint_data,
            image_results = image_results
        )
        status.update(
            label="✅ Phase 3 Complete - Report Ready",
            state="complete"
        )

    return report


# ─────────────────────────────────────────
# MAIN LAYOUT
# ─────────────────────────────────────────
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### 📸 Upload Target Image")
    uploaded_file = st.file_uploader(
        "Drop target image here",
        type=["jpg", "png", "jpeg"],
        help="Upload a clear frontal face image"
    )

    if uploaded_file is not None:
        st.image(
            uploaded_file,
            caption="🎯 Target Loaded",
            use_column_width=True
        )
        st.success(f"✅ {uploaded_file.name}")
        st.info(f"📦 {uploaded_file.size / 1024:.1f} KB")

    st.markdown("---")
    st.markdown("### 🔎 OR Search By Name Only")
    name_only = st.text_input(
        "Enter name directly:",
        placeholder="e.g. Elon Musk"
    )

    if st.button(
        "🔍 Search By Name",
        use_container_width=True
    ):
        if name_only:
            with col2:
                st.markdown(f"### 🔍 Investigating: {name_only}")
                with st.spinner("Running deep OSINT search..."):
                    osint_data    = deep_osint_search(name_only)
                    image_results = reverse_image_search("", name_only)
                    report        = format_deep_report(
                        name          = name_only,
                        details       = "Direct name search",
                        confidence    = 1.0,
                        osint_data    = osint_data,
                        image_results = image_results
                    )

                st.markdown("---")
                st.markdown("### 📋 Deep Investigation Report")
                st.markdown(report)

                # Save & Download
                os.makedirs(LOGS_DIR, exist_ok=True)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                log_file  = os.path.join(
                    LOGS_DIR, f"report_{timestamp}.md"
                )
                with open(log_file, "w") as lf:
                    lf.write(report)

                st.download_button(
                    label     = "📥 Download Report",
                    data      = report,
                    file_name = f"ironclad_{name_only}_{timestamp}.md",
                    mime      = "text/markdown"
                )

with col2:
    st.markdown("### 🔍 Investigation Panel")

    if uploaded_file is not None:
        # Save temp
        os.makedirs(TEMP_DIR, exist_ok=True)
        temp_path = os.path.join(TEMP_DIR, "temp_query.jpg")
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        if st.button(
            "🚀 Execute Deep Investigation",
            type="primary",
            use_container_width=True
        ):
            try:
                report = run_deep_investigation(
                    temp_path,
                    match_threshold
                )

                st.markdown("---")
                st.markdown("### 📋 Deep Investigation Dossier")
                st.markdown(report)

                # Save log
                os.makedirs(LOGS_DIR, exist_ok=True)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                log_file  = os.path.join(
                    LOGS_DIR,
                    f"report_{timestamp}.md"
                )
                with open(log_file, "w") as lf:
                    lf.write(report)

                st.download_button(
                    label     = "📥 Download Full Report",
                    data      = report,
                    file_name = f"ironclad_report_{timestamp}.md",
                    mime      = "text/markdown"
                )

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.code(str(e))

    else:
        st.markdown("""
            <div style='
                border: 2px dashed #444;
                border-radius: 10px;
                padding: 40px;
                text-align: center;
                color: #888;
            '>
                <h2>📂 Upload Image or Search By Name</h2>
                <p>Upload a face image on the left</p>
                <p>OR use the Name Search box</p>
                <br/>
                <p>🔬 Face Detection → 🌐 OSINT → 📋 Report</p>
            </div>
        """, unsafe_allow_html=True)

# ─────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────
st.markdown("---")
st.markdown("""
    <div style='text-align:center; color:#666; font-size:12px;'>
        🛡️ Ironclad v2.0.0 | Deep OSINT Engine |
        100% Local | Zero Cost | Authorized Use Only
    </div>
""", unsafe_allow_html=True)

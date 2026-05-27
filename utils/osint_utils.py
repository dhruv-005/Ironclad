

# ─────────────────────────────────────────
# SEARCH BY EMAIL
# ─────────────────────────────────────────
def search_by_email(email: str) -> dict:
    """Search for information associated with an email address."""
    results = {}
    ddgs    = DDGS()

    try:
        r = list(ddgs.text(
            f'"{email}" person profile contact',
            max_results=5
        ))
        results["email_search"] = r
    except Exception as e:
        results["error"] = str(e)

    return results


# ─────────────────────────────────────────
# SEARCH BY USERNAME
# ─────────────────────────────────────────
def search_by_username(username: str) -> dict:
    """Search for a username across multiple platforms."""
    platforms = [
        "twitter.com", "instagram.com", "github.com",
        "reddit.com", "tiktok.com", "youtube.com"
    ]
    results = {}
    ddgs    = DDGS()

    for platform in platforms:
        try:
            r = list(ddgs.text(
                f"site:{platform} {username}",
                max_results=2
            ))
            if r:
                results[platform] = r
        except:
            pass

    return results

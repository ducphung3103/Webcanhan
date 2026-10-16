"""
Rule-Based Tagging and Categorization System for CP Problems and Materials.
Operates deterministically without relying on costly LLM API calls.
"""

import re
from typing import Dict, List, Tuple, Any

# Keyword rules for categorizing topics
TOPIC_RULES = {
    "Graph Theory": [
        r"\bgraph\b", r"\bđồ thị\b", r"\bdijkstra\b", r"\bshortest path\b", r"\bđường đi ngắn nhất\b",
        r"\bbfs\b", r"\bdfs\b", r"\bmst\b", r"\bcây khung\b", r"\bflow\b", r"\bluồng\b",
        r"\bmatching\b", r"\bcặp ghép\b", r"\btarjan\b", r"\bscc\b", r"\btopo\b", r"\btopological\b",
        r"\beuler\b", r"\b2-sat\b", r"\bbipartite\b", r"\bhaitộc\b", r"\bbridge\b", r"\bcầu\b", r"\bkhớp\b"
    ],
    "Tree": [
        r"\btree\b", r"\bcây\b", r"\blca\b", r"\breroot\b", r"\brerooting\b", r"\bhld\b",
        r"\bheavy[- ]light\b", r"\bcentroid\b", r"\bmo on tree\b", r"\beuler tour\b",
        r"\bdsu tree\b", r"\bsmall to large\b"
    ],
    "Dynamic Programming": [
        r"\bdp\b", r"\bqhđ\b", r"\bquy hoạch động\b", r"\bsos dp\b", r"\bdigit dp\b", r"\bbitmask\b",
        r"\bcht\b", r"\bconvex hull trick\b", r"\balien\b", r"\bknapsack\b", r"\bbalo\b",
        r"\bdivide and conquer dp\b", r"\bd&c dp\b", r"\bmatrix exponentiation\b", r"\bnhân ma trận\b"
    ],
    "Data Structures": [
        r"\bctdl\b", r"\bdata structure\b", r"\bsegment tree\b", r"\bit\b", r"\bfenwick\b",
        r"\bbit\b", r"\bmo\b", r"\bchia căn\b", r"\bsqrt\b", r"\btrie\b", r"\btreap\b",
        r"\bpersistent\b", r"\bmonotonic\b", r"\bdsu\b", r"\bdisjoint set\b"
    ],
    "Mathematics": [
        r"\bmath\b", r"\btoán\b", r"\bnumber theory\b", r"\bsố học\b", r"\bmodulo\b",
        r"\blucas\b", r"\bcombinatorics\b", r"\btổ hợp\b", r"\bbao hàm\b", r"\binclusion[- ]exclusion\b",
        r"\bchia kẹo\b", r"\bsieve\b", r"\bsàng\b", r"\bprobability\b", r"\bxác suất\b",
        r"\bexpected value\b", r"\bkỳ vọng\b", r"\bfft\b", r"\bntt\b", r"\bbitwise\b", r"\bxor\b"
    ],
    "Geometry & Sweepline": [
        r"\bgeometry\b", r"\bhình học\b", r"\bhình\b", r"\bsweepline\b", r"\bconvex hull\b",
        r"\bbao lồi\b", r"\bpolygon\b", r"\bđa giác\b", r"\bvector\b", r"\bpoint in polygon\b"
    ],
    "Strings": [
        r"\bstring\b", r"\bxâu\b", r"\bchuỗi\b", r"\bhash\b", r"\bkmp\b", r"\bz function\b",
        r"\bz-algo\b", r"\baho[- ]corasick\b", r"\bsuffix automaton\b", r"\bsuffix array\b",
        r"\bmanacher\b"
    ],
    "Greedy & Search": [
        r"\bgreedy\b", r"\btham lam\b", r"\bbinary search\b", r"\bbs\b", r"\bchặt nhị phân\b",
        r"\bternary search\b", r"\btwo pointers\b", r"\bhai con trỏ\b", r"\bmeet in the middle\b"
    ],
    "Game Theory & Adhoc": [
        r"\bgame\b", r"\btrò chơi\b", r"\bnim\b", r"\bsprague\b", r"\badhoc\b", r"\bnhận xét\b",
        r"\bobservation\b", r"\bconstructive\b", r"\binteractive\b"
    ]
}

def detect_platform(url: str) -> str:
    """Identify the competitive programming platform from URL."""
    if not url or not isinstance(url, str):
        return "Other"
    url_lower = url.lower()
    if "codeforces.com" in url_lower:
        return "Codeforces"
    if "oj.vnoi.info" in url_lower or "vnoi.info" in url_lower:
        return "VNOI"
    if "cses.fi" in url_lower:
        return "CSES"
    if "lqdoj.edu.vn" in url_lower:
        return "LQDOJ"
    if "oj.uz" in url_lower:
        return "OJ.UZ"
    if "atcoder.jp" in url_lower:
        return "AtCoder"
    if "dmoj.ca" in url_lower:
        return "DMOJ"
    if "marisaoj.com" in url_lower:
        return "MarisaOJ"
    if "hackerrank.com" in url_lower:
        return "HackerRank"
    if "usaco.org" in url_lower:
        return "USACO"
    if "spoj.com" in url_lower:
        return "SPOJ"
    if "ioi-jp.org" in url_lower:
        return "JOI"
    if "youtube.com" in url_lower or "youtu.be" in url_lower:
        return "YouTube"
    if any(k in url_lower for k in ["wiki", "cp-algorithms", "viblo", "docs.google"]):
        return "Material"
    return "Other"

def extract_problem_info(url: str) -> Tuple[str, str]:
    """
    Extracts (problem_id, readable_title) from a CP problem URL.
    """
    if not url or not isinstance(url, str):
        return "", ""

    # Codeforces: .../contest/786/problem/C or .../problemset/problem/1200/D or .../gym/101628/problem/A
    cf_match = re.search(r"codeforces\.com/(?:contest|problemset/problem|gym)/(\d+)(?:/problem)?/([A-Za-z0-9]+)", url)
    if cf_match:
        contest_id, prob_idx = cf_match.groups()
        pid = f"CF-{contest_id}{prob_idx.upper()}"
        return pid, f"Codeforces {contest_id}{prob_idx.upper()}"

    # VNOI: .../problem/voi21_rmat or .../problem/fc101_fcgif
    vnoi_match = re.search(r"oj\.vnoi\.info/problem/([a-zA-Z0-9_\-]+)", url)
    if vnoi_match:
        code = vnoi_match.group(1)
        return f"VNOI-{code}", f"VNOI {code.replace('_', ' ').title()}"

    # CSES: .../task/1654
    cses_match = re.search(r"cses\.fi/problemset/task/(\d+)", url)
    if cses_match:
        task_id = cses_match.group(1)
        return f"CSES-{task_id}", f"CSES Task {task_id}"

    # LQDOJ: .../problem/diffgraph
    lqdoj_match = re.search(r"lqdoj\.edu\.vn/problem/([a-zA-Z0-9_\-]+)", url)
    if lqdoj_match:
        code = lqdoj_match.group(1)
        return f"LQDOJ-{code}", f"LQDOJ {code.replace('_', ' ').title()}"

    # OJ.UZ: .../problem/view/CEOI22_abraca
    ojuz_match = re.search(r"oj\.uz/problem/view/([a-zA-Z0-9_\-]+)", url)
    if ojuz_match:
        code = ojuz_match.group(1)
        return f"OJUZ-{code}", f"OJ.UZ {code.replace('_', ' ')}"

    # AtCoder: .../tasks/abc250_e
    atcoder_match = re.search(r"atcoder\.jp/contests/([a-zA-Z0-9_\-]+)/tasks/([a-zA-Z0-9_\-]+)", url)
    if atcoder_match:
        contest, task = atcoder_match.groups()
        return f"AC-{task.upper()}", f"AtCoder {task.upper()}"

    # Generic Fallback
    parts = [p for p in url.split("/") if p and not p.startswith("http")]
    slug = parts[-1] if parts else "Problem"
    slug = re.sub(r"[^a-zA-Z0-9_\-]", "", slug)
    return slug[:20], slug.replace("_", " ").title()[:40]

def categorize_item(text_context: str, sheet_name: str = "") -> Tuple[str, List[str]]:
    """
    Given a combination of notes, tags, URL, and sheet context,
    determines the primary topic category and a list of specific tags.
    """
    search_text = f"{sheet_name} {text_context}".lower()
    matched_topics = []

    for topic, patterns in TOPIC_RULES.items():
        for pattern in patterns:
            if re.search(pattern, search_text, re.IGNORECASE):
                matched_topics.append(topic)
                break

    # If sheet name strongly matches, prioritize it
    sheet_lower = sheet_name.lower()
    if "tree" in sheet_lower and "graph" in sheet_lower:
        if "tree" in search_text:
            primary_topic = "Tree"
        else:
            primary_topic = "Graph Theory"
    elif "dp" in sheet_lower or "greedy" in sheet_lower:
        primary_topic = "Dynamic Programming" if "dp" in search_text else "Greedy & Search"
    elif "mo" in sheet_lower or "chia căn" in sheet_lower or "ctdl" in sheet_lower:
        primary_topic = "Data Structures"
    elif "math" in sheet_lower or "hình" in sheet_lower or "sweepline" in sheet_lower:
        primary_topic = "Geometry & Sweepline" if any(k in search_text for k in ["hình", "geometry", "sweepline"]) else "Mathematics"
    elif "adhoc" in sheet_lower or "game" in sheet_lower or "string" in sheet_lower:
        primary_topic = "Strings" if any(k in search_text for k in ["string", "xâu", "hash", "kmp", "z function"]) else "Game Theory & Adhoc"
    elif matched_topics:
        primary_topic = matched_topics[0]
    else:
        primary_topic = "General CP"

    # Specific tags extraction
    raw_tags = set()
    # Add matches from matched topics
    for t in matched_topics:
        raw_tags.add(t)

    # Add specific technique keywords
    technique_keywords = [
        "dijkstra", "small to large", "reroot", "mo on tree", "dsu", "dsu tree",
        "shotest path", "sos dp", "bitmask", "chia căn", "trie", "gộp trie",
        "bao hàm loại trừ", "chia kẹo", "lucas", "sweepline", "hình học",
        "hash 2d", "aho-corasick", "z function", "prefixsum", "topo", "centroid",
        "cặp ghép", "observation", "centroid", "euler tour", "lca", "segtree"
    ]
    for kw in technique_keywords:
        if kw in search_text:
            raw_tags.add(kw.title())

    # If extra notes exist in text_context, split by comma
    for piece in re.split(r"[,;+]", text_context):
        piece = piece.strip()
        if 2 < len(piece) < 25 and not piece.startswith("http") and not piece.isdigit():
            raw_tags.add(piece.title())

    tags_list = sorted(list(raw_tags))
    if not tags_list:
        tags_list = [primary_topic]

    return primary_topic, tags_list

def normalize_difficulty(rating_val: Any, explicit_diff: str = "") -> Tuple[str, int]:
    """
    Normalizes rating numbers and difficulty strings into standard format.
    Returns (difficulty_label, numeric_rating).
    """
    num_rating = 0
    if rating_val:
        try:
            # Handle float or string like '2400.0' or '2400'
            cleaned = str(rating_val).replace(".0", "").strip()
            if cleaned.isdigit():
                num_rating = int(cleaned)
        except Exception:
            num_rating = 0

    if num_rating > 0:
        if num_rating < 1400:
            diff_label = "Easy"
        elif num_rating < 1900:
            diff_label = "Medium"
        elif num_rating < 2400:
            diff_label = "Hard"
        elif num_rating < 2800:
            diff_label = "Master / VOI"
        else:
            diff_label = "Grandmaster / TST"
        return diff_label, num_rating

    # If no numeric rating, inspect explicit text
    exp_lower = str(explicit_diff).lower().strip()
    if any(k in exp_lower for k in ["tst", "grandmaster", "3000"]):
        return "Grandmaster / TST", 2800
    if any(k in exp_lower for k in ["voi", "master", "hard", "khó"]):
        return "Hard", 2200
    if any(k in exp_lower for k in ["medium", "vừa", "trung bình"]):
        return "Medium", 1600
    if any(k in exp_lower for k in ["easy", "dễ", "basic"]):
        return "Easy", 1200

    return "Medium", 1500

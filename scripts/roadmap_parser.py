"""
Roadmap Parser: Extracts the structured CP curriculum hierarchy from 'New Roadmap.docx'.
Classifies into 4 main tiers: BASIC, INTERMEDIATE, HARD, INSANE.
"""

import sys
import re
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List, Dict, Any

# Ensure project root in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

DOCX_PATH = PROJECT_ROOT / "New Roadmap.docx"

def extract_paragraphs_from_docx(docx_path: Path) -> List[str]:
    """Reads raw paragraphs from a .docx file without requiring external libraries."""
    if not docx_path.exists():
        print(f"[Roadmap] Error: {docx_path} does not exist.")
        return []

    with zipfile.ZipFile(docx_path) as z:
        xml_content = z.read("word/document.xml")
    
    tree = ET.fromstring(xml_content)
    paragraphs = []
    for p in tree.iter("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p"):
        p_text = "".join(t.text for t in p.iter("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t") if t.text)
        cleaned = p_text.strip()
        if cleaned:
            paragraphs.append(cleaned)
    return paragraphs

def build_roadmap_tree() -> List[Dict[str, Any]]:
    """
    Parses paragraphs into a structured list of roadmap topic nodes
    with tier, category, title, and keywords.
    """
    raw_lines = extract_paragraphs_from_docx(DOCX_PATH)
    if not raw_lines:
        return []

    roadmap_nodes: List[Dict[str, Any]] = []
    
    current_tier = "BASIC"
    current_category = "Basic Foundations"
    
    tier_markers = {
        "BASIC": "BASIC",
        "INTERMEDIATE": "INTERMEDIATE",
        "HARD": "HARD",
        "INSANE": "INSANE (ĐỪNG HỌC MẤY CL NÀY)"
    }

    # Category detector patterns
    category_patterns = [
        "Basic C++ / Python", "Basic Programming Language & Brute Force",
        "Basic Container", "Basic Algorithm", "Basic Data Structure",
        "Basic Algorithm & Data Structure 2", "Basic Dynamic Programming",
        "Basic Graph", "Basic String", "Basic Tree",
        "Intermediate Graph", "Intermediate Data Structure", "Intermediate Tree",
        "Trick for VOI", "Intermediate Math", "Intermediate DP", "Intermediate Geometry",
        "Others Intermediate",
        "Hard Data Structure", "Hard Tree", "Hard Math", "Hard Dynamic Programming",
        "Hard Graph", "Hard Geometry", "Other Hard",
        "Insane DP", "Insane Graph", "Insane Math", "Insane Data Structure",
        "Insane String", "Insane Tree"
    ]

    for line in raw_lines:
        line_clean = line.strip()
        line_upper = line_clean.upper()

        # Check Tier Change
        if line_upper == "BASIC":
            current_tier = "BASIC"
            current_category = "Basic Programming & Container"
            continue
        elif line_upper == "INTERMEDIATE":
            current_tier = "INTERMEDIATE"
            current_category = "Intermediate Graph & DS"
            continue
        elif line_upper == "HARD":
            current_tier = "HARD"
            current_category = "Hard Algorithms"
            continue
        elif "INSANE" in line_upper:
            current_tier = "INSANE"
            current_category = "Advanced Insane Topics"
            continue

        # Check Category Change
        matched_cat = next((cat for cat in category_patterns if cat.lower() == line_clean.lower()), None)
        if matched_cat:
            current_category = matched_cat
            continue

        # Skip trivial headings or instructions
        if line_clean.lower() in ["how to code / run", "variable", "queries"]:
            continue

        # Generate Node ID and Keywords
        node_id = re.sub(r"[^a-zA-Z0-9]+", "_", line_clean.lower()).strip("_")
        keywords = generate_keywords_for_topic(line_clean)

        roadmap_nodes.append({
            "id": f"{current_tier.lower()}_{node_id}",
            "title": line_clean,
            "tier": current_tier,
            "category": current_category,
            "keywords": keywords,
            "problems": []
        })

    print(f"[Roadmap] Successfully generated {len(roadmap_nodes)} roadmap topics across 4 tiers.")
    return roadmap_nodes

def generate_keywords_for_topic(title: str) -> List[str]:
    """Generates matching keywords and regex patterns for a roadmap topic."""
    t_lower = title.lower()
    keywords = set()
    keywords.add(t_lower)

    # Specific topic mappings
    mapping = {
        "prefixsum": ["prefix sum", "prefixsum", "mảng cộng dồn", "diff array", "2d sum"],
        "diff array": ["diff array", "difference array", "mảng hiệu"],
        "number theory": ["number theory", "số học", "prime", "sieve", "sàng", "gcd", "lcm", "arithmetic"],
        "prime -> prime sieve": ["prime", "sieve", "sàng nguyên tố", "nguyên tố"],
        "recursion": ["recursion", "đệ quy", "backtrack", "quay lui", "branch and bound"],
        "sorting": ["sorting", "sắp xếp", "merge sort", "bubble sort", "sort"],
        "greedy": ["greedy", "tham lam"],
        "binary search": ["binary search", "bs", "chặt nhị phân", "tìm kiếm nhị phân"],
        "two pointer": ["two pointer", "two pointers", "hai con trỏ"],
        "stack / queue / deque": ["stack", "queue", "deque", "ngăn xếp", "hàng đợi", "monotonic"],
        "monotonic stack / deque": ["monotonic", "monotonic stack", "monotonic deque", "deque dp"],
        "priority_queue / heap": ["heap", "priority queue", "priority_queue", "pq"],
        "meet in the middle": ["meet in the middle", "mitm"],
        "bitwise": ["bitwise", "xor", "and", "or", "bitmask"],
        "bitmask": ["bitmask", "mask", "mặt nạ bit", "dp bitmask", "sos dp"],
        "disjoint set union": ["dsu", "disjoint set", "union find", "small to large", "set merging"],
        "dsu on array": ["dsu", "disjoint set"],
        "set merging - small to large": ["small to large", "gộp tập", "sack"],
        "rmq": ["rmq", "sparse table", "range minimum query"],
        "dp knapsack": ["knapsack", "balo", "dp knapsack"],
        "dp lis": ["lis", "dãy con tăng", "longest increasing subsequence"],
        "dp lcs": ["lcs", "dãy con chung"],
        "dp bitmask": ["dp bitmask", "bitmask dp", "sos dp"],
        "dfs": ["dfs", "depth first search", "duyệt theo chiều sâu"],
        "bridge & articulation point": ["bridge", "articulation", "cầu", "khớp", "tarjan"],
        "bfs": ["bfs", "breadth first search", "bfs 0-1", "dial"],
        "strongly connected component (scc)": ["scc", "strongly connected", "liên thông mạnh", "tarjan", "kosaraju"],
        "topological sort": ["topo", "topological", "sắp xếp topo"],
        "euler circuit": ["euler", "eulerian", "chu trình euler"],
        "hash": ["hash", "hashing", "băm", "hash 2d"],
        "kmp": ["kmp", "knuth morris pratt", "tiền tố"],
        "manacher": ["manacher", "palindrome"],
        "binary lifting & lowest common ancestor": ["lca", "binary lifting", "tổ tiên chung"],
        "lca o(log2(n))": ["lca", "binary lifting"],
        "dijkstra": ["dijkstra", "shortest path", "đường đi ngắn nhất"],
        "floyd": ["floyd", "floyd warshall"],
        "mst": ["mst", "kruskal", "prim", "cây khung"],
        "segment tree": ["segtree", "segment tree", "it", "cây phân đoạn"],
        "lazy propagation": ["lazy", "lazy propagation", "lười"],
        "segtree merge": ["segtree merge", "gộp segtree"],
        "binary index tree": ["bit", "fenwick", "binary index tree"],
        "euler tour": ["euler tour", "euler tour tree"],
        "rerooting": ["reroot", "rerooting", "đổi gốc"],
        "dp on tree": ["dp on tree", "dp tree", "quy hoạch động trên cây"],
        "sack (dsu on tree)": ["sack", "dsu on tree", "small to large on tree"],
        "inclusion & exclusion": ["inclusion", "exclusion", "bao hàm", "bao hàm loại trừ"],
        "dp digit": ["digit dp", "dp chữ số", "lexicographical"],
        "dp range": ["dp range", "quy hoạch động đoạn"],
        "dp sos": ["sos dp", "sum over subsets"],
        "sweep line": ["sweep line", "sweepline", "quét"],
        "convex hull": ["convex hull", "bao lồi"],
        "mo algorithm": ["mo", "mo algorithm", "mo on tree", "chia căn"],
        "heavy - light decomposition": ["hld", "heavy light", "heavy-light decomposition"],
        "centroid decomposition": ["centroid", "centroid decomposition"],
        "matrix multiplication": ["matrix", "nhân ma trận", "matrix exponentiation"],
        "game theory": ["game", "nim", "grundy", "trò chơi"],
        "dp cht": ["cht", "convex hull trick", "bao lồi dp"],
        "dp alien trick": ["alien trick", "wqs binary search"],
        "2-sat": ["2-sat", "2sat"],
        "flow": ["flow", "luồng", "max flow", "dinic", "edmonds karp", "min cut"],
        "maximum matching": ["matching", "cặp ghép", "bipartite matching", "hungarian", "hopcroft"],
        "persistent segment tree": ["persistent", "persistent segtree", "persistent tree"],
        "treap": ["treap", "cartesian tree"],
        "aho-corasick": ["aho-corasick", "aho corasick", "trie"],
        "interactive": ["interactive", "tương tác"],
        "constructive": ["constructive", "xây dựng"]
    }

    for key, kw_list in mapping.items():
        if key in t_lower:
            keywords.update(kw_list)

    return list(keywords)

if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    nodes = build_roadmap_tree()
    for n in nodes[:15]:
        print(f"[{n['tier']}] [{n['category']}] -> {n['title']} (Keywords: {len(n['keywords'])})")

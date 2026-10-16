"""
Account Crawler & Problem Mapper:
1. Extracts account handles from 'Link Em Phung Duc Nong 15p.xlsx' (sheet 'Note').
2. Fetches verified solved submissions from Codeforces API for 'DeruckLoveNewTechnology'.
3. Ingests all problems from local Excel workbooks.
4. Maps every problem into its suitable place in the 4-tier Roadmap (New Roadmap.docx)
   using rule-based keyword & tag matching without expensive LLM tokens.
"""

import os
import sys
import json
import time
from pathlib import Path
from typing import Dict, List, Any, Set, Tuple

# Fix SSLKEYLOGFILE on Windows if corrupted
os.environ.pop("SSLKEYLOGFILE", None)

# Configure UTF-8 encoding for Windows stdout/stderr
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import openpyxl
import requests
from scripts.roadmap_parser import build_roadmap_tree
from scripts.scraper import CPDataProcessor
from scripts.tagger import detect_platform, extract_problem_info, normalize_difficulty

class ProblemRoadmapMapper:
    def __init__(self):
        self.accounts: Dict[str, str] = {}
        self.cf_solved_problems: Dict[str, Dict[str, Any]] = {}
        self.all_problems: Dict[str, Dict[str, Any]] = {}
        self.roadmap_nodes: List[Dict[str, Any]] = []

    def extract_accounts_from_sheet(self) -> Dict[str, str]:
        """Extracts handles from sheet 'Note' in 'Link Em Phung Duc Nong 15p.xlsx'."""
        excel_path = PROJECT_ROOT / "Link Em Phung Duc Nong 15p.xlsx"
        if not excel_path.exists():
            return {}

        wb = openpyxl.load_workbook(excel_path, data_only=True)
        if "Note" not in wb.sheetnames:
            return {}

        sheet = wb["Note"]
        rows = list(sheet.iter_rows(values_only=True))
        
        # Expected layout: col 5 is platform, col 6 is handle
        for row in rows:
            if len(row) > 6 and row[5] and row[6]:
                plat = str(row[5]).strip()
                handle = str(row[6]).strip()
                if plat and handle and plat.lower() != "platform":
                    self.accounts[plat] = handle

        print(f"[Accounts] Found {len(self.accounts)} platform accounts in sheet 'Note':")
        for plat, handle in self.accounts.items():
            print(f"  - {plat}: {handle}")
        return self.accounts

    def fetch_codeforces_solved_problems(self) -> Dict[str, Dict[str, Any]]:
        """Queries Codeforces API to fetch verified solved problems for the user's handle."""
        cf_handle = self.accounts.get("Codeforces", "DeruckLoveNewTechnology")
        print(f"[Codeforces] Fetching solved submissions for handle: {cf_handle}...")

        try:
            url = f"https://codeforces.com/api/user.status?handle={cf_handle}&from=1&count=5000"
            resp = requests.get(url, timeout=20)
            if resp.status_code != 200:
                print(f"[Codeforces] Warning: HTTP {resp.status_code} from Codeforces API")
                return {}

            data = resp.json()
            if data.get("status") != "OK":
                print(f"[Codeforces] API Comment: {data.get('comment')}")
                return {}

            submissions = data.get("result", [])
            for sub in submissions:
                if sub.get("verdict") == "OK":
                    prob = sub.get("problem", {})
                    c_id = prob.get("contestId")
                    idx = prob.get("index")
                    if not c_id or not idx:
                        continue
                    
                    pid = f"CF-{c_id}{idx}"
                    prob_url = f"https://codeforces.com/contest/{c_id}/problem/{idx}"
                    rating = prob.get("rating", 1500)
                    tags = prob.get("tags", [])
                    name = prob.get("name", f"Problem {idx}")

                    diff_label, num_rating = normalize_difficulty(rating)

                    self.cf_solved_problems[prob_url] = {
                        "id": pid,
                        "title": f"Codeforces {c_id}{idx} - {name}",
                        "url": prob_url,
                        "platform": "Codeforces",
                        "rating": num_rating,
                        "difficulty": diff_label,
                        "tags": tags,
                        "notes": "Solved on Codeforces",
                        "source_sheet": "Codeforces API (DeruckLoveNewTechnology)",
                        "solved": True,
                        "status": "Solved"
                    }

            print(f"[Codeforces] Successfully parsed {len(self.cf_solved_problems)} unique solved problems!")
        except Exception as e:
            print(f"[Codeforces] Notice: Could not reach Codeforces API ({e}). Continuing with local data.")

        return self.cf_solved_problems

    def merge_all_problems(self):
        """Combines local spreadsheet problems and Codeforces solved submissions."""
        # 1. Local Excel extraction
        processor = CPDataProcessor(use_web_enrichment=False)
        data = processor.process_all()
        local_exercises = data.get("exercises", [])

        # Add local exercises
        for ex in local_exercises:
            url = ex.get("url", "").strip()
            if not url:
                continue
            
            # Check if solved via Codeforces API or local sheet mark
            is_cf_solved = url in self.cf_solved_problems
            # Check if source sheet marked as done
            is_sheet_done = "✓" in ex.get("notes", "") or "true" in ex.get("notes", "").lower()
            ex["solved"] = is_cf_solved or is_sheet_done or (ex.get("status") == "Solved")
            if is_cf_solved:
                ex["status"] = "Solved"
                # Enrich tags from Codeforces API if local tags are generic
                cf_data = self.cf_solved_problems[url]
                if cf_data.get("tags"):
                    ex["tags"] = sorted(list(set(ex.get("tags", []) + cf_data["tags"])))
                if cf_data.get("rating"):
                    ex["rating"] = cf_data["rating"]
                    ex["difficulty"] = cf_data["difficulty"]

            self.all_problems[url] = ex

        # Add remaining CF solved problems that weren't in local sheets
        for url, cf_prob in self.cf_solved_problems.items():
            if url not in self.all_problems:
                self.all_problems[url] = cf_prob

        print(f"[Mapper] Total unified problem collection: {len(self.all_problems)} problems.")
        solved_count = sum(1 for p in self.all_problems.values() if p.get("solved"))
        print(f"[Mapper] Total verified solved problems: {solved_count} / {len(self.all_problems)}")

    def map_problems_to_roadmap(self):
        """Classifies each problem into its best-fitting Roadmap topic node."""
        self.roadmap_nodes = build_roadmap_tree()
        if not self.roadmap_nodes:
            print("[Mapper] Error: No roadmap nodes found.")
            return

        print(f"[Mapper] Mapping {len(self.all_problems)} problems into {len(self.roadmap_nodes)} Roadmap nodes...")

        # Precompute matchers for roadmap nodes
        node_matchers = []
        for node in self.roadmap_nodes:
            keywords = [kw.lower() for kw in node.get("keywords", [])]
            title_clean = node.get("title", "").lower()
            cat_clean = node.get("category", "").lower()
            tier = node.get("tier", "BASIC")
            node_matchers.append({
                "node": node,
                "title": title_clean,
                "category": cat_clean,
                "tier": tier,
                "keywords": keywords
            })

        for p_url, prob in self.all_problems.items():
            best_node = None
            best_score = -1

            # Compile text representation for matching
            tags_text = " ".join(prob.get("tags", [])).lower()
            title_text = prob.get("title", "").lower()
            notes_text = prob.get("notes", "").lower()
            sheet_text = prob.get("source_sheet", "").lower()
            search_blob = f"{title_text} {tags_text} {notes_text} {sheet_text}"

            for matcher in node_matchers:
                score = 0
                node = matcher["node"]

                # Keyword exact match
                for kw in matcher["keywords"]:
                    if kw in search_blob:
                        # Longer keyword matches are stronger
                        score += 5 + len(kw)

                # Topic title match
                if matcher["title"] in search_blob:
                    score += 15

                # Notes specific high-precision boost
                for kw in matcher["keywords"]:
                    if kw in notes_text or kw in tags_text:
                        score += 10

                if score > best_score:
                    best_score = score
                    best_node = node

            # If no match found or very weak, assign to a default node based on topic
            if not best_node or best_score <= 0:
                best_node = self._fallback_node(prob)

            # Assign problem to roadmap node
            prob["roadmap_tier"] = best_node["tier"]
            prob["roadmap_category"] = best_node["category"]
            prob["roadmap_topic_id"] = best_node["id"]
            prob["roadmap_topic_title"] = best_node["title"]

            best_node["problems"].append({
                "id": prob.get("id"),
                "title": prob.get("title"),
                "url": prob.get("url"),
                "platform": prob.get("platform"),
                "rating": prob.get("rating"),
                "difficulty": prob.get("difficulty"),
                "solved": prob.get("solved", False),
                "tags": prob.get("tags", [])
            })

        # Calculate statistics per roadmap node
        for node in self.roadmap_nodes:
            node_probs = node["problems"]
            node["total_problems"] = len(node_probs)
            node["solved_problems"] = sum(1 for p in node_probs if p.get("solved"))
            node["completion_pct"] = round((node["solved_problems"] / len(node_probs) * 100), 1) if node_probs else 0

        # Summary statistics
        total_mapped = sum(node["total_problems"] for node in self.roadmap_nodes)
        nodes_with_problems = sum(1 for node in self.roadmap_nodes if node["total_problems"] > 0)
        print(f"[Mapper] Successfully mapped {total_mapped} problem assignments across {nodes_with_problems} active Roadmap nodes!")

    def _fallback_node(self, prob: Dict[str, Any]) -> Dict[str, Any]:
        """Provides high-accuracy fallback node based on tags and topic."""
        tags = [t.lower() for t in prob.get("tags", [])]
        topic = (prob.get("topic") or "General CP").lower()
        title = prob.get("title", "").lower()
        notes = prob.get("notes", "").lower()
        combined = f"{' '.join(tags)} {topic} {title} {notes}"

        # Dynamic Programming
        if any(k in combined for k in ["dp", "dynamic programming", "quy hoạch động"]):
            node = next((n for n in self.roadmap_nodes if n["title"].lower() in ["normal dp", "basic dp", "dp knapsack"]), None)
            if node: return node

        # Graphs
        if any(k in combined for k in ["graph", "đồ thị", "dfs", "bfs", "shortest paths"]):
            node = next((n for n in self.roadmap_nodes if n["title"].lower() in ["normal dfs", "shortest path", "dijkstra"]), None)
            if node: return node

        # Trees
        if any(k in combined for k in ["tree", "cây", "lca", "reroot"]):
            node = next((n for n in self.roadmap_nodes if n["title"].lower() in ["binary lifting", "introduction of tree", "dp on tree"]), None)
            if node: return node

        # Data Structures
        if any(k in combined for k in ["data structures", "segtree", "fenwick", "bit", "dsu"]):
            node = next((n for n in self.roadmap_nodes if n["title"].lower() in ["normal segment tree", "binary index tree", "dsu on array"]), None)
            if node: return node

        # Math / Number Theory
        if any(k in combined for k in ["math", "số học", "number theory", "combinatorics"]):
            node = next((n for n in self.roadmap_nodes if n["title"].lower() in ["number theory", "prime -> prime sieve", "modulo & gcd"]), None)
            if node: return node

        # Greedy
        if "greedy" in combined or "tham lam" in combined:
            node = next((n for n in self.roadmap_nodes if n["title"].lower() == "greedy"), None)
            if node: return node

        # Binary Search / Two Pointers
        if any(k in combined for k in ["binary search", "bs", "two pointers", "chặt nhị phân"]):
            node = next((n for n in self.roadmap_nodes if n["title"].lower() in ["binary search", "two pointer"]), None)
            if node: return node

        # Strings
        if any(k in combined for k in ["string", "xâu", "hash", "kmp"]):
            node = next((n for n in self.roadmap_nodes if n["title"].lower() in ["hash", "kmp", "basic string"]), None)
            if node: return node

        # Geometry
        if any(k in combined for k in ["geometry", "hình học", "sweep line", "convex hull"]):
            node = next((n for n in self.roadmap_nodes if n["title"].lower() in ["polygon", "sweep line", "convex hull"]), None)
            if node: return node

        # Constructive / Adhoc / Implementation
        if any(k in combined for k in ["constructive", "adhoc", "implementation", "brute force"]):
            node = next((n for n in self.roadmap_nodes if n["title"].lower() in ["constructive", "adhoc", "basic programming language & brute force"]), None)
            if node: return node

        # Default to first non-empty basic node
        return next((n for n in self.roadmap_nodes if n["tier"] == "BASIC" and n["title"].lower() == "greedy"), self.roadmap_nodes[0])

def run_roadmap_and_account_pipeline():
    mapper = ProblemRoadmapMapper()
    mapper.extract_accounts_from_sheet()
    mapper.fetch_codeforces_solved_problems()
    mapper.merge_all_problems()
    mapper.map_problems_to_roadmap()
    return mapper

if __name__ == "__main__":
    mapper = run_roadmap_and_account_pipeline()
    # Print sample populated roadmap nodes
    print("\n--- SAMPLE POPULATED ROADMAP TOPICS ---")
    active_nodes = [n for n in mapper.roadmap_nodes if n["total_problems"] > 0]
    for n in active_nodes[:15]:
        print(f"[{n['tier']}] {n['title']}: {n['solved_problems']}/{n['total_problems']} solved ({n['completion_pct']}%)")

"""
Modular Crawler and Data Processor for Competitive Programming (CP) Materials.
Extracts data from local Excel workbooks, live Google Sheets (via gspread),
and enriches problem metadata from CP web platforms (Codeforces, VNOI, CSES, AtCoder).
"""

import os
import re
import sys
import json
import time
from pathlib import Path

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
from bs4 import BeautifulSoup
from typing import Dict, List, Any, Optional

from config.config import (
    LOCAL_EXCEL_FILES,
    GOOGLE_SPREADSHEET_ID,
    get_service_account_dict
)
from scripts.tagger import (
    detect_platform,
    extract_problem_info,
    categorize_item,
    normalize_difficulty
)

class CPDataProcessor:
    """
    Unified Data Processor that reads from multiple sources,
    cleans, standardizes, categorizes, and organizes CP learning materials.
    """

    def __init__(self, use_web_enrichment: bool = False):
        self.use_web_enrichment = use_web_enrichment
        self.exercises: List[Dict[str, Any]] = []
        self.materials: List[Dict[str, Any]] = []
        self.roadmap: List[Dict[str, Any]] = []
        self.projects: List[Dict[str, Any]] = []
        self.seen_urls = set()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

    def process_all(self) -> Dict[str, List[Dict[str, Any]]]:
        """Runs the full parsing pipeline across local files, Google Sheets, and web sources."""
        print("[Processor] Starting CP Data Ingestion...")

        # 1. Ingest local workbooks
        for filepath in LOCAL_EXCEL_FILES:
            if filepath.exists():
                print(f"[Processor] Ingesting local Excel workbook: {filepath.name}")
                self.parse_local_workbook(str(filepath))
            else:
                print(f"[Processor] Workbook not found: {filepath}")

        # 2. Try Google Sheets via gspread if credentials exist
        self.try_ingest_google_sheets()

        # 3. Add default CP portfolio projects and templates
        self.add_default_portfolio_projects()

        # 4. Web metadata enrichment (optional / non-blocking)
        if self.use_web_enrichment:
            self.enrich_with_web_crawling()

        print(f"[Processor] Ingestion Complete:")
        print(f"  - Exercises: {len(self.exercises)}")
        print(f"  - Materials/Tutorials: {len(self.materials)}")
        print(f"  - Roadmap Checklist: {len(self.roadmap)}")
        print(f"  - Portfolio Projects: {len(self.projects)}")

        return {
            "exercises": self.exercises,
            "materials": self.materials,
            "roadmap": self.roadmap,
            "projects": self.projects
        }

    def parse_local_workbook(self, file_path: str):
        """Parse workbooks with multiple custom CP sheets."""
        try:
            wb = openpyxl.load_workbook(file_path, data_only=True)
        except Exception as e:
            print(f"[Processor] Error opening {file_path}: {e}")
            return

        for sheet_name in wb.sheetnames:
            sheet = wb[sheet_name]
            s_lower = sheet_name.lower().strip()

            # Handle Checklist / Algorithm Review sheets
            if "danh sách thuật toán" in s_lower or "thuật toán" in s_lower:
                self.parse_algorithm_checklist(sheet, sheet_name)
                continue

            # Handle Notes / Goals
            if s_lower == "note":
                self.parse_notes_sheet(sheet)
                continue

            # Standard Problem & Material sheets
            self.parse_problem_sheet(sheet, sheet_name)

    def parse_problem_sheet(self, sheet, sheet_name: str):
        """Scans grid rows for problem links, notes, ratings, and tags."""
        rows = list(sheet.iter_rows(values_only=True))
        if not rows:
            return

        for r_idx, row in enumerate(rows):
            # Check for empty row
            if not any(row):
                continue

            for col_idx, cell in enumerate(row):
                if not isinstance(cell, str):
                    continue

                # Find any HTTP/HTTPS links
                urls = re.findall(r"https?://[^\s,]+", cell)
                for url in urls:
                    url = url.strip().rstrip(").,'\"")
                    if not url or url in self.seen_urls:
                        continue
                    self.seen_urls.add(url)

                    # Gather neighboring cells for context (notes, ratings, tags)
                    context_cells = []
                    for delta in [-2, -1, 1, 2, 3]:
                        n_idx = col_idx + delta
                        if 0 <= n_idx < len(row) and row[n_idx] is not None:
                            val_str = str(row[n_idx]).strip()
                            if val_str and not val_str.startswith("http"):
                                context_cells.append(val_str)

                    context_text = " ".join(context_cells)

                    # Determine rating if any
                    rating_val = None
                    for c_val in context_cells:
                        cleaned = c_val.replace(".0", "").strip()
                        if cleaned.isdigit() and 800 <= int(cleaned) <= 3800:
                            rating_val = int(cleaned)
                            break

                    platform = detect_platform(url)

                    # Classify as Exercise vs Material
                    if platform in ["YouTube", "Material"] or any(k in url.lower() for k in ["blog", "wiki", "youtube", "tutorial", "docs.google"]):
                        # Learning Material / Blog / Video
                        title = context_text if len(context_text) > 3 else f"{platform} Resource"
                        primary_topic, tags = categorize_item(context_text, sheet_name)
                        self.materials.append({
                            "id": f"mat_{len(self.materials) + 1}",
                            "title": title[:100],
                            "url": url,
                            "platform": platform,
                            "topic": primary_topic,
                            "tags": tags,
                            "source_sheet": sheet_name,
                            "notes": context_text[:200]
                        })
                    else:
                        # CP Exercise
                        pid, ptitle = extract_problem_info(url)
                        primary_topic, tags = categorize_item(context_text, sheet_name)
                        diff_label, num_rating = normalize_difficulty(rating_val, context_text)

                        self.exercises.append({
                            "id": pid or f"prob_{len(self.exercises) + 1}",
                            "title": ptitle,
                            "url": url,
                            "platform": platform,
                            "topic": primary_topic,
                            "tags": tags,
                            "difficulty": diff_label,
                            "rating": num_rating if num_rating > 0 else 1500,
                            "notes": context_text[:200],
                            "source_sheet": sheet_name,
                            "status": "Ready to Solve"
                        })

    def parse_algorithm_checklist(self, sheet, sheet_name: str):
        """Parses VOI/ICPC algorithm checklist topics, difficulties, and completion status."""
        rows = list(sheet.iter_rows(values_only=True))
        current_category = "Đồ thị"
        last_topic = ""

        for row in rows:
            if not any(row):
                continue
            cells = [c for c in row if c is not None and str(c).strip()]
            if not cells:
                continue

            first_val = str(row[0]).strip().lower() if row[0] is not None else ""

            # Check if this row is a category header (e.g. 'Đồ thị', 'Quy hoạch động', 'Cấu trúc dữ liệu')
            if len(cells) == 1 and not str(cells[0]).startswith("http") and not first_val in ["true", "false", "✓"]:
                text = str(cells[0]).strip()
                if "review" not in text.lower() and "hoàn thành" not in text.lower():
                    current_category = text
                continue

            # Check for header row
            if "link wiki" in [str(c).lower() for c in cells] or "độ khó" in [str(c).lower() for c in cells]:
                continue

            # Standard checklist row
            is_completed = first_val in ["true", "✓", "1", "v", "yes"]
            topic_name = str(row[1]).strip() if len(row) > 1 and row[1] is not None else ""
            if topic_name:
                last_topic = topic_name
            else:
                topic_name = last_topic

            item_title = str(row[2]).strip() if len(row) > 2 and row[2] is not None else ""
            difficulty_raw = str(row[3]).strip() if len(row) > 3 and row[3] is not None else "1.0"
            wiki_or_notes = str(row[4]).strip() if len(row) > 4 and row[4] is not None else ""

            # If item_title is a URL, add it to exercises or link
            link = ""
            if item_title.startswith("http"):
                link = item_title
                item_title = f"{topic_name} Practice"
            elif any(str(c).startswith("http") for c in cells):
                link = next((str(c) for c in cells if str(c).startswith("http")), "")

            display_name = item_title if item_title else topic_name
            if display_name and display_name.lower() not in ["topic", "độ khó", "link wiki", "none"]:
                self.roadmap.append({
                    "id": f"road_{len(self.roadmap) + 1}",
                    "name": display_name,
                    "topic": topic_name or current_category,
                    "category": current_category,
                    "difficulty": f"Level {difficulty_raw.replace('.0', '')}" if difficulty_raw else "Level 1",
                    "completed": is_completed,
                    "link": link,
                    "notes": wiki_or_notes[:200]
                })

    def parse_notes_sheet(self, sheet):
        """Parses goal tracking and unlearned topics from Note sheet."""
        rows = list(sheet.iter_rows(values_only=True))
        for row in rows:
            for c in row:
                if isinstance(c, str) and c.strip():
                    text = c.strip()
                    if text.startswith(">") or "bài trước VOI" in text or "Nhì QG" in text or "TST" in text:
                        self.projects.append({
                            "id": f"proj_goal_{len(self.projects)+1}",
                            "title": f"Goal: {text}",
                            "category": "Target Milestone",
                            "description": "Competitive Programming Target Goal & Achievements",
                            "status": "In Progress",
                            "tags": ["Milestone", "Target", "VOI"]
                        })

    def try_ingest_google_sheets(self):
        """Reads data from a Master Google Sheet if gspread and credentials are valid."""
        if not GOOGLE_SPREADSHEET_ID:
            print("[Processor] Note: GOOGLE_SPREADSHEET_ID not provided. Skipping Google Sheets ingestion.")
            return

        cred_dict = get_service_account_dict()
        if not cred_dict:
            print("[Processor] Note: No service account credentials found for Google Sheets. Skipping.")
            return

        try:
            import gspread
            gc = gspread.service_account_from_dict(cred_dict)
            sh = gc.open_by_key(GOOGLE_SPREADSHEET_ID)
            print(f"[Processor] Successfully connected to Google Sheet: {sh.title}")

            for ws in sh.worksheets():
                records = ws.get_all_records()
                for r in records:
                    url = r.get("url") or r.get("URL") or r.get("Link") or ""
                    if url and url not in self.seen_urls:
                        self.seen_urls.add(url)
                        platform = detect_platform(url)
                        title = r.get("title") or r.get("Title") or r.get("Problem") or ""
                        topic = r.get("topic") or r.get("Topic") or "General CP"
                        tags_str = r.get("tags") or r.get("Tags") or ""
                        tags = [t.strip() for t in str(tags_str).split(",") if t.strip()] or [topic]
                        diff = r.get("difficulty") or r.get("Difficulty") or "Medium"
                        rating = r.get("rating") or r.get("Rating") or 1500

                        self.exercises.append({
                            "id": r.get("id") or extract_problem_info(url)[0],
                            "title": title or extract_problem_info(url)[1],
                            "url": url,
                            "platform": platform,
                            "topic": topic,
                            "tags": tags,
                            "difficulty": diff,
                            "rating": int(rating) if str(rating).isdigit() else 1500,
                            "notes": r.get("notes") or "",
                            "source_sheet": f"GoogleSheet:{ws.title}",
                            "status": r.get("status") or "Ready to Solve"
                        })
        except Exception as e:
            print(f"[Processor] Warning during Google Sheets ingestion: {e}")

    def add_default_portfolio_projects(self):
        """Adds curated CP portfolio projects, contest templates, and tooling."""
        defaults = [
            {
                "id": "proj-cp-templates",
                "title": "C++ Competitive Programming Library & Templates",
                "category": "Algorithm Library",
                "description": "Production-grade C++20 algorithms: HLD, Dynamic Segment Tree, Centroid Decomposition, CHT, SOS DP, Flow, Matrix Exponentiation.",
                "url": "https://github.com/",
                "tags": ["C++20", "Templates", "Data Structures", "Graph"],
                "status": "Active"
            },
            {
                "id": "proj-cp-lms-portfolio",
                "title": "Automated CP Learning Management System",
                "category": "Web & Automation",
                "description": "Automated learning dashboard syncing 700+ curated CP problems, lectures, and VOI milestones between Google Sheets, Firestore, and GitHub Pages.",
                "url": "https://github.com/",
                "tags": ["Python", "Firestore", "GitHub Pages", "TailwindCSS"],
                "status": "Completed"
            },
            {
                "id": "proj-codeforces-tracker",
                "title": "Codeforces Contest & Problem Tracker",
                "category": "Analytics Tool",
                "description": "Rule-based analysis engine monitoring problem solving velocity, topic strengths/weaknesses, and rating progression towards Master rank.",
                "url": "https://codeforces.com/",
                "tags": ["Codeforces API", "Data Analysis", "Python"],
                "status": "In Progress"
            }
        ]
        # Avoid duplicate ids
        existing_ids = {p["id"] for p in self.projects}
        for d in defaults:
            if d["id"] not in existing_ids:
                self.projects.append(d)

    def enrich_with_web_crawling(self, sample_limit: int = 15):
        """
        Crawls online websites (Codeforces API or Web Scraper) to enrich
        problem titles, tags, and ratings where missing.
        Keeps request rate low and handles failures gracefully.
        """
        print(f"[Crawler] Enriching metadata for up to {sample_limit} items...")
        count = 0
        for item in self.exercises:
            if count >= sample_limit:
                break
            url = item["url"]
            # Example: enrich VNOI title if generic
            if item["platform"] == "VNOI" and "VNOI " in item["title"]:
                try:
                    resp = requests.get(url, headers=self.headers, timeout=4)
                    if resp.status_code == 200:
                        soup = BeautifulSoup(resp.text, "html.parser")
                        h2 = soup.find("h2") or soup.find("h1")
                        if h2:
                            clean_t = h2.get_text(strip=True)
                            if clean_t:
                                item["title"] = f"VNOI - {clean_t}"
                                count += 1
                                time.sleep(0.5)
                except Exception:
                    pass

def run_scraper(use_web_enrichment: bool = False) -> Dict[str, List[Dict[str, Any]]]:
    """Helper entry point for scraper module."""
    processor = CPDataProcessor(use_web_enrichment=use_web_enrichment)
    return processor.process_all()

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    data = run_scraper(use_web_enrichment=False)
    print(f"Scraped {len(data['exercises'])} exercises, {len(data['materials'])} materials.")

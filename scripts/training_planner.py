"""
Automated Competitive Programming Training & Review Generator
Specially tailored for DeruckLoveNewTechnology - ICPC & Olympic Tin học Sinh viên.
Zero-token automated pipeline: Crawls, filters, categorizes, and formats Excel.
"""

import os
import sys
import json
import datetime
import requests
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from bs4 import BeautifulSoup
from pathlib import Path
from collections import defaultdict

# Force UTF-8 encoding on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

PROJECT_ROOT = Path(r"D:\0.CP\Webcanhan")
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.tagger import detect_platform, extract_problem_info, normalize_difficulty, TOPIC_RULES, categorize_item

# Styling Constants matching "Bản sao của code cùng Coản Coản.xlsx"
FONT_NAME = "Times New Roman"

FILL_HEADER_YELLOW = PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid")
FILL_HEADER_BLUE = PatternFill(start_color="CFE2F3", end_color="CFE2F3", fill_type="solid")
FILL_HEADER_PEACH = PatternFill(start_color="FCE5CD", end_color="FCE5CD", fill_type="solid")
FILL_HEADER_PURPLE = PatternFill(start_color="D9D2E9", end_color="D9D2E9", fill_type="solid")

FILL_SOLVED_LIME = PatternFill(start_color="00FF00", end_color="00FF00", fill_type="solid")
FILL_REVIEW_WARNING = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid") # Soft yellow alert
FILL_NOTE_BLUE = PatternFill(start_color="CFE2F3", end_color="CFE2F3", fill_type="solid")
FILL_RATING_PEACH = PatternFill(start_color="FCE5CD", end_color="FCE5CD", fill_type="solid")
FILL_DATE_YELLOW = PatternFill(start_color="FFFFF2", end_color="FFFFF2", fill_type="solid")
FILL_MOCK_CONTEST = PatternFill(start_color="F4CCCC", end_color="F4CCCC", fill_type="solid") # Soft coral for mock tests

FONT_TITLE_RED = Font(name=FONT_NAME, size=20, bold=True, color="EA4335")
FONT_TITLE_DARK = Font(name=FONT_NAME, size=18, bold=True, color="000000")
FONT_COUNT_RED = Font(name=FONT_NAME, size=14, bold=True, color="EA4335")
FONT_HEADER_BOLD = Font(name=FONT_NAME, size=12, bold=True, color="000000")
FONT_LINK_BLUE = Font(name=FONT_NAME, size=11, bold=False, color="0000FF", underline="single")
FONT_LINK_SOLVED = Font(name=FONT_NAME, size=11, bold=False, color="0000FF", underline="single")
FONT_TEXT_REGULAR = Font(name=FONT_NAME, size=11, bold=False, color="000000")
FONT_TEXT_BOLD = Font(name=FONT_NAME, size=11, bold=True, color="000000")

BORDER_THIN = Border(
    left=Side(style='thin', color='D9D9D9'),
    right=Side(style='thin', color='D9D9D9'),
    top=Side(style='thin', color='D9D9D9'),
    bottom=Side(style='thin', color='D9D9D9')
)
BORDER_HEADER = Border(
    left=Side(style='thin', color='000000'),
    right=Side(style='thin', color='000000'),
    top=Side(style='medium', color='000000'),
    bottom=Side(style='medium', color='000000')
)

ALIGN_LEFT = Alignment(horizontal='left', vertical='center')
ALIGN_CENTER = Alignment(horizontal='center', vertical='center')
ALIGN_RIGHT = Alignment(horizontal='right', vertical='center')


class CPAutomatedManager:
    def __init__(self, handle: str = "DeruckLoveNewTechnology"):
        self.handle = handle
        self.now = datetime.datetime(2026, 10, 16)
        self.cutoff_date = self.now - datetime.timedelta(days=60) # 2 months ago
        self.cf_problems = {}
        self.ladder_problems = []
        self.original_sheets = {}
        self.old_hard_problems = []
        self.topic_problems = defaultdict(lambda: {"left": [], "right": []})
        self.trick_notes = []

    def fetch_all_sources(self):
        """Fetches from Codeforces API, Ladder 16, and reads existing Excel workbooks."""
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Step 1: Querying Codeforces API for {self.handle}...")
        cf_url = f"https://codeforces.com/api/user.status?handle={self.handle}&from=1&count=10000"
        try:
            resp = requests.get(cf_url, timeout=30)
            if resp.status_code == 200:
                data = resp.json()
                if data.get("status") == "OK":
                    submissions = data.get("result", [])
                    print(f"  -> Fetched {len(submissions)} submissions from Codeforces.")
                    for sub in submissions:
                        prob = sub.get("problem", {})
                        cid = prob.get("contestId")
                        idx = prob.get("index")
                        if not cid or not idx:
                            continue
                        key = f"{cid}{idx}"
                        sub_time = datetime.datetime.fromtimestamp(sub["creationTimeSeconds"])
                        verdict = sub.get("verdict")

                        if key not in self.cf_problems:
                            self.cf_problems[key] = {
                                "key": key,
                                "cid": cid,
                                "idx": idx,
                                "name": prob.get("name", f"Problem {idx}"),
                                "rating": prob.get("rating"),
                                "tags": prob.get("tags", []),
                                "url": f"https://codeforces.com/problemset/problem/{cid}/{idx}",
                                "solved": False,
                                "last_sub_time": sub_time,
                                "solved_time": None
                            }

                        p = self.cf_problems[key]
                        if sub_time > p["last_sub_time"]:
                            p["last_sub_time"] = sub_time
                        if verdict == "OK":
                            p["solved"] = True
                            if p["solved_time"] is None or sub_time > p["solved_time"]:
                                p["solved_time"] = sub_time
        except Exception as e:
            print(f"  [Notice] Could not load from Codeforces API: {e}")

        # 2. Ladder 16
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Step 2: Fetching Ladder 16 (1700 <= Rating <= 1799)...")
        ladder_url = "https://earthshakira.github.io/a2oj-clientside/server/Ladder16.html"
        try:
            l_resp = requests.get(ladder_url, timeout=20)
            l_resp.encoding = "utf-8"
            soup = BeautifulSoup(l_resp.text, "html.parser")
            tables = soup.find_all("table")
            prob_table = tables[1] if len(tables) > 1 else tables[0]
            for row in prob_table.find_all("tr")[1:]:
                cols = row.find_all("td")
                if len(cols) >= 4:
                    idx = cols[0].text.strip()
                    link_tag = cols[1].find("a")
                    pname = link_tag.text.strip() if link_tag else cols[1].text.strip()
                    href = link_tag.get("href") if link_tag else ""
                    judge = cols[2].text.strip()
                    diff = cols[3].text.strip()

                    cid = None
                    pidx = None
                    if "codeforces.com" in href:
                        parts = href.rstrip("/").split("/")
                        if len(parts) >= 2:
                            pidx = parts[-1]
                            cid = parts[-2]

                    key = f"{cid}{pidx}" if cid and pidx else None
                    lp = {
                        "ladder_idx": int(idx),
                        "name": pname,
                        "url": href,
                        "judge": judge,
                        "diff_level": int(diff),
                        "cid": cid,
                        "pidx": pidx,
                        "key": key,
                        "solved": False,
                        "last_sub": None,
                        "rating": None,
                        "tags": [],
                        "review_needed": False
                    }
                    if key and key in self.cf_problems:
                        cfp = self.cf_problems[key]
                        lp["solved"] = cfp["solved"]
                        lp["last_sub"] = cfp["last_sub_time"]
                        lp["rating"] = cfp["rating"] or (1600 + int(diff) * 100)
                        lp["tags"] = cfp["tags"]
                        if cfp["solved"]:
                            lp["review_needed"] = (cfp["last_sub_time"] <= self.cutoff_date)
                    self.ladder_problems.append(lp)
            print(f"  -> Parsed {len(self.ladder_problems)} problems from Ladder 16.")
        except Exception as e:
            print(f"  [Error] Ladder 16 fetch failed: {e}")

        # 3. Read original workbook
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Step 3: Loading original 'Bản sao của code cùng Coản Coản.xlsx'...")
        orig_path = PROJECT_ROOT / "Bản sao của code cùng Coản Coản.xlsx"
        if orig_path.exists():
            wb = openpyxl.load_workbook(orig_path, data_only=True)
            for sname in wb.sheetnames:
                ws = wb[sname]
                rows = []
                for r in range(1, ws.max_row + 1):
                    row_data = []
                    has_val = False
                    for c in range(1, min(ws.max_column + 1, 15)):
                        cell = ws.cell(r, c)
                        val = cell.value
                        fill = cell.fill.start_color.rgb if cell.fill and cell.fill.start_color else None
                        is_solved_color = (fill == "FF00FF00" or fill == "00FF00")
                        row_data.append({
                            "val": val,
                            "solved": is_solved_color,
                            "fill": fill
                        })
                        if val is not None:
                            has_val = True
                    if has_val:
                        rows.append(row_data)
                self.original_sheets[sname] = rows
            print(f"  -> Loaded {len(self.original_sheets)} sheets from existing workbook.")

    def filter_forgotten_hard_problems(self):
        """
        Extracts problems at hard level (Rating >= 1600) solved >= 2 months ago and untouched since.
        """
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Step 4: Filtering forgotten hard problems (Rating >= 1600, untouched >= 2 months)...")
        candidates = []

        # From Codeforces verified submissions
        for p in self.cf_problems.values():
            if p["solved"] and p["rating"] and p["rating"] >= 1600:
                if p["last_sub_time"] <= self.cutoff_date:
                    days_ago = (self.now - p["last_sub_time"]).days
                    
                    # Classify topic
                    topic_str = " ".join(p.get("tags", []))
                    primary_topic, specific_tags = categorize_item(f"{p['name']} {topic_str}")
                    
                    # Determine ICPC/OLP review priority
                    r = p["rating"]
                    if r >= 2400:
                        priority = "P2 - Master/TST (2400+)"
                    elif r >= 2000:
                        priority = "P1 - Cực kỳ quan trọng (2000-2300)"
                    elif r >= 1800:
                        priority = "P1 - Trọng tâm ICPC/OLP (1800-1900)"
                    else:
                        priority = "P3 - Luyện phản xạ nhanh (1600-1700)"

                    candidates.append({
                        "key": p["key"],
                        "name": p["name"],
                        "url": p["url"],
                        "rating": p["rating"],
                        "platform": "Codeforces",
                        "tags": p.get("tags", []),
                        "topic": primary_topic,
                        "last_sub": p["last_sub_time"],
                        "days_ago": days_ago,
                        "priority": priority,
                        "source": "Codeforces Submissions"
                    })

        # Also check Ladder 16 old solved problems (if not already included)
        seen_keys = {c["key"] for c in candidates}
        for lp in self.ladder_problems:
            if lp.get("review_needed") and lp.get("key") and lp["key"] not in seen_keys:
                days_ago = (self.now - lp["last_sub"]).days if lp.get("last_sub") else 365
                primary_topic, specific_tags = categorize_item(f"{lp['name']} {' '.join(lp.get('tags', []))}")
                r = lp.get("rating") or (1600 + lp["diff_level"] * 100)
                candidates.append({
                    "key": lp["key"],
                    "name": lp["name"],
                    "url": lp["url"],
                    "rating": r,
                    "platform": "Codeforces",
                    "tags": lp.get("tags", []),
                    "topic": primary_topic,
                    "last_sub": lp.get("last_sub"),
                    "days_ago": days_ago,
                    "priority": "P1 - Ladder 16 Review",
                    "source": "A2OJ Ladder 16"
                })

        # Sort candidates by rating descending, then days_ago descending
        candidates.sort(key=lambda x: (x["rating"], x["days_ago"]), reverse=True)
        self.old_hard_problems = candidates
        print(f"  -> Total forgotten hard problems filtered: {len(self.old_hard_problems)}")

    def build_schedule_data(self):
        """
        Creates a concrete 7-Week Training & Mock Testing Schedule for ICPC & Olympic Tin học Sinh viên.
        Starting Monday 2026-10-19 through Sunday 2026-12-06.
        """
        schedule = []
        cur_date = datetime.date(2026, 10, 19)

        # 7 Weeks breakdown
        weeks_plan = [
            # Week 1
            {
                "week_num": 1,
                "theme": "Tuần 1: Củng cố Cây (Tree), DSU nâng cao & Đường đi ngắn nhất (Shortest Path)",
                "days": [
                    ("Thứ Hai", "Ôn tập Lý thuyết & Re-solve bài cũ: DSU Tree & Small to Large", "https://codeforces.com/contest/1416/problem/D", "Codeforces 1416D - DSU Tree", "2600", "Re-solve bài cũ", "Chưa làm"),
                    ("Thứ Ba", "Luyện tập Ladder 16: Graph & Shortest Paths", "https://codeforces.com/contest/295/problem/B", "Codeforces 295B - Greg and Graph (Floyd-Warshall trick)", "1700", "Ladder 16 Re-solve", "Chưa làm"),
                    ("Thứ Tư", "Kiểm tra cá nhân OLP Mini-Contest #1 (2.5h)", "https://codeforces.com/contest/1996", "Codeforces Round 962 (Div. 3/2)", "1200-1800", "Mini Mock Test", "Chưa làm"),
                    ("Thứ Năm", "Re-solve bài cũ: Mo on Tree & Rerooting", "https://codeforces.com/problemset/problem/375/D", "Codeforces 375D - Mo on tree", "2400", "Re-solve bài cũ", "Chưa làm"),
                    ("Thứ Sáu", "Thực hành Ladder 16: DFS/BFS & Constructive", "https://codeforces.com/problemset/problem/217/A", "Codeforces 217A - Ice Skating", "1400", "Ladder 16", "Chưa làm"),
                    ("Thứ Bảy", "Upsolving & Tối ưu hóa Code Template (Tree/Graph)", "https://oj.vnoi.info/problem/diffgraph", "LQDOJ diffgraph - Small to large, reroot", "Hard", "VNOI/LQDOJ Practice", "Chưa làm"),
                    ("Chủ Nhật", "MOCK TEST 1: ICPC Regional Simulation 5 Giờ (Team Contest #1)", "https://codeforces.com/gym/104021", "2022-2023 ICPC Asia Yokohama Regional", "ICPC Team", "FULL MOCK TEST", "Chưa làm"),
                ]
            },
            # Week 2
            {
                "week_num": 2,
                "theme": "Tuần 2: Dynamic Programming nâng cao (SOS DP, CHT, Bitmask, Tree DP)",
                "days": [
                    ("Thứ Hai", "Ôn tập SOS DP & Bitmask: Re-solve các bài kinh điển", "https://cses.fi/problemset/task/1654", "CSES 1654 - SOS DP", "2100", "Re-solve", "Chưa làm"),
                    ("Thứ Ba", "Re-solve bài cũ: SOS DP & Bao hàm loại trừ", "https://codeforces.com/problemset/problem/449/D", "Codeforces 449D - Jzzhu and Numbers", "2400", "Re-solve bài cũ", "Chưa làm"),
                    ("Thứ Tư", "Kiểm tra cá nhân OLP Mock Contest #2 (3h)", "https://codeforces.com/contest/1987", "Codeforces Round 955 (Div. 2/1)", "1500-2200", "OLP Mock Test", "Chưa làm"),
                    ("Thứ Năm", "Convex Hull Trick & Li Chao Tree / Alien's Trick", "https://codeforces.com/problemset/problem/1715/E", "Codeforces 1715E - Long Way Home (Dijkstra + CHT)", "2400", "Re-solve bài cũ", "Chưa làm"),
                    ("Thứ Sáu", "Ladder 16: DP & Strings (KMP + DP)", "https://codeforces.com/problemset/problem/346/B", "Codeforces 346B - Lucky Common Subsequence", "2000", "Ladder 16 Re-solve", "Chưa làm"),
                    ("Thứ Bảy", "Upsolve các bài DP chưa hoàn thành & Team Strategy", "https://oj.vnoi.info/problem/voi21_or", "VOI 2021 OR - SOS DP", "VOI", "VOI Practice", "Chưa làm"),
                    ("Chủ Nhật", "MOCK TEST 2: ICPC Regional Simulation 5 Giờ (Team Contest #2)", "https://codeforces.com/gym/104114", "2022 ICPC Asia Can Tho Regional Contest", "ICPC Team", "FULL MOCK TEST", "Chưa làm"),
                ]
            },
            # Week 3
            {
                "week_num": 3,
                "theme": "Tuần 3: Cấu trúc dữ liệu nâng cao & Chia căn (Mo, Sqrt Decomposition, SegTree)",
                "days": [
                    ("Thứ Hai", "Chia căn & Sqrt Decomposition: Re-solve bài cũ", "https://codeforces.com/problemset/problem/13/E", "Codeforces 13E - Holes (Chia căn)", "2700", "Re-solve bài cũ", "Chưa làm"),
                    ("Thứ Ba", "Ladder 16: Segment Tree & Modulo Trick", "https://codeforces.com/problemset/problem/438/D", "Codeforces 438D - The Child and Sequence", "2300", "Ladder 16 Re-solve", "Chưa làm"),
                    ("Thứ Tư", "Kiểm tra cá nhân OLP Mock Contest #3 (3.5h - CTDL & DP)", "https://oj.vnoi.info/problem/coci1920_o_paint", "COCI 1920 Paint - Chia căn lớn bé & DSU", "Hard", "OLP Mock Test", "Chưa làm"),
                    ("Thứ Năm", "Persistent Segment Tree & Treap cơ bản", "https://codeforces.com/contest/986/problem/E", "Codeforces 986E - Prince's Problem (Tree, DS, Math)", "2800", "Re-solve bài cũ", "Chưa làm"),
                    ("Thứ Sáu", "Ladder 16: Data Structures & Hashing", "https://codeforces.com/problemset/problem/126/B", "Codeforces 126B - Password", "1700", "Ladder 16 Re-solve", "Chưa làm"),
                    ("Thứ Bảy", "Review Template SegTree Lazy & Fenwick 2D", "https://oj.vnoi.info/problem/segtree_itteq1", "VNOI ITTEQ1 - Segment Tree nâng cao", "Hard", "Review Template", "Chưa làm"),
                    ("Chủ Nhật", "MOCK TEST 3: ICPC Regional Simulation 5 Giờ (Team Contest #3)", "https://codeforces.com/gym/103449", "2021-2022 ICPC Asia Hanoi Regional Contest", "ICPC Team", "FULL MOCK TEST", "Chưa làm"),
                ]
            },
            # Week 4
            {
                "week_num": 4,
                "theme": "Tuần 4: Toán học, Tổ hợp, Nghịch đảo Modulo & Hình học Sweepline",
                "days": [
                    ("Thứ Hai", "Bao hàm loại trừ & Lucas Theorem: Re-solve bài cũ", "https://codeforces.com/contest/1043/problem/F", "Codeforces 1043F - Make It One (Bao hàm)", "2400", "Re-solve bài cũ", "Chưa làm"),
                    ("Thứ Ba", "Toán chia kẹo Euler & Nghịch đảo modulo", "https://oj.vnoi.info/problem/c11tct", "VNOI c11tct - Chia kẹo, Lucas theory", "Hard", "VNOI Math", "Chưa làm"),
                    ("Thứ Tư", "Kiểm tra cá nhân OLP Mock Contest #4 (3h - Toán & Tổ hợp)", "https://codeforces.com/contest/1974", "Codeforces Round 946", "Div.3/2", "OLP Mock Test", "Chưa làm"),
                    ("Thứ Năm", "Hình học Sweepline & Convex Hull: Re-solve bài cũ", "https://codeforces.com/contest/529/problem/C", "Codeforces 529C - Sweepline (Rooks Defender)", "2200", "Re-solve bài cũ", "Chưa làm"),
                    ("Thứ Sáu", "Hình học tính toán & Bao lồi (Monotone Chain)", "https://oj.vnoi.info/problem/cavli", "VNOI cavli - Hình học, Bao lồi", "Hard", "Geometry", "Chưa làm"),
                    ("Thứ Bảy", "Ladder 16: Math & Number Theory", "https://codeforces.com/problemset/problem/354/C", "Codeforces 354C - Vasya and Beautiful Arrays", "2100", "Ladder 16 Re-solve", "Chưa làm"),
                    ("Chủ Nhật", "MOCK TEST 4: ICPC Regional Simulation 5 Giờ (Team Contest #4)", "https://codeforces.com/gym/104639", "2023-2024 ICPC Asia Hue Regional Contest", "ICPC Team", "FULL MOCK TEST", "Chưa làm"),
                ]
            },
            # Week 5
            {
                "week_num": 5,
                "theme": "Tuần 5: Thuật toán Xâu ký tự (Strings), Luồng cực đại (Flow) & Game Theory",
                "days": [
                    ("Thứ Hai", "KMP, Z-function & Hash 2D: Re-solve bài cũ", "https://codeforces.com/problemset/problem/432/D", "Codeforces 432D - Prefixes and Suffixes", "2000", "Ladder 16 Re-solve", "Chưa làm"),
                    ("Thứ Ba", "Aho-Corasick & DP trên Trie", "https://lqdoj.edu.vn/problem/lqdoj2022r4ugpalind", "LQDOJ ugpalind - DP + Aho-Corasick", "Hard", "LQDOJ String", "Chưa làm"),
                    ("Thứ Tư", "Kiểm tra cá nhân OLP Mock Contest #5 (3.5h - Đề Siêu Cúp / Chuyên Tin)", "https://cms.ioi-jp.org/joi2023-sp1-open", "JOI Spring Camp 2023 Contest 1", "JOI", "OLP Mock Test", "Chưa làm"),
                    ("Thứ Năm", "Luồng cực đại (Dinic) & Cặp ghép cực đại", "https://codeforces.com/contest/944/problem/F", "Codeforces 944F - CTDL, Game", "2400", "Re-solve bài cũ", "Chưa làm"),
                    ("Thứ Sáu", "Game Theory: Nim, Sprague-Grundy & Nhận xét Adhoc", "https://codeforces.com/contest/2181/problem/F", "Codeforces 2181F - Fragmented Nim", "1600", "Re-solve bài cũ", "Chưa làm"),
                    ("Thứ Bảy", "Ladder 16: KMP String Differencing", "https://codeforces.com/problemset/problem/471/D", "Codeforces 471D - MUH and Cube Walls", "1800", "Ladder 16 Re-solve", "Chưa làm"),
                    ("Chủ Nhật", "MOCK TEST 5: ICPC Vietnam National Simulation 5 Giờ (Team Contest #5)", "https://codeforces.com/gym/104725", "2023 ICPC Vietnam National Contest", "ICPC Team", "FULL MOCK TEST", "Chưa làm"),
                ]
            },
            # Week 6
            {
                "week_num": 6,
                "theme": "Tuần 6: Tổng lực Luyện đề, Chiến thuật Team & Stress Testing",
                "days": [
                    ("Thứ Hai", "Upsolving bài khó Mock Test 5 & Phân tích bug phòng thi", "https://codeforces.com/contest/1442/problem/C", "Codeforces 1442C - Graph, Shortest Path", "2400", "Re-solve bài cũ", "Chưa làm"),
                    ("Thứ Ba", "Re-solve bài cũ: DSU on Tree / Small to large", "https://codeforces.com/problemset/problem/570/D", "Codeforces 570D - Tree Requests", "2200", "Ladder 16 Re-solve", "Chưa làm"),
                    ("Thứ Tư", "Kiểm tra cá nhân OLP Mock Contest #6 (3h - Đề Olympic các năm)", "https://oj.vnoi.info/problem/voi21_rmat", "VOI 2021 RMAT - Observation & Matrix", "VOI", "OLP Mock Test", "Chưa làm"),
                    ("Thứ Năm", "Kiểm tra và hoàn thiện ICPC Team Notebook (Codeforces Template)", "https://codeforces.com/contest/1697/problem/E", "Codeforces 1697E - Graph, DP, Tổ hợp", "2400", "Re-solve bài cũ", "Chưa làm"),
                    ("Thứ Sáu", "Thực hành Stress Test (Viết script sinh test ngẫu nhiên đối chiếu)", "https://dmoj.ca/problem/coci06c1p6", "COCI 06 c1p6 - Hash 2D", "Hard", "Stress Test Lab", "Chưa làm"),
                    ("Thứ Bảy", "Review toàn bộ các Trick lỏ & bẫy tràn số (Overflow, MOD, 1LL<<x)", "https://codeforces.com/contest/786/problem/B", "Codeforces 786B - Dijkstra đoạn", "2200", "Trick lỏ", "Chưa làm"),
                    ("Chủ Nhật", "MOCK TEST 6: FINAL FULL ICPC SIMULATION 5 GIỜ", "https://codeforces.com/gym/103960", "2022-2023 ICPC Brazil Subregional / Asia Archive", "ICPC Team", "FINAL MOCK TEST", "Chưa làm"),
                ]
            },
            # Week 7
            {
                "week_num": 7,
                "theme": "Tuần 7: Tapering, Thư giãn trí não & Rà soát lần cuối trước giờ G",
                "days": [
                    ("Thứ Hai", "Re-solve nhẹ nhàng: Ladder 16 các bài trung bình (Lấy cảm giác tay)", "https://codeforces.com/problemset/problem/476/B", "Codeforces 476B - Dreamoon and WiFi", "1300", "Ladder 16", "Chưa làm"),
                    ("Thứ Ba", "Rà soát lại danh sách 137 bài khó đã ôn tập", "https://codeforces.com/contest/2181/problem/D", "Codeforces 2181D - Doorway (BS + DS)", "2000", "Re-solve nhẹ", "Chưa làm"),
                    ("Thứ Tư", "Kiểm tra Template Notebook, máy chấm, compiler flags (-O2, -fsanitize)", "https://codeforces.com", "Chuẩn bị môi trường thi & template in ấn", "Preparation", "Checklist", "Chưa làm"),
                    ("Thứ Năm", "Chiến thuật tâm lý: Phân bổ thời gian, nhận diện bài bẫy", "https://codeforces.com", "Họp chiến thuật team ICPC", "Strategy", "Team Meeting", "Chưa làm"),
                    ("Thứ Sáu", "Nghỉ ngơi, ngủ đủ giấc, chuẩn bị thẻ sinh viên & CCCD", "https://codeforces.com", "Nghỉ ngơi chuẩn bị cho ngày thi", "Rest", "Rest & Recharge", "Hoàn thành"),
                    ("Thứ Bảy", "NGÀY THI OLYMPIC TIN HỌC SINH VIÊN (CÁ NHÂN)", "https://olp.vn", "Olympic Tin học Sinh viên Toàn quốc", "CONTEST", "OFFICIAL CONTEST", "Đến giờ G!"),
                    ("Chủ Nhật", "NGÀY THI ICPC REGIONAL (TEAM 3 NGƯỜI / 5 GIỜ)", "https://icpc.global", "ICPC Asia Regional Contest", "CONTEST", "OFFICIAL CONTEST", "Đến giờ G!"),
                ]
            }
        ]

        day_offset = 0
        for w in weeks_plan:
            for day_name, activity, link, prob_name, rating, session_type, status in w["days"]:
                calc_date = cur_date + datetime.timedelta(days=day_offset)
                schedule.append({
                    "date": calc_date,
                    "day_name": day_name,
                    "week_num": w["week_num"],
                    "week_theme": w["theme"],
                    "activity": activity,
                    "link": link,
                    "problem_name": prob_name,
                    "rating": rating,
                    "session_type": session_type,
                    "status": status
                })
                day_offset += 1

        return schedule

    def populate_topic_sheets(self, wb: openpyxl.Workbook):
        """
        Populates the algorithmic topic sheets matching the exact structure and layout of 'Bản sao của code cùng Coản Coản.xlsx':
        1. Tree & Graph
        2. DP & Greedy
        3. Mo, chia căn, ctdl
        4. Math, hình, sweepline
        5. Adhoc-Game, String
        """
        # Map of sheet configurations
        sheet_configs = [
            {
                "name": "Tree & Graph",
                "left_title": "Tree",
                "left_count_range": "A2:A250",
                "right_title": "Graph",
                "right_count_range": "D2:D250",
                "left_filter": lambda p: p.get("topic") == "Tree" or "tree" in str(p.get("tags", [])).lower() or "cây" in str(p.get("note", "")).lower(),
                "right_filter": lambda p: p.get("topic") == "Graph Theory" or "graph" in str(p.get("tags", [])).lower() or "đồ thị" in str(p.get("note", "")).lower()
            },
            {
                "name": "DP & Greedy",
                "left_title": "DP",
                "left_count_range": "A2:A250",
                "right_title": "Greedy",
                "right_count_range": "D2:D250",
                "left_filter": lambda p: p.get("topic") == "Dynamic Programming" or "dp" in str(p.get("tags", [])).lower() or "qhđ" in str(p.get("note", "")).lower(),
                "right_filter": lambda p: p.get("topic") == "Greedy & Search" or "greedy" in str(p.get("tags", [])).lower() or "tham lam" in str(p.get("note", "")).lower()
            },
            {
                "name": "Mo, chia căn, ctdl",
                "left_title": "Mo, chia căn, ctdl",
                "left_count_range": "A2:A250",
                "right_title": "Advanced Data Structures",
                "right_count_range": "D2:D250",
                "left_filter": lambda p: any(k in str(p.get("note", "")).lower() or k in str(p.get("tags", [])).lower() for k in ["mo", "chia căn", "sqrt"]),
                "right_filter": lambda p: p.get("topic") == "Data Structures" or any(k in str(p.get("tags", [])).lower() for k in ["data structures", "segment tree", "fenwick", "trie", "treap", "dsu"])
            },
            {
                "name": "Math, hình, sweepline",
                "left_title": "Math, bitwise",
                "left_count_range": "A2:A250",
                "right_title": "Geometry, sweepline",
                "right_count_range": "D2:D250",
                "left_filter": lambda p: p.get("topic") == "Mathematics" or any(k in str(p.get("tags", [])).lower() for k in ["math", "number theory", "combinatorics", "bitmasks", "matrices"]),
                "right_filter": lambda p: p.get("topic") == "Geometry & Sweepline" or any(k in str(p.get("tags", [])).lower() for k in ["geometry", "sweepline", "convex hull"])
            },
            {
                "name": "Adhoc-Game, String",
                "left_title": "Adhoc, nhận xét, game",
                "left_count_range": "A2:A250",
                "right_title": "String , Z , Hash, Kmp, ..",
                "right_count_range": "D2:D250",
                "left_filter": lambda p: p.get("topic") == "Game Theory & Adhoc" or any(k in str(p.get("tags", [])).lower() for k in ["games", "constructive", "adhoc", "interactive"]),
                "right_filter": lambda p: p.get("topic") == "Strings" or any(k in str(p.get("tags", [])).lower() for k in ["strings", "string suffix structures", "hashing"])
            }
        ]

        # Extract all existing problems from original workbook
        for cfg in sheet_configs:
            sname = cfg["name"]
            ws = wb.create_sheet(title=sname)
            ws.views.sheetView[0].showGridLines = True

            # Row 1: Header (Matching original style)
            # Left Header
            c_a1 = ws.cell(1, 1, cfg["left_title"])
            c_a1.fill = FILL_HEADER_YELLOW
            c_a1.font = FONT_TITLE_RED
            c_a1.alignment = ALIGN_CENTER

            c_b1 = ws.cell(1, 2, f'=COUNTA(valuesByColor("lime", "", {cfg["left_count_range"]}))')
            c_b1.fill = FILL_HEADER_BLUE
            c_b1.font = FONT_COUNT_RED
            c_b1.alignment = ALIGN_CENTER

            c_c1 = ws.cell(1, 3, "")
            c_c1.fill = FILL_HEADER_PEACH

            # Right Header
            c_d1 = ws.cell(1, 4, cfg["right_title"])
            c_d1.fill = FILL_HEADER_YELLOW
            c_d1.font = FONT_TITLE_RED
            c_d1.alignment = ALIGN_CENTER

            c_e1 = ws.cell(1, 5, f'=COUNTA(valuesByColor("lime", "", {cfg["right_count_range"]}))')
            c_e1.fill = FILL_HEADER_BLUE
            c_e1.font = FONT_COUNT_RED
            c_e1.alignment = ALIGN_CENTER

            c_f1 = ws.cell(1, 6, "")
            c_f1.fill = FILL_HEADER_PEACH

            ws.row_dimensions[1].height = 36.0

            # Gather rows from original sheet if present
            left_rows = []
            right_rows = []
            if sname in self.original_sheets:
                for row_data in self.original_sheets[sname][1:]: # skip header
                    # Left side
                    if len(row_data) >= 1 and row_data[0]["val"]:
                        url_l = str(row_data[0]["val"]).strip()
                        note_l = str(row_data[1]["val"]) if len(row_data) > 1 and row_data[1]["val"] else ""
                        rat_l = str(row_data[2]["val"]) if len(row_data) > 2 and row_data[2]["val"] else ""
                        left_rows.append({
                            "url": url_l,
                            "note": note_l,
                            "rating": rat_l,
                            "solved": row_data[0]["solved"]
                        })
                    # Right side
                    if len(row_data) >= 4 and row_data[3]["val"]:
                        url_r = str(row_data[3]["val"]).strip()
                        note_r = str(row_data[4]["val"]) if len(row_data) > 4 and row_data[4]["val"] else ""
                        rat_r = str(row_data[5]["val"]) if len(row_data) > 5 and row_data[5]["val"] else ""
                        right_rows.append({
                            "url": url_r,
                            "note": note_r,
                            "rating": rat_r,
                            "solved": row_data[3]["solved"]
                        })

            # Check if any forgotten hard problems or ladder 16 problems belong here and aren't already included
            existing_urls = {r["url"] for r in left_rows + right_rows}
            for p in self.old_hard_problems:
                if p["url"] not in existing_urls:
                    if cfg["left_filter"](p):
                        left_rows.append({
                            "url": p["url"],
                            "note": f"{', '.join(p['tags'][:3])} (Ôn lại: {p['days_ago']} ngày)",
                            "rating": str(p["rating"]),
                            "solved": True
                        })
                        existing_urls.add(p["url"])
                    elif cfg["right_filter"](p):
                        right_rows.append({
                            "url": p["url"],
                            "note": f"{', '.join(p['tags'][:3])} (Ôn lại: {p['days_ago']} ngày)",
                            "rating": str(p["rating"]),
                            "solved": True
                        })
                        existing_urls.add(p["url"])

            # Write rows
            max_r = max(len(left_rows), len(right_rows))
            for i in range(max_r):
                r_idx = i + 2
                ws.row_dimensions[r_idx].height = 20.0

                # Left side
                if i < len(left_rows):
                    lr = left_rows[i]
                    c_link = ws.cell(r_idx, 1, lr["url"])
                    c_link.font = FONT_LINK_BLUE
                    c_link.alignment = ALIGN_LEFT
                    c_link.border = BORDER_THIN
                    if lr["solved"]:
                        c_link.fill = FILL_SOLVED_LIME

                    c_note = ws.cell(r_idx, 2, lr["note"])
                    c_note.fill = FILL_NOTE_BLUE
                    c_note.font = FONT_TEXT_REGULAR
                    c_note.alignment = ALIGN_LEFT
                    c_note.border = BORDER_THIN

                    c_rat = ws.cell(r_idx, 3, lr["rating"])
                    c_rat.fill = FILL_RATING_PEACH
                    c_rat.font = FONT_TEXT_REGULAR
                    c_rat.alignment = ALIGN_CENTER
                    c_rat.border = BORDER_THIN
                else:
                    for c_col in (1, 2, 3):
                        c = ws.cell(r_idx, c_col, "")
                        c.border = BORDER_THIN

                # Right side
                if i < len(right_rows):
                    rr = right_rows[i]
                    c_link = ws.cell(r_idx, 4, rr["url"])
                    c_link.font = FONT_LINK_BLUE
                    c_link.alignment = ALIGN_LEFT
                    c_link.border = BORDER_THIN
                    if rr["solved"]:
                        c_link.fill = FILL_SOLVED_LIME

                    c_note = ws.cell(r_idx, 5, rr["note"])
                    c_note.fill = FILL_NOTE_BLUE
                    c_note.font = FONT_TEXT_REGULAR
                    c_note.alignment = ALIGN_LEFT
                    c_note.border = BORDER_THIN

                    c_rat = ws.cell(r_idx, 6, rr["rating"])
                    c_rat.fill = FILL_RATING_PEACH
                    c_rat.font = FONT_TEXT_REGULAR
                    c_rat.alignment = ALIGN_CENTER
                    c_rat.border = BORDER_THIN
                else:
                    for c_col in (4, 5, 6):
                        c = ws.cell(r_idx, c_col, "")
                        c.border = BORDER_THIN

            # Set column widths matching original
            ws.column_dimensions["A"].width = 46.0
            ws.column_dimensions["B"].width = 28.0
            ws.column_dimensions["C"].width = 13.0
            ws.column_dimensions["D"].width = 46.0
            ws.column_dimensions["E"].width = 28.0
            ws.column_dimensions["F"].width = 13.0

    def generate_full_workbook(self, output_file: Path):
        """Generates the comprehensive multi-sheet training workbook."""
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Step 5: Generating Workbook: {output_file.name}...")
        wb = openpyxl.Workbook()
        # Remove default sheet
        default_sheet = wb.active
        wb.remove(default_sheet)

        # ---------------------------------------------------------------------
        # Sheet 1: Lịch Training & Mock Tests (Based on '1 month to VOI' format)
        # ---------------------------------------------------------------------
        ws_sched = wb.create_sheet(title="Lịch Training & Mock Tests")
        ws_sched.views.sheetView[0].showGridLines = True
        
        # Headers
        sched_headers = ["Ngày / Thứ", "Tuần & Chủ đề trọng tâm", "Hoạt động & Mục tiêu chi tiết", "Link Bài tập / Contest", "Tên Bài / Contest", "Target Rating", "Loại hình", "Trạng thái"]
        ws_sched.row_dimensions[1].height = 28.0
        for col_idx, h in enumerate(sched_headers, 1):
            cell = ws_sched.cell(1, col_idx, h)
            cell.fill = FILL_HEADER_YELLOW
            cell.font = FONT_HEADER_BOLD
            cell.alignment = ALIGN_CENTER
            cell.border = BORDER_HEADER

        schedule_items = self.build_schedule_data()
        for idx, item in enumerate(schedule_items, 2):
            ws_sched.row_dimensions[idx].height = 22.0
            is_mock = "MOCK TEST" in item["problem_name"] or "Regional" in item["problem_name"] or "Mini" in item["session_type"]

            c1 = ws_sched.cell(idx, 1, f"{item['date'].strftime('%Y-%m-%d')} ({item['day_name']})")
            c1.font = FONT_TEXT_BOLD if is_mock else FONT_TEXT_REGULAR
            c1.alignment = ALIGN_CENTER
            c1.border = BORDER_THIN
            c1.fill = FILL_MOCK_CONTEST if is_mock else FILL_HEADER_BLUE

            c2 = ws_sched.cell(idx, 2, item["week_theme"])
            c2.font = FONT_TEXT_REGULAR
            c2.alignment = ALIGN_LEFT
            c2.border = BORDER_THIN

            c3 = ws_sched.cell(idx, 3, item["activity"])
            c3.font = FONT_TEXT_REGULAR
            c3.alignment = ALIGN_LEFT
            c3.border = BORDER_THIN

            c4 = ws_sched.cell(idx, 4, item["link"])
            c4.font = FONT_LINK_BLUE
            c4.alignment = ALIGN_LEFT
            c4.border = BORDER_THIN
            if is_mock:
                c4.fill = FILL_MOCK_CONTEST

            c5 = ws_sched.cell(idx, 5, item["problem_name"])
            c5.font = FONT_TEXT_BOLD if is_mock else FONT_TEXT_REGULAR
            c5.alignment = ALIGN_LEFT
            c5.border = BORDER_THIN

            c6 = ws_sched.cell(idx, 6, item["rating"])
            c6.font = FONT_TEXT_REGULAR
            c6.alignment = ALIGN_CENTER
            c6.border = BORDER_THIN
            c6.fill = FILL_RATING_PEACH

            c7 = ws_sched.cell(idx, 7, item["session_type"])
            c7.font = FONT_TEXT_BOLD if is_mock else FONT_TEXT_REGULAR
            c7.alignment = ALIGN_CENTER
            c7.border = BORDER_THIN
            if is_mock:
                c7.fill = FILL_MOCK_CONTEST

            c8 = ws_sched.cell(idx, 8, item["status"])
            c8.font = FONT_TEXT_BOLD
            c8.alignment = ALIGN_CENTER
            c8.border = BORDER_THIN
            if item["status"] == "Hoàn thành":
                c8.fill = FILL_SOLVED_LIME
            elif is_mock:
                c8.fill = FILL_REVIEW_WARNING

        ws_sched.column_dimensions["A"].width = 22.0
        ws_sched.column_dimensions["B"].width = 38.0
        ws_sched.column_dimensions["C"].width = 44.0
        ws_sched.column_dimensions["D"].width = 40.0
        ws_sched.column_dimensions["E"].width = 44.0
        ws_sched.column_dimensions["F"].width = 16.0
        ws_sched.column_dimensions["G"].width = 20.0
        ws_sched.column_dimensions["H"].width = 16.0

        # ---------------------------------------------------------------------
        # Sheet 2 - 6: Algorithmic Categories (Matching format of original sheet)
        # ---------------------------------------------------------------------
        self.populate_topic_sheets(wb)

        # ---------------------------------------------------------------------
        # Sheet 7: Hard Review (>=2 tháng) - The 137 Forgotten Hard Problems
        # ---------------------------------------------------------------------
        ws_hard = wb.create_sheet(title="Hard Review (>=2 tháng)")
        ws_hard.views.sheetView[0].showGridLines = True
        ws_hard.row_dimensions[1].height = 28.0

        hard_headers = ["STT", "Mã Bài (ID)", "Tên Bài Tập", "Link Bài", "Rating", "Chủ đề chính", "Tags kỹ thuật", "Ngày làm gần nhất", "Số ngày chưa đụng vào", "Độ ưu tiên ôn tập", "Trạng thái Re-solve"]
        for c_idx, h in enumerate(hard_headers, 1):
            cell = ws_hard.cell(1, c_idx, h)
            cell.fill = FILL_HEADER_YELLOW
            cell.font = FONT_HEADER_BOLD
            cell.alignment = ALIGN_CENTER
            cell.border = BORDER_HEADER

        for idx, prob in enumerate(self.old_hard_problems, 2):
            ws_hard.row_dimensions[idx].height = 20.0
            
            c1 = ws_hard.cell(idx, 1, idx - 1)
            c1.alignment = ALIGN_CENTER
            c1.border = BORDER_THIN

            c2 = ws_hard.cell(idx, 2, prob["key"])
            c2.alignment = ALIGN_CENTER
            c2.font = FONT_TEXT_BOLD
            c2.border = BORDER_THIN

            c3 = ws_hard.cell(idx, 3, prob["name"])
            c3.alignment = ALIGN_LEFT
            c3.font = FONT_TEXT_REGULAR
            c3.border = BORDER_THIN

            c4 = ws_hard.cell(idx, 4, prob["url"])
            c4.font = FONT_LINK_BLUE
            c4.alignment = ALIGN_LEFT
            c4.border = BORDER_THIN
            c4.fill = FILL_SOLVED_LIME # Solved long ago

            c5 = ws_hard.cell(idx, 5, prob["rating"])
            c5.font = FONT_TEXT_BOLD
            c5.alignment = ALIGN_CENTER
            c5.border = BORDER_THIN
            c5.fill = FILL_RATING_PEACH

            c6 = ws_hard.cell(idx, 6, prob["topic"])
            c6.font = FONT_TEXT_REGULAR
            c6.alignment = ALIGN_LEFT
            c6.border = BORDER_THIN
            c6.fill = FILL_NOTE_BLUE

            c7 = ws_hard.cell(idx, 7, ", ".join(prob["tags"][:5]))
            c7.font = FONT_TEXT_REGULAR
            c7.alignment = ALIGN_LEFT
            c7.border = BORDER_THIN

            date_str = prob["last_sub"].strftime('%Y-%m-%d') if prob["last_sub"] else "N/A"
            c8 = ws_hard.cell(idx, 8, date_str)
            c8.alignment = ALIGN_CENTER
            c8.font = FONT_TEXT_REGULAR
            c8.border = BORDER_THIN

            c9 = ws_hard.cell(idx, 9, f"{prob['days_ago']} ngày")
            c9.alignment = ALIGN_CENTER
            c9.font = FONT_TEXT_BOLD
            c9.border = BORDER_THIN
            if prob['days_ago'] > 180:
                c9.fill = FILL_REVIEW_WARNING

            c10 = ws_hard.cell(idx, 10, prob["priority"])
            c10.alignment = ALIGN_LEFT
            c10.font = FONT_TEXT_BOLD
            c10.border = BORDER_THIN
            if "P1" in prob["priority"]:
                c10.fill = FILL_REVIEW_WARNING
            elif "P2" in prob["priority"]:
                c10.fill = FILL_HEADER_PURPLE

            c11 = ws_hard.cell(idx, 11, "Cần Re-solve")
            c11.alignment = ALIGN_CENTER
            c11.font = FONT_TEXT_REGULAR
            c11.border = BORDER_THIN

        ws_hard.column_dimensions["A"].width = 8.0
        ws_hard.column_dimensions["B"].width = 14.0
        ws_hard.column_dimensions["C"].width = 34.0
        ws_hard.column_dimensions["D"].width = 46.0
        ws_hard.column_dimensions["E"].width = 12.0
        ws_hard.column_dimensions["F"].width = 24.0
        ws_hard.column_dimensions["G"].width = 38.0
        ws_hard.column_dimensions["H"].width = 16.0
        ws_hard.column_dimensions["I"].width = 18.0
        ws_hard.column_dimensions["J"].width = 34.0
        ws_hard.column_dimensions["K"].width = 16.0

        # ---------------------------------------------------------------------
        # Sheet 8: Ladder 16 (Review & Re-solve) - All 100 A2OJ Problems
        # ---------------------------------------------------------------------
        ws_l16 = wb.create_sheet(title="Ladder 16 - Review & Re-solve")
        ws_l16.views.sheetView[0].showGridLines = True
        ws_l16.row_dimensions[1].height = 28.0

        l16_headers = ["ID", "Tên Bài Tập", "Link Bài", "Judge", "Mức Độ (A2OJ)", "CF Rating", "Tags", "Trạng thái", "Ngày làm gần nhất", "Ghi chú ôn tập"]
        for c_idx, h in enumerate(l16_headers, 1):
            cell = ws_l16.cell(1, c_idx, h)
            cell.fill = FILL_HEADER_YELLOW
            cell.font = FONT_HEADER_BOLD
            cell.alignment = ALIGN_CENTER
            cell.border = BORDER_HEADER

        for idx, lp in enumerate(self.ladder_problems, 2):
            ws_l16.row_dimensions[idx].height = 20.0

            c1 = ws_l16.cell(idx, 1, lp["ladder_idx"])
            c1.alignment = ALIGN_CENTER
            c1.border = BORDER_THIN

            c2 = ws_l16.cell(idx, 2, lp["name"])
            c2.alignment = ALIGN_LEFT
            c2.font = FONT_TEXT_REGULAR
            c2.border = BORDER_THIN

            c3 = ws_l16.cell(idx, 3, lp["url"])
            c3.font = FONT_LINK_BLUE
            c3.alignment = ALIGN_LEFT
            c3.border = BORDER_THIN
            if lp["solved"]:
                c3.fill = FILL_SOLVED_LIME

            c4 = ws_l16.cell(idx, 4, lp["judge"])
            c4.alignment = ALIGN_CENTER
            c4.font = FONT_TEXT_REGULAR
            c4.border = BORDER_THIN

            c5 = ws_l16.cell(idx, 5, lp["diff_level"])
            c5.alignment = ALIGN_CENTER
            c5.font = FONT_TEXT_BOLD
            c5.border = BORDER_THIN
            c5.fill = FILL_RATING_PEACH

            c6 = ws_l16.cell(idx, 6, lp["rating"] or "")
            c6.alignment = ALIGN_CENTER
            c6.font = FONT_TEXT_REGULAR
            c6.border = BORDER_THIN

            c7 = ws_l16.cell(idx, 7, ", ".join(lp.get("tags", [])[:4]))
            c7.alignment = ALIGN_LEFT
            c7.font = FONT_TEXT_REGULAR
            c7.border = BORDER_THIN

            # Status label
            if lp.get("review_needed"):
                status_str = "ĐÃ LÀM >= 2 THÁNG (CẦN ÔN LẠI)"
                st_fill = FILL_REVIEW_WARNING
                note_str = "Đã quên kiến thức -> Re-solve ngay"
            elif lp["solved"]:
                status_str = "Đã hoàn thành gần đây"
                st_fill = FILL_SOLVED_LIME
                note_str = "Đã nắm chắc"
            else:
                status_str = "Chưa làm"
                st_fill = None
                note_str = "Mục tiêu luyện tập"

            c8 = ws_l16.cell(idx, 8, status_str)
            c8.alignment = ALIGN_CENTER
            c8.font = FONT_TEXT_BOLD
            c8.border = BORDER_THIN
            if st_fill:
                c8.fill = st_fill

            date_str = lp["last_sub"].strftime('%Y-%m-%d') if lp.get("last_sub") else "Chưa nộp"
            c9 = ws_l16.cell(idx, 9, date_str)
            c9.alignment = ALIGN_CENTER
            c9.font = FONT_TEXT_REGULAR
            c9.border = BORDER_THIN

            c10 = ws_l16.cell(idx, 10, note_str)
            c10.alignment = ALIGN_LEFT
            c10.font = FONT_TEXT_REGULAR
            c10.border = BORDER_THIN

        ws_l16.column_dimensions["A"].width = 8.0
        ws_l16.column_dimensions["B"].width = 30.0
        ws_l16.column_dimensions["D"].width = 12.0
        ws_l16.column_dimensions["E"].width = 14.0
        ws_l16.column_dimensions["F"].width = 12.0
        ws_l16.column_dimensions["G"].width = 32.0
        ws_l16.column_dimensions["H"].width = 32.0
        ws_l16.column_dimensions["I"].width = 16.0
        ws_l16.column_dimensions["J"].width = 28.0

        # ---------------------------------------------------------------------
        # Sheet 9: trick lỏ & Template Note
        # ---------------------------------------------------------------------
        ws_trick = wb.create_sheet(title="trick lỏ & Template Note")
        ws_trick.views.sheetView[0].showGridLines = True
        ws_trick.row_dimensions[1].height = 28.0

        trick_headers = ["STT", "Chủ đề / Dạng bài", "Link Tham khảo", "Trick lỏ & Kinh nghiệm phòng thi", "Lưu ý cài đặt (Edge Cases)", "Mức độ quan trọng"]
        for c_idx, h in enumerate(trick_headers, 1):
            cell = ws_trick.cell(1, c_idx, h)
            cell.fill = FILL_HEADER_YELLOW
            cell.font = FONT_HEADER_BOLD
            cell.alignment = ALIGN_CENTER
            cell.border = BORDER_HEADER

        curated_tricks = [
            ("Đồ thị (Graph)", "https://codeforces.com/contest/786/problem/B", "Dijkstra trên đoạn / Segment Tree build đồ thị: Giảm số cạnh từ O(N^2) xuống O(N log N)", "Chú ý phân biệt cây đi vào (In-tree) và cây đi ra (Out-tree)", "Rất cao (ICPC/VOI)"),
            ("Cây (Tree)", "https://codeforces.com/contest/601/problem/D", "Gộp Trie + Small to Large kết hợp Euler Tour", "Nhớ clear biến toàn cục trước mỗi test case (t=1..T)", "Rất cao (ICPC/VOI)"),
            ("Cây (Tree)", "https://oj.vnoi.info/problem/vmtree", "Tính đường kính / Tâm cây không cần cài Centroid phức tạp", "Chỉ cần 2 lần BFS/DFS tìm đường kính", "Cao"),
            ("Quy hoạch động (DP)", "https://cses.fi/problemset/task/1654", "SOS DP (Sum Over Subsets) độ phức tạp O(N * 2^N) thay vì O(3^N)", "Chạy vòng for mask trước rồi mới đến bit (hoặc ngược lại) đúng thứ tự", "Cực kỳ cao (OLP)"),
            ("Cấu trúc dữ liệu", "https://codeforces.com/problemset/problem/13/E", "Chia căn (Block decomposition): Cập nhật trong block O(1), truy vấn O(sqrt N)", "Kích thước block tối ưu thường là sqrt(N) hoặc sqrt(N * log N)", "Cao"),
            ("Toán học (Math)", "https://codeforces.com/contest/1043/problem/F", "Bao hàm loại trừ (Inclusion-Exclusion) đếm số cách chọn GCD = 1", "Sử dụng hàm Mobius mu(d) để tính nhanh tổng bao hàm", "Cực kỳ cao (OLP)"),
            ("Hình học (Geometry)", "https://codeforces.com/contest/529/problem/C", "Sweepline quét tọa độ X, Segment tree quản lý khoảng tọa độ Y", "Cần nén tọa độ (Coordinate Compression) cẩn thận", "Rất cao (ICPC)"),
            ("Xâu ký tự (Strings)", "https://codeforces.com/problemset/problem/126/B", "Mảng Pi (KMP) để tìm tiền tố vừa là hậu tố vừa xuất hiện ở giữa", "KMP chỉ cần 5 dòng code, an toàn hơn Hash 100%", "Cực kỳ cao"),
            ("Template C++", "https://codeforces.com", "Fast I/O: cin.tie(0)->sync_with_stdio(0); cout.tie(0); Tránh endl", "Không dùng endl vì nó flush buffer gây TLE", "Bắt buộc"),
            ("Template C++", "https://codeforces.com", "Tràn số 64-bit: Ép kiểu (1LL << x) và (long long)a * b % MOD", "Cẩn thận với modulo số âm: ((a % MOD) + MOD) % MOD", "Bắt buộc"),
            ("ICPC Teamwork", "https://icpc.global", "Chiến thuật 3 người 1 máy: Đọc đề -> Phân bài Easy trước -> Gõ test tay -> Code mượt", "1 người code, 2 người vẽ test case biên trên giấy", "Bắt buộc (ICPC)"),
        ]

        # Ingest tricks from original workbook if any
        if "trick lỏ" in self.original_sheets:
            for row_data in self.original_sheets["trick lỏ"]:
                if len(row_data) >= 1 and row_data[0]["val"] and str(row_data[0]["val"]).startswith("http"):
                    u = str(row_data[0]["val"])
                    t1 = str(row_data[1]["val"]) if len(row_data) > 1 and row_data[1]["val"] else "Ghi chú"
                    t2 = str(row_data[2]["val"]) if len(row_data) > 2 and row_data[2]["val"] else ""
                    curated_tricks.append(("Kinh nghiệm từ Sheet", u, f"{t1} {t2}", "Kiểm tra kỹ giới hạn bộ nhớ", "Trung bình"))

        for idx, t in enumerate(curated_tricks, 2):
            ws_trick.row_dimensions[idx].height = 22.0

            c1 = ws_trick.cell(idx, 1, idx - 1)
            c1.alignment = ALIGN_CENTER
            c1.border = BORDER_THIN

            c2 = ws_trick.cell(idx, 2, t[0])
            c2.alignment = ALIGN_CENTER
            c2.font = FONT_TEXT_BOLD
            c2.border = BORDER_THIN
            c2.fill = FILL_NOTE_BLUE

            c3 = ws_trick.cell(idx, 3, t[1])
            c3.font = FONT_LINK_BLUE
            c3.alignment = ALIGN_LEFT
            c3.border = BORDER_THIN

            c4 = ws_trick.cell(idx, 4, t[2])
            c4.font = FONT_TEXT_REGULAR
            c4.alignment = ALIGN_LEFT
            c4.border = BORDER_THIN

            c5 = ws_trick.cell(idx, 5, t[3])
            c5.font = FONT_TEXT_REGULAR
            c5.alignment = ALIGN_LEFT
            c5.border = BORDER_THIN

            c6 = ws_trick.cell(idx, 6, t[4])
            c6.font = FONT_TEXT_BOLD
            c6.alignment = ALIGN_CENTER
            c6.border = BORDER_THIN
            c6.fill = FILL_REVIEW_WARNING if "Bắt buộc" in t[4] or "Cực kỳ" in t[4] else FILL_RATING_PEACH

        ws_trick.column_dimensions["A"].width = 8.0
        ws_trick.column_dimensions["B"].width = 24.0
        ws_trick.column_dimensions["C"].width = 46.0
        ws_trick.column_dimensions["D"].width = 54.0
        ws_trick.column_dimensions["E"].width = 46.0
        ws_trick.column_dimensions["F"].width = 24.0

        # Save workbook
        try:
            wb.save(output_file)
            print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Successfully saved to: {output_file} ({output_file.stat().st_size // 1024} KB)")
        except PermissionError:
            alt_file = output_file.parent / f"{output_file.stem}_new.xlsx"
            wb.save(alt_file)
            print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Notice: '{output_file.name}' is locked. Saved to '{alt_file.name}' instead ({alt_file.stat().st_size // 1024} KB)")

    def export_frontend_json(self, json_path: Path):
        """Exports the complete training dataset directly to web/data/data.json."""
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Step 6: Updating Web Frontend JSON: {json_path.name}...")
        
        # 1. Schedule
        schedule_items = self.build_schedule_data()
        serializable_schedule = []
        for s in schedule_items:
            item = dict(s)
            if isinstance(item.get("date"), (datetime.date, datetime.datetime)):
                item["date"] = item["date"].strftime("%Y-%m-%d")
            serializable_schedule.append(item)

        # 2. Ladder 16
        serializable_ladder = []
        for lp in self.ladder_problems:
            item = dict(lp)
            if isinstance(item.get("last_sub"), (datetime.date, datetime.datetime)):
                item["last_sub"] = item["last_sub"].strftime("%Y-%m-%d %H:%M:%S")
            serializable_ladder.append(item)

        # 3. Hard Problems
        serializable_hard = []
        for hp in self.old_hard_problems:
            item = dict(hp)
            if isinstance(item.get("last_sub"), (datetime.date, datetime.datetime)):
                item["last_sub"] = item["last_sub"].strftime("%Y-%m-%d %H:%M:%S")
            serializable_hard.append(item)

        # 4. Tricks
        curated_tricks = [
            {"category": "Đồ thị (Graph)", "link": "https://codeforces.com/contest/786/problem/B", "trick": "Dijkstra trên đoạn / Segment Tree build đồ thị: Giảm số cạnh từ O(N^2) xuống O(N log N)", "edge_case": "Chú ý phân biệt cây đi vào (In-tree) và cây đi ra (Out-tree)", "priority": "Rất cao (ICPC/VOI)"},
            {"category": "Cây (Tree)", "link": "https://codeforces.com/contest/601/problem/D", "trick": "Gộp Trie + Small to Large kết hợp Euler Tour", "edge_case": "Nhớ clear biến toàn cục trước mỗi test case (t=1..T)", "priority": "Rất cao (ICPC/VOI)"},
            {"category": "Cây (Tree)", "link": "https://oj.vnoi.info/problem/vmtree", "trick": "Tính đường kính / Tâm cây không cần cài Centroid phức tạp", "edge_case": "Chỉ cần 2 lần BFS/DFS tìm đường kính", "priority": "Cao"},
            {"category": "Quy hoạch động (DP)", "link": "https://cses.fi/problemset/task/1654", "trick": "SOS DP (Sum Over Subsets) độ phức tạp O(N * 2^N) thay vì O(3^N)", "edge_case": "Chạy vòng for mask trước rồi mới đến bit (hoặc ngược lại) đúng thứ tự", "priority": "Cực kỳ cao (OLP)"},
            {"category": "Cấu trúc dữ liệu", "link": "https://codeforces.com/problemset/problem/13/E", "trick": "Chia căn (Block decomposition): Cập nhật trong block O(1), truy vấn O(sqrt N)", "edge_case": "Kích thước block tối ưu thường là sqrt(N) hoặc sqrt(N * log N)", "priority": "Cao"},
            {"category": "Toán học (Math)", "link": "https://codeforces.com/contest/1043/problem/F", "trick": "Bao hàm loại trừ (Inclusion-Exclusion) đếm số cách chọn GCD = 1", "edge_case": "Sử dụng hàm Mobius mu(d) để tính nhanh tổng bao hàm", "priority": "Cực kỳ cao (OLP)"},
            {"category": "Hình học (Geometry)", "link": "https://codeforces.com/contest/529/problem/C", "trick": "Sweepline quét tọa độ X, Segment tree quản lý khoảng tọa độ Y", "edge_case": "Cần nén tọa độ (Coordinate Compression) cẩn thận", "priority": "Rất cao (ICPC)"},
            {"category": "Xâu ký tự (Strings)", "link": "https://codeforces.com/problemset/problem/126/B", "trick": "Mảng Pi (KMP) để tìm tiền tố vừa là hậu tố vừa xuất hiện ở giữa", "edge_case": "KMP chỉ cần 5 dòng code, an toàn hơn Hash 100%", "priority": "Cực kỳ cao"},
            {"category": "Template C++", "link": "https://codeforces.com", "trick": "Fast I/O: cin.tie(0)->sync_with_stdio(0); cout.tie(0); Tránh endl", "edge_case": "Không dùng endl vì nó flush buffer gây TLE", "priority": "Bắt buộc"},
            {"category": "Template C++", "link": "https://codeforces.com", "trick": "Tràn số 64-bit: Ép kiểu (1LL << x) và (long long)a * b % MOD", "edge_case": "Cẩn thận với modulo số âm: ((a % MOD) + MOD) % MOD", "priority": "Bắt buộc"},
            {"category": "ICPC Teamwork", "link": "https://icpc.global", "trick": "Chiến thuật 3 người 1 máy: Đọc đề -> Phân bài Easy trước -> Gõ test tay -> Code mượt", "edge_case": "1 người code, 2 người vẽ test case biên trên giấy", "priority": "Bắt buộc (ICPC)"}
        ]

        # Read existing data if available
        existing_data = {}
        if json_path.exists():
            try:
                with open(json_path, "r", encoding="utf-8") as f:
                    existing_data = json.load(f)
            except Exception:
                pass

        payload = {
            "updated_at": datetime.datetime.now().isoformat(),
            "user_handle": self.handle,
            "stats": {
                "total_cf_submissions": len(self.cf_problems),
                "total_cf_solved": sum(1 for p in self.cf_problems.values() if p["solved"]),
                "ladder16_total": len(self.ladder_problems),
                "ladder16_solved": sum(1 for p in self.ladder_problems if p["solved"]),
                "ladder16_review_needed": sum(1 for p in self.ladder_problems if p.get("review_needed")),
                "ladder16_unsolved": sum(1 for p in self.ladder_problems if not p["solved"]),
                "hard_review_count": len(self.old_hard_problems),
                "schedule_total_days": len(serializable_schedule),
                "accounts": {"Codeforces": self.handle}
            },
            "schedule": serializable_schedule,
            "ladder16": serializable_ladder,
            "old_hard_problems": serializable_hard,
            "tricks": curated_tricks,
            "exercises": existing_data.get("exercises", []),
            "materials": existing_data.get("materials", []),
            "roadmap_nodes": existing_data.get("roadmap_nodes", []),
            "projects": existing_data.get("projects", [])
        }

        json_path.parent.mkdir(parents=True, exist_ok=True)
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)

        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Frontend JSON snapshot updated: {json_path} ({json_path.stat().st_size // 1024} KB)")


def run_pipeline():
    manager = CPAutomatedManager(handle="DeruckLoveNewTechnology")
    manager.fetch_all_sources()
    manager.filter_forgotten_hard_problems()
    
    out_path = PROJECT_ROOT / "ICPC_OLP_Training_Deruck.xlsx"
    manager.generate_full_workbook(out_path)

    json_path = PROJECT_ROOT / "web" / "data" / "data.json"
    manager.export_frontend_json(json_path)

    # Summary
    print("\n" + "=" * 60)
    print("✨ AUTOMATED GENERATION COMPLETED SUCCESSFULLY!")
    print(f"📊 Total Hard Problems Filtered (>= 2 Months): {len(manager.old_hard_problems)}")
    print(f"🧗 Ladder 16 Problems Analyzed: {len(manager.ladder_problems)} (Solved: {sum(1 for p in manager.ladder_problems if p['solved'])}, Need Review: {sum(1 for p in manager.ladder_problems if p.get('review_needed'))})")
    print(f"📁 Output Multi-Sheet Workbook: {out_path.name}")
    print(f"🌐 Frontend JSON Snapshot: {json_path.name}")
    print("=" * 60)

if __name__ == "__main__":
    run_pipeline()

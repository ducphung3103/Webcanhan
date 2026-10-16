"""
Master Schedule Builder for DeruckLoveNewTechnology (Master 2107)
Generates high-intensity 8-week syllabus (56 days x 4 problems = 224 concrete problem assignments)
Tailored for ICPC Regional 2026 & Olympic Tin học Sinh viên (Chuyên Tin / Siêu Cúp)
"""

import datetime

def get_master_schedule():
    """
    Returns the complete 56-day schedule with 4 designated problem slots per day (224 problems total).
    Reflects the official 2026 ICPC & OLP dates:
    - 17-18/10/2026: ICPC Miền Nam (ĐH KHTN TP.HCM)
    - 24-25/10/2026: ICPC Miền Trung (ĐH Khoa học Huế)
    - 08-09/11/2026: ICPC Quốc gia 2026 (Vietnam National Contest)
    - 08-11/12/2026: Chung kết OLP'26 & ICPC Asia Danang 2026 (VKU Đà Nẵng)
    """
    cur_date = datetime.date(2026, 10, 17)
    
    # 8 Weeks Plan (56 days)
    weeks_data = [
        # =========================================================================
        # TUẦN 1 (17/10 - 23/10): ICPC MIỀN NAM 2026 & CÂY (TREE), DSU, SHORTEST PATH
        # =========================================================================
        {
            "week_num": 1,
            "theme": "Tuần 1: VÒNG THI ICPC MIỀN NAM 2026 & Củng cố Cây (Tree), DSU, Shortest Path",
            "days": [
                {
                    "day_name": "Thứ Bảy",
                    "activity": "Thử máy Vòng thi ICPC Miền Nam 2026 (ĐH KHTN TP.HCM) & Speed Warm-up",
                    "session_type": "THỬ MÁY & WARM-UP",
                    "problems": [
                        {"slot": "Slot 1: ⚡ Speed Warm-up (10-15m)", "name": "Codeforces 217A - Ice Skating", "url": "https://codeforces.com/problemset/problem/217/A", "rating": 1400, "tag": "Graph / DSU components", "time_est": "15m"},
                        {"slot": "Slot 2: 🎯 Core ICPC Topic (25-35m)", "name": "Codeforces 295B - Greg and Graph", "url": "https://codeforces.com/contest/295/problem/B", "rating": 1700, "tag": "Floyd-Warshall reverse trick - Ladder 16", "time_est": "25m"},
                        {"slot": "Slot 3: 🏆 OLP Decisive (35-45m)", "name": "Codeforces 1746D - Paths on the Tree", "url": "https://codeforces.com/problemset/problem/1746/D", "rating": 2200, "tag": "Tree DP, Divide and Conquer", "time_est": "40m"},
                        {"slot": "Slot 4: 🧗 Mastery Re-solve (45-60m)", "name": "Codeforces 1416D - DSU-Tree and Queries", "url": "https://codeforces.com/contest/1416/problem/D", "rating": 2600, "tag": "DSU Tree, Small to Large - Re-solve bài cũ", "time_est": "55m"}
                    ]
                },
                {
                    "day_name": "Chủ Nhật",
                    "activity": "CHÍNH THỨC THI ICPC MIỀN NAM 2026 (5 GIỜ)",
                    "session_type": "OFFICIAL CONTEST (5H)",
                    "problems": [
                        {"slot": "Slot 1: 🏆 OFFICIAL CONTEST (5H)", "name": "ICPC Southern Vietnam Regional Contest 2026", "url": "https://codeforces.com/gyms", "rating": 2200, "tag": "5h Live Contest - ĐH KHTN TP.HCM", "time_est": "300m"},
                        {"slot": "Slot 2: 🎯 Target Upsolve 1", "name": "Upsolve Bài Đồ thị / Cây mức trung bình trong đề", "url": "https://codeforces.com/gyms", "rating": 1900, "tag": "Upsolving đề thi thật", "time_est": "45m"},
                        {"slot": "Slot 3: 🏆 Target Upsolve 2", "name": "Upsolve Bài Quy hoạch động phân hóa trong đề", "url": "https://codeforces.com/gyms", "rating": 2200, "tag": "Upsolving đề thi thật", "time_est": "50m"},
                        {"slot": "Slot 4: 🧗 Target Upsolve 3", "name": "Upsolve Bài khó nhất trong tầm với (Hard Decisive)", "url": "https://codeforces.com/gyms", "rating": 2400, "tag": "Upsolving đề thi thật", "time_est": "60m"}
                    ]
                },
                {
                    "day_name": "Thứ Hai",
                    "activity": "Mổ xẻ chiến thuật đề Miền Nam & Rerooting Tree DP",
                    "session_type": "UPSOLVING & TREE DP",
                    "problems": [
                        {"slot": "Slot 1: ⚡ Speed Warm-up (10-15m)", "name": "Codeforces 1338A - Powered Addition", "url": "https://codeforces.com/problemset/problem/1338/A", "rating": 1500, "tag": "Greedy / Bitwise speed", "time_est": "15m"},
                        {"slot": "Slot 2: 🎯 Core ICPC Topic (25-35m)", "name": "Codeforces 1187E - Tree Painting", "url": "https://codeforces.com/problemset/problem/1187/E", "rating": 2100, "tag": "Rerooting DP trên Cây - Coản Coản sheet", "time_est": "30m"},
                        {"slot": "Slot 3: 🏆 OLP Decisive (35-45m)", "name": "Codeforces 375D - Tree and Queries", "url": "https://codeforces.com/problemset/problem/375/D", "rating": 2400, "tag": "Mo on Tree, DSU on Tree - Re-solve bài cũ", "time_est": "45m"},
                        {"slot": "Slot 4: 🧗 Mastery Re-solve (45-60m)", "name": "Codeforces 1707C - DFS Trees", "url": "https://codeforces.com/problemset/problem/1707/C", "rating": 2600, "tag": "DFS Tree, Euler Tour - Re-solve bài cũ", "time_est": "60m"}
                    ]
                },
                {
                    "day_name": "Thứ Ba",
                    "activity": "Đường đi ngắn nhất & Dijkstra trạng thái nâng cao",
                    "session_type": "SHORTEST PATH & GRAPH",
                    "problems": [
                        {"slot": "Slot 1: ⚡ Speed Warm-up (10-15m)", "name": "Codeforces 126B - Password", "url": "https://codeforces.com/problemset/problem/126/B", "rating": 1700, "tag": "KMP / Z-algo prefix-suffix - Ladder 16", "time_est": "20m"},
                        {"slot": "Slot 2: 🎯 Core ICPC Topic (25-35m)", "name": "Codeforces 1442C - Graph Coloring and Shortest Path", "url": "https://codeforces.com/contest/1442/problem/C", "rating": 2400, "tag": "Dijkstra 2 chiều trạng thái - Re-solve bài cũ", "time_est": "45m"},
                        {"slot": "Slot 3: 🏆 OLP Decisive (35-45m)", "name": "Codeforces 1697E - Transparent Graph", "url": "https://codeforces.com/contest/1697/problem/E", "rating": 2400, "tag": "Graph, DP, Tổ hợp - Re-solve bài cũ", "time_est": "45m"},
                        {"slot": "Slot 4: 🧗 Mastery Re-solve (45-60m)", "name": "Codeforces 1856E2 - PermuTree (hard version)", "url": "https://codeforces.com/problemset/problem/1856/E2", "rating": 2700, "tag": "Tree, Knapsack, Bitset - Re-solve bài cũ", "time_est": "60m"}
                    ]
                },
                {
                    "day_name": "Thứ Tư",
                    "activity": "Cây khung nhỏ nhất (MST) & DSU Rollback",
                    "session_type": "MST & DSU ROLLBACK",
                    "problems": [
                        {"slot": "Slot 1: ⚡ Speed Warm-up (10-15m)", "name": "Codeforces 161D - Distance in Tree", "url": "https://codeforces.com/problemset/problem/161/D", "rating": 1800, "tag": "Tree DP cơ bản - Ladder 16", "time_est": "20m"},
                        {"slot": "Slot 2: 🎯 Core ICPC Topic (25-35m)", "name": "Codeforces 1633E - Spanning Tree Queries", "url": "https://codeforces.com/problemset/problem/1633/E", "rating": 2100, "tag": "MST, Sweepline ternary - Re-solve bài cũ", "time_est": "35m"},
                        {"slot": "Slot 3: 🏆 OLP Decisive (35-45m)", "name": "Codeforces 1761E - Make It Connected", "url": "https://codeforces.com/problemset/problem/1761/E", "rating": 2400, "tag": "Graph, Connected components - Re-solve bài cũ", "time_est": "45m"},
                        {"slot": "Slot 4: 🧗 Mastery Re-solve (45-60m)", "name": "Codeforces 613D - Kingdom and its Cities", "url": "https://codeforces.com/problemset/problem/613/D", "rating": 2800, "tag": "Virtual Tree / Auxiliary Tree - Re-solve bài cũ", "time_est": "70m"}
                    ]
                },
                {
                    "day_name": "Thứ Năm",
                    "activity": "Heavy-Light Decomposition & Cây phân đoạn trên Cây",
                    "session_type": "HLD & TREE QUERIES",
                    "problems": [
                        {"slot": "Slot 1: ⚡ Speed Warm-up (10-15m)", "name": "Codeforces 1365D - Solve The Maze", "url": "https://codeforces.com/problemset/problem/1365/D", "rating": 1700, "tag": "BFS / Constructive graph - Ladder 16", "time_est": "15m"},
                        {"slot": "Slot 2: 🎯 Core ICPC Topic (25-35m)", "name": "Codeforces 1709E - XOR Tree", "url": "https://codeforces.com/problemset/problem/1709/E", "rating": 2300, "tag": "DSU on Tree, Trie XOR - Re-solve bài cũ", "time_est": "40m"},
                        {"slot": "Slot 3: 🏆 OLP Decisive (35-45m)", "name": "Codeforces 1774F1 - Magician and Pigs (Easy)", "url": "https://codeforces.com/problemset/problem/1774/F1", "rating": 2400, "tag": "Tree / DP Observation - Re-solve bài cũ", "time_est": "45m"},
                        {"slot": "Slot 4: 🧗 Mastery Re-solve (45-60m)", "name": "Codeforces 1858E1 - Rollbacks (Easy Version)", "url": "https://codeforces.com/problemset/problem/1858/E1", "rating": 2500, "tag": "Tree, DSU Rollback - Re-solve bài cũ", "time_est": "60m"}
                    ]
                },
                {
                    "day_name": "Thứ Sáu",
                    "activity": "Rà soát Template & Chuẩn bị chiến thuật Vòng Miền Trung",
                    "session_type": "TEMPLATE REVIEW",
                    "problems": [
                        {"slot": "Slot 1: ⚡ Speed Warm-up (10-15m)", "name": "Codeforces 118D - Caesar's Legions", "url": "https://codeforces.com/problemset/problem/118/D", "rating": 1600, "tag": "DP cơ bản lấy nhịp tay", "time_est": "15m"},
                        {"slot": "Slot 2: 🎯 Core ICPC Topic (25-35m)", "name": "Codeforces 1691E - Number of Groups", "url": "https://codeforces.com/problemset/problem/1691/E", "rating": 2200, "tag": "Segment Tree + DSU - Re-solve bài cũ", "time_est": "35m"},
                        {"slot": "Slot 3: 🏆 OLP Decisive (35-45m)", "name": "Codeforces 1689E - AND-OR-MAX", "url": "https://codeforces.com/problemset/problem/1689/E", "rating": 2400, "tag": "Graph, Connectedness, Bitwise - Re-solve bài cũ", "time_est": "45m"},
                        {"slot": "Slot 4: 🧗 Checklist", "name": "In ấn & Rà soát Template HLD, DSU Rollback, Euler Tour", "url": "https://codeforces.com", "rating": 2000, "tag": "Team Notebook checklist", "time_est": "30m"}
                    ]
                }
            ]
        },

        # =========================================================================
        # TUẦN 2 (24/10 - 30/10): ICPC MIỀN TRUNG 2026 & SOS DP, CHT, BITMASK
        # =========================================================================
        {
            "week_num": 2,
            "theme": "Tuần 2: VÒNG THI ICPC MIỀN TRUNG 2026 & Quy hoạch động nâng cao (SOS DP, CHT, Bitmask)",
            "days": [
                {
                    "day_name": "Thứ Bảy",
                    "activity": "Thử máy Vòng thi ICPC Miền Trung 2026 (ĐH Khoa học Huế) & Speed Warm-up",
                    "session_type": "THỬ MÁY & WARM-UP",
                    "problems": [
                        {"slot": "Slot 1: ⚡ Speed Warm-up (10-15m)", "name": "Codeforces 471D - MUH and Cube Walls", "url": "https://codeforces.com/problemset/problem/471/D", "rating": 1800, "tag": "Differencing + KMP - Ladder 16 review", "time_est": "20m"},
                        {"slot": "Slot 2: 🎯 Core ICPC Topic (25-35m)", "name": "CSES 1654 - SOS DP", "url": "https://cses.fi/problemset/task/1654", "rating": 2100, "tag": "Sum Over Subsets DP kinh điển", "time_est": "30m"},
                        {"slot": "Slot 3: 🏆 OLP Decisive (35-45m)", "name": "Codeforces 1743E - FTL", "url": "https://codeforces.com/problemset/problem/1743/E", "rating": 2100, "tag": "Knapsack DP - Re-solve bài cũ", "time_est": "40m"},
                        {"slot": "Slot 4: 🧗 Mastery Re-solve (45-60m)", "name": "Codeforces 449D - Jzzhu and Numbers", "url": "https://codeforces.com/problemset/problem/449/D", "rating": 2400, "tag": "SOS DP + Bao hàm loại trừ - Re-solve bài cũ", "time_est": "50m"}
                    ]
                },
                {
                    "day_name": "Chủ Nhật",
                    "activity": "CHÍNH THỨC THI ICPC MIỀN TRUNG 2026 (5 GIỜ)",
                    "session_type": "OFFICIAL CONTEST (5H)",
                    "problems": [
                        {"slot": "Slot 1: 🏆 OFFICIAL CONTEST (5H)", "name": "ICPC Central Vietnam Regional Contest 2026", "url": "https://codeforces.com/gyms", "rating": 2200, "tag": "5h Live Contest - ĐH Khoa học Huế", "time_est": "300m"},
                        {"slot": "Slot 2: 🎯 Target Upsolve 1", "name": "Upsolve Bài Quy hoạch động phân hóa trong đề", "url": "https://codeforces.com/gyms", "rating": 2000, "tag": "Upsolving đề thi thật", "time_est": "45m"},
                        {"slot": "Slot 3: 🏆 Target Upsolve 2", "name": "Upsolve Bài Cấu trúc dữ liệu trong đề", "url": "https://codeforces.com/gyms", "rating": 2200, "tag": "Upsolving đề thi thật", "time_est": "50m"},
                        {"slot": "Slot 4: 🧗 Target Upsolve 3", "name": "Upsolve Bài khó quyết định thứ hạng", "url": "https://codeforces.com/gyms", "rating": 2400, "tag": "Upsolving đề thi thật", "time_est": "60m"}
                    ]
                },
                {
                    "day_name": "Thứ Hai",
                    "activity": "Mổ xẻ đề Miền Trung & Convex Hull Trick (CHT)",
                    "session_type": "CHT & OPTIMIZATION",
                    "problems": [
                        {"slot": "Slot 1: ⚡ Speed Warm-up (10-15m)", "name": "Codeforces 346B - Lucky Common Subsequence", "url": "https://codeforces.com/problemset/problem/346/B", "rating": 2000, "tag": "DP + KMP Automaton - Ladder 16 review", "time_est": "30m"},
                        {"slot": "Slot 2: 🎯 Core ICPC Topic (25-35m)", "name": "Codeforces 1661D - Progressions Covering", "url": "https://codeforces.com/problemset/problem/1661/D", "rating": 1900, "tag": "Difference Array DP - Re-solve bài cũ", "time_est": "30m"},
                        {"slot": "Slot 3: 🏆 OLP Decisive (35-45m)", "name": "Codeforces 1715E - Long Way Home", "url": "https://codeforces.com/problemset/problem/1715/E", "rating": 2400, "tag": "Dijkstra + CHT - Re-solve bài cũ", "time_est": "45m"},
                        {"slot": "Slot 4: 🧗 Mastery Re-solve (45-60m)", "name": "Codeforces 1859E - Maximum Monogonosity", "url": "https://codeforces.com/problemset/problem/1859/E", "rating": 2500, "tag": "Dynamic Programming - Re-solve bài cũ", "time_est": "55m"}
                    ]
                },
                {
                    "day_name": "Thứ Ba",
                    "activity": "Li Chao Tree & WQS Binary Search (Alien's Trick)",
                    "session_type": "LI CHAO & ALIEN TRICK",
                    "problems": [
                        {"slot": "Slot 1: ⚡ Speed Warm-up (10-15m)", "name": "Codeforces 319B - Psychos in a Line", "url": "https://codeforces.com/problemset/problem/319/B", "rating": 1800, "tag": "Monotonic Stack - Ladder 16", "time_est": "20m"},
                        {"slot": "Slot 2: 🎯 Core ICPC Topic (25-35m)", "name": "Codeforces 1638D - Big Brush", "url": "https://codeforces.com/problemset/problem/1638/D", "rating": 2000, "tag": "Reverse DP / Greedy - Re-solve bài cũ", "time_est": "35m"},
                        {"slot": "Slot 3: 🏆 OLP Decisive (35-45m)", "name": "Codeforces 1768D - Lucky Permutation", "url": "https://codeforces.com/problemset/problem/1768/D", "rating": 1900, "tag": "Cycle Decomposition DP - Re-solve bài cũ", "time_est": "35m"},
                        {"slot": "Slot 4: 🧗 Mastery Re-solve (45-60m)", "name": "Codeforces 1292D - Chaotic V.", "url": "https://codeforces.com/problemset/problem/1292/D", "rating": 2700, "tag": "Number Theory DP on Tree - Re-solve bài cũ", "time_est": "65m"}
                    ]
                },
                {
                    "day_name": "Thứ Tư",
                    "activity": "Mini-Mock OLP Contest (2.5h) & Bitmask DP",
                    "session_type": "OLP MINI TEST (2.5H)",
                    "problems": [
                        {"slot": "Slot 1: 🏆 OLP Mini Contest (2.5h)", "name": "Codeforces Round 955 (Div. 2/1)", "url": "https://codeforces.com/contest/1987", "rating": 1900, "tag": "Simulation 4 bài thi cá nhân", "time_est": "150m"},
                        {"slot": "Slot 2: 🎯 Core ICPC Topic (25-35m)", "name": "Codeforces 1779D - Boris and His Amazing Haircut", "url": "https://codeforces.com/problemset/problem/1779/D", "rating": 1900, "tag": "Monotonic Stack + SegTree - Re-solve bài cũ", "time_est": "30m"},
                        {"slot": "Slot 3: 🏆 OLP Decisive (35-45m)", "name": "Codeforces 1801C - Music Festival", "url": "https://codeforces.com/problemset/problem/1801/C", "rating": 1900, "tag": "LIS / Coordinate compression - Re-solve bài cũ", "time_est": "35m"},
                        {"slot": "Slot 4: 🧗 Mastery Re-solve (45-60m)", "name": "Codeforces 1736C2 - Good Subarrays (Hard)", "url": "https://codeforces.com/problemset/problem/1736/C2", "rating": 2000, "tag": "DP Prefix Max SegTree - Re-solve bài cũ", "time_est": "45m"}
                    ]
                },
                {
                    "day_name": "Thứ Năm",
                    "activity": "DP Digit & DP kết hợp Cấu trúc dữ liệu",
                    "session_type": "DP ON DATA STRUCTURES",
                    "problems": [
                        {"slot": "Slot 1: ⚡ Speed Warm-up (10-15m)", "name": "Codeforces 189A - Cut Ribbon", "url": "https://codeforces.com/problemset/problem/189/A", "rating": 1300, "tag": "Knapsack speed warm-up", "time_est": "10m"},
                        {"slot": "Slot 2: 🎯 Core ICPC Topic (25-35m)", "name": "Codeforces 1765K - Torus Path", "url": "https://codeforces.com/problemset/problem/1765/K", "rating": 1900, "tag": "Matrix / Adhoc DP - Re-solve bài cũ", "time_est": "30m"},
                        {"slot": "Slot 3: 🏆 OLP Decisive (35-45m)", "name": "Codeforces 1733D2 - Zero-One (Hard Version)", "url": "https://codeforces.com/problemset/problem/1733/D2", "rating": 2000, "tag": "Dynamic Programming - Re-solve bài cũ", "time_est": "40m"},
                        {"slot": "Slot 4: 🧗 Mastery Re-solve (45-60m)", "name": "Codeforces 1974G - Money Buys Less Happiness Now", "url": "https://codeforces.com/problemset/problem/1974/G", "rating": 2600, "tag": "Priority Queue DP - Re-solve bài cũ", "time_est": "50m"}
                    ]
                },
                {
                    "day_name": "Thứ Sáu",
                    "activity": "DP Chia để trị (Divide and Conquer Optimization) & Knuth DP",
                    "session_type": "DNC OPTIMIZATION",
                    "problems": [
                        {"slot": "Slot 1: ⚡ Speed Warm-up (10-15m)", "name": "Codeforces 432D - Prefixes and Suffixes", "url": "https://codeforces.com/problemset/problem/432/D", "rating": 2000, "tag": "Z-function + DP - Ladder 16 review", "time_est": "25m"},
                        {"slot": "Slot 2: 🎯 Core ICPC Topic (25-35m)", "name": "Codeforces 1718B - Fibonacci Strings", "url": "https://codeforces.com/problemset/problem/1718/B", "rating": 1900, "tag": "Greedy / DP - Re-solve bài cũ", "time_est": "35m"},
                        {"slot": "Slot 3: 🏆 OLP Decisive (35-45m)", "name": "Codeforces 1737D - Ela and the Crickets", "url": "https://codeforces.com/problemset/problem/1737/D", "rating": 2000, "tag": "Shortest Path / Floyd DP - Re-solve bài cũ", "time_est": "40m"},
                        {"slot": "Slot 4: 🧗 Checklist", "name": "Review Template CHT, Li Chao, Alien Trick, SOS DP", "url": "https://codeforces.com", "rating": 2200, "tag": "DP Optimization Notebook", "time_est": "30m"}
                    ]
                }
            ]
        },

        # =========================================================================
        # TUẦN 3 (31/10 - 06/11): TỔNG LỰC CHUẨN BỊ ICPC QUỐC GIA 2026 & CHIA CĂN, CTDL
        # =========================================================================
        {
            "week_num": 3,
            "theme": "Tuần 3: TỔNG LỰC CHUẨN BỊ CHO KỲ THI ICPC QUỐC GIA 2026 & Chia căn, Cấu trúc dữ liệu",
            "days": [
                {
                    "day_name": "Thứ Bảy",
                    "activity": "Chia căn (Sqrt Decomposition) & Mo's Algorithm nâng cao",
                    "session_type": "SQRT DECOMPOSITION",
                    "problems": [
                        {"slot": "Slot 1: ⚡ Speed Warm-up (10-15m)", "name": "Codeforces 220B - Little Elephant and Array", "url": "https://codeforces.com/problemset/problem/220/B", "rating": 1800, "tag": "Mo's Algorithm cơ bản - Ladder 16", "time_est": "25m"},
                        {"slot": "Slot 2: 🎯 Core ICPC Topic (25-35m)", "name": "Codeforces 438D - The Child and Sequence", "url": "https://codeforces.com/problemset/problem/438/D", "rating": 2300, "tag": "Segment Tree Modulo - Ladder 16 review", "time_est": "35m"},
                        {"slot": "Slot 3: 🏆 OLP Decisive (35-45m)", "name": "Codeforces 13E - Holes", "url": "https://codeforces.com/problemset/problem/13/E", "rating": 2700, "tag": "Chia căn mảng nảy - Re-solve bài cũ", "time_est": "50m"},
                        {"slot": "Slot 4: 🧗 Mastery Re-solve (45-60m)", "name": "Codeforces 1957F1 - Frequency Mismatch (Easy)", "url": "https://codeforces.com/problemset/problem/1957/F1", "rating": 2600, "tag": "Randomized / Hashing / Sqrt - Re-solve bài cũ", "time_est": "60m"}
                    ]
                },
                {
                    "day_name": "Chủ Nhật",
                    "activity": "MOCK TEST QUỐC GIA 5H: Giả lập ICPC Vietnam National 2023",
                    "session_type": "FULL MOCK TEST (5H)",
                    "problems": [
                        {"slot": "Slot 1: 🏆 FULL MOCK TEST (5H)", "name": "2023 ICPC Vietnam National Contest", "url": "https://codeforces.com/gym/104725", "rating": 2200, "tag": "Giả lập 5h Vòng Quốc Gia", "time_est": "300m"},
                        {"slot": "Slot 2: 🎯 Target Upsolve 1", "name": "Upsolve Bài Segment Tree / CTDL phân hóa trong đề", "url": "https://codeforces.com/gym/104725", "rating": 2100, "tag": "Upsolving đề thi thật", "time_est": "45m"},
                        {"slot": "Slot 3: 🏆 Target Upsolve 2", "name": "Upsolve Bài Đồ thị / Chia căn trong đề", "url": "https://codeforces.com/gym/104725", "rating": 2300, "tag": "Upsolving đề thi thật", "time_est": "50m"},
                        {"slot": "Slot 4: 🧗 Target Upsolve 3", "name": "Upsolve Bài quyết định top 5 toàn quốc", "url": "https://codeforces.com/gym/104725", "rating": 2500, "tag": "Upsolving đề thi thật", "time_est": "60m"}
                    ]
                },
                {
                    "day_name": "Thứ Hai",
                    "activity": "Upsolve Mock Quốc Gia & Segment Tree nâng cao (Beats, Lazy)",
                    "session_type": "SEGTREE & UPSOLVE",
                    "problems": [
                        {"slot": "Slot 1: ⚡ Speed Warm-up (10-15m)", "name": "Codeforces 380C - Sereja and Brackets", "url": "https://codeforces.com/problemset/problem/380/C", "rating": 1700, "tag": "SegTree kết hợp ngoặc - Ladder 16", "time_est": "20m"},
                        {"slot": "Slot 2: 🎯 Core ICPC Topic (25-35m)", "name": "Codeforces 786B - Legacy", "url": "https://codeforces.com/contest/786/problem/B", "rating": 2200, "tag": "Segment Tree trên đồ thị - Re-solve bài cũ", "time_est": "40m"},
                        {"slot": "Slot 3: 🏆 OLP Decisive (35-45m)", "name": "Codeforces 1476E - Pattern Matching", "url": "https://codeforces.com/problemset/problem/1476/E", "rating": 2200, "tag": "Trie + Topo Sort - Re-solve bài cũ", "time_est": "40m"},
                        {"slot": "Slot 4: 🧗 Mastery Re-solve (45-60m)", "name": "Codeforces 375C - Circling Round Treasures", "url": "https://codeforces.com/problemset/problem/375/C", "rating": 2600, "tag": "BFS + Bitmask - Re-solve bài cũ", "time_est": "60m"}
                    ]
                },
                {
                    "day_name": "Thứ Ba",
                    "activity": "Persistent Data Structures (SegTree, Treap)",
                    "session_type": "PERSISTENT DS",
                    "problems": [
                        {"slot": "Slot 1: ⚡ Speed Warm-up (10-15m)", "name": "Codeforces 354C - Vasya and Beautiful Arrays", "url": "https://codeforces.com/problemset/problem/354/C", "rating": 2100, "tag": "Prefix sums / Divisors - Ladder 16 review", "time_est": "30m"},
                        {"slot": "Slot 2: 🎯 Core ICPC Topic (25-35m)", "name": "Codeforces 1768E - Partial Sorting", "url": "https://codeforces.com/problemset/problem/1768/E", "rating": 2300, "tag": "Permutations / Math - Re-solve bài cũ", "time_est": "40m"},
                        {"slot": "Slot 3: 🏆 OLP Decisive (35-45m)", "name": "In ấn & Rà soát Team Notebook chuẩn cho vòng Quốc Gia", "url": "https://codeforces.com", "rating": 2000, "tag": "Notebook checklist", "time_est": "30m"},
                        {"slot": "Slot 4: 🧗 Mastery Re-solve (45-60m)", "name": "Codeforces 986E - Prince's Problem", "url": "https://codeforces.com/contest/986/problem/E", "rating": 2800, "tag": "Persistent SegTree + Prime - Re-solve bài cũ", "time_est": "70m"}
                    ]
                },
                {
                    "day_name": "Thứ Tư",
                    "activity": "Chia căn truy vấn & Stress Testing phòng thi",
                    "session_type": "STRESS TESTING LAB",
                    "problems": [
                        {"slot": "Slot 1: ⚡ Speed Warm-up (10-15m)", "name": "Codeforces 570D - Tree Requests", "url": "https://codeforces.com/problemset/problem/570/D", "rating": 2200, "tag": "DSU on Tree / Euler Tour - Ladder 16 review", "time_est": "30m"},
                        {"slot": "Slot 2: 🎯 Core ICPC Topic (25-35m)", "name": "APIO19_bridges - Bridges", "url": "https://oj.uz/problem/view/APIO19_bridges", "rating": 2400, "tag": "Chia căn truy vấn & DSU rollback", "time_est": "45m"},
                        {"slot": "Slot 3: 🏆 OLP Decisive (35-45m)", "name": "Codeforces 1783E - Game of the Year", "url": "https://codeforces.com/problemset/problem/1783/E", "rating": 2300, "tag": "Prefix sum / Math - Re-solve bài cũ", "time_est": "40m"},
                        {"slot": "Slot 4: 🧗 Stress Test Lab", "name": "Rà soát bẫy tràn số (MOD, 64-bit) & Viết test generator", "url": "https://codeforces.com", "rating": 2200, "tag": "Stress testing script lab", "time_est": "40m"}
                    ]
                },
                {
                    "day_name": "Thứ Năm",
                    "activity": "Chiến thuật tâm lý thi đấu 3 người 1 máy vòng Quốc Gia",
                    "session_type": "TEAM STRATEGY",
                    "problems": [
                        {"slot": "Slot 1: ⚡ Speed Warm-up (10-15m)", "name": "Codeforces 476B - Dreamoon and WiFi", "url": "https://codeforces.com/problemset/problem/476/B", "rating": 1300, "tag": "Bitwise speed warm-up", "time_est": "10m"},
                        {"slot": "Slot 2: 🎯 Core ICPC Topic (25-35m)", "name": "Codeforces 1730C - Minimum Notation", "url": "https://codeforces.com/problemset/problem/1730/C", "rating": 1900, "tag": "Greedy / String - Re-solve bài cũ", "time_est": "25m"},
                        {"slot": "Slot 3: 🏆 OLP Decisive (35-45m)", "name": "Codeforces 1749D - Counting Arrays", "url": "https://codeforces.com/problemset/problem/1749/D", "rating": 1900, "tag": "Number Theory / Modulo - Re-solve bài cũ", "time_est": "30m"},
                        {"slot": "Slot 4: 🧗 Team Meeting", "name": "Họp chiến thuật Team ICPC: Phân vai đọc đề, code, trace bug", "url": "https://codeforces.com", "rating": 2000, "tag": "Team coordination meeting", "time_est": "30m"}
                    ]
                },
                {
                    "day_name": "Thứ Sáu",
                    "activity": "Thư giãn, nạp năng lượng & sẵn sàng cho Vòng Quốc Gia",
                    "session_type": "REST & RECHARGE",
                    "problems": [
                        {"slot": "Slot 1: ⚡ Speed Warm-up", "name": "Gõ nhẹ 1 bài template cơ bản lấy nhịp tay", "url": "https://codeforces.com/problemset/problem/71/A", "rating": 1000, "tag": "Warm-up nhẹ nhàng", "time_est": "5m"},
                        {"slot": "Slot 2: 🎯 Verification", "name": "Kiểm tra tài khoản, thông tin đội và điểm thi tập trung", "url": "https://olp.vn", "rating": 1500, "tag": "Checklist hành chính", "time_est": "15m"},
                        {"slot": "Slot 3: 🏆 Rest", "name": "Nghỉ ngơi, ngủ đủ giấc, chuẩn bị tinh thần thi đấu", "url": "https://olp.vn", "rating": 1500, "tag": "Giữ gìn thể lực", "time_est": "0m"},
                        {"slot": "Slot 4: 🧗 Ready", "name": "Sẵn sàng 100% bước vào Kỳ thi ICPC Quốc gia 2026", "url": "https://olp.vn", "rating": 2400, "tag": "Tâm lý tự tin vững vàng", "time_est": "0m"}
                    ]
                }
            ]
        },

        # =========================================================================
        # TUẦN 4 (07/11 - 13/11): KỲ THI ICPC QUỐC GIA 2026 & CHUYỂN GIAO SANG OLP
        # =========================================================================
        {
            "week_num": 4,
            "theme": "Tuần 4: KỲ THI ICPC QUỐC GIA 2026 (08-09/11) & Bước ngoặt chuyển giao sang Olympic",
            "days": [
                {
                    "day_name": "Thứ Bảy",
                    "activity": "Thử máy Kỳ thi ICPC Quốc gia 2026 tại điểm thi tập trung",
                    "session_type": "THỬ MÁY & WARM-UP",
                    "problems": [
                        {"slot": "Slot 1: ⚡ Thử máy tập trung (2h)", "name": "ICPC Vietnam National 2026 - Practice Session", "url": "https://codeforces.com/gyms", "rating": 1800, "tag": "Thử máy thi đấu thực tế", "time_est": "120m"},
                        {"slot": "Slot 2: 🎯 Speed Warm-up 1", "name": "Codeforces 126B - Password", "url": "https://codeforces.com/problemset/problem/126/B", "rating": 1700, "tag": "String speed check", "time_est": "15m"},
                        {"slot": "Slot 3: 🏆 Speed Warm-up 2", "name": "Codeforces 295B - Greg and Graph", "url": "https://codeforces.com/contest/295/problem/B", "rating": 1700, "tag": "Graph speed check", "time_est": "15m"},
                        {"slot": "Slot 4: 🧗 Checklist", "name": "Kiểm tra bàn phím, compiler, hệ điều hành điểm thi", "url": "https://olp.vn", "rating": 1600, "tag": "Hardware & environment check", "time_est": "20m"}
                    ]
                },
                {
                    "day_name": "Chủ Nhật",
                    "activity": "CHÍNH THỨC THI ICPC QUỐC GIA 2026 (VIETNAM NATIONAL - 5 GIỜ)",
                    "session_type": "OFFICIAL CONTEST (5H)",
                    "problems": [
                        {"slot": "Slot 1: 🏆 OFFICIAL CONTEST (5H)", "name": "2026 ICPC Vietnam National Contest", "url": "https://codeforces.com/gyms", "rating": 2300, "tag": "5h Thi tập trung toàn quốc", "time_est": "300m"},
                        {"slot": "Slot 2: 🎯 Target Upsolve 1", "name": "Upsolve Bài Toán học / Tổ hợp trong đề", "url": "https://codeforces.com/gyms", "rating": 2000, "tag": "Upsolving đề thi thật", "time_est": "45m"},
                        {"slot": "Slot 3: 🏆 Target Upsolve 2", "name": "Upsolve Bài Cấu trúc dữ liệu trong đề", "url": "https://codeforces.com/gyms", "rating": 2200, "tag": "Upsolving đề thi thật", "time_est": "50m"},
                        {"slot": "Slot 4: 🧗 Target Upsolve 3", "name": "Upsolve Bài phân hóa xác định vé Regional Đà Nẵng", "url": "https://codeforces.com/gyms", "rating": 2400, "tag": "Upsolving đề thi thật", "time_est": "60m"}
                    ]
                },
                {
                    "day_name": "Thứ Hai",
                    "activity": "Tổng kết kết quả vòng Quốc gia & Khởi động giai đoạn OLP",
                    "session_type": "DEBRIEF & OLP TRANSITION",
                    "problems": [
                        {"slot": "Slot 1: ⚡ Speed Warm-up (10-15m)", "name": "Codeforces 264B - Good Sequences", "url": "https://codeforces.com/problemset/problem/264/B", "rating": 1600, "tag": "Sieve / DP", "time_est": "20m"},
                        {"slot": "Slot 2: 🎯 Core OLP Topic (25-35m)", "name": "Codeforces 1043F - Make It One", "url": "https://codeforces.com/contest/1043/problem/F", "rating": 2400, "tag": "Bao hàm loại trừ / Mobius - Re-solve bài cũ", "time_est": "40m"},
                        {"slot": "Slot 3: 🏆 OLP Decisive (35-45m)", "name": "Codeforces 1924D - Balanced Subsequences", "url": "https://codeforces.com/problemset/problem/1924/D", "rating": 2700, "tag": "Catalan, Tổ hợp, DP - Re-solve bài cũ", "time_est": "60m"},
                        {"slot": "Slot 4: 🧗 Debrief", "name": "Tổng kết kết quả vòng Quốc Gia & Lập danh sách trọng tâm OLP", "url": "https://olp.vn", "rating": 2000, "tag": "National Contest Debrief", "time_est": "30m"}
                    ]
                },
                {
                    "day_name": "Thứ Ba",
                    "activity": "Toán học & Số học: Bao hàm loại trừ, Phi hàm Euler, Nghịch đảo",
                    "session_type": "MATH & NUMBER THEORY",
                    "problems": [
                        {"slot": "Slot 1: ⚡ Speed Warm-up (10-15m)", "name": "Codeforces 474D - Flowers", "url": "https://codeforces.com/problemset/problem/474/D", "rating": 1700, "tag": "DP + Prefix sums - Ladder 16", "time_est": "20m"},
                        {"slot": "Slot 2: 🎯 Core OLP Topic (25-35m)", "name": "VNOI c11tct - Chia kẹo Euler & Lucas", "url": "https://oj.vnoi.info/problem/c11tct", "rating": 2100, "tag": "Toán tổ hợp nâng cao", "time_est": "35m"},
                        {"slot": "Slot 3: 🏆 OLP Decisive (35-45m)", "name": "VNOI fc090_divcan - Bao hàm, Lucas", "url": "https://oj.vnoi.info/problem/fc090_divcan", "rating": 2200, "tag": "Tổ hợp, Nghịch đảo modulo", "time_est": "40m"},
                        {"slot": "Slot 4: 🧗 Mastery Re-solve (45-60m)", "name": "Codeforces 1989F - Simultaneous Coloring", "url": "https://codeforces.com/problemset/problem/1989/F", "rating": 2700, "tag": "2-SAT / Math - Re-solve bài cũ", "time_est": "65m"}
                    ]
                },
                {
                    "day_name": "Thứ Tư",
                    "activity": "Tổ hợp nâng cao, Hệ số nhị thức & Đa thức (FFT/NTT)",
                    "session_type": "COMBINATORICS & POLYNOMIALS",
                    "problems": [
                        {"slot": "Slot 1: ⚡ Speed Warm-up (10-15m)", "name": "Codeforces 1856E1 - PermuTree (Easy Version)", "url": "https://codeforces.com/problemset/problem/1856/E1", "rating": 2100, "tag": "Tree Knapsack DP - Re-solve bài cũ", "time_est": "30m"},
                        {"slot": "Slot 2: 🎯 Core OLP Topic (25-35m)", "name": "Codeforces 1700E - Sereja and Arrangement of Numbers", "url": "https://codeforces.com/problemset/problem/1700/E", "rating": 2400, "tag": "Math / Greedy - Re-solve bài cũ", "time_est": "45m"},
                        {"slot": "Slot 3: 🏆 OLP Decisive (35-45m)", "name": "Codeforces 1710B - Rain", "url": "https://codeforces.com/problemset/problem/1710/B", "rating": 2200, "tag": "Difference array / Math - Re-solve bài cũ", "time_est": "40m"},
                        {"slot": "Slot 4: 🧗 Template", "name": "Rà soát Template NTT, FFT, Inverse Modulo, Pascal Triangle", "url": "https://codeforces.com", "rating": 2200, "tag": "Polynomials Notebook", "time_est": "30m"}
                    ]
                },
                {
                    "day_name": "Thứ Năm",
                    "activity": "Lý thuyết trò chơi (Game Theory): Nim, Sprague-Grundy",
                    "session_type": "GAME THEORY",
                    "problems": [
                        {"slot": "Slot 1: ⚡ Speed Warm-up (10-15m)", "name": "Codeforces 2181F - Fragmented Nim", "url": "https://codeforces.com/contest/2181/problem/F", "rating": 1600, "tag": "Game Nim - Re-solve bài cũ", "time_est": "20m"},
                        {"slot": "Slot 2: 🎯 Core OLP Topic (25-35m)", "name": "Codeforces 944F - CTDL, Game", "url": "https://codeforces.com/contest/944/problem/F", "rating": 2400, "tag": "Game Theory / Graph - Re-solve bài cũ", "time_est": "45m"},
                        {"slot": "Slot 3: 🏆 OLP Decisive (35-45m)", "name": "Codeforces 1705E - Mark and Professor Koro", "url": "https://codeforces.com/problemset/problem/1705/E", "rating": 2200, "tag": "Bitwise / SegTree - Re-solve bài cũ", "time_est": "40m"},
                        {"slot": "Slot 4: 🧗 Mastery Re-solve (45-60m)", "name": "Codeforces 1823E - Removing Graph", "url": "https://codeforces.com/problemset/problem/1823/E", "rating": 2400, "tag": "Game Theory / Grundy on Graph - Re-solve", "time_est": "50m"}
                    ]
                },
                {
                    "day_name": "Thứ Sáu",
                    "activity": "Nhân ma trận (Matrix Exponentiation) & Khử Gauss",
                    "session_type": "MATRIX & GAUSS",
                    "problems": [
                        {"slot": "Slot 1: ⚡ Speed Warm-up (10-15m)", "name": "Codeforces 166E - Tetrahedron", "url": "https://codeforces.com/problemset/problem/166/E", "rating": 1600, "tag": "Matrix DP cơ bản", "time_est": "15m"},
                        {"slot": "Slot 2: 🎯 Core OLP Topic (25-35m)", "name": "Codeforces 1667B - Optimal Partition", "url": "https://codeforces.com/problemset/problem/1667/B", "rating": 2000, "tag": "Fenwick Tree + DP - Re-solve bài cũ", "time_est": "35m"},
                        {"slot": "Slot 3: 🏆 OLP Decisive (35-45m)", "name": "Codeforces 1672F1 - Array Shuffling", "url": "https://codeforces.com/problemset/problem/1672/F1", "rating": 2000, "tag": "Constructive / Cycles - Re-solve bài cũ", "time_est": "40m"},
                        {"slot": "Slot 4: 🧗 Template", "name": "Template Nhân ma trận nhị phân & Khử Gauss modulo 2", "url": "https://codeforces.com", "rating": 2200, "tag": "Linear Algebra Notebook", "time_est": "30m"}
                    ]
                }
            ]
        },

        # =========================================================================
        # TUẦN 5 (14/11 - 20/11): CHUYÊN SÂU OLYMPIC: HÌNH HỌC, SWEEPLINE, CTDL NÂNG CAO
        # =========================================================================
        {
            "week_num": 5,
            "theme": "Tuần 5: Chuyên sâu Olympic: Hình học tính toán, Sweepline & Cấu trúc dữ liệu nâng cao",
            "days": [
                {
                    "day_name": "Thứ Bảy",
                    "activity": "Hình học tính toán: Bao lồi (Monotone Chain / Graham Scan)",
                    "session_type": "CONVEX HULL & GEOMETRY",
                    "problems": [
                        {"slot": "Slot 1: ⚡ Speed Warm-up (10-15m)", "name": "Codeforces 166A - Rank List", "url": "https://codeforces.com/problemset/problem/166/A", "rating": 1200, "tag": "Custom comparator speed check", "time_est": "10m"},
                        {"slot": "Slot 2: 🎯 Core OLP Topic (25-35m)", "name": "VNOI cavli - Bao lồi & Hình học tính toán", "url": "https://oj.vnoi.info/problem/cavli", "rating": 2100, "tag": "Bao lồi Monotone Chain - Coản Coản sheet", "time_est": "35m"},
                        {"slot": "Slot 3: 🏆 OLP Decisive (35-45m)", "name": "Codeforces 1468G - Hình học, Tầm nhìn đỉnh núi", "url": "https://codeforces.com/contest/1468/problem/G", "rating": 2200, "tag": "Hình học tính toán, Giao điểm tia", "time_est": "40m"},
                        {"slot": "Slot 4: 🧗 Mastery Re-solve (45-60m)", "name": "Codeforces 2004F - Make a Palindrome", "url": "https://codeforces.com/problemset/problem/2004/F", "rating": 2600, "tag": "Hash / Palindrome - Re-solve bài cũ", "time_est": "60m"}
                    ]
                },
                {
                    "day_name": "Chủ Nhật",
                    "activity": "MOCK TEST OLP #1: Đề thi Siêu Cúp / Chuyên Tin các năm (3.5 Giờ)",
                    "session_type": "OLP MOCK TEST (3.5H)",
                    "problems": [
                        {"slot": "Slot 1: 🏆 OLP MOCK TEST (3.5H)", "name": "JOI Spring Camp 2023 Contest 1", "url": "https://cms.ioi-jp.org/joi2023-sp1-open", "rating": 2300, "tag": "Giả lập 3.5h Kỳ thi Cá nhân OLP", "time_est": "210m"},
                        {"slot": "Slot 2: 🎯 Target Upsolve 1", "name": "Upsolve Bài Hình học / Sweepline trong đề", "url": "https://cms.ioi-jp.org/joi2023-sp1-open", "rating": 2100, "tag": "Upsolving đề thi OLP", "time_est": "45m"},
                        {"slot": "Slot 3: 🏆 Target Upsolve 2", "name": "Upsolve Bài Quy hoạch động phân hóa trong đề", "url": "https://cms.ioi-jp.org/joi2023-sp1-open", "rating": 2300, "tag": "Upsolving đề thi OLP", "time_est": "50m"},
                        {"slot": "Slot 4: 🧗 Target Upsolve 3", "name": "Upsolve Bài Cấu trúc dữ liệu nâng cao", "url": "https://cms.ioi-jp.org/joi2023-sp1-open", "rating": 2500, "tag": "Upsolving đề thi OLP", "time_est": "60m"}
                    ]
                },
                {
                    "day_name": "Thứ Hai",
                    "activity": "Sweepline quét tọa độ X kết hợp Segment Tree",
                    "session_type": "SWEEPLINE & SEGTREE",
                    "problems": [
                        {"slot": "Slot 1: ⚡ Speed Warm-up (10-15m)", "name": "Codeforces 1666C - Connect the Points", "url": "https://codeforces.com/problemset/problem/1666/C", "rating": 1800, "tag": "Geometry / Manhattan - Re-solve bài cũ", "time_est": "25m"},
                        {"slot": "Slot 2: 🎯 Core OLP Topic (25-35m)", "name": "Codeforces 529C - Sweepline (Rooks Defender)", "url": "https://codeforces.com/contest/529/problem/C", "rating": 2200, "tag": "Sweepline + SegTree - Re-solve bài cũ", "time_est": "40m"},
                        {"slot": "Slot 3: 🏆 OLP Decisive (35-45m)", "name": "Codeforces 1698E - Permutation Shift", "url": "https://codeforces.com/problemset/problem/1698/E", "rating": 2200, "tag": "Sweepline / Greedy - Re-solve bài cũ", "time_est": "40m"},
                        {"slot": "Slot 4: 🧗 Mastery Re-solve (45-60m)", "name": "Codeforces 1704E - Count Seconds", "url": "https://codeforces.com/problemset/problem/1704/E", "rating": 2200, "tag": "DAG / Modulo Simulation - Re-solve bài cũ", "time_est": "45m"}
                    ]
                },
                {
                    "day_name": "Thứ Ba",
                    "activity": "Giao điểm đoạn thẳng, Điểm trong đa giác, Nửa mặt phẳng",
                    "session_type": "GEOMETRY PRIMITIVES",
                    "problems": [
                        {"slot": "Slot 1: ⚡ Speed Warm-up (10-15m)", "name": "Codeforces 280B - Maximum Xor Secondary", "url": "https://codeforces.com/problemset/problem/280/B", "rating": 1800, "tag": "Monotonic Stack - Ladder 16", "time_est": "25m"},
                        {"slot": "Slot 2: 🎯 Core OLP Topic (25-35m)", "name": "Codeforces 1699D - Almost Triple Deletions", "url": "https://codeforces.com/problemset/problem/1699/D", "rating": 2200, "tag": "DP + Observation - Re-solve bài cũ", "time_est": "40m"},
                        {"slot": "Slot 3: 🏆 OLP Decisive (35-45m)", "name": "Codeforces 1713E - Cross Swapping", "url": "https://codeforces.com/problemset/problem/1713/E", "rating": 2300, "tag": "2-SAT / DSU - Re-solve bài cũ", "time_est": "45m"},
                        {"slot": "Slot 4: 🧗 Template", "name": "Template Cross product, Line intersection, Point in Polygon", "url": "https://codeforces.com", "rating": 2200, "tag": "Geometry Core Notebook", "time_est": "30m"}
                    ]
                },
                {
                    "day_name": "Thứ Tư",
                    "activity": "Kỹ thuật Chia căn lớn bé & Cấu trúc dữ liệu trên lưới 2D",
                    "session_type": "SQRT HEAVY-LIGHT",
                    "problems": [
                        {"slot": "Slot 1: ⚡ Speed Warm-up (10-15m)", "name": "Codeforces 368B - Sereja and Suffixes", "url": "https://codeforces.com/problemset/problem/368/B", "rating": 1300, "tag": "Prefix distinct speed check", "time_est": "10m"},
                        {"slot": "Slot 2: 🎯 Core OLP Topic (25-35m)", "name": "COCI 1920 Paint - Chia căn lớn bé & DSU", "url": "https://oj.vnoi.info/problem/coci1920_o_paint", "rating": 2200, "tag": "Chia căn lớn bé & DSU", "time_est": "40m"},
                        {"slot": "Slot 3: 🏆 OLP Decisive (35-45m)", "name": "Codeforces 1726D - Edge Split", "url": "https://codeforces.com/problemset/problem/1726/D", "rating": 2100, "tag": "Spanning Tree / Cycles - Re-solve bài cũ", "time_est": "40m"},
                        {"slot": "Slot 4: 🧗 Mastery Re-solve (45-60m)", "name": "Codeforces 1738E - Balance Addicts", "url": "https://codeforces.com/problemset/problem/1738/E", "rating": 2300, "tag": "Combinatorics / Two Pointers - Re-solve bài cũ", "time_est": "50m"}
                    ]
                },
                {
                    "day_name": "Thứ Năm",
                    "activity": "Fenwick 2D, Segment Tree 2D & Quadtree",
                    "session_type": "2D DATA STRUCTURES",
                    "problems": [
                        {"slot": "Slot 1: ⚡ Speed Warm-up (10-15m)", "name": "Codeforces 339D - Xenia and Bit Operations", "url": "https://codeforces.com/problemset/problem/339/D", "rating": 1400, "tag": "SegTree bitwise speed check", "time_est": "10m"},
                        {"slot": "Slot 2: 🎯 Core OLP Topic (25-35m)", "name": "VNOI ITTEQ1 - Segment Tree nâng cao", "url": "https://oj.vnoi.info/problem/segtree_itteq1", "rating": 2100, "tag": "Segment Tree nâng cao", "time_est": "35m"},
                        {"slot": "Slot 3: 🏆 OLP Decisive (35-45m)", "name": "Codeforces 1740E - Hanging Hearts", "url": "https://codeforces.com/problemset/problem/1740/E", "rating": 2000, "tag": "Tree DP - Re-solve bài cũ", "time_est": "35m"},
                        {"slot": "Slot 4: 🧗 Mastery Re-solve (45-60m)", "name": "Codeforces 1748D - ConstructOR", "url": "https://codeforces.com/problemset/problem/1748/D", "rating": 2300, "tag": "Bitwise / Number Theory - Re-solve bài cũ", "time_est": "45m"}
                    ]
                },
                {
                    "day_name": "Thứ Sáu",
                    "activity": "Rà soát kho bài tập Hình học & Sweepline",
                    "session_type": "GEOMETRY REVIEW",
                    "problems": [
                        {"slot": "Slot 1: ⚡ Speed Warm-up (10-15m)", "name": "Codeforces 1753B - Factorial Divisibility", "url": "https://codeforces.com/problemset/problem/1753/B", "rating": 1900, "tag": "Number theory simulation - Re-solve bài cũ", "time_est": "25m"},
                        {"slot": "Slot 2: 🎯 Core OLP Topic (25-35m)", "name": "Codeforces 1750D - Count GCD", "url": "https://codeforces.com/problemset/problem/1750/D", "rating": 2000, "tag": "Number Theory / Inclusion-Exclusion", "time_est": "35m"},
                        {"slot": "Slot 3: 🏆 OLP Decisive (35-45m)", "name": "Codeforces 1762D - GCD Queries", "url": "https://codeforces.com/problemset/problem/1762/D", "rating": 2100, "tag": "Interactive / Number Theory - Re-solve bài cũ", "time_est": "40m"},
                        {"slot": "Slot 4: 🧗 Template", "name": "Tổng hợp template Hình học: Monotone chain, Convex polygon", "url": "https://codeforces.com", "rating": 2200, "tag": "Geometry & Sweepline Notebook", "time_est": "30m"}
                    ]
                }
            ]
        },

        # =========================================================================
        # TUẦN 6 (21/11 - 27/11): XÂU KÝ TỰ (STRINGS), LUỒNG CỰC ĐẠI, GAME THEORY
        # =========================================================================
        {
            "week_num": 6,
            "theme": "Tuần 6: Xâu ký tự (Strings), Luồng cực đại (Flow) & Game Theory",
            "days": [
                {
                    "day_name": "Thứ Bảy",
                    "activity": "Xâu ký tự (Strings): KMP, Z-function & 2D Hashing",
                    "session_type": "STRING ALGORITHMS",
                    "problems": [
                        {"slot": "Slot 1: ⚡ Speed Warm-up (10-15m)", "name": "Codeforces 432D - Prefixes and Suffixes", "url": "https://codeforces.com/problemset/problem/432/D", "rating": 2000, "tag": "Z-algo + DP - Ladder 16 review", "time_est": "25m"},
                        {"slot": "Slot 2: 🎯 Core ICPC Topic (25-35m)", "name": "DMOJ coci06c1p6 - Hash 2D", "url": "https://dmoj.ca/problem/coci06c1p6", "rating": 2100, "tag": "2D Hashing - Coản Coản sheet", "time_est": "35m"},
                        {"slot": "Slot 3: 🏆 OLP Decisive (35-45m)", "name": "Codeforces 1758D - Range = √Sum", "url": "https://codeforces.com/problemset/problem/1758/D", "rating": 1900, "tag": "Constructive / Math - Re-solve bài cũ", "time_est": "30m"},
                        {"slot": "Slot 4: 🧗 Mastery Re-solve (45-60m)", "name": "Codeforces 1764D - Doremy's Pegging Game", "url": "https://codeforces.com/problemset/problem/1764/D", "rating": 2200, "tag": "Combinatorics / Circle - Re-solve bài cũ", "time_est": "45m"}
                    ]
                },
                {
                    "day_name": "Chủ Nhật",
                    "activity": "MOCK TEST REGIONAL #4: 2023-2024 ICPC Asia Hue Regional Contest (5H)",
                    "session_type": "FULL MOCK TEST (5H)",
                    "problems": [
                        {"slot": "Slot 1: 🏆 FULL MOCK TEST (5H)", "name": "2023-2024 ICPC Asia Hue Regional Contest", "url": "https://codeforces.com/gym/104639", "rating": 2200, "tag": "5h Đấu tập Đội tuyển Regional", "time_est": "300m"},
                        {"slot": "Slot 2: 🎯 Target Upsolve 1", "name": "Upsolve Bài Xâu ký tự / Aho-Corasick trong đề", "url": "https://codeforces.com/gym/104639", "rating": 2100, "tag": "Upsolving đề thi thật", "time_est": "45m"},
                        {"slot": "Slot 3: 🏆 Target Upsolve 2", "name": "Upsolve Bài Luồng cực đại / Cặp ghép trong đề", "url": "https://codeforces.com/gym/104639", "rating": 2300, "tag": "Upsolving đề thi thật", "time_est": "50m"},
                        {"slot": "Slot 4: 🧗 Target Upsolve 3", "name": "Upsolve Bài quyết định top 3 Regional", "url": "https://codeforces.com/gym/104639", "rating": 2500, "tag": "Upsolving đề thi thật", "time_est": "60m"}
                    ]
                },
                {
                    "day_name": "Thứ Hai",
                    "activity": "Aho-Corasick Automaton & Dynamic Programming trên Trie",
                    "session_type": "AHO-CORASICK & TRIE DP",
                    "problems": [
                        {"slot": "Slot 1: ⚡ Speed Warm-up (10-15m)", "name": "Codeforces 1767D - Playoff", "url": "https://codeforces.com/problemset/problem/1767/D", "rating": 1800, "tag": "Binary tree / Greedy - Re-solve bài cũ", "time_est": "25m"},
                        {"slot": "Slot 2: 🎯 Core OLP Topic (25-35m)", "name": "LQDOJ ugpalind - DP + Aho-Corasick", "url": "https://lqdoj.edu.vn/problem/lqdoj2022r4ugpalind", "rating": 2200, "tag": "DP + Aho-Corasick Automaton", "time_est": "40m"},
                        {"slot": "Slot 3: 🏆 OLP Decisive (35-45m)", "name": "Codeforces 1770D - Koxia and Game", "url": "https://codeforces.com/problemset/problem/1770/D", "rating": 2200, "tag": "Graph / Components - Re-solve bài cũ", "time_est": "40m"},
                        {"slot": "Slot 4: 🧗 Mastery Re-solve (45-60m)", "name": "Codeforces 1774E - Two Paths", "url": "https://codeforces.com/problemset/problem/1774/E", "rating": 2200, "tag": "Tree / LCA / Greedy - Re-solve bài cũ", "time_est": "45m"}
                    ]
                },
                {
                    "day_name": "Thứ Ba",
                    "activity": "Luồng cực đại (Max Flow - Dinic) & Cắt hẹp nhất (Min Cut)",
                    "session_type": "MAX FLOW & MIN CUT",
                    "problems": [
                        {"slot": "Slot 1: ⚡ Speed Warm-up (10-15m)", "name": "Codeforces 1772E - Permutation Game", "url": "https://codeforces.com/problemset/problem/1772/E", "rating": 1800, "tag": "Game Theory / Adhoc - Re-solve bài cũ", "time_est": "25m"},
                        {"slot": "Slot 2: 🎯 Core ICPC Topic (25-35m)", "name": "Codeforces 1780D - Bit Guessing Game", "url": "https://codeforces.com/problemset/problem/1780/D", "rating": 1900, "tag": "Interactive / Bitwise - Re-solve bài cũ", "time_est": "35m"},
                        {"slot": "Slot 3: 🏆 OLP Decisive (35-45m)", "name": "Codeforces 1787D - Game on Axis", "url": "https://codeforces.com/problemset/problem/1787/D", "rating": 2200, "tag": "Tree / DFS / Counting - Re-solve bài cũ", "time_est": "40m"},
                        {"slot": "Slot 4: 🧗 Template", "name": "Template Dinic Algorithm O(V^2 E) & Các mô hình Min Cut", "url": "https://codeforces.com", "rating": 2200, "tag": "Max Flow Notebook", "time_est": "30m"}
                    ]
                },
                {
                    "day_name": "Thứ Tư",
                    "activity": "Cặp ghép hai phía cực đại & Luồng chi phí cực tiểu (MCMF)",
                    "session_type": "BIPARTITE MATCHING & MCMF",
                    "problems": [
                        {"slot": "Slot 1: ⚡ Speed Warm-up (10-15m)", "name": "Codeforces 1787C - Remove the Bracket", "url": "https://codeforces.com/problemset/problem/1787/C", "rating": 1800, "tag": "DP / Greedy - Re-solve bài cũ", "time_est": "25m"},
                        {"slot": "Slot 2: 🎯 Core ICPC Topic (25-35m)", "name": "Codeforces 1792D - Fixed Prefix Permutations", "url": "https://codeforces.com/problemset/problem/1792/D", "rating": 1800, "tag": "Trie / Permutations - Re-solve bài cũ", "time_est": "30m"},
                        {"slot": "Slot 3: 🏆 OLP Decisive (35-45m)", "name": "Codeforces 1799D2 - Hot Start Up (Hard)", "url": "https://codeforces.com/problemset/problem/1799/D2", "rating": 2200, "tag": "SegTree + DP - Re-solve bài cũ", "time_est": "40m"},
                        {"slot": "Slot 4: 🧗 Template", "name": "Template Hopcroft-Karp & MCMF with Dijkstra Potentials", "url": "https://codeforces.com", "rating": 2300, "tag": "Min Cost Max Flow Notebook", "time_est": "35m"}
                    ]
                },
                {
                    "day_name": "Thứ Năm",
                    "activity": "Suffix Automaton (SAM) & Suffix Array (SA)",
                    "session_type": "SUFFIX AUTOMATON",
                    "problems": [
                        {"slot": "Slot 1: ⚡ Speed Warm-up (10-15m)", "name": "Codeforces 1799D1 - Hot Start Up (Easy)", "url": "https://codeforces.com/problemset/problem/1799/D1", "rating": 1800, "tag": "DP cơ bản - Re-solve bài cũ", "time_est": "20m"},
                        {"slot": "Slot 2: 🎯 Core OLP Topic (25-35m)", "name": "Codeforces 1795E - Explosions?", "url": "https://codeforces.com/problemset/problem/1795/E", "rating": 2000, "tag": "Monotonic Stack / DP - Re-solve bài cũ", "time_est": "35m"},
                        {"slot": "Slot 3: 🏆 OLP Decisive (35-45m)", "name": "Codeforces 1805D - A Wide, Wide Graph", "url": "https://codeforces.com/problemset/problem/1805/D", "rating": 1900, "tag": "Tree Diameter - Re-solve bài cũ", "time_est": "30m"},
                        {"slot": "Slot 4: 🧗 Template", "name": "Template Suffix Automaton: Đếm xâu con phân biệt, K-th substring", "url": "https://codeforces.com", "rating": 2400, "tag": "Suffix Structures Notebook", "time_est": "35m"}
                    ]
                },
                {
                    "day_name": "Thứ Sáu",
                    "activity": "Kiểm tra tiến độ hoàn thành kho bài tập đã giải từ lâu",
                    "session_type": "HARD REVIEW DEBRIEF",
                    "problems": [
                        {"slot": "Slot 1: ⚡ Speed Warm-up (10-15m)", "name": "Codeforces 1815B - Sum Graph", "url": "https://codeforces.com/problemset/problem/1815/B", "rating": 2100, "tag": "Interactive / Graph - Re-solve bài cũ", "time_est": "35m"},
                        {"slot": "Slot 2: 🎯 Core ICPC Topic (25-35m)", "name": "Codeforces 1821E - Rearrange Brackets", "url": "https://codeforces.com/problemset/problem/1821/E", "rating": 2000, "tag": "Greedy / Brackets - Re-solve bài cũ", "time_est": "30m"},
                        {"slot": "Slot 3: 🏆 OLP Decisive (35-45m)", "name": "Codeforces 1806E - Tree Master", "url": "https://codeforces.com/problemset/problem/1806/E", "rating": 2400, "tag": "Sqrt on Tree / DP - Re-solve bài cũ", "time_est": "45m"},
                        {"slot": "Slot 4: 🧗 Debrief", "name": "Kiểm tra thống kê: Đã re-solve được bao nhiêu trong 137 bài cũ!", "url": "https://codeforces.com", "rating": 2200, "tag": "Review progress report", "time_est": "25m"}
                    ]
                }
            ]
        },

        # =========================================================================
        # TUẦN 7 (28/11 - 04/12): TỔNG DUYỆT CUỐI CÙNG & CHUẨN BỊ LÊN ĐƯỜNG ĐI ĐÀ NẴNG
        # =========================================================================
        {
            "week_num": 7,
            "theme": "Tuần 7: Tổng duyệt cuối cùng & Chuẩn bị lên đường đi Đà Nẵng",
            "days": [
                {
                    "day_name": "Thứ Bảy",
                    "activity": "FINAL MOCK TEST ICPC: 2022-2023 ICPC Asia Yokohama Regional (5 Giờ)",
                    "session_type": "FINAL MOCK TEST (5H)",
                    "problems": [
                        {"slot": "Slot 1: 🏆 FINAL MOCK TEST (5H)", "name": "2022-2023 ICPC Asia Yokohama Regional", "url": "https://codeforces.com/gym/104021", "rating": 2300, "tag": "5h Final Simulation", "time_est": "300m"},
                        {"slot": "Slot 2: 🎯 Target Upsolve 1", "name": "Upsolve Bài phân hóa mức trung bình trong đề", "url": "https://codeforces.com/gym/104021", "rating": 2100, "tag": "Upsolving đề thi Yokohama", "time_est": "45m"},
                        {"slot": "Slot 3: 🏆 Target Upsolve 2", "name": "Upsolve Bài phân hóa mức cao trong đề", "url": "https://codeforces.com/gym/104021", "rating": 2300, "tag": "Upsolving đề thi thật", "time_est": "50m"},
                        {"slot": "Slot 4: 🧗 Target Upsolve 3", "name": "Upsolve Bài thử thách World Finals trong đề", "url": "https://codeforces.com/gym/104021", "rating": 2600, "tag": "Upsolving đề thi thật", "time_est": "60m"}
                    ]
                },
                {
                    "day_name": "Chủ Nhật",
                    "activity": "MOCK TEST OLP #2: Đề Olympic Tin học Sinh viên Toàn quốc (3.5 Giờ)",
                    "session_type": "FINAL OLP MOCK (3.5H)",
                    "problems": [
                        {"slot": "Slot 1: 🏆 FINAL OLP MOCK (3.5H)", "name": "VOI 2021 RMAT - Observation & Matrix", "url": "https://oj.vnoi.info/problem/voi21_rmat", "rating": 2300, "tag": "Giả lập 3.5h Đề thi Olympic SV", "time_est": "210m"},
                        {"slot": "Slot 2: 🎯 Target Upsolve 1", "name": "Upsolve Bài Toán học / Ma trận trong đề", "url": "https://oj.vnoi.info/problem/voi21_rmat", "rating": 2100, "tag": "Upsolving đề thi OLP", "time_est": "45m"},
                        {"slot": "Slot 3: 🏆 Target Upsolve 2", "name": "Upsolve Bài Quy hoạch động phân hóa trong đề", "url": "https://oj.vnoi.info/problem/voi21_rmat", "rating": 2300, "tag": "Upsolving đề thi OLP", "time_est": "50m"},
                        {"slot": "Slot 4: 🧗 Target Upsolve 3", "name": "Upsolve Bài Cấu trúc dữ liệu trong đề", "url": "https://oj.vnoi.info/problem/voi21_rmat", "rating": 2400, "tag": "Upsolving đề thi OLP", "time_est": "60m"}
                    ]
                },
                {
                    "day_name": "Thứ Hai",
                    "activity": "Upsolve bài khó Mock Test & Đóng gói toàn bộ code mẫu",
                    "session_type": "FINAL UPSOLVE & CODE PACK",
                    "problems": [
                        {"slot": "Slot 1: ⚡ Speed Warm-up (10-15m)", "name": "Codeforces 1824B1 - LuoTianyi and Floating Islands (Easy)", "url": "https://codeforces.com/problemset/problem/1824/B1", "rating": 1900, "tag": "Tree / Combinatorics - Re-solve bài cũ", "time_est": "25m"},
                        {"slot": "Slot 2: 🎯 Core ICPC Topic (25-35m)", "name": "Codeforces 1827B1 - Range Sorting (Easy)", "url": "https://codeforces.com/problemset/problem/1827/B1", "rating": 1900, "tag": "Monotonic Stack - Re-solve bài cũ", "time_est": "30m"},
                        {"slot": "Slot 3: 🏆 OLP Decisive (35-45m)", "name": "Codeforces 1824B2 - LuoTianyi and Floating Islands (Hard)", "url": "https://codeforces.com/problemset/problem/1824/B2", "rating": 2300, "tag": "Tree / Math - Re-solve bài cũ", "time_est": "45m"},
                        {"slot": "Slot 4: 🧗 Mastery Re-solve (45-60m)", "name": "Codeforces 1827B2 - Range Sorting (Hard)", "url": "https://codeforces.com/problemset/problem/1827/B2", "rating": 2300, "tag": "Fenwick / Cartesian Tree - Re-solve bài cũ", "time_est": "50m"}
                    ]
                },
                {
                    "day_name": "Thứ Ba",
                    "activity": "In ấn Team Notebook bản cứng (25 trang chuẩn ICPC quốc tế)",
                    "session_type": "NOTEBOOK PRINTING",
                    "problems": [
                        {"slot": "Slot 1: ⚡ Speed Warm-up (10-15m)", "name": "Codeforces 1830B - Theofanis' Nightmare", "url": "https://codeforces.com/problemset/problem/1830/B", "rating": 1900, "tag": "Sqrt / Pairs - Re-solve bài cũ", "time_est": "25m"},
                        {"slot": "Slot 2: 🎯 Core ICPC Topic (25-35m)", "name": "Codeforces 1841E - Fill in the Matrix", "url": "https://codeforces.com/problemset/problem/1841/E", "rating": 2000, "tag": "Cartesian Tree / Greedy - Re-solve bài cũ", "time_est": "35m"},
                        {"slot": "Slot 3: 🏆 OLP Decisive (35-45m)", "name": "Codeforces 1832D2 - Red-Blue Operations (Hard)", "url": "https://codeforces.com/problemset/problem/1832/D2", "rating": 2400, "tag": "Greedy / Math - Re-solve bài cũ", "time_est": "45m"},
                        {"slot": "Slot 4: 🧗 Printing Task", "name": "In ấn 3 bản cứng Team Notebook (đúng quy định 25 trang)", "url": "https://codeforces.com", "rating": 2000, "tag": "ICPC Team Notebook", "time_est": "30m"}
                    ]
                },
                {
                    "day_name": "Thứ Tư",
                    "activity": "Kiểm tra compiler flags (-O2, -fsanitize=undefined) & máy chấm",
                    "session_type": "COMPILER ENVIRONMENT CHECK",
                    "problems": [
                        {"slot": "Slot 1: ⚡ Speed Warm-up (10-15m)", "name": "Codeforces 1844E - Great Grids", "url": "https://codeforces.com/problemset/problem/1844/E", "rating": 2200, "tag": "2-SAT / Bipartite - Re-solve bài cũ", "time_est": "35m"},
                        {"slot": "Slot 2: 🎯 Core ICPC Topic (25-35m)", "name": "Codeforces 1842E - Tenzing and Triangle", "url": "https://codeforces.com/problemset/problem/1842/E", "rating": 2300, "tag": "SegTree + DP - Re-solve bài cũ", "time_est": "40m"},
                        {"slot": "Slot 3: 🏆 OLP Decisive (35-45m)", "name": "Codeforces 1837F - Editorial for Two", "url": "https://codeforces.com/problemset/problem/1837/F", "rating": 2400, "tag": "Binary Search / Priority Queue - Re-solve", "time_est": "45m"},
                        {"slot": "Slot 4: 🧗 Flags Check", "name": "Thử nghiệm cờ biên dịch: -O2 -fsanitize=undefined,address", "url": "https://codeforces.com", "rating": 2100, "tag": "Compiler flags verification", "time_est": "25m"}
                    ]
                },
                {
                    "day_name": "Thứ Năm",
                    "activity": "Họp chiến thuật team 3 người 1 máy lần cuối trước khi bay",
                    "session_type": "FINAL TEAM STRATEGY",
                    "problems": [
                        {"slot": "Slot 1: ⚡ Speed Warm-up (10-15m)", "name": "Codeforces 1850H - The Third Letter", "url": "https://codeforces.com/problemset/problem/1850/H", "rating": 1700, "tag": "Weighted DSU speed check", "time_est": "15m"},
                        {"slot": "Slot 2: 🎯 Core ICPC Topic (25-35m)", "name": "Codeforces 1851G - Vlad and the Mountains", "url": "https://codeforces.com/problemset/problem/1851/G", "rating": 1900, "tag": "Offline queries + DSU - Re-solve bài cũ", "time_est": "30m"},
                        {"slot": "Slot 3: 🏆 OLP Decisive (35-45m)", "name": "Codeforces 1856C - To Become Max", "url": "https://codeforces.com/problemset/problem/1856/C", "rating": 1600, "tag": "Binary search on answer speed check", "time_est": "20m"},
                        {"slot": "Slot 4: 🧗 Final Team Meeting", "name": "Họp chiến thuật Team ICPC: Phân chia máy và xử lý áp lực", "url": "https://codeforces.com", "rating": 2200, "tag": "Team mindset and strategy", "time_est": "30m"}
                    ]
                },
                {
                    "day_name": "Thứ Sáu",
                    "activity": "Nghỉ ngơi, chuẩn bị hành lý, giấy tờ tùy thân và vé đi Đà Nẵng",
                    "session_type": "PACKING & TRAVEL PREP",
                    "problems": [
                        {"slot": "Slot 1: ⚡ Travel Prep", "name": "Kiểm tra CCCD/CMND, thẻ sinh viên, giấy cử đoàn của trường", "url": "https://olp.vn", "rating": 1500, "tag": "Travel documents checklist", "time_est": "15m"},
                        {"slot": "Slot 2: 🎯 Gear Check", "name": "Chuẩn bị bàn phím cơ dự phòng (nếu BTC cho phép) & áo ấm", "url": "https://olp.vn", "rating": 1500, "tag": "Hardware & clothing checklist", "time_est": "15m"},
                        {"slot": "Slot 3: 🏆 Mental Rest", "name": "Thư giãn, nghe nhạc, nạp năng lượng tinh thần", "url": "https://olp.vn", "rating": 1500, "tag": "Mental relaxation", "time_est": "0m"},
                        {"slot": "Slot 4: 🧗 Ready to Fly", "name": "Hoàn tất chuẩn bị để cất cánh đến TP. Đà Nẵng!", "url": "https://olp.vn", "rating": 2400, "tag": "Flight to Da Nang", "time_est": "0m"}
                    ]
                }
            ]
        },

        # =========================================================================
        # TUẦN 8 (05/12 - 11/12): CHUNG KẾT TOÀN QUỐC OLP'26 & ICPC ASIA DANANG 2026
        # =========================================================================
        {
            "week_num": 8,
            "theme": "Tuần 8: VÒNG CHUNG KẾT TOÀN QUỐC OLP'26 & ICPC ASIA DANANG 2026 (TẠI VKU)",
            "days": [
                {
                    "day_name": "Thứ Bảy",
                    "activity": "Di chuyển đến TP. Đà Nẵng, nhận phòng & ổn định nơi lưu trú",
                    "session_type": "ARRIVE IN DA NANG",
                    "problems": [
                        {"slot": "Slot 1: ⚡ Check-in", "name": "Di chuyển đến Đà Nẵng, nhận phòng khách sạn", "url": "https://olp.vn", "rating": 1200, "tag": "Arrival & Check-in", "time_est": "0m"},
                        {"slot": "Slot 2: 🎯 Team Gathering", "name": "Họp mặt toàn đội, ăn uống nhẹ nhàng", "url": "https://olp.vn", "rating": 1200, "tag": "Team dinner & bonding", "time_est": "0m"},
                        {"slot": "Slot 3: 🏆 Climate Adapt", "name": "Làm quen với thời tiết, khí hậu Đà Nẵng", "url": "https://olp.vn", "rating": 1200, "tag": "Adaptation", "time_est": "0m"},
                        {"slot": "Slot 4: 🧗 Rest", "name": "Nghỉ ngơi sớm sau chuyến bay/xe", "url": "https://olp.vn", "rating": 1200, "tag": "Good night sleep", "time_est": "0m"}
                    ]
                },
                {
                    "day_name": "Chủ Nhật",
                    "activity": "Tham quan Trường ĐH CNTT và Truyền thông Việt - Hàn (VKU Đà Nẵng)",
                    "session_type": "SITE VISIT (VKU)",
                    "problems": [
                        {"slot": "Slot 1: ⚡ Venue Tour", "name": "Thăm quan khuôn viên trường VKU Đà Nẵng", "url": "https://olp.vn", "rating": 1200, "tag": "Site inspection", "time_est": "0m"},
                        {"slot": "Slot 2: 🎯 Hall Inspection", "name": "Định vị phòng thi, khu vực cách ly, hội trường khai mạc", "url": "https://olp.vn", "rating": 1200, "tag": "Logistics check", "time_est": "0m"},
                        {"slot": "Slot 3: 🏆 Friendly Chat", "name": "Giao lưu với các đoàn đội tuyển bạn toàn quốc", "url": "https://olp.vn", "rating": 1500, "tag": "Community networking", "time_est": "0m"},
                        {"slot": "Slot 4: 🧗 Mental Prep", "name": "Chuẩn bị tâm lý thi đấu tự tin", "url": "https://olp.vn", "rating": 1500, "tag": "Focus & calm", "time_est": "0m"}
                    ]
                },
                {
                    "day_name": "Thứ Hai",
                    "activity": "Gõ code nhẹ nhàng vài bài cơ bản lấy cảm giác phím mượt mà",
                    "session_type": "LIGHT KEYBOARD WARM-UP",
                    "problems": [
                        {"slot": "Slot 1: ⚡ Warm-up 1", "name": "Codeforces 476B - Dreamoon and WiFi", "url": "https://codeforces.com/problemset/problem/476/B", "rating": 1300, "tag": "Light warm-up", "time_est": "10m"},
                        {"slot": "Slot 2: 🎯 Warm-up 2", "name": "Codeforces 217A - Ice Skating", "url": "https://codeforces.com/problemset/problem/217/A", "rating": 1400, "tag": "DSU warm-up", "time_est": "15m"},
                        {"slot": "Slot 3: 🏆 Warm-up 3", "name": "Codeforces 295B - Greg and Graph", "url": "https://codeforces.com/contest/295/problem/B", "rating": 1700, "tag": "Floyd trick warm-up", "time_est": "20m"},
                        {"slot": "Slot 4: 🧗 Rest", "name": "Nghỉ ngơi, giữ đầu óc thông thoáng cho ngày thi cá nhân OLP", "url": "https://olp.vn", "rating": 1500, "tag": "Mental freshness", "time_est": "0m"}
                    ]
                },
                {
                    "day_name": "Thứ Ba",
                    "activity": "ĐĂNG KÝ THAM GIA OLP & ICPC ASIA DANANG TẠI VKU; CHUNG KẾT OLYMPIC AI",
                    "session_type": "REGISTRATION & CEREMONY",
                    "problems": [
                        {"slot": "Slot 1: ⚡ Check-in", "name": "Đăng ký OLP'26 & ICPC Asia Danang tại VKU Đà Nẵng", "url": "https://olp.vn", "rating": 1500, "tag": "Official Registration", "time_est": "30m"},
                        {"slot": "Slot 2: 🎯 Badge & Kit", "name": "Nhận thẻ thi, áo đấu, quà lưu niệm Ban tổ chức", "url": "https://olp.vn", "rating": 1500, "tag": "Kit Collection", "time_est": "20m"},
                        {"slot": "Slot 3: 🏆 Opening Ceremony", "name": "Dự Lễ Khai Mạc Olympic Tin học Sinh viên Toàn quốc 2026", "url": "https://olp.vn", "rating": 1500, "tag": "Ceremony", "time_est": "60m"},
                        {"slot": "Slot 4: 🧗 Early Sleep", "name": "Ngủ sớm chuẩn bị cho buổi sáng thi đấu cá nhân OLP", "url": "https://olp.vn", "rating": 2000, "tag": "Recharge for Game Day", "time_est": "0m"}
                    ]
                },
                {
                    "day_name": "Thứ Tư",
                    "activity": "CHÍNH THỨC THI OLYMPIC TIN HỌC SINH VIÊN (OLP'26) - KHỐI CHUYÊN TIN & SIÊU CÚP",
                    "session_type": "OFFICIAL CONTEST (OLP'26)",
                    "problems": [
                        {"slot": "Slot 1: 🏆 OFFICIAL CONTEST (3-4H)", "name": "Kỳ thi Cá nhân Olympic Tin học SV 2026 (09/12/2026)", "url": "https://olp.vn", "rating": 2400, "tag": "Tranh giải Nhất / Cúp Vàng OLP", "time_est": "240m"},
                        {"slot": "Slot 2: 🎯 Target Upsolve 1", "name": "Upsolve & Thảo luận bài thi cá nhân OLP", "url": "https://olp.vn", "rating": 2100, "tag": "Debrief OLP", "time_est": "45m"},
                        {"slot": "Slot 3: 🏆 Target Upsolve 2", "name": "Chuyển trạng thái tâm lý từ Cá nhân sang Đồng đội 3 người", "url": "https://olp.vn", "rating": 2000, "tag": "Team mode activation", "time_est": "30m"},
                        {"slot": "Slot 4: 🧗 Ready for Asia", "name": "Sẵn sàng cho trận chung kết cao nhất: ICPC Asia Danang!", "url": "https://olp.vn", "rating": 2400, "tag": "Asia Regional readiness", "time_est": "0m"}
                    ]
                },
                {
                    "day_name": "Thứ Năm",
                    "activity": "KHAI MẠC ICPC ASIA DANANG 2026; THỬ MÁY (PRACTICE SESSION 2H) & NỘP NOTEBOOK",
                    "session_type": "PRACTICE & NOTEBOOK CHECK",
                    "problems": [
                        {"slot": "Slot 1: ⚡ Practice Session (2h)", "name": "Khai mạc & Thử máy ICPC Asia Danang (10/12/2026)", "url": "https://olp.vn", "rating": 2000, "tag": "Practice Session 2h chính thức", "time_est": "120m"},
                        {"slot": "Slot 2: 🎯 Notebook Submission", "name": "Nộp Team Notebook 25 trang cho Ban Giám Khảo kiểm duyệt", "url": "https://olp.vn", "rating": 1800, "tag": "Notebook Verification", "time_est": "20m"},
                        {"slot": "Slot 3: 🏆 Final Team Meeting", "name": "Họp chiến thuật xuất trận lần cuối: Săn giải Nhất & Vé World Finals!", "url": "https://olp.vn", "rating": 2200, "tag": "Final War Room", "time_est": "30m"},
                        {"slot": "Slot 4: 🧗 Rest", "name": "Nghỉ ngơi, ngủ đủ giấc, chuẩn bị 5 tiếng thi đấu lịch sử", "url": "https://olp.vn", "rating": 2000, "tag": "Pre-battle rest", "time_est": "0m"}
                    ]
                },
                {
                    "day_name": "Thứ Sáu",
                    "activity": "CHÍNH THỨC THI LẬP TRÌNH QUỐC TẾ ICPC ASIA DANANG 2026 (5 TIẾNG: 08:00 - 13:00)",
                    "session_type": "OFFICIAL CONTEST (5H ASIA)",
                    "problems": [
                        {"slot": "Slot 1: 🏆 OFFICIAL CONTEST (5H)", "name": "Chính thức thi ICPC Asia Danang 2026 (11/12/2026: 08:00 - 13:00)", "url": "https://icpc.global", "rating": 2600, "tag": "5h Đấu đỉnh cao Châu Á", "time_est": "300m"},
                        {"slot": "Slot 2: 🎯 Closing Ceremony", "name": "Dự Lễ Bế mạc & Trao giải Olympic Tin học SV và ICPC Asia Danang", "url": "https://olp.vn", "rating": 2000, "tag": "Award Ceremony", "time_est": "120m"},
                        {"slot": "Slot 3: 🏆 Gala Dinner", "name": "Gala Dinner tổng kết mùa giải & Giao lưu cộng đồng CP", "url": "https://olp.vn", "rating": 1500, "tag": "Celebration", "time_est": "120m"},
                        {"slot": "Slot 4: 🧗 Champion", "name": "Hoàn thành mỹ mãn mùa giải ICPC & Olympic Tin học SV 2026!", "url": "https://olp.vn", "rating": 2800, "tag": "Mission Accomplished", "time_est": "0m"}
                    ]
                }
            ]
        }
    ]

    schedule = []
    day_offset = 0

    for w in weeks_data:
        w_num = w["week_num"]
        w_theme = w["theme"]
        for d in w["days"]:
            calc_date = cur_date + datetime.timedelta(days=day_offset)
            date_str = calc_date.strftime("%Y-%m-%d")
            day_name = d["day_name"]
            
            # Format backward-compatible summary fields
            probs = d["problems"]
            prob_names_summary = f"Bộ {len(probs)} bài: " + ", ".join(p["name"].split(" - ")[0] for p in probs)
            ratings = [p["rating"] for p in probs if isinstance(p.get("rating"), (int, float))]
            rating_str = f"{min(ratings)} - {max(ratings)}" if ratings else "1600 - 2400"
            primary_link = probs[0]["url"]

            # Add unique id to each problem
            enriched_probs = []
            for p_idx, p in enumerate(probs, 1):
                enriched_p = dict(p)
                enriched_p["id"] = f"{date_str}_p{p_idx}"
                enriched_probs.append(enriched_p)

            schedule.append({
                "date": calc_date,
                "date_str": date_str,
                "day_name": day_name,
                "week_num": w_num,
                "week_theme": w_theme,
                "activity": d["activity"],
                "session_type": d["session_type"],
                "target_count": len(probs),
                "problems": enriched_probs,
                # Backward-compatible fields
                "link": primary_link,
                "problem_name": prob_names_summary,
                "rating": rating_str,
                "status": "Chưa làm"
            })
            day_offset += 1

    return schedule

if __name__ == "__main__":
    sched = get_master_schedule()
    print(f"Total days: {len(sched)}")
    total_probs = sum(len(d['problems']) for d in sched)
    print(f"Total problems: {total_probs}")

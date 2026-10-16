"""
Export module: Converts cleaned, categorized, and roadmap-mapped CP learning data into:
1. A master multi-sheet Excel file (.xlsx) using Pandas & OpenPyXL.
2. A high-performance JSON snapshot (web/data/data.json) for instant GitHub Pages static hosting.
"""

import sys
import json
from pathlib import Path
from typing import Dict, List, Any

# Configure UTF-8 encoding for Windows stdout/stderr
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd
from config.config import MASTER_EXCEL_PATH, FRONTEND_DATA_JSON
from scripts.account_crawler import run_roadmap_and_account_pipeline

def compute_hierarchical_stats(exercises: List[Dict[str, Any]], roadmap_nodes: List[Dict[str, Any]], accounts: Dict[str, str]) -> Dict[str, Any]:
    """Computes comprehensive metrics across accounts, tiers, and categories."""
    platform_counts = {}
    tier_counts = {"BASIC": 0, "INTERMEDIATE": 0, "HARD": 0, "INSANE": 0}
    tier_solved = {"BASIC": 0, "INTERMEDIATE": 0, "HARD": 0, "INSANE": 0}
    difficulty_counts = {}
    total_solved = 0

    for ex in exercises:
        plat = ex.get("platform", "Other")
        platform_counts[plat] = platform_counts.get(plat, 0) + 1

        tier = ex.get("roadmap_tier", "BASIC")
        if tier in tier_counts:
            tier_counts[tier] += 1
            if ex.get("solved"):
                tier_solved[tier] += 1

        if ex.get("solved"):
            total_solved += 1

        diff = ex.get("difficulty", "Medium")
        difficulty_counts[diff] = difficulty_counts.get(diff, 0) + 1

    stats = {
        "total_exercises": len(exercises),
        "total_solved": total_solved,
        "solved_percentage": round((total_solved / len(exercises) * 100), 1) if exercises else 0,
        "total_roadmap_topics": len(roadmap_nodes),
        "active_roadmap_topics": sum(1 for n in roadmap_nodes if n.get("total_problems", 0) > 0),
        "accounts": accounts,
        "platform_distribution": platform_counts,
        "tier_distribution": tier_counts,
        "tier_solved": tier_solved,
        "difficulty_distribution": difficulty_counts,
    }
    return stats

def export_full_dataset(mapper, output_excel: Path = MASTER_EXCEL_PATH, output_json: Path = FRONTEND_DATA_JSON):
    """Exports both master Excel and frontend data.json with full roadmap hierarchy."""
    exercises = list(mapper.all_problems.values())
    roadmap_nodes = mapper.roadmap_nodes
    accounts = mapper.accounts

    print(f"\n[Export] Generating Master Excel at: {output_excel} ...")

    # 1. Exercises DataFrame
    exercises_df = pd.DataFrame(exercises)
    if not exercises_df.empty and "tags" in exercises_df.columns:
        exercises_df["tags"] = exercises_df["tags"].apply(lambda t: ", ".join(t) if isinstance(t, list) else str(t))

    # Reorder key columns
    cols_order = ["id", "title", "url", "platform", "rating", "difficulty", "roadmap_tier", "roadmap_topic_title", "solved", "status", "tags", "notes", "source_sheet"]
    existing_cols = [c for c in cols_order if c in exercises_df.columns] + [c for c in exercises_df.columns if c not in cols_order]
    exercises_df = exercises_df[existing_cols]

    # 2. Roadmap Hierarchy DataFrame
    roadmap_rows = []
    for node in roadmap_nodes:
        prob_samples = ", ".join([p.get("id") or "" for p in node.get("problems", [])[:5]])
        roadmap_rows.append({
            "Tier": node.get("tier"),
            "Category": node.get("category"),
            "Topic ID": node.get("id"),
            "Topic Name": node.get("title"),
            "Total Problems": node.get("total_problems", 0),
            "Solved Problems": node.get("solved_problems", 0),
            "Completion %": f"{node.get('completion_pct', 0)}%",
            "Sample Problems": prob_samples
        })
    roadmap_df = pd.DataFrame(roadmap_rows)

    # 3. Accounts DataFrame
    accounts_rows = []
    for plat, handle in accounts.items():
        accounts_rows.append({"Platform": plat, "Handle / Username": handle})
    accounts_df = pd.DataFrame(accounts_rows)

    # 4. Stats Summary DataFrame
    stats = compute_hierarchical_stats(exercises, roadmap_nodes, accounts)
    stats_rows = [
        {"Metric": "Total Problems Collected", "Value": stats["total_exercises"]},
        {"Metric": "Total Verified Solved", "Value": stats["total_solved"]},
        {"Metric": "Overall Completion %", "Value": f"{stats['solved_percentage']}%"},
        {"Metric": "Curriculum Roadmap Topics", "Value": stats["total_roadmap_topics"]},
        {"Metric": "Active Topics with Problems", "Value": stats["active_roadmap_topics"]},
    ]
    for tier, cnt in stats["tier_distribution"].items():
        stats_rows.append({"Metric": f"Tier [{tier}] Problems", "Value": f"{stats['tier_solved'].get(tier, 0)} / {cnt}"})
    for plat, cnt in stats["platform_distribution"].items():
        stats_rows.append({"Metric": f"Platform: {plat}", "Value": cnt})

    stats_df = pd.DataFrame(stats_rows)

    # Write multi-sheet Excel
    try:
        with pd.ExcelWriter(output_excel, engine="openpyxl") as writer:
            roadmap_df.to_excel(writer, sheet_name="Roadmap_Hierarchy", index=False)
            exercises_df.to_excel(writer, sheet_name="Exercises", index=False)
            accounts_df.to_excel(writer, sheet_name="User_Accounts", index=False)
            stats_df.to_excel(writer, sheet_name="Stats_Summary", index=False)
        print(f"[Export] Master Excel updated! ({output_excel.name} - {output_excel.stat().st_size // 1024} KB)")
    except PermissionError:
        alt_path = output_excel.parent / "master_cp_data_updated.xlsx"
        print(f"[Export] Notice: '{output_excel.name}' is currently open in Microsoft Excel.")
        print(f"[Export] Saving updated master dataset to '{alt_path.name}' instead...")
        with pd.ExcelWriter(alt_path, engine="openpyxl") as writer:
            roadmap_df.to_excel(writer, sheet_name="Roadmap_Hierarchy", index=False)
            exercises_df.to_excel(writer, sheet_name="Exercises", index=False)
            accounts_df.to_excel(writer, sheet_name="User_Accounts", index=False)
            stats_df.to_excel(writer, sheet_name="Stats_Summary", index=False)
        print(f"[Export] Alternative Master Excel updated! ({alt_path.name} - {alt_path.stat().st_size // 1024} KB)")

    # 5. Export JSON for Web Frontend
    print(f"[Export] Generating Frontend JSON snapshot at: {output_json} ...")
    payload = {
        "updated_at": pd.Timestamp.now().isoformat(),
        "stats": stats,
        "accounts": accounts,
        "roadmap_nodes": roadmap_nodes,
        "exercises": exercises,
        "materials": [],
        "projects": [
            {
                "id": "proj-goal-voi",
                "title": "Goal: >2000 Problems before VOI",
                "category": "Target Milestone",
                "description": f"Verified solved: {stats['total_solved']} problems across Codeforces, VNOJ, CSES, LQDOJ. Target: Candidate Master & Nhì Quốc Gia.",
                "status": "In Progress",
                "tags": ["VOI", "Candidate Master", "ICPC"]
            }
        ]
    }
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    print(f"[Export] Frontend JSON snapshot updated! ({output_json.stat().st_size // 1024} KB)")

if __name__ == "__main__":
    mapper = run_roadmap_and_account_pipeline()
    export_full_dataset(mapper)

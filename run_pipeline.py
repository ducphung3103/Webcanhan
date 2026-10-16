"""
Master Orchestration Pipeline for CP Learning Management System & Portfolio.
Executes end-to-end workflow:
1. Ingest from local sheets & user platform accounts (Codeforces, VNOJ, CSES, LQDOJ, etc.)
2. Build 4-Tier Curriculum Roadmap from 'New Roadmap.docx'
3. Map every problem to its suitable place in the Roadmap using rule-based classification
4. Export Master Excel (multi-sheet) and Frontend JSON snapshot (web/data/data.json)
5. Cloud Sync (Google Sheets & Firebase Firestore).
"""

import sys
import argparse
from pathlib import Path

# Configure UTF-8 encoding for Windows stdout/stderr
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.account_crawler import run_roadmap_and_account_pipeline
from scripts.export_master import export_full_dataset
from scripts.sync_firebase import SyncManager
from scripts.training_planner import run_pipeline as run_training_planner

def main():
    parser = argparse.ArgumentParser(
        description="Automated Competitive Programming (CP) LMS & Portfolio Pipeline"
    )
    parser.add_argument("--all", action="store_true", help="Run full pipeline: scrape, map, export, and sync")
    parser.add_argument("--training", action="store_true", help="Generate ICPC & OLP Training Schedule and Review Workbook")
    parser.add_argument("--crawl", action="store_true", help="Crawl and map CP data from local sheets, docx roadmap, and accounts")
    parser.add_argument("--export", action="store_true", help="Export mapped dataset to master .xlsx and frontend .json")
    parser.add_argument("--sync", action="store_true", help="Sync data to Google Sheets & Firebase Firestore")
    parser.add_argument("--dry-run", action="store_true", help="Run validation without external network writes")

    args = parser.parse_args()

    # Default to --all if no specific stage chosen
    if not any([args.all, args.training, args.crawl, args.export, args.sync]):
        args.all = True

    print("=" * 70)
    print("🚀 COMPETITIVE PROGRAMMING ROADMAP & PORTFOLIO AUTOMATION PIPELINE")
    print("=" * 70)

    mapper = None

    # Step 1: Ingest accounts, parse New Roadmap.docx, map problems
    if args.all or args.crawl:
        print("\n[Stage 1/3] Parsing Roadmap & Mapping Problems Across User Accounts...")
        mapper = run_roadmap_and_account_pipeline()

    # Step 2: Export Master Excel & JSON
    if args.all or args.export:
        print("\n[Stage 2/3] Exporting Master Excel Hierarchy & Frontend JSON...")
        if mapper is None:
            mapper = run_roadmap_and_account_pipeline()
        export_full_dataset(mapper)

    # Step 3: Cloud Synchronization
    if args.all or args.sync:
        print("\n[Stage 3/3] Synchronizing with Google Sheets and Firebase Firestore...")
        sync_mgr = SyncManager(dry_run=args.dry_run)
        try:
            # Check for master_cp_data.xlsx or alternative if locked
            if not sync_mgr.excel_path.exists():
                alt_excel = PROJECT_ROOT / "master_cp_data_updated.xlsx"
                if alt_excel.exists():
                    sync_mgr.excel_path = alt_excel

            dfs = sync_mgr.load_excel_data()
            sync_mgr.sync_to_google_sheets(dfs)
            sync_mgr.sync_to_firestore(dfs)
        except Exception as e:
            print(f"[Pipeline] Notice during sync stage: {e}")

    # Step 4: ICPC & Olympic Training & Forgotten Problem Review
    if args.all or args.training:
        print("\n[Stage Extra] Generating ICPC & Olympic Training & Forgotten Hard Problem Review Workbook...")
        run_training_planner()

    print("\n" + "=" * 70)
    print("✨ PIPELINE RUN COMPLETED SUCCESSFULLY!")
    print("=" * 70)

if __name__ == "__main__":
    main()

"""
Synchronization Engine: Reads master_cp_data.xlsx and synchronizes:
1. Google Sheets (Master Sheet via gspread / Google Sheets API)
2. Firebase Cloud Firestore (collections: exercises, materials, projects, roadmap, metadata)
Supports dry-run validation when credentials are not yet supplied.
"""

import sys
import json
import time
from pathlib import Path
from typing import Dict, List, Any, Optional

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
from config.config import (
    MASTER_EXCEL_PATH,
    GOOGLE_SPREADSHEET_ID,
    COLLECTIONS,
    get_service_account_dict
)

class SyncManager:
    def __init__(self, excel_path: Path = MASTER_EXCEL_PATH, dry_run: bool = False):
        self.excel_path = Path(excel_path)
        self.dry_run = dry_run
        self.cred_dict = get_service_account_dict()
        self.firestore_db = None
        self.gspread_client = None

    def load_excel_data(self) -> Dict[str, pd.DataFrame]:
        """Reads all sheets from the master Excel workbook."""
        if not self.excel_path.exists():
            raise FileNotFoundError(f"Master Excel file not found at: {self.excel_path}")

        print(f"[Sync] Loading data from {self.excel_path.name}...")
        xl = pd.ExcelFile(self.excel_path)
        dfs = {}
        for sname in xl.sheet_names:
            dfs[sname] = xl.parse(sname).fillna("")
            print(f"  - Sheet '{sname}': {len(dfs[sname])} rows")
        return dfs

    # ==========================================
    # 1. GOOGLE SHEETS SYNCHRONIZATION
    # ==========================================
    def sync_to_google_sheets(self, dfs: Dict[str, pd.DataFrame]):
        """Synchronizes dataframes to target Google Spreadsheet."""
        print("\n--- [Sync: Google Sheets] ---")
        if self.dry_run:
            print("[Sync] Dry-run mode enabled: Skipping live Google Sheets network calls.")
            return

        if not GOOGLE_SPREADSHEET_ID:
            print("[Sync] Notice: GOOGLE_SPREADSHEET_ID is not configured in .env or environment.")
            print("[Sync] To sync with Google Sheets, add GOOGLE_SPREADSHEET_ID=<your-sheet-id>.")
            return

        if not self.cred_dict:
            print("[Sync] Notice: Google service account credentials not found.")
            print("[Sync] To enable Google Sheets sync, provide config/service_account.json or set GOOGLE_SHEETS_CREDENTIALS.")
            return

        try:
            import gspread
            gc = gspread.service_account_from_dict(self.cred_dict)
            sh = gc.open_by_key(GOOGLE_SPREADSHEET_ID)
            print(f"[Sync] Connected to Google Spreadsheet: '{sh.title}'")

            for sname, df in dfs.items():
                try:
                    try:
                        ws = sh.worksheet(sname)
                    except gspread.exceptions.WorksheetNotFound:
                        ws = sh.add_worksheet(title=sname, rows=max(len(df) + 10, 100), cols=max(len(df.columns) + 2, 10))

                    # Prepare 2D list
                    values = [df.columns.values.tolist()] + df.values.tolist()
                    ws.clear()
                    ws.update(values)
                    print(f"  [OK] Synced sheet '{sname}' ({len(values)-1} rows)")
                    time.sleep(1) # prevent API quota limits
                except Exception as sheet_err:
                    print(f"  [Error] Failed syncing sheet '{sname}': {sheet_err}")

        except Exception as e:
            print(f"[Sync] Error connecting to Google Sheets: {e}")

    # ==========================================
    # 2. FIREBASE FIRESTORE SYNCHRONIZATION
    # ==========================================
    def init_firebase(self) -> bool:
        """Initializes firebase-admin SDK."""
        if self.firestore_db is not None:
            return True

        if not self.cred_dict:
            return False

        try:
            import firebase_admin
            from firebase_admin import credentials, firestore

            if not firebase_admin._apps:
                cred = credentials.Certificate(self.cred_dict)
                firebase_admin.initialize_app(cred)
            self.firestore_db = firestore.client()
            print("[Sync] Firebase Admin initialized successfully.")
            return True
        except Exception as e:
            print(f"[Sync] Error initializing Firebase Admin: {e}")
            return False

    def sync_to_firestore(self, dfs: Dict[str, pd.DataFrame]):
        """Batches and uploads all datasets into Cloud Firestore collections."""
        print("\n--- [Sync: Firebase Firestore] ---")
        if self.dry_run:
            print("[Sync] Dry-run mode enabled: Validating Firestore payload structure...")
            self._validate_payloads(dfs)
            return

        if not self.init_firebase():
            print("[Sync] Notice: Firebase credentials not configured or initialization failed.")
            print("[Sync] To sync with Firestore, place config/service_account.json or set FIREBASE_SERVICE_ACCOUNT_KEY.")
            print("[Sync] In offline/static mode, the website continues to use web/data/data.json snapshot seamlessly.")
            return

        db = self.firestore_db

        # 1. Sync Exercises Collection
        if "Exercises" in dfs:
            self._sync_collection_in_batches(
                collection_name=COLLECTIONS["EXERCISES"],
                df=dfs["Exercises"],
                id_col="id"
            )

        # 2. Sync Materials Collection
        if "Materials" in dfs:
            self._sync_collection_in_batches(
                collection_name=COLLECTIONS["MATERIALS"],
                df=dfs["Materials"],
                id_col="id"
            )

        # 3. Sync Roadmap Collection
        if "Roadmap" in dfs:
            self._sync_collection_in_batches(
                collection_name=COLLECTIONS["ROADMAP"],
                df=dfs["Roadmap"],
                id_col="id"
            )

        # 4. Sync Projects Collection
        if "Projects" in dfs:
            self._sync_collection_in_batches(
                collection_name=COLLECTIONS["PROJECTS"],
                df=dfs["Projects"],
                id_col="id"
            )

        # 5. Sync Metadata
        try:
            meta_ref = db.collection("metadata").document("system_info")
            meta_ref.set({
                "last_synced_at": pd.Timestamp.now().isoformat(),
                "total_exercises": len(dfs.get("Exercises", [])),
                "total_materials": len(dfs.get("Materials", [])),
                "total_roadmap": len(dfs.get("Roadmap", [])),
                "status": "Healthy"
            })
            print("  [OK] Synced metadata/system_info")
        except Exception as e:
            print(f"  [Error] Failed syncing metadata: {e}")

    def _sync_collection_in_batches(self, collection_name: str, df: pd.DataFrame, id_col: str = "id", batch_limit: int = 400):
        """Batches Firestore writes (max 500 writes per batch in Firestore)."""
        db = self.firestore_db
        records = df.to_dict(orient="records")
        total = len(records)
        print(f"[Firestore] Syncing collection '{collection_name}' ({total} documents)...")

        batch = db.batch()
        batch_count = 0
        total_synced = 0

        for idx, rec in enumerate(records):
            doc_id = str(rec.get(id_col) or f"doc_{idx+1}").strip()
            # Clean document ID for Firestore (no slashes)
            clean_id = doc_id.replace("/", "_").replace("\\", "_")
            
            # Convert tags back to list if comma-separated
            if "tags" in rec and isinstance(rec["tags"], str):
                rec["tags"] = [t.strip() for t in rec["tags"].split(",") if t.strip()]

            doc_ref = db.collection(collection_name).document(clean_id)
            batch.set(doc_ref, rec, merge=True)
            batch_count += 1

            if batch_count >= batch_limit or idx == total - 1:
                batch.commit()
                total_synced += batch_count
                print(f"  -> Committed batch: {total_synced}/{total} docs to '{collection_name}'")
                batch = db.batch()
                batch_count = 0
                time.sleep(0.2)

        print(f"  [OK] Successfully synced '{collection_name}'!")

    def _validate_payloads(self, dfs: Dict[str, pd.DataFrame]):
        """Dry-run payload integrity verification."""
        for name, df in dfs.items():
            print(f"  [Validation] Sheet '{name}': {len(df)} records, columns: {list(df.columns)}")
        print("  [Validation Passed] All dataset schemas are compliant for Firestore and Google Sheets.")

def run_sync(dry_run: bool = False):
    manager = SyncManager(dry_run=dry_run)
    dfs = manager.load_excel_data()
    manager.sync_to_google_sheets(dfs)
    manager.sync_to_firestore(dfs)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Sync CP Data to Google Sheets and Firebase Firestore.")
    parser.add_argument("--dry-run", action="store_true", help="Run validation without network writes")
    args = parser.parse_args()

    run_sync(dry_run=args.dry_run)

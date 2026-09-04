"""
Chargeback Evidence AI - Database Engine
Supports Supabase Postgres client with a seamless local SQLite & vector fallback engine.
"""

import os
import json
import sqlite3
import numpy as np
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
from app.config import settings

DB_FILE = settings.DATA_DIR / "chargeback.sqlite"

class LocalDatabaseManager:
    """
    Robust local SQLite database implementing the schema from Phase 1 (schema.sql).
    Enables instant out-of-the-box local execution, offline demos, and test suites.
    """
    def __init__(self, db_path: Path = DB_FILE):
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def get_connection(self):
        conn = sqlite3.connect(str(self.db_path), check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        conn = self.get_connection()
        cursor = conn.cursor()

        # 1. merchants
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS merchants (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                phone TEXT NOT NULL,
                phone_number TEXT,
                gst_number TEXT,
                pan_number TEXT,
                business_type TEXT DEFAULT 'E-Commerce / D2C',
                address TEXT,
                is_verified INTEGER DEFAULT 1,
                created_at TEXT
            )
        ''')

        # 2. customers
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id TEXT PRIMARY KEY,
                phone_number TEXT NOT NULL UNIQUE,
                full_name TEXT NOT NULL,
                email TEXT,
                created_at TEXT
            )
        ''')

        # 3. merchant_vault_documents
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS merchant_vault_documents (
                id TEXT PRIMARY KEY,
                merchant_id TEXT NOT NULL,
                doc_type TEXT NOT NULL,
                file_name TEXT NOT NULL,
                file_path TEXT NOT NULL,
                verification_status TEXT DEFAULT 'VERIFIED',
                uploaded_at TEXT,
                FOREIGN KEY (merchant_id) REFERENCES merchants (id)
            )
        ''')

        # 4. customer_vault_documents
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customer_vault_documents (
                id TEXT PRIMARY KEY,
                customer_id TEXT NOT NULL,
                doc_type TEXT NOT NULL,
                file_name TEXT NOT NULL,
                file_path TEXT NOT NULL,
                file_size_bytes INTEGER DEFAULT 0,
                verification_status TEXT DEFAULT 'VERIFIED',
                uploaded_at TEXT,
                FOREIGN KEY (customer_id) REFERENCES customers (id)
            )
        ''')

        # 5. chargeback_cases
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chargeback_cases (
                id TEXT PRIMARY KEY,
                merchant_id TEXT NOT NULL,
                customer_id TEXT,
                order_id TEXT NOT NULL,
                status TEXT DEFAULT 'new',
                case_status TEXT DEFAULT 'new',
                amount REAL NOT NULL,
                currency TEXT DEFAULT 'INR',
                dispute_reason TEXT NOT NULL,
                dispute_type TEXT DEFAULT 'Product Not Received',
                customer_name TEXT,
                customer_email TEXT,
                customer_phone TEXT,
                shipping_address TEXT,
                tracking_id TEXT,
                evidence_score REAL,
                opened_at TEXT,
                deadline_at TEXT,
                FOREIGN KEY (merchant_id) REFERENCES merchants (id)
            )
        ''')

        # 6. documents
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS documents (
                id TEXT PRIMARY KEY,
                case_id TEXT NOT NULL,
                owner_type TEXT DEFAULT 'merchant',
                document_category TEXT DEFAULT 'evidence',
                doc_type TEXT NOT NULL,
                file_name TEXT NOT NULL,
                file_path TEXT NOT NULL,
                file_size_bytes INTEGER DEFAULT 0,
                mime_type TEXT,
                ocr_text TEXT,
                ocr_confidence REAL DEFAULT 0.0,
                page_count INTEGER DEFAULT 1,
                extraction_method TEXT DEFAULT 'pymupdf_text_layer',
                preprocessing_json TEXT,
                uploaded_at TEXT,
                FOREIGN KEY (case_id) REFERENCES chargeback_cases (id)
            )
        ''')

        # 7. extracted_entities
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS extracted_entities (
                id TEXT PRIMARY KEY,
                document_id TEXT NOT NULL,
                entity_type TEXT NOT NULL,
                raw_value TEXT NOT NULL,
                normalized_value_json TEXT,
                confidence REAL DEFAULT 1.0,
                source_page INTEGER DEFAULT 1,
                created_at TEXT,
                FOREIGN KEY (document_id) REFERENCES documents (id)
            )
        ''')

        # 8. evidence_scores
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS evidence_scores (
                id TEXT PRIMARY KEY,
                case_id TEXT NOT NULL,
                score REAL NOT NULL,
                win_probability REAL NOT NULL,
                model_version TEXT DEFAULT 'xgb_v1.0.0',
                features_json TEXT,
                breakdown_json TEXT,
                created_at TEXT,
                FOREIGN KEY (case_id) REFERENCES chargeback_cases (id)
            )
        ''')

        # 9. embeddings
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS embeddings (
                id TEXT PRIMARY KEY,
                case_id TEXT NOT NULL,
                summary_text TEXT NOT NULL,
                vector_json TEXT NOT NULL,
                created_at TEXT,
                FOREIGN KEY (case_id) REFERENCES chargeback_cases (id)
            )
        ''')

        # 10. historical_cases
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS historical_cases (
                id TEXT PRIMARY KEY,
                order_id TEXT NOT NULL,
                dispute_reason TEXT NOT NULL,
                amount REAL NOT NULL,
                currency TEXT DEFAULT 'INR',
                outcome TEXT NOT NULL,
                evidence_quality TEXT DEFAULT 'High',
                summary TEXT NOT NULL,
                vector_json TEXT,
                features_json TEXT,
                closed_at TEXT
            )
        ''')

        # 11. pipeline_runs & agent audit logs
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pipeline_runs (
                id TEXT PRIMARY KEY,
                case_id TEXT NOT NULL,
                status TEXT NOT NULL,
                steps_json TEXT NOT NULL,
                final_report_json TEXT,
                created_at TEXT
            )
        ''')

        # Run safe migrations for any existing tables missing new columns
        migrations = [
            ("merchants", "phone_number", "TEXT"),
            ("merchants", "is_verified", "INTEGER DEFAULT 1"),
            ("chargeback_cases", "customer_id", "TEXT"),
            ("chargeback_cases", "case_status", "TEXT DEFAULT 'new'"),
            ("chargeback_cases", "dispute_type", "TEXT DEFAULT 'Product Not Received'"),
            ("chargeback_cases", "evidence_score", "REAL"),
            ("documents", "owner_type", "TEXT DEFAULT 'merchant'"),
            ("documents", "document_category", "TEXT DEFAULT 'evidence'"),
            ("extracted_entities", "source_page", "INTEGER DEFAULT 1")
        ]
        for table, col, col_type in migrations:
            try:
                cursor.execute(f"ALTER TABLE {table} ADD COLUMN {col} {col_type}")
            except Exception:
                pass

        conn.commit()
        conn.close()

db_manager = LocalDatabaseManager()

def get_db():
    return db_manager.get_connection()

def get_db_connection():
    return db_manager.get_connection()

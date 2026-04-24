from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Iterable


SCHEMA_STATEMENTS: tuple[str, ...] = (
    """
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        nickname TEXT NOT NULL DEFAULT '',
        phone TEXT NOT NULL DEFAULT '',
        line_id TEXT NOT NULL DEFAULT '',
        tags TEXT NOT NULL DEFAULT '',
        visit_count INTEGER NOT NULL DEFAULT 0,
        last_visit_date TEXT,
        memo TEXT NOT NULL DEFAULT '',
        created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
    )
    """,
    "CREATE INDEX IF NOT EXISTS idx_customers_name ON customers(name)",
    "CREATE INDEX IF NOT EXISTS idx_customers_nickname ON customers(nickname)",
    "CREATE INDEX IF NOT EXISTS idx_customers_last_visit ON customers(last_visit_date)",
)


class DatabaseManager:
    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

    def connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        return connection

    def initialize(self) -> None:
        with self.connect() as connection:
            self._apply_statements(connection, SCHEMA_STATEMENTS)
            self._seed_if_empty(connection)

    @staticmethod
    def _apply_statements(connection: sqlite3.Connection, statements: Iterable[str]) -> None:
        for statement in statements:
            connection.execute(statement)
        connection.commit()

    @staticmethod
    def _seed_if_empty(connection: sqlite3.Connection) -> None:
        existing = connection.execute("SELECT COUNT(*) AS count FROM customers").fetchone()["count"]
        if existing:
            return
        demo_rows = (
            (
                "高橋 健司",
                "ケンさん",
                "090-1111-2222",
                "kenji_line",
                "常連,ウイスキー,金曜来店",
                12,
                "2026-04-18",
                "山崎が好き。新しいボトルの話題で盛り上がる。イベント告知はLINE反応良好。",
            ),
            (
                "佐々木 美穂",
                "みほちゃん",
                "080-3333-4444",
                "",
                "紹介客,カラオケ好き",
                4,
                "2026-03-27",
                "90年代J-POPが鉄板。年度末は忙しく来店間隔が空きやすい。",
            ),
            (
                "中村 恒一",
                "コウさん",
                "070-5555-6666",
                "ko_naka",
                "休眠注意,焼酎",
                8,
                "2026-02-11",
                "年度初めに再来店フォロー候補。静かな席を好む。",
            ),
        )
        connection.executemany(
            """
            INSERT INTO customers (
                name, nickname, phone, line_id, tags, visit_count, last_visit_date, memo
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            demo_rows,
        )
        connection.commit()


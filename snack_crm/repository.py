from __future__ import annotations

from datetime import date, datetime
from typing import Optional

from .database import DatabaseManager
from .models import Customer, DashboardStats


class CustomerRepository:
    def __init__(self, db: DatabaseManager) -> None:
        self.db = db

    def list_customers(self, keyword: str = "") -> list[Customer]:
        normalized = f"%{keyword.strip()}%"
        query = """
            SELECT *
            FROM customers
            WHERE ? = '%%'
               OR name LIKE ?
               OR nickname LIKE ?
               OR phone LIKE ?
               OR tags LIKE ?
               OR memo LIKE ?
            ORDER BY
                CASE WHEN last_visit_date IS NULL THEN 1 ELSE 0 END,
                last_visit_date DESC,
                name COLLATE NOCASE ASC
        """
        with self.db.connect() as connection:
            rows = connection.execute(
                query,
                (normalized, normalized, normalized, normalized, normalized, normalized),
            ).fetchall()
        return [self._row_to_customer(row) for row in rows]

    def create_customer(self, customer: Customer) -> int:
        with self.db.connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO customers (
                    name, nickname, phone, line_id, tags, visit_count, last_visit_date, memo, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                """,
                (
                    customer.name,
                    customer.nickname,
                    customer.phone,
                    customer.line_id,
                    customer.tags,
                    customer.visit_count,
                    customer.last_visit_date.isoformat() if customer.last_visit_date else None,
                    customer.memo,
                ),
            )
            connection.commit()
            return int(cursor.lastrowid)

    def update_customer(self, customer: Customer) -> None:
        with self.db.connect() as connection:
            connection.execute(
                """
                UPDATE customers
                SET
                    name = ?,
                    nickname = ?,
                    phone = ?,
                    line_id = ?,
                    tags = ?,
                    visit_count = ?,
                    last_visit_date = ?,
                    memo = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
                """,
                (
                    customer.name,
                    customer.nickname,
                    customer.phone,
                    customer.line_id,
                    customer.tags,
                    customer.visit_count,
                    customer.last_visit_date.isoformat() if customer.last_visit_date else None,
                    customer.memo,
                    customer.id,
                ),
            )
            connection.commit()

    def delete_customer(self, customer_id: int) -> None:
        with self.db.connect() as connection:
            connection.execute("DELETE FROM customers WHERE id = ?", (customer_id,))
            connection.commit()

    def get_customer(self, customer_id: int) -> Optional[Customer]:
        with self.db.connect() as connection:
            row = connection.execute("SELECT * FROM customers WHERE id = ?", (customer_id,)).fetchone()
        return self._row_to_customer(row) if row else None

    def increment_visit(self, customer_id: int, visit_date: date) -> None:
        with self.db.connect() as connection:
            current = connection.execute(
                "SELECT visit_count, last_visit_date FROM customers WHERE id = ?",
                (customer_id,),
            ).fetchone()
            if current is None:
                return
            existing_last = current["last_visit_date"]
            new_last = visit_date.isoformat()
            if existing_last and existing_last > new_last:
                new_last = existing_last
            connection.execute(
                """
                UPDATE customers
                SET
                    visit_count = visit_count + 1,
                    last_visit_date = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
                """,
                (new_last, customer_id),
            )
            connection.commit()

    def dashboard_stats(self) -> DashboardStats:
        with self.db.connect() as connection:
            total_customers = connection.execute("SELECT COUNT(*) AS value FROM customers").fetchone()["value"]
            total_visits = connection.execute(
                "SELECT COALESCE(SUM(visit_count), 0) AS value FROM customers"
            ).fetchone()["value"]
            active_this_month = connection.execute(
                """
                SELECT COUNT(*) AS value
                FROM customers
                WHERE last_visit_date IS NOT NULL
                  AND strftime('%Y-%m', last_visit_date) = strftime('%Y-%m', 'now', 'localtime')
                """
            ).fetchone()["value"]
            dormant_customers = connection.execute(
                """
                SELECT COUNT(*) AS value
                FROM customers
                WHERE last_visit_date IS NULL
                   OR julianday('now', 'localtime') - julianday(last_visit_date) >= 30
                """
            ).fetchone()["value"]
        return DashboardStats(
            total_customers=total_customers,
            total_visits=total_visits,
            active_this_month=active_this_month,
            dormant_customers=dormant_customers,
        )

    @staticmethod
    def _row_to_customer(row) -> Customer:
        last_visit = date.fromisoformat(row["last_visit_date"]) if row["last_visit_date"] else None
        created_at = datetime.fromisoformat(row["created_at"]) if row["created_at"] else None
        updated_at = datetime.fromisoformat(row["updated_at"]) if row["updated_at"] else None
        return Customer(
            id=row["id"],
            name=row["name"],
            nickname=row["nickname"],
            phone=row["phone"],
            line_id=row["line_id"],
            tags=row["tags"],
            visit_count=row["visit_count"],
            last_visit_date=last_visit,
            memo=row["memo"],
            created_at=created_at,
            updated_at=updated_at,
        )

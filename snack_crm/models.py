from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional


@dataclass(slots=True)
class Customer:
    id: Optional[int]
    name: str
    nickname: str
    phone: str
    line_id: str
    tags: str
    visit_count: int
    last_visit_date: Optional[date]
    memo: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass(slots=True)
class DashboardStats:
    total_customers: int
    total_visits: int
    active_this_month: int
    dormant_customers: int


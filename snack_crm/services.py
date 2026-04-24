from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Protocol

from .models import Customer
from .repository import CustomerRepository


class LineDeliveryGateway(Protocol):
    def send_segment_message(self, segment_id: str, message: str) -> None:
        """Future extension point for LINE segment delivery."""

    def send_customer_message(self, customer_id: int, message: str) -> None:
        """Future extension point for one-to-one LINE delivery."""


@dataclass(slots=True)
class NoopLineDeliveryGateway:
    def send_segment_message(self, segment_id: str, message: str) -> None:
        return None

    def send_customer_message(self, customer_id: int, message: str) -> None:
        return None


class CustomerService:
    def __init__(
        self,
        repository: CustomerRepository,
        line_gateway: LineDeliveryGateway | None = None,
    ) -> None:
        self.repository = repository
        self.line_gateway = line_gateway or NoopLineDeliveryGateway()

    def search_customers(self, keyword: str = "") -> list[Customer]:
        return self.repository.list_customers(keyword)

    def create_customer(self, payload: Customer) -> int:
        self._validate_customer(payload)
        return self.repository.create_customer(payload)

    def update_customer(self, payload: Customer) -> None:
        if payload.id is None:
            raise ValueError("更新対象の顧客IDがありません。")
        self._validate_customer(payload)
        self.repository.update_customer(payload)

    def delete_customer(self, customer_id: int) -> None:
        self.repository.delete_customer(customer_id)

    def register_visit(self, customer_id: int, visit_date: date) -> None:
        self.repository.increment_visit(customer_id, visit_date)

    def get_customer(self, customer_id: int) -> Customer | None:
        return self.repository.get_customer(customer_id)

    def get_dashboard_stats(self):
        return self.repository.dashboard_stats()

    @staticmethod
    def _validate_customer(customer: Customer) -> None:
        if not customer.name.strip():
            raise ValueError("顧客名は必須です。")
        if customer.visit_count < 0:
            raise ValueError("来店回数は0以上で入力してください。")


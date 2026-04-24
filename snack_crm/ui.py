from __future__ import annotations

import tkinter as tk
from datetime import date
from pathlib import Path
from tkinter import messagebox, ttk

from .database import DatabaseManager
from .models import Customer
from .repository import CustomerRepository
from .services import CustomerService


class SnackCRMApp(tk.Tk):
    BG = "#0F172A"
    PANEL = "#111827"
    PANEL_ALT = "#1F2937"
    CARD = "#F8FAFC"
    ACCENT = "#D4A017"
    ACCENT_SOFT = "#F4E3A3"
    TEXT = "#E5E7EB"
    MUTED = "#94A3B8"
    SUCCESS = "#0F766E"
    WARN = "#B45309"
    DANGER = "#B91C1C"

    def __init__(self, service: CustomerService) -> None:
        super().__init__()
        self.service = service
        self.selected_customer_id: int | None = None
        self.title("Snack CRM Studio")
        self.geometry("1400x860")
        self.minsize(1240, 760)
        self.configure(bg=self.BG)
        self.option_add("*Font", "{Yu Gothic UI} 10")
        self.style = ttk.Style(self)
        self._configure_style()
        self._build_ui()
        self.refresh_all()

    def _configure_style(self) -> None:
        self.style.theme_use("clam")
        self.style.configure("Root.TFrame", background=self.BG)
        self.style.configure("Panel.TFrame", background=self.PANEL)
        self.style.configure("PanelAlt.TFrame", background=self.PANEL_ALT)
        self.style.configure("Card.TFrame", background=self.CARD)
        self.style.configure(
            "Heading.TLabel",
            background=self.BG,
            foreground="white",
            font=("Yu Gothic UI Semibold", 28),
        )
        self.style.configure(
            "Subheading.TLabel",
            background=self.BG,
            foreground=self.ACCENT_SOFT,
            font=("Yu Gothic UI", 11),
        )
        self.style.configure(
            "CardTitle.TLabel",
            background=self.CARD,
            foreground="#334155",
            font=("Yu Gothic UI Semibold", 10),
        )
        self.style.configure(
            "CardValue.TLabel",
            background=self.CARD,
            foreground="#0F172A",
            font=("Yu Gothic UI Semibold", 22),
        )
        self.style.configure(
            "PanelTitle.TLabel",
            background=self.PANEL,
            foreground="white",
            font=("Yu Gothic UI Semibold", 14),
        )
        self.style.configure(
            "PanelText.TLabel",
            background=self.PANEL,
            foreground=self.MUTED,
            font=("Yu Gothic UI", 10),
        )
        self.style.configure(
            "FormLabel.TLabel",
            background=self.PANEL_ALT,
            foreground=self.TEXT,
            font=("Yu Gothic UI", 10),
        )
        self.style.configure(
            "Primary.TButton",
            background=self.ACCENT,
            foreground="#111827",
            borderwidth=0,
            focusthickness=0,
            padding=(16, 10),
            font=("Yu Gothic UI Semibold", 10),
        )
        self.style.map(
            "Primary.TButton",
            background=[("active", "#EAB308")],
            foreground=[("disabled", "#475569")],
        )
        self.style.configure(
            "Secondary.TButton",
            background="#334155",
            foreground="white",
            borderwidth=0,
            focusthickness=0,
            padding=(14, 10),
            font=("Yu Gothic UI", 10),
        )
        self.style.map("Secondary.TButton", background=[("active", "#475569")])
        self.style.configure(
            "Treeview",
            background="white",
            fieldbackground="white",
            foreground="#0F172A",
            rowheight=34,
            borderwidth=0,
            font=("Yu Gothic UI", 10),
        )
        self.style.configure(
            "Treeview.Heading",
            background="#E2E8F0",
            foreground="#0F172A",
            relief="flat",
            font=("Yu Gothic UI Semibold", 10),
        )
        self.style.map(
            "Treeview",
            background=[("selected", "#FDE68A")],
            foreground=[("selected", "#111827")],
        )
        self.style.configure(
            "Modern.TEntry",
            fieldbackground="white",
            foreground="#0F172A",
            bordercolor="#64748B",
            lightcolor="#64748B",
            darkcolor="#64748B",
            padding=8,
        )

    def _build_ui(self) -> None:
        root = ttk.Frame(self, style="Root.TFrame", padding=24)
        root.pack(fill="both", expand=True)

        header = ttk.Frame(root, style="Root.TFrame")
        header.pack(fill="x")
        ttk.Label(header, text="Snack CRM Studio", style="Heading.TLabel").pack(anchor="w")
        ttk.Label(
            header,
            text="顧客情報・来店状況・次回フォローを一画面で管理",
            style="Subheading.TLabel",
        ).pack(anchor="w", pady=(4, 0))

        self.stats_frame = ttk.Frame(root, style="Root.TFrame")
        self.stats_frame.pack(fill="x", pady=(24, 18))

        main = ttk.Frame(root, style="Root.TFrame")
        main.pack(fill="both", expand=True)
        main.columnconfigure(0, weight=4)
        main.columnconfigure(1, weight=3)
        main.rowconfigure(0, weight=1)

        left = ttk.Frame(main, style="Panel.TFrame", padding=18)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 14))
        right = ttk.Frame(main, style="PanelAlt.TFrame", padding=18)
        right.grid(row=0, column=1, sticky="nsew")

        self._build_customer_list(left)
        self._build_editor(right)

    def _build_customer_list(self, parent: ttk.Frame) -> None:
        header = ttk.Frame(parent, style="Panel.TFrame")
        header.pack(fill="x")
        ttk.Label(header, text="顧客一覧", style="PanelTitle.TLabel").pack(side="left")
        ttk.Label(
            header,
            text="名前・ニックネーム・タグ・メモで横断検索",
            style="PanelText.TLabel",
        ).pack(side="left", padx=(14, 0))

        search_row = ttk.Frame(parent, style="Panel.TFrame")
        search_row.pack(fill="x", pady=(18, 14))
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_row, textvariable=self.search_var, style="Modern.TEntry")
        search_entry.pack(side="left", fill="x", expand=True)
        search_entry.bind("<KeyRelease>", lambda _event: self.refresh_customer_list())
        ttk.Button(
            search_row,
            text="検索",
            style="Primary.TButton",
            command=self.refresh_customer_list,
        ).pack(side="left", padx=10)
        ttk.Button(
            search_row,
            text="クリア",
            style="Secondary.TButton",
            command=self._clear_search,
        ).pack(side="left")

        columns = ("name", "nickname", "visits", "last_visit", "tags")
        self.tree = ttk.Treeview(parent, columns=columns, show="headings")
        headings = {
            "name": "顧客名",
            "nickname": "呼び名",
            "visits": "来店回数",
            "last_visit": "最終来店日",
            "tags": "タグ",
        }
        widths = {"name": 170, "nickname": 110, "visits": 90, "last_visit": 110, "tags": 250}
        anchors = {"name": "w", "nickname": "w", "visits": "center", "last_visit": "center", "tags": "w"}
        for key in columns:
            self.tree.heading(key, text=headings[key])
            self.tree.column(key, width=widths[key], anchor=anchors[key])
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self._on_tree_selected)

        toolbar = ttk.Frame(parent, style="Panel.TFrame")
        toolbar.pack(fill="x", pady=(14, 0))
        ttk.Button(toolbar, text="新規登録", style="Primary.TButton", command=self._reset_form).pack(
            side="left"
        )
        ttk.Button(toolbar, text="削除", style="Secondary.TButton", command=self._delete_selected).pack(
            side="left", padx=(10, 0)
        )
        ttk.Button(toolbar, text="来店 +1", style="Secondary.TButton", command=self._increment_visit).pack(
            side="right"
        )

    def _build_editor(self, parent: ttk.Frame) -> None:
        ttk.Label(parent, text="顧客編集", style="PanelTitle.TLabel").pack(anchor="w")
        ttk.Label(
            parent,
            text="登録・編集・メモ更新・来店カウント調整",
            style="FormLabel.TLabel",
        ).pack(anchor="w", pady=(4, 16))

        form = ttk.Frame(parent, style="PanelAlt.TFrame")
        form.pack(fill="both", expand=True)

        self.form_vars = {
            "name": tk.StringVar(),
            "nickname": tk.StringVar(),
            "phone": tk.StringVar(),
            "line_id": tk.StringVar(),
            "tags": tk.StringVar(),
            "visit_count": tk.StringVar(value="0"),
            "last_visit_date": tk.StringVar(),
        }
        fields = (
            ("顧客名", "name"),
            ("呼び名", "nickname"),
            ("電話番号", "phone"),
            ("LINE ID / 将来連携キー", "line_id"),
            ("タグ", "tags"),
            ("来店回数", "visit_count"),
            ("最終来店日 (YYYY-MM-DD)", "last_visit_date"),
        )
        for label, key in fields:
            ttk.Label(form, text=label, style="FormLabel.TLabel").pack(anchor="w", pady=(0, 6))
            ttk.Entry(form, textvariable=self.form_vars[key], style="Modern.TEntry").pack(fill="x", pady=(0, 12))

        ttk.Label(form, text="メモ", style="FormLabel.TLabel").pack(anchor="w", pady=(0, 6))
        self.memo_text = tk.Text(
            form,
            height=10,
            bg="white",
            fg="#0F172A",
            insertbackground="#0F172A",
            relief="flat",
            padx=12,
            pady=12,
            font=("Yu Gothic UI", 10),
        )
        self.memo_text.pack(fill="both", expand=True)

        action_row = ttk.Frame(form, style="PanelAlt.TFrame")
        action_row.pack(fill="x", pady=(16, 0))
        ttk.Button(action_row, text="保存", style="Primary.TButton", command=self._save_customer).pack(
            side="left"
        )
        ttk.Button(action_row, text="フォーム初期化", style="Secondary.TButton", command=self._reset_form).pack(
            side="left", padx=(10, 0)
        )

        info = ttk.Frame(parent, style="PanelAlt.TFrame")
        info.pack(fill="x", pady=(18, 0))
        self.detail_title = tk.Label(
            info,
            text="顧客を選択すると詳細が表示されます",
            bg=self.PANEL_ALT,
            fg="white",
            font=("Yu Gothic UI Semibold", 12),
            anchor="w",
        )
        self.detail_title.pack(fill="x")
        self.detail_body = tk.Label(
            info,
            text="LINE配信管理は `CustomerService` に Gateway を差し替えるだけで拡張できる構成です。",
            bg=self.PANEL_ALT,
            fg=self.MUTED,
            justify="left",
            anchor="w",
            font=("Yu Gothic UI", 10),
            wraplength=420,
        )
        self.detail_body.pack(fill="x", pady=(8, 0))

    def refresh_all(self) -> None:
        self._render_stats()
        self.refresh_customer_list()

    def _render_stats(self) -> None:
        for child in self.stats_frame.winfo_children():
            child.destroy()

        stats = self.service.get_dashboard_stats()
        cards = (
            ("登録顧客", stats.total_customers, "現在の顧客台帳"),
            ("累計来店", stats.total_visits, "会計前でも回数だけ先に記録可能"),
            ("今月アクティブ", stats.active_this_month, "今月来店のある顧客"),
            ("休眠候補", stats.dormant_customers, "30日以上来店なし"),
        )
        for index, (title, value, caption) in enumerate(cards):
            card = ttk.Frame(self.stats_frame, style="Card.TFrame", padding=18)
            card.grid(row=0, column=index, padx=(0, 12 if index < len(cards) - 1 else 0), sticky="nsew")
            self.stats_frame.columnconfigure(index, weight=1)
            ttk.Label(card, text=title, style="CardTitle.TLabel").pack(anchor="w")
            ttk.Label(card, text=str(value), style="CardValue.TLabel").pack(anchor="w", pady=(10, 8))
            tk.Label(
                card,
                text=caption,
                bg=self.CARD,
                fg="#64748B",
                font=("Yu Gothic UI", 9),
                anchor="w",
            ).pack(fill="x")

    def refresh_customer_list(self) -> None:
        for item in self.tree.get_children():
            self.tree.delete(item)
        for customer in self.service.search_customers(self.search_var.get()):
            last_visit = customer.last_visit_date.isoformat() if customer.last_visit_date else "-"
            self.tree.insert(
                "",
                "end",
                iid=str(customer.id),
                values=(customer.name, customer.nickname, customer.visit_count, last_visit, customer.tags),
            )

    def _clear_search(self) -> None:
        self.search_var.set("")
        self.refresh_customer_list()

    def _save_customer(self) -> None:
        try:
            visit_count = int(self.form_vars["visit_count"].get() or "0")
        except ValueError:
            messagebox.showerror("入力エラー", "来店回数は数値で入力してください。")
            return

        last_visit_raw = self.form_vars["last_visit_date"].get().strip()
        try:
            last_visit_date = date.fromisoformat(last_visit_raw) if last_visit_raw else None
        except ValueError:
            messagebox.showerror("入力エラー", "最終来店日は YYYY-MM-DD 形式で入力してください。")
            return

        payload = Customer(
            id=self.selected_customer_id,
            name=self.form_vars["name"].get().strip(),
            nickname=self.form_vars["nickname"].get().strip(),
            phone=self.form_vars["phone"].get().strip(),
            line_id=self.form_vars["line_id"].get().strip(),
            tags=self.form_vars["tags"].get().strip(),
            visit_count=visit_count,
            last_visit_date=last_visit_date,
            memo=self.memo_text.get("1.0", "end").strip(),
        )
        try:
            if self.selected_customer_id is None:
                new_id = self.service.create_customer(payload)
                self.selected_customer_id = new_id
            else:
                self.service.update_customer(payload)
        except ValueError as exc:
            messagebox.showerror("保存できません", str(exc))
            return

        self.refresh_all()
        self._select_customer(self.selected_customer_id)
        messagebox.showinfo("保存完了", "顧客情報を保存しました。")

    def _reset_form(self) -> None:
        self.selected_customer_id = None
        for key, variable in self.form_vars.items():
            variable.set("0" if key == "visit_count" else "")
        self.memo_text.delete("1.0", "end")
        self.detail_title.config(text="新規顧客を登録")
        self.detail_body.config(
            text="顧客情報を入力して保存すると、一覧とダッシュボードに即時反映されます。"
        )
        for item in self.tree.selection():
            self.tree.selection_remove(item)

    def _delete_selected(self) -> None:
        customer_id = self._selected_tree_customer_id()
        if customer_id is None:
            messagebox.showwarning("未選択", "削除する顧客を一覧から選択してください。")
            return
        customer = self.service.get_customer(customer_id)
        if customer is None:
            return
        if not messagebox.askyesno("削除確認", f"{customer.name} を削除しますか？"):
            return
        self.service.delete_customer(customer_id)
        self._reset_form()
        self.refresh_all()

    def _increment_visit(self) -> None:
        customer_id = self._selected_tree_customer_id()
        if customer_id is None:
            messagebox.showwarning("未選択", "来店を登録する顧客を一覧から選択してください。")
            return
        self.service.register_visit(customer_id, date.today())
        self.refresh_all()
        self._select_customer(customer_id)

    def _on_tree_selected(self, _event) -> None:
        customer_id = self._selected_tree_customer_id()
        if customer_id is None:
            return
        self._select_customer(customer_id)

    def _select_customer(self, customer_id: int | None) -> None:
        if customer_id is None:
            return
        customer = self.service.get_customer(customer_id)
        if customer is None:
            return
        self.selected_customer_id = customer.id
        self.form_vars["name"].set(customer.name)
        self.form_vars["nickname"].set(customer.nickname)
        self.form_vars["phone"].set(customer.phone)
        self.form_vars["line_id"].set(customer.line_id)
        self.form_vars["tags"].set(customer.tags)
        self.form_vars["visit_count"].set(str(customer.visit_count))
        self.form_vars["last_visit_date"].set(
            customer.last_visit_date.isoformat() if customer.last_visit_date else ""
        )
        self.memo_text.delete("1.0", "end")
        self.memo_text.insert("1.0", customer.memo)
        dormant_text = self._describe_dormancy(customer.last_visit_date)
        self.detail_title.config(text=f"{customer.name} / {customer.nickname or '呼び名未設定'}")
        self.detail_body.config(
            text=(
                f"来店回数: {customer.visit_count} 回\n"
                f"最終来店: {customer.last_visit_date.isoformat() if customer.last_visit_date else '未登録'}\n"
                f"状態: {dormant_text}\n"
                f"将来のLINE配信連携キー: {customer.line_id or '未設定'}"
            )
        )
        item_id = str(customer.id)
        if item_id in self.tree.get_children():
            self.tree.selection_set(item_id)
            self.tree.focus(item_id)

    @staticmethod
    def _describe_dormancy(last_visit_date: date | None) -> str:
        if last_visit_date is None:
            return "来店履歴未登録"
        days = (date.today() - last_visit_date).days
        if days >= 60:
            return f"長期休眠候補 ({days}日)"
        if days >= 30:
            return f"フォロー優先 ({days}日)"
        return f"アクティブ ({days}日)"

    def _selected_tree_customer_id(self) -> int | None:
        selection = self.tree.selection()
        if not selection:
            return None
        return int(selection[0])


def create_app(database_path: Path | None = None) -> SnackCRMApp:
    db_path = database_path or Path("data") / "snack_crm.db"
    database = DatabaseManager(db_path)
    database.initialize()
    repository = CustomerRepository(database)
    service = CustomerService(repository=repository)
    return SnackCRMApp(service)

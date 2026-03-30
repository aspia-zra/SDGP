import customtkinter as ctk
from tkinter import ttk
<<<<<<< HEAD
from gui import theme
from controllers.finance_controller import FinanceController
from gui import navbar
from models import user_session

=======
from . import theme
from . import nav
from models import user_session
from models.finance_controller import FinanceController
>>>>>>> origin/Azra-management-dashboard

class FinanceView(ctk.CTkFrame):

    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=theme.BACKGROUND)
        self.app_controller = controller
        self.fc = FinanceController()

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

<<<<<<< HEAD
        self.nav = navbar.navbar(self, parent, mode=user_session.user_type.lower())
=======
        self.nav = nav.navbar(self, parent, mode=user_session.user_type.lower())
>>>>>>> origin/Azra-management-dashboard
        self.nav.grid(row=0, rowspan=2, column=0, sticky="ns")

        self._build_header()
        self._build_body()
        self.after(100, self.refresh)

<<<<<<< HEAD
    def _build_header(self):
        hdr = ctk.CTkFrame(self, fg_color=theme.SURFACE, height=70, corner_radius=0)
        hdr.grid(row=0, column=1, sticky="ew")
        hdr.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(hdr, text="Finance Dashboard",
                     font=theme.TITLE_FONT,
                     text_color=theme.PRIMARY).grid(row=0, column=0, sticky="w", padx=30, pady=15)

    def _build_body(self):
        self.scroll = ctk.CTkScrollableFrame(self, fg_color=theme.BACKGROUND,
                                              scrollbar_button_color=theme.PRIMARY)
        self.scroll.grid(row=1, column=1, padx=20, pady=10, sticky="nsew")
        self.scroll.grid_columnconfigure(0, weight=1)
=======
    # ── Header ────────────────────────────────────────────────────
    def _build_header(self):
        hdr = ctk.CTkFrame(self, fg_color=theme.SURFACE,
                           height=70, corner_radius=0)
        hdr.grid(row=0, column=1, sticky="ew")
        hdr.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(hdr, text="Finance Dashboard",
                     font=theme.TITLE_FONT,
                     text_color=theme.PRIMARY).grid(
            row=0, column=0, sticky="w", padx=30, pady=15)

    # ── Body ──────────────────────────────────────────────────────
    def _build_body(self):
        self.scroll = ctk.CTkScrollableFrame(
            self, fg_color=theme.BACKGROUND,
            scrollbar_button_color=theme.PRIMARY)
        self.scroll.grid(row=1, column=1, padx=20,
                         pady=10, sticky="nsew")
        self.scroll.grid_columnconfigure(0, weight=1)

>>>>>>> origin/Azra-management-dashboard
        self._build_summary_cards()
        self._build_middle_row()
        self._build_transactions_table()

<<<<<<< HEAD
    def _build_summary_cards(self):
        row = ctk.CTkFrame(self.scroll, fg_color="transparent")
        row.grid(row=0, column=0, sticky="ew", padx=5, pady=10)
        configs = [
            ("Total Outstanding", "outstanding"),
            ("Pending", "pending"),
            ("Overdue", "overdue"),
            ("Paid", "paid"),
=======
    # ── Summary cards ─────────────────────────────────────────────
    def _build_summary_cards(self):
        row = ctk.CTkFrame(self.scroll, fg_color="transparent")
        row.grid(row=0, column=0, sticky="ew", padx=5, pady=10)

        configs = [
            ("Total Outstanding", "outstanding"),
            ("Pending",           "pending"),
            ("Overdue",           "overdue"),
            ("Paid",              "paid"),
>>>>>>> origin/Azra-management-dashboard
        ]
        self.sum_labels = {}
        for i, (title, key) in enumerate(configs):
            row.grid_columnconfigure(i, weight=1)
<<<<<<< HEAD
            card = ctk.CTkFrame(row, fg_color=theme.SURFACE, corner_radius=14)
            card.grid(row=0, column=i, padx=8, pady=4, sticky="ew")
            ctk.CTkLabel(card, text=title, font=theme.SMALL_FONT,
                         text_color=theme.TEXT_SECONDARY).pack(pady=(12, 2))
            lbl = ctk.CTkLabel(card, text="£0.00",
                               font=("Helvetica", 22, "bold"), text_color=theme.PRIMARY)
            lbl.pack(pady=(0, 12))
            self.sum_labels[key] = lbl

=======
            card = ctk.CTkFrame(row, fg_color=theme.SURFACE,
                                corner_radius=14)
            card.grid(row=0, column=i, padx=8,
                      pady=4, sticky="ew")
            ctk.CTkLabel(card,
                         text=title,
                         font=theme.SMALL_FONT,
                         text_color=theme.TEXT_SECONDARY
                         ).pack(pady=(12, 2))
            lbl = ctk.CTkLabel(card, text="£0.00",
                               font=("Helvetica", 22, "bold"),
                               text_color=theme.PRIMARY)
            lbl.pack(pady=(0, 12))
            self.sum_labels[key] = lbl

    # ── Middle row ────────────────────────────────────────────────
>>>>>>> origin/Azra-management-dashboard
    def _build_middle_row(self):
        mid = ctk.CTkFrame(self.scroll, fg_color="transparent")
        mid.grid(row=1, column=0, sticky="ew", padx=5, pady=10)
        mid.grid_columnconfigure(0, weight=1)
        mid.grid_columnconfigure(1, weight=1)

<<<<<<< HEAD
        rate_card = ctk.CTkFrame(mid, fg_color=theme.SURFACE, corner_radius=14)
        rate_card.grid(row=0, column=0, padx=8, pady=4, sticky="nsew")
        ctk.CTkLabel(rate_card, text="Collection Rate",
                     font=theme.HEADING_FONT, text_color=theme.PRIMARY).pack(pady=(16, 6))
        self.rate_lbl = ctk.CTkLabel(rate_card, text="0%",
                                      font=("Helvetica", 38, "bold"), text_color=theme.PRIMARY)
        self.rate_lbl.pack(pady=10)
        stats = ctk.CTkFrame(rate_card, fg_color="transparent")
        stats.pack(pady=(0, 16))
        ctk.CTkLabel(stats, text="Paid:", font=theme.SMALL_FONT,
                     text_color=theme.TEXT_SECONDARY).grid(row=0, column=0, padx=8)
        self.paid_n_lbl = ctk.CTkLabel(stats, text="0",
                                        font=theme.BODY_FONT, text_color=theme.SUCCESS)
        self.paid_n_lbl.grid(row=0, column=1, padx=8)
        ctk.CTkLabel(stats, text="Outstanding:", font=theme.SMALL_FONT,
                     text_color=theme.TEXT_SECONDARY).grid(row=0, column=2, padx=8)
        self.out_n_lbl = ctk.CTkLabel(stats, text="0",
                                       font=theme.BODY_FONT, text_color=theme.DANGER)
        self.out_n_lbl.grid(row=0, column=3, padx=8)

        dues_card = ctk.CTkFrame(mid, fg_color=theme.SURFACE, corner_radius=14)
        dues_card.grid(row=0, column=1, padx=8, pady=4, sticky="nsew")
        ctk.CTkLabel(dues_card, text="Due in Next 7 Days",
                     font=theme.HEADING_FONT, text_color=theme.PRIMARY).pack(pady=(16, 6))
        self.dues_frame = ctk.CTkScrollableFrame(dues_card, fg_color=theme.BACKGROUND,
                                                  height=130, corner_radius=8)
        self.dues_frame.pack(fill="x", expand=True, padx=12, pady=(0, 16))

    def _build_transactions_table(self):
        frame = ctk.CTkFrame(self.scroll, fg_color=theme.SURFACE, corner_radius=14)
        frame.grid(row=2, column=0, sticky="ew", padx=5, pady=10)
        frame.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(frame, text="Recent Transactions",
                     font=theme.HEADING_FONT, text_color=theme.PRIMARY).pack(pady=(16, 8))

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Finance.Treeview", background=theme.BACKGROUND,
                        foreground=theme.TEXT_PRIMARY, rowheight=28,
                        fieldbackground=theme.BACKGROUND, font=("Helvetica", 11))
        style.configure("Finance.Treeview.Heading", background=theme.PRIMARY,
                        foreground="white", font=("Helvetica", 11, "bold"), relief="flat")
        style.map("Finance.Treeview", background=[("selected", theme.PRIMARY_LIGHT)])

        cols = ("Invoice", "Tenant", "Apartment", "Amount", "Due Date", "Status")
        self.txn_tree = ttk.Treeview(frame, columns=cols, show="headings",
                                      style="Finance.Treeview", height=8)
=======
        # Collection rate card
        rate_card = ctk.CTkFrame(mid, fg_color=theme.SURFACE,
                                 corner_radius=14)
        rate_card.grid(row=0, column=0, padx=8,
                       pady=4, sticky="nsew")

        ctk.CTkLabel(rate_card, text="Collection Rate",
                     font=theme.HEADING_FONT,
                     text_color=theme.PRIMARY
                     ).pack(pady=(16, 6))

        self.rate_lbl = ctk.CTkLabel(
            rate_card, text="0%",
            font=("Helvetica", 38, "bold"),
            text_color=theme.PRIMARY)
        self.rate_lbl.pack(pady=10)

        stats = ctk.CTkFrame(rate_card, fg_color="transparent")
        stats.pack(pady=(0, 16))

        ctk.CTkLabel(stats, text="Paid:",
                     font=theme.SMALL_FONT,
                     text_color=theme.TEXT_SECONDARY
                     ).grid(row=0, column=0, padx=8)
        self.paid_n_lbl = ctk.CTkLabel(
            stats, text="0",
            font=theme.BODY_FONT,
            text_color=theme.SUCCESS)
        self.paid_n_lbl.grid(row=0, column=1, padx=8)

        ctk.CTkLabel(stats, text="Outstanding:",
                     font=theme.SMALL_FONT,
                     text_color=theme.TEXT_SECONDARY
                     ).grid(row=0, column=2, padx=8)
        self.out_n_lbl = ctk.CTkLabel(
            stats, text="0",
            font=theme.BODY_FONT,
            text_color=theme.DANGER)
        self.out_n_lbl.grid(row=0, column=3, padx=8)

        # Upcoming dues card
        dues_card = ctk.CTkFrame(mid, fg_color=theme.SURFACE,
                                  corner_radius=14)
        dues_card.grid(row=0, column=1, padx=8,
                       pady=4, sticky="nsew")

        ctk.CTkLabel(dues_card, text="Due in Next 7 Days",
                     font=theme.HEADING_FONT,
                     text_color=theme.PRIMARY
                     ).pack(pady=(16, 6))

        self.dues_frame = ctk.CTkScrollableFrame(
            dues_card, fg_color=theme.BACKGROUND,
            height=130, corner_radius=8)
        self.dues_frame.pack(fill="x", expand=True,
                              padx=12, pady=(0, 16))

    # ── Transactions table ────────────────────────────────────────
    def _build_transactions_table(self):
        frame = ctk.CTkFrame(self.scroll, fg_color=theme.SURFACE,
                             corner_radius=14)
        frame.grid(row=2, column=0, sticky="ew",
                   padx=5, pady=10)
        frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(frame, text="Recent Transactions",
                     font=theme.HEADING_FONT,
                     text_color=theme.PRIMARY
                     ).pack(pady=(16, 8))

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Finance.Treeview",
                        background=theme.BACKGROUND,
                        foreground=theme.TEXT_PRIMARY,
                        rowheight=28,
                        fieldbackground=theme.BACKGROUND,
                        font=("Helvetica", 11))
        style.configure("Finance.Treeview.Heading",
                        background=theme.PRIMARY,
                        foreground="white",
                        font=("Helvetica", 11, "bold"),
                        relief="flat")
        style.map("Finance.Treeview",
                  background=[("selected", theme.PRIMARY_LIGHT)])

        cols = ("Invoice", "Tenant", "Apartment",
                "Amount", "Due Date", "Status")
        self.txn_tree = ttk.Treeview(
            frame, columns=cols, show="headings",
            style="Finance.Treeview", height=8)

>>>>>>> origin/Azra-management-dashboard
        widths = (80, 160, 110, 110, 110, 100)
        for col, w in zip(cols, widths):
            self.txn_tree.heading(col, text=col)
            self.txn_tree.column(col, width=w, anchor="center")

<<<<<<< HEAD
        self.txn_tree.tag_configure("paid", foreground=theme.SUCCESS)
        self.txn_tree.tag_configure("pending", foreground=theme.WARNING)
        self.txn_tree.tag_configure("overdue", foreground=theme.DANGER)

        sb = ttk.Scrollbar(frame, orient="vertical", command=self.txn_tree.yview)
        self.txn_tree.configure(yscrollcommand=sb.set)
        self.txn_tree.pack(side="left", fill="both", expand=True, padx=(12, 0), pady=(0, 16))
        sb.pack(side="right", fill="y", pady=(0, 16), padx=(0, 8))

    def refresh(self):
        try:
            s = self.fc.get_summary()
            self.sum_labels["outstanding"].configure(text=s["outstanding"])
            self.sum_labels["pending"].configure(text=s["pending"])
            self.sum_labels["overdue"].configure(text=s["overdue"])
            self.sum_labels["paid"].configure(text=s["paid"])
            self.rate_lbl.configure(text=s["rate"])
            self.paid_n_lbl.configure(text=str(s["paid_n"]))
            self.out_n_lbl.configure(text=str(s["pending_n"] + s["overdue_n"]))
=======
        self.txn_tree.tag_configure("paid",
                                     foreground=theme.SUCCESS)
        self.txn_tree.tag_configure("pending",
                                     foreground=theme.WARNING)
        self.txn_tree.tag_configure("overdue",
                                     foreground=theme.DANGER)

        sb = ttk.Scrollbar(frame, orient="vertical",
                           command=self.txn_tree.yview)
        self.txn_tree.configure(yscrollcommand=sb.set)
        self.txn_tree.pack(side="left", fill="both",
                           expand=True,
                           padx=(12, 0), pady=(0, 16))
        sb.pack(side="right", fill="y",
                pady=(0, 16), padx=(0, 8))

    # ── Refresh ───────────────────────────────────────────────────
    def refresh(self):
        try:
            s = self.fc.get_summary()
            self.sum_labels["outstanding"].configure(
                text=s["outstanding"])
            self.sum_labels["pending"].configure(
                text=s["pending"])
            self.sum_labels["overdue"].configure(
                text=s["overdue"])
            self.sum_labels["paid"].configure(
                text=s["paid"])
            self.rate_lbl.configure(text=s["rate"])
            self.paid_n_lbl.configure(
                text=str(s["paid_n"]))
            self.out_n_lbl.configure(
                text=str(s["pending_n"] + s["overdue_n"]))
>>>>>>> origin/Azra-management-dashboard
            self._refresh_dues()
            self._refresh_transactions()
        except Exception as e:
            print(f"Finance refresh error: {e}")

    def _refresh_dues(self):
        for w in self.dues_frame.winfo_children():
            w.destroy()
        dues = self.fc.get_upcoming_dues()
        if not dues:
<<<<<<< HEAD
            ctk.CTkLabel(self.dues_frame, text="No upcoming dues",
                         font=theme.BODY_FONT, text_color=theme.TEXT_SECONDARY).pack(pady=12)
            return
        for d in dues:
            row = ctk.CTkFrame(self.dues_frame, fg_color="transparent")
            row.pack(fill="x", padx=4, pady=2)
            ctk.CTkLabel(row, text=f"{d['tenant']} — {d['apt']}",
                         font=theme.BODY_FONT, text_color=theme.TEXT_PRIMARY,
                         anchor="w").pack(side="left", fill="x", expand=True)
            ctk.CTkLabel(row, text=f"{d['amount']}  {d['due']}",
                         font=theme.SMALL_FONT, text_color=theme.PRIMARY).pack(side="right")
=======
            ctk.CTkLabel(self.dues_frame,
                         text="No upcoming dues",
                         font=theme.BODY_FONT,
                         text_color=theme.TEXT_SECONDARY
                         ).pack(pady=12)
            return
        for d in dues:
            row = ctk.CTkFrame(self.dues_frame,
                               fg_color="transparent")
            row.pack(fill="x", padx=4, pady=2)
            ctk.CTkLabel(row,
                         text=f"{d['tenant']} — {d['apt']}",
                         font=theme.BODY_FONT,
                         text_color=theme.TEXT_PRIMARY,
                         anchor="w").pack(
                side="left", fill="x", expand=True)
            ctk.CTkLabel(row,
                         text=f"{d['amount']}  {d['due']}",
                         font=theme.SMALL_FONT,
                         text_color=theme.PRIMARY
                         ).pack(side="right")
>>>>>>> origin/Azra-management-dashboard

    def _refresh_transactions(self):
        for item in self.txn_tree.get_children():
            self.txn_tree.delete(item)
        for t in self.fc.get_recent_transactions():
            tag = t["status"].lower()
<<<<<<< HEAD
            self.txn_tree.insert("", "end",
                                  values=(t["invoice"], t["tenant"], t["apt"],
                                          t["amount"], t["due"], t["status"]),
                                  tags=(tag,))
=======
            self.txn_tree.insert(
                "", "end",
                values=(t["invoice"], t["tenant"],
                        t["apt"], t["amount"],
                        t["due"], t["status"]),
                tags=(tag,))
>>>>>>> origin/Azra-management-dashboard

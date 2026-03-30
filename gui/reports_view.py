import customtkinter as ctk
from tkinter import ttk
from gui import theme
from controllers.report_controller import ReportController

class ReportsView(ctk.CTkFrame):

    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=theme.BACKGROUND)
        self.app_controller = controller
        self.rc = ReportController()
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self._build_header()
        self._build_tabs()

    def _build_header(self):
        hdr = ctk.CTkFrame(self, fg_color=theme.SURFACE,
                           height=70, corner_radius=0)
        hdr.grid(row=0, column=0, sticky="ew")
        ctk.CTkLabel(hdr, text="Reports",
                     font=theme.TITLE_FONT,
                     text_color=theme.PRIMARY).pack(
                     side="left", padx=30, pady=15)

    def _build_tabs(self):
        self.tabs = ctk.CTkTabview(
            self,
            fg_color=theme.BACKGROUND,
            segmented_button_fg_color=theme.SURFACE,
            segmented_button_selected_color=theme.PRIMARY,
            segmented_button_selected_hover_color=theme.PRIMARY_DARK,
            segmented_button_unselected_color=theme.SURFACE,
            text_color=theme.TEXT_PRIMARY
        )
        self.tabs.grid(row=1, column=0, padx=20,
                       pady=10, sticky="nsew")
        self.tabs.add("Occupancy")
        self.tabs.add("Financial")
        self.tabs.add("Maintenance")
        self._build_occupancy_tab(self.tabs.tab("Occupancy"))
        self._build_financial_tab(self.tabs.tab("Financial"))
        self._build_maintenance_tab(self.tabs.tab("Maintenance"))

    # ── Occupancy ─────────────────────────────────────────────────
    def _build_occupancy_tab(self, tab):
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(1, weight=1)

        # Filter row
        frow = ctk.CTkFrame(tab, fg_color=theme.SURFACE,
                            corner_radius=10)
        frow.grid(row=0, column=0, sticky="ew", padx=5, pady=8)
        ctk.CTkLabel(frow, text="Filter by City:",
                     font=theme.BODY_FONT,
                     text_color=theme.TEXT_PRIMARY).pack(
                     side="left", padx=12, pady=10)
        self.city_var = ctk.StringVar(value="All")
        ctk.CTkComboBox(
            frow,
            values=["All", "Bristol", "Cardiff",
                    "London", "Manchester"],
            variable=self.city_var,
            command=lambda _: self._load_occupancy(),
            fg_color=theme.BACKGROUND,
            border_color=theme.PRIMARY_LIGHT,
            button_color=theme.PRIMARY,
            button_hover_color=theme.PRIMARY_DARK,
            width=180
        ).pack(side="left", padx=8)

        # Table — note "Tenants" column instead of names
        self.occ_tree = self._make_tree(
            tab, row=1,
            cols=("Apartment", "Type", "Rent",
                  "Status", "City", "Tenants"),
            widths=(110, 110, 100, 100, 110, 80)
        )
        self._load_occupancy()

    def _load_occupancy(self):
        city = None if self.city_var.get() == "All" \
               else self.city_var.get()
        rows = self.rc.get_occupancy_data(city)
        self._fill_tree(
            self.occ_tree,
            [(r["apartment"], r["type"], r["rent"],
              r["status"], r["city"], r["tenants"])
             for r in rows]
        )

    # ── Financial ─────────────────────────────────────────────────
    def _build_financial_tab(self, tab):
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(1, weight=1)

        self.fin_cards = self._make_summary_row(
            tab, row=0,
            labels=["Outstanding", "Pending",
                    "Overdue", "Paid"]
        )
        self.fin_tree = self._make_tree(
            tab, row=1,
            cols=("Invoice", "Amount", "Due Date",
                  "Status", "Tenant"),
            widths=(80, 110, 110, 100, 160)
        )
        self._load_financial()

    def _load_financial(self):
        data, summary = self.rc.get_financial_data()
        self.fin_cards["Outstanding"].configure(
            text=summary["outstanding"])
        self.fin_cards["Pending"].configure(
            text=summary["pending"])
        self.fin_cards["Overdue"].configure(
            text=summary["overdue"])
        self.fin_cards["Paid"].configure(
            text=summary["paid"])
        self._fill_tree(
            self.fin_tree,
            [(r["invoice"], r["amount"], r["due"],
              r["status"], r["tenant"]) for r in data]
        )

    # ── Maintenance ───────────────────────────────────────────────
    def _build_maintenance_tab(self, tab):
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(1, weight=1)

        self.maint_cards = self._make_summary_row(
            tab, row=0,
            labels=["Total Cost", "Total Hours"]
        )
        self.maint_tree = self._make_tree(
            tab, row=1,
            cols=("Log ID", "Apartment", "Date",
                  "Hours", "Cost", "Notes"),
            widths=(70, 120, 140, 70, 100, 200)
        )
        self._load_maintenance()

    def _load_maintenance(self):
        data, summary = self.rc.get_maintenance_data()
        self.maint_cards["Total Cost"].configure(
            text=summary["total_cost"])
        self.maint_cards["Total Hours"].configure(
            text=summary["total_hours"])
        self._fill_tree(
            self.maint_tree,
            [(r["id"], r["apt"], r["date"],
              r["hours"], r["cost"], r["notes"])
             for r in data]
        )

    # ── Shared helpers ────────────────────────────────────────────
    def _make_tree(self, parent, row, cols, widths):
        frame = ctk.CTkFrame(parent, fg_color=theme.SURFACE,
                             corner_radius=10)
        frame.grid(row=row, column=0, sticky="nsew",
                   padx=5, pady=8)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Custom.Treeview",
                        background=theme.BACKGROUND,
                        foreground=theme.TEXT_PRIMARY,
                        rowheight=28,
                        fieldbackground=theme.BACKGROUND,
                        font=("Helvetica", 11))
        style.configure("Custom.Treeview.Heading",
                        background=theme.PRIMARY,
                        foreground="white",
                        font=("Helvetica", 11, "bold"),
                        relief="flat")
        style.map("Custom.Treeview",
                  background=[("selected", theme.PRIMARY_LIGHT)])

        tree = ttk.Treeview(frame, columns=cols,
                            show="headings",
                            style="Custom.Treeview",
                            height=14)
        for col, w in zip(cols, widths):
            tree.heading(col, text=col)
            tree.column(col, width=w, anchor="center")

        sb = ttk.Scrollbar(frame, orient="vertical",
                           command=tree.yview)
        tree.configure(yscrollcommand=sb.set)
        tree.grid(row=0, column=0, sticky="nsew",
                  padx=(8, 0), pady=8)
        sb.grid(row=0, column=1, sticky="ns",
                pady=8, padx=(0, 4))
        return tree

    def _make_summary_row(self, parent, row, labels):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.grid(row=row, column=0, sticky="ew",
                   padx=5, pady=8)
        for i in range(len(labels)):
            frame.grid_columnconfigure(i, weight=1)
        cards = {}
        for i, label in enumerate(labels):
            card = ctk.CTkFrame(frame, fg_color=theme.SURFACE,
                                corner_radius=12)
            card.grid(row=0, column=i, padx=8,
                      pady=4, sticky="ew")
            ctk.CTkLabel(card, text=label,
                         font=theme.SMALL_FONT,
                         text_color=theme.TEXT_SECONDARY
                         ).pack(pady=(12, 2))
            val = ctk.CTkLabel(card, text="£0.00",
                               font=theme.HEADING_FONT,
                               text_color=theme.PRIMARY)
            val.pack(pady=(0, 12))
            cards[label] = val
        return cards

    @staticmethod
    def _fill_tree(tree, rows):
        for item in tree.get_children():
            tree.delete(item)
        for row in rows:
            tree.insert("", "end", values=row)
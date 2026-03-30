import customtkinter as ctk
from models.user import UserTbl


class LoginPage(ctk.CTkFrame):

    def __init__(self, parent, login_success_callback):
        super().__init__(parent)

        self.login_success_callback = login_success_callback
        self.password_visible = False

        self.user_model = UserTbl()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.card = ctk.CTkFrame(self, width=420, height=420, corner_radius=20)
        self.card.grid(row=0, column=0)
        self.card.grid_propagate(False)

        ctk.CTkLabel(
            self.card,
            text="Paragon",
            font=("Georgia", 26, "bold"),
            text_color="#4f9cf9"
        ).pack(pady=(40, 0))

        ctk.CTkLabel(
            self.card,
            text="Apartment System",
            font=("Arial", 12),
            text_color="gray"
        ).pack(pady=(2, 25))

        self.email_entry = ctk.CTkEntry(
            self.card,
            width=320,
            height=42,
            placeholder_text="Email Address",
            corner_radius=10
        )
        self.email_entry.pack(pady=6)

        pw_frame = ctk.CTkFrame(self.card, fg_color="transparent")
        pw_frame.pack(pady=6)

        self.password_entry = ctk.CTkEntry(
            pw_frame,
            width=262,
            height=42,
            placeholder_text="Password",
            show="*",
            corner_radius=10
        )
        self.password_entry.pack(side="left")

        self.toggle_btn = ctk.CTkButton(
            pw_frame,
            text="Show",
            width=52,
            height=42,
            corner_radius=10,
            fg_color="#2b2b3b",
            hover_color="#3a3a4f",
            text_color="#8aa5c7",
            font=("Arial", 11),
            command=self.toggle_password
        )
        self.toggle_btn.pack(side="left", padx=(6, 0))

        self.error_label = ctk.CTkLabel(
            self.card,
            text="",
            font=("Arial", 11),
            text_color="#f87171"
        )
        self.error_label.pack()

        ctk.CTkButton(
            self.card,
            text="Sign In",
            width=320,
            height=44,
            corner_radius=10,
            font=("Arial", 14, "bold"),
            command=self.handle_login
        ).pack(pady=(6, 0))

        self.email_entry.bind("<Return>", lambda e: self.password_entry.focus())
        self.password_entry.bind("<Return>", lambda e: self.handle_login())

    def toggle_password(self):
        if self.password_visible == False:
            self.password_entry.configure(show="")
            self.toggle_btn.configure(text="Hide")
            self.password_visible = True
        else:
            self.password_entry.configure(show="*")
            self.toggle_btn.configure(text="Show")
            self.password_visible = False

    def handle_login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        if email == "" or password == "":
            self.error_label.configure(text="Please enter email and password")
            return

        user = self.user_model.login(email, password)

        if user != None:
            self.login_success_callback(user)
        else:
            self.error_label.configure(text="Invalid email or password")
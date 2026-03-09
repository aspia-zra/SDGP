import tkinter as tk


def create_sidebar(parent):

    sidebar = tk.Frame(parent, bg="#0d1f63", width=220)
    sidebar.pack(side="left", fill="y")

    title = tk.Label(
        sidebar,
        text="Paragon\nApartments",
        bg="#0d1f63",
        fg="white",
        font=("Arial", 16, "bold")
    )

    title.pack(pady=30)

    buttons = [
        "Profile",
        "Notifications",
        "Settings",
        "Payments",
        "Complaints",
        "Repairs"
    ]

    for name in buttons:

        btn = tk.Button(
            sidebar,
            text=name,
            bg="#0d1f63",
            fg="white",
            relief="flat",
            font=("Arial", 11),
            width=18
        )

        btn.pack(pady=6)

    logout = tk.Button(
        sidebar,
        text="Logout",
        bg="white",
        fg="black",
        width=15
    )

    logout.pack(side="bottom", pady=25)
from tkinter import *
import customtkinter as ctk
from gui.Admindash import *
from gui.loginpage import *
from gui.pages_mngdash import mngdashboard
from gui import page_mdash
import models.user_session as user_session
from gui.nav import *


class App(ctk.CTk):
	def __init__(self):
		super().__init__()
		ctk.set_appearance_mode("light")
		ctk.set_default_color_theme("blue")
		self.configure(fg_color="#f5f6fa")

		self.title("Paragon Apartment System")
		self.geometry("1000x700")

		self.grid_columnconfigure(0, weight=1)
		self.grid_rowconfigure(0, weight=1)

		self.current_page = None
		self._install_bgerror_filter()
		self.protocol("WM_DELETE_WINDOW", self._on_close)

		self.show_login()

	def _install_bgerror_filter(self):
		# Suppress harmless Tcl background callback errors during shutdown.
		self.tk.eval(
			"""
proc bgerror {msg} {
    if {[string match "*invalid command name*" $msg] ||
        [string match "*application has been destroyed*" $msg]} {
        return
    }
    puts stderr $msg
}
"""
		)

	def _on_close(self):
		try:
			if self.current_page is not None and self.current_page.winfo_exists():
				self.current_page.destroy()
		except Exception:
			pass
		self.destroy()

	def clear_page(self):
		if self.current_page is not None:
			self.current_page.destroy()

	def show_login(self):
		self.clear_page()
		self.current_page = LoginPage(self, self.show_dashboard)
		self.current_page.grid(row=0, column=0, sticky="nsew")

	# add dashboard page based on role
	def show_dashboard(self, user=None):
		# Some navigation callbacks invoke this method without a user object.
		# Use current session role first, and fall back to role from provided user.
		role = user_session.user_type
		if role == "" and isinstance(user, dict):
			role = user.get("Role", "")

		self.navbar_mode = role

		if role == "admin":
			self.clear_page()
			self.current_page = admindashboard(self)
			self.current_page.grid(row=0, column=0, sticky="nsew")
		elif role == "manager":
			self.clear_page()
			self.current_page = mngdashboard(self)
			self.current_page.grid(row=0, column=0, sticky="nsew")
		elif role == "maintenance":
			self.clear_page()
			self.current_page = page_mdash.DashboardPage(self)
			self.current_page.grid(row=0, column=0, sticky="nsew")
		else:
			self.clear_page()
			label = ctk.CTkLabel(self, text="Hello")
			label.grid(row=0, column=0)


if __name__ == '__main__':
	app = App()
	app.mainloop()
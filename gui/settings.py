from tkinter import *
import customtkinter as ctk
from . import NavBar
from models import user_session
from models.settingBE import changeEmail, changePhone, changePassword, changeFontsize

class settings(ctk.CTkFrame):
    def __init__(self, main):
        super().__init__(main)

        self.main = main
        self.grid(row=0, column=0, sticky="nsew")

        self.nav = NavBar.navbar(self, self.main)
        self.nav.grid(row=0, column=0, sticky="ns")

        self.grid_columnconfigure(1, weight = 1)
        self.grid_rowconfigure(0, weight = 1)

        self.createSettings()

    def createSettings(self):

        self.container = Frame(self, bg="#f5f5f5")
        self.container.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_columnconfigure(1, weight=1)

        self.container.grid_rowconfigure(1, weight=1)
        self.container.grid_rowconfigure(2, weight=1)

        titleFrame = Frame(self.container)
        titleFrame.grid(row = 0, column=0, columnspan = 2, pady = 20,)

        titlelabel = Label(titleFrame, text="Settings", font=("Arial", 50, "bold"), bg = NavBar.BG_COLOR)
        titlelabel.grid(row= 0, column = 0,pady=20)

        #### LEFT SIDE
        # UPDTAE PHONE NUMBER
        phoneFrame = Frame(self.container)
        phoneFrame.grid(row = 1, column = 0, pady = 20)

        phoneNumber = Label(phoneFrame, text="Current Number: " + user_session.current_phone)
        phoneNumber.grid(row = 0, column = 0, pady=10)
        
        changePhoneNumber = Label(phoneFrame, text="Change Phone Number:")
        changePhoneNumber.grid(row = 1, column = 0, pady=10)
        
        phoneNumberEntry = Entry(phoneFrame)
        phoneNumberEntry.grid(row = 2, column = 0, pady=10)

        def submit_phone():
            msg = changePhone(phoneNumberEntry.get())
            result_label.config(text=msg, fg="green" if "update" in msg else "red")

            if "updated" in msg:
                phoneNumber.config(text="Current Number: " + user_session.current_phone)
            elif "Must" in msg or "already" in msg:
                phoneNumber.config(text="Current Number: " + user_session.current_phone)
            
            result_label.after(3000, lambda: result_label.config(text=""))
        
        submitphone = Button(phoneFrame, text="Update Phone", command=submit_phone)
        submitphone.grid(row = 3, column = 0,pady=10)


        # UPDDATE EMAIL
        emailFrame = Frame(self.container)
        emailFrame.grid(row= 2, column=0, padx=20, pady=20)

        email = Label(emailFrame, text="Current Email: " + user_session.current_email)
        email.grid(row=0, column=0,pady=10)

        emailLabel = Label(emailFrame, text="Change Email:")
        emailLabel.grid(row= 1, column=0, pady=10)

        changeEmailEntry = Entry(emailFrame)
        changeEmailEntry.grid(row=2, column=0,pady=10)

        def submit_email():
            msg = changeEmail(changeEmailEntry.get())
            result_label.config(text=msg, fg="green" if "update" in msg else "red")

            if "updated" in msg:
                email.config(text="Current Email: " + user_session.current_email)
            elif "Must" in msg or "already" in msg:
                email.config(text="Current Email: " + user_session.current_email)
            
            result_label.after(3000, lambda: result_label.config(text=""))

        submitemail = Button(emailFrame, text="Update Email", command = submit_email)
        submitemail.grid(row=3, column=0, pady=10)

        #### RIGHT SIDE
        # Password updaye
        passwordFrame = Frame(self.container)
        passwordFrame.grid(row= 1, column=1, padx=20, pady=20)

        currentPasswordlbl = Label(passwordFrame, text="Enter Current Password:")
        currentPasswordlbl.grid(row= 0, column=1, pady=10)

        currentpasswordEntry = Entry(passwordFrame, show="*")
        currentpasswordEntry.grid(row= 1, column=1,pady=10)
        
        changePasswordlbl = Label(passwordFrame, text="Enter New Password:")
        changePasswordlbl.grid(row= 2, column=1, pady=10)
        
        passwordEntry = Entry(passwordFrame, show="*")
        passwordEntry.grid(row= 3, column=1, pady=10)

        # Maybe add a confirm password?

        def submit_password():
            msg = changePassword(passwordEntry.get(), currentpasswordEntry.get())
            result_label.config(text=msg, fg="green" if "update" in msg else "red")

            if "updated" in msg:
                passwordEntry.delete(0, END)
                currentpasswordEntry.delete(0, END)
            
            result_label.after(3000, lambda: result_label.config(text=""))
        
        submitpassword = Button(passwordFrame, text="Update Password", command=submit_password)
        submitpassword.grid(row= 2, column=1,pady=10)


        # Change FontSize
        fontsizeframe = Frame(self.container)
        fontsizeframe.grid(row= 2, column=1, padx=20, pady=20)

        fontsize = Label(fontsizeframe, text="Current Font Size: " + str(user_session.personal_fontsize))
        fontsize.grid(row=0, column=1, pady=10)

        fontsizelbl = Label(fontsizeframe, text="Change Font Size:")
        fontsizelbl.grid(row=1, column=1, pady=10)

        changefontsizeEntry = Entry(fontsizeframe)
        changefontsizeEntry.grid(row=2, column=1, pady=10)

        def submit_fontsize():
            msg = changeFontsize(changefontsizeEntry.get())
            result_label.config(text=msg, fg="green" if "update" in msg else "red")

            if "updated" in msg:
                fontsize.config(text="Current Font Size: " + str(user_session.personal_fontsize))
                
                titlelabel.config(font=("Arial", user_session.personal_fontsize, "bold"))
                phoneNumber.config(font=("Arial", user_session.personal_fontsize))
                changePhoneNumber.config(font=("Arial", user_session.personal_fontsize))
                email.config(font=("Arial", user_session.personal_fontsize))
                emailLabel.config(font=("Arial", user_session.personal_fontsize))
                currentPasswordlbl.config(font=("Arial", user_session.personal_fontsize))
                changePasswordlbl.config(font=("Arial", user_session.personal_fontsize))
                fontsizelbl.config(font=("Arial", user_session.personal_fontsize))
                submitphone.config(font=("Arial", user_session.personal_fontsize))
                submitemail.config(font=("Arial", user_session.personal_fontsize))
                submitpassword.config(font=("Arial", user_session.personal_fontsize))
                submitfontsize.config(font=("Arial", user_session.personal_fontsize))
            
                changefontsizeEntry.delete(0, END)

            result_label.after(3000, lambda: result_label.config(text=""))

        submitfontsize = Button(fontsizeframe, text="Update Font Size", command = submit_fontsize)
        submitfontsize.grid(row=3, column=1,pady=10)

        result_label = Label(titleFrame, text="")
        result_label.grid(row=1, column=0, columnspan=2, pady=10)
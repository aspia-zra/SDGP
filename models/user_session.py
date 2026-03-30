from db.dbconnect import *
logged_in = False
current_user_id = None
current_user_name = ""
current_email = ""
current_phone = ""
user_type = ""
user_base = None
personal_fontsize = 12

def user_sessions(user):
    global current_user_id, current_user_name, current_email, \
        current_phone, user_type, user_base, personal_fontsize
    if user:
        current_user_id = user["userID"]
        current_user_name = user["fullName"]
        current_email = user["Email"]
        current_phone = user["Phone"]
        user_type = user["Role"]
        user_base = user["locationID"]
        logged_in = True

        # opened_page = ""  -maybe be add in later
    personal_fontsize = 12

user_type = ""
user_base = None  
user_id = None
user_name = ""
logged_in = False
current_user_id = None

def user_sessions(user):
    global user_type, user_base, user_id, user_name, logged_in, current_user_id
    user_type = user.get("Role", "")
    user_base = user.get("locationID", None)
    user_id = user.get("userID", None)
    user_name = user.get("fullName", "")
    logged_in = True
    current_user_id = user.get("userID", None)

def clear():
    global user_type, user_base, user_id, user_name, logged_in, current_user_id
    user_type = ""
    user_base = None
    user_id = None
    user_name = ""
    logged_in = False
    current_user_id = None
# Save current logged in user details
# When some logs in, this page details are updated to the new logged in user
# All done in logging/out page
from db import db
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


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
# Save current logged in user details
# When someone logs in, this page details are updated to the new logged in user
# All done in login/logout pages

logged_in = False
current_user_id = None
current_user_name = ""
current_email = ""
current_phone = ""
user_type = ""
user_base = None
personal_fontsize = 12

def user_sessions(user):
    """Update session details for the logged-in user."""
    global current_user_id, current_user_name, current_email, \
           current_phone, user_type, user_base, personal_fontsize, logged_in

    if user:
        current_user_id = user["userID"]
        current_user_name = user["fullName"]
        current_email = user["Email"]
        current_phone = user["Phone"]
        user_type = user["Role"]
        user_base = user.get("locationID")  # safe get if key might not exist
        logged_in = True
        personal_fontsize = 12
    else:
        # Clear session if user is None
        current_user_id = None
        current_user_name = ""
        current_email = ""
        current_phone = ""
        user_type = ""
        user_base = None
        logged_in = False
        personal_fontsize = 12
#Separate python file for logging in and out
from passlib.hash import sha256_crypt
from . import dbfunc
from . import user_session

def changeEmail(new_email):
    conn = dbfunc.getconnection()
    if conn is not None:  # Checking if connection is None
        if conn.is_connected():  # Checking if connection is established
            cursor = conn.cursor()
            cursor.execute("""SELECT * FROM UserTbl 
                WHERE Email = %s AND userID = %s
                """, (new_email, user_session.current_user_id))
            existingemail = cursor.fetchone()
            
            if not new_email:
                return "Must enter an email!"
            
            if user_session.current_email == new_email:
                return "Must enter a new email."

            if existingemail:
                return "Email already registered."

            if new_email:
                cursor = conn.cursor()
                cursor.execute("UPDATE UserTbl SET Email=%s WHERE userID=%s" 
                    ,(new_email, user_session.current_user_id))
                conn.commit()
                user_session.current_email = new_email
                return "Your email has been updated."

            cursor.close()
            conn.close()
        else:
            print('DB connection error')
    else:
        print('DBFunc error')

def changePhone(new_phone):
    conn = dbfunc.getconnection()
    if conn is not None:  # Checking if connection is None
        if conn.is_connected():  # Checking if connection is established
            cursor = conn.cursor()
            cursor.execute("""SELECT * FROM UserTbl 
                           WHERE Phone = %s AND userID != %s""", (new_phone, user_session.current_user_id))
            existingNumber = cursor.fetchone()
            
            if not new_phone:
                return "Must enter a phone number!"
            
            if user_session.current_phone == new_phone:
                return "Must enter a new phone number." 

            if existingNumber: #If someone else is using the same number
                return "Number already registered."

            if new_phone:
                cursor = conn.cursor()
                cursor.execute("UPDATE UserTbl SET Phone=%s WHERE userID=%s" 
                    ,(new_phone, user_session.current_user_id))
                conn.commit()
                user_session.current_phone = new_phone
                return "Your phone number has been updated."

            cursor.close()
            conn.close()
        else:
            print('DB connection error')
    else:
        print('DBFunc error')

def changePassword(new_password, current_password):
    conn = dbfunc.getconnection()
    cursor = conn.cursor()
    cursor.execute("SELECT Password FROM UserTbl WHERE userID = %s",(user_session.current_user_id,))
    rows = cursor.fetchone()
    if rows:
        rpassword = rows[0]
        if current_password != rpassword: # Checks current password in DB before allowing change
            return "Current password incorrect, try again"
        
        if len(new_password) < 8:
            return "New password must be atleast 8 characters long"
        
        if any(char.isdigit() for char in new_password) == False:
            return "New password must include a number"
    
        #hashednew_password = sha256_crypt.hash((str(new_password))) 

        cursor.execute("UPDATE UserTbl SET Password=%s WHERE userID=%s" 
            ,(new_password, user_session.current_user_id))
        conn.commit()
    
        cursor.execute("SELECT fullName FROM UserTbl WHERE userID = %s", (user_session.current_user_id,))
        rows = cursor.fetchone()
        fullname= rows[0]

        return fullname + "'s password has been updated."

def changeFontsize(new_fontsize):
    if not new_fontsize.isdigit():
        return "Must be a number."
    if int(new_fontsize)>30:
        user_session.personal_fontsize = 30
        return "The maximum font size is 30."
    elif int(new_fontsize) < 12:
        user_session.personal_fontsize = 12
        return "The minimum font size is 12."
    else:
        user_session.personal_fontsize = new_fontsize
        return "Personal font size updated."
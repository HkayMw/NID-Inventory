from controller.user_controller import UserController
import hashlib
import datetime


def add_admin(id_number, firstname, lastname, othernames, password, created_by):
    # Hash the password
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    user_type = 'admin'
    # user_type = 'clerk'
    created_on = str(datetime.datetime.now())
    # Create an instance of UserModel
    user_controller = UserController()
    
    user_data={"id_number": id_number, "firstname": firstname, "lastname": lastname, "othernames": othernames, "password_hash": password_hash, "user_type": user_type, "created_by": created_by, "created_on": created_on}

    # Add the admin user
    print(user_controller.add_user(user_data))


    # print(f"Admin user {id_number} added successfully!")


# Example usage:
add_admin("WT3E6MQF", "Harry", "Kanyumbu", "Banda", "password123", "WT3E6MQF")

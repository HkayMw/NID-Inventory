from model.user_model import UserModel
import hashlib


def add_admin(id_no, first_name, last_name, other_names, password, created_by):
    # Hash the password
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    # User type is 'admin'
    user_type = 'operator'

    # Create an instance of UserModel
    user_model = UserModel()

    # Add the admin user
    user_model.add_user(id_no, first_name, last_name, other_names, password_hash, user_type, created_by)

    print(f"Admin user {id_no} added successfully!")


# Example usage:
add_admin("WT3E6MQF1", "Harry", "Kanyumbu", "", "password123", "WT3E6MQF")

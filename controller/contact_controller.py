# controller/contact_controller.py

from controller.controller import Controller
from model.contact_model import ContactModel
from datetime import datetime, timedelta
from kivymd.app import MDApp


class ContactController(Controller):
    def __init__(self):
        super().__init__(ContactModel())
        self.app = MDApp.get_running_app()
        
    def add_contact(self, id_number, phone_number):
        
        # Validate ID number (8 characters) and phone number (10 digits)
        if len(id_number) == 8 and phone_number.isdigit() and len(phone_number) == 10:
            created_on = str(datetime.now())
            created_by = self.app.user_details['id_number']
            
            data = {'id_number': id_number.upper(), 'phone_number': phone_number, 'created_on': created_on, 'created_by': created_by}
            
        else:
            error_msg = ''
            if len(id_number) != 8:
                error_msg += "ID must be 8 characters"
            if not phone_number.isdigit() or len(phone_number) != 10:
                if len(error_msg) > 1:
                    error_msg += " & "
                error_msg += "Phone number must be 10 digits"
                
            return False, error_msg, None
        
        success, message, last_row_id = self.create(data)
        
        if success:
            return success, message, id_number
        else:
            if message == 'An error occurred: UNIQUE constraint failed: contact.id_number from model.model':
                success, message, row = self.update_contact(id_number, phone_number)
                
                if success:
                    return success, message, id_number
                else:
                    return False, message, None
            
            return success, message, last_row_id

    def update_contact(self, id_number, phone_number):
        
        # Validate ID number (8 characters) and phone number (10 digits)
        if len(id_number) == 8 and phone_number.isdigit() and len(phone_number) == 10:
            created_on = str(datetime.now())
            from kivymd.app import MDApp

            
        else:
            error_msg = ''
            if len(id_number) != 8:
                error_msg += "ID must be 8 characters"
            if not phone_number.isdigit() or len(phone_number) != 10:
                if len(error_msg) > 1:
                    error_msg += " & "
                error_msg += "Phone number must be 10 digits"
                
            return False, error_msg, None
        
        created_on = str(datetime.now())
        created_by = self.app.user_details['id_number']
        
        where_clause = 'id_number = :id_number'
        params = {'id_number': id_number}
        data = {'phone_number': phone_number, 'updated_on': created_on, 'updated_by': created_by}
        
        success, message, row = self.update(data,where_clause,params)
        if success:
            return success, message, id_number
        else:
            return False, message, None
        
    def add_contacts(selfr):
        pass
    
    def search_contact(self,id_number=None, id_numbers=None):
        
        if id_number:
            # Validate ID number (8 characters) and phone number (10 digits)
            if len(id_number) == 8:
                where_clause = 'id_number = :id_number'
                params = {'id_number': id_number.upper()}
                
                success, message, rows = self.read(where_clause, params)
                if success:
                    # contact = {'id_number': rows[0][0], 'phone_number': rows[0][1]}
                    
                    if rows:
                        columns = ['id_number', 'phone_number','created_on', 'updated_on', 'created_by', 'updated_by']
                        
                        contacts = [dict(zip(columns, row)) for row in rows]
                    
                        return success, message, contacts
                    else:
                        return success, message, None
                        
                else:
                    return False, message, None
                
            else:
                error_msg = ''
                if len(id_number) != 8:
                    error_msg += "ID must be 8 characters"
                    
                return False, error_msg, None
        
        if id_numbers:
            # Filter for multiple ID numbers (make sure all IDs are 8 characters long)
            id_numbers = [id.upper() for id in id_numbers if len(id) == 8]
            if not id_numbers:
                return False, "No valid 8-character ID numbers provided", None
            
            placeholders = ', '.join([':id{}'.format(i) for i in range(len(id_numbers))])
            where_clause = 'id_number IN ({})'.format(placeholders)
            params = {f'id{i}': id_numbers[i] for i in range(len(id_numbers))}
            
            success, message, rows = self.read(where_clause, params)
            if success:
                if rows:
                    columns = ['id_number', 'phone_number', 'created_on', 'updated_on', 'created_by', 'updated_by']
                    contacts = [dict(zip(columns, row)) for row in rows]
                    return success, message, contacts
                else:
                    return success, message, None
            else:
                return False, message, None
        
        # If neither id_number nor id_numbers are provided
        return False, "No ID numbers provided", None
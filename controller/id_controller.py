# controller/id_controller.py

from kivymd.app import MDApp
from controller.controller import Controller
from controller.batch_controller import BatchController
from model.id_model import IdModel
from Assets.qr_code import QRCode
from datetime import datetime, timedelta


class IdController(Controller):
    def __init__(self):
        super().__init__(IdModel())
        self.batch_controller = BatchController()
        self.app = MDApp.get_running_app()
        
    def add_id(self,data):
        
        success, message, record_id = self.create(data)
        
        if success:
            # record_id = message
            return success, f"Record Added Successfully: ", record_id
        else:
            return False, message, None
        
    def search_id(self, search_type, id_number=None, firstname=None, lastname=None, signature=None, qr_code=None):
        """
        Searches for records based on the provided search type and parameters.
        
        :param search_type: Type of search ('id', 'name', or 'qr_code')
        :param id_number: ID number to search (if search_type is 'id')
        :param firstname: First name to search (if search_type is 'name')
        :param lastname: Last name to search (if search_type is 'name')
        :param qr_code: QR code to search (if search_type is 'qr_code')
        :return: Success status, message, and search results if successful
        """
        if search_type == 'id':
            # Validate ID Number
            if len(id_number) != 8:
                # self.ids.notice.theme_text_color = "Error"
                return False, "Invalid ID Number, Check for typos", None
            # Search by ID Number
            where_clause = 'id_number = :id_number'
            params = {'id_number': id_number.upper()}
            order_by = 'lastname'
            order_type = 'ASC'
            
        elif search_type == 'signature':
            
            # self.ids.notice.theme_text_color = "Error"
            # Search by ID Signature
            where_clause = 'signature = :signature'
            params = {'signature': signature.upper()}
            order_by = 'lastname'
            order_type = 'ASC'
        
        elif search_type == 'name':
            #validate names
            if firstname == '' and lastname == '':
                return False, 'Atleast firstname or lastname is required', None
            else:
                # Search by Name using regex on both first and last name
                where_clause = 'firstname LIKE :firstname AND lastname LIKE :lastname'
                params = {'firstname': f'%{firstname}%', 'lastname': f'%{lastname}%'}
                order_by = 'lastname'
                order_type = 'ASC'
        
        elif search_type == 'qr_code':
            #validate and process qr code
            qr_code = QRCode(qr_code.upper())
            success, message, qr = qr_code.process()
            order_by = 'lastname'
            order_type = 'ASC'
            # print(id)
            
            if success:
                #check if its ID qr code
                if qr['type'] == '03':
                    # Search by ID Number
                    where_clause = 'id_number = :id_number'
                    params = {'id_number': qr['id_number'].upper()}
                    order_by = 'lastname'
                    order_type = 'ASC'
                    
                #check if its general sticker
                if qr['type'] == '01':
                    pass
                
                # check if it id number sticker
                if qr['type'] == '10':
                    pass
            else:
                return False, message, None
                
        
        else:
            where_clause = None
            params = None
            order_by = 'lastname'
            order_type = 'ASC'
            print(f"Invalid search type: {search_type}. Error from {__name__}")

        # Perform the search using the read_records method from the Controller class
        success, message, result = self.read(where_clause, params, order_by, order_type)
        
        if success:
            if result:
                columns = ['signature', 'id_number', 'firstname', 'lastname', 'othernames', 'gender', 'd_o_b', 'status', 'batch', 'notified_on', 'created_on', 'updated_on', 'created_by', 'updated_by']
                
                result = [dict(zip(columns, row)) for row in result]

                return True, "Search Successful", result
            else:
                return False, "No records found", None
        else:
            return False, f"Search error: {message}", None
        
    def issue_id(self, signature):
        # self.current_user = self.app.user_details
        # self.user_id = self.current_user['id_number']
        print(signature)
        updated_on = str(datetime.now())
        updated_by = self.app.user_details['id_number']
        
        where_clause = 'signature = :signature'
        params = {'signature': signature}
        data = {'status': 'Issued', 'updated_on': updated_on, 'updated_by': updated_by}
        
        success, message, row = self.update(data, where_clause, params)
        if success:
            query = f"insert into collection (signature, issued_out_on, issued_out_by) values('{signature}', '{updated_on}', '{updated_by}')"
            
            success1, message, row = self.custom_query(query)
            
            print(success1, message, row)
            
            if success1:
                return success, message, row
        else:
            return False, message, row
        
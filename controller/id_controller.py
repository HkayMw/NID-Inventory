# controller/id_controller.py

from controller.controller import Controller
from model.id_model import IdModel
from Assets.qr_code import QRCode




class IdController(Controller):
    def __init__(self):
        super().__init__(IdModel())
        
    def add_id(self,data):
        
        success, message, record_id = self.create(data)
        
        if success:
            # record_id = message
            return success, f"Record Added Successfully: ", record_id
        else:
            return False, message, None
        
    def search_id(self, search_type, id_number=None, firstname=None, lastname=None, qr_code=None):
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
        
        elif search_type == 'name':
            #validate names
            if firstname == '' and lastname == '':
                return False, 'Atleast firstname or lastname is required', None
            else:
                # Search by Name using regex on both first and last name
                where_clause = 'firstname LIKE :firstname AND lastname LIKE :lastname'
                params = {'firstname': f'%{firstname}%', 'lastname': f'%{lastname}%'}
        
        elif search_type == 'qr_code':
            #validate and process qr code
            qr_code = QRCode(qr_code.upper())
            success, message, qr = qr_code.process()
            # print(id)
            
            if success:
                #check if its ID qr code
                if qr['type'] == '03':
                    # Search by ID Number
                    where_clause = 'id_number = :id_number'
                    params = {'id_number': qr['id_number'].upper()}
                    
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
            print(f"Invalid search type: {search_type}. Error from {__name__}")

        # Perform the search using the read_records method from the Controller class
        success, message, result = self.read(where_clause, params)
        
        if success:
            if result:
                columns = ['id_number', 'issue_date', 'firstname', 'lastname', 'othernames', 'gender', 'd_o_b', 'status', 'sorting_key', 'notified_on', 'created_on', 'updated_on', 'created_by', 'updated_by']
                
                result = [dict(zip(columns, row)) for row in result]

                return True, "Search Successful", result
            else:
                return False, "No records found", None
        else:
            return False, f"Search error: {message}", None
        
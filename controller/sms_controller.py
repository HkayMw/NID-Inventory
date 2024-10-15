
from kivymd.app import MDApp
from controller.controller import Controller
from model.model import Model
from datetime import datetime, timedelta

import africastalking



class SMSController(Controller):
    def __init__(self):
        super().__init__(Model())
        self.app = MDApp.get_running_app()
    
    def init_api(self):
        
        query = 'SELECT username, api_key FROM notification_api WHERE name = "africastalking"'
        
        success, message, data = self.custom_query(query)
        if success:
            # print(data)
            
            username = data[0][0]
            api_key = data[0][1]
            
            # print(username)
            # print(api_key)
            
            africastalking.initialize(
            username = username,
            api_key = api_key)
        else:
            self.app.ids.notice.text = 'Failed to initialise API, contact Administrator'
            
    def send_sms(self, sms, limit=None):
        self.sms = africastalking.SMS
        
        # Get phone numbers and id signatures
        query = F"SELECT id.signature, c.phone_number FROM id JOIN contact c ON id.id_number = c.id_number WHERE id.notified_on IS NULL ORDER BY id.created_on ASC"
        if limit:
            query += f" LIMIT {limit};"
        # print(query)
        success, message, data = self.custom_query(query)
        if not success:
            # print(message)
            return False, message, None
        
        else:
            notified = []
            id_signatures = {}
            phone_numbers = []
            # format phone numbers
            for row in data:
                phone_number = self.format_phone_number(row[1])
                phone_numbers.append(phone_number)
                id_signatures[phone_number] = row[0]
                
                # print(id_signatures)
                # print(phone_numbers)
            if len(phone_numbers) == 0:
                return False, "All clients with contacts available already notified", None 
            try:
                response = self.sms.send(sms, phone_numbers)
                # print(response)
            except Exception as e:
                print(f'Oops, we have a problem: {e}')
                return False, "Something went wrong, contact administrator", None
            
            recipients = self.extract_sms_responce_data(response)
            for recipient in recipients:
                if recipient['status'] == 'Success':
                    id_signature = id_signatures[recipient['phone_number']]
                    notified.append(id_signature)
                    
                else:
                    return False, f'Something went wrong @ {__name__}', None
                    
            
            return success, f'{len(notified)} Clients notified successfully', notified
    
    def get_to_be_notified(self):
        
        query = 'SELECT COUNT(*) FROM id JOIN contact c ON id.id_number = c.id_number WHERE id.notified_on IS NULL;'
        
        success, message, data = self.custom_query(query)
        if success:
            return success, message, data
        else:
            return False, message, None
        
    def format_phone_number(self, phone_number):
        # Check if the phone number starts with '0'
        if phone_number.startswith('0'):
            # Replace the first '0' with '+265'
            phone_number = '+265' + phone_number[1:]
        return phone_number
    
    def extract_sms_responce_data(self, response):
        # Extract message details
        message_data = response['SMSMessageData']
        message_content = message_data['Message']
        total_cost = message_content.split("Total Cost: ")[-1]  # Extract total cost
        total_recipients = int(message_content.split("Sent to ")[-1].split("/")[0])  # Extract total recipients

        # Extract recipient details
        recipients = message_data['Recipients']
        recipient_data = []

        for recipient in recipients:
            recipient_info = {
                'phone_number': recipient['number'],
                'message_id': recipient['messageId'],
                'status': recipient['status'],
                'status_code': recipient['statusCode'],
                'message_parts': recipient['messageParts'],
                'cost': recipient['cost'],
            }
            recipient_data.append(recipient_info)
            
        # data = {"total_recipients", total_recipients}
            
        return recipient_data

        # Display extracted data
        print("Message Content:", message_content)
        print("Total Cost:", total_cost)
        print("Total Recipients:", total_recipients)
        print("Recipient Data:")
        for data in recipient_data:
            print(data)
            


    # # Example usage
    # phone_number = "0987123456"
    # formatted_number = format_phone_number(phone_number)
    # print(formatted_number)
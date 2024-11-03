from controller.controller import Controller
from model.model import Model
from datetime import datetime, timedelta
from kivymd.app import MDApp
import requests


class SyncController(Controller):
    def __init__(self):
        super().__init__(Model())
        self.app = MDApp.get_running_app()
        
    def check_pending_records(self):
        
    
        query = "SELECT id.signature, id.id_number, id.status FROM id LEFT JOIN client_portal ON id.signature = client_portal.signature WHERE client_portal.signature IS NULL OR id.updated_on > client_portal.uploaded_on;"
        
        success, message, data = self.custom_query(query)
        if success:
            # print(data)
            # print(all_query)

            # data['total_ids'] = int(total_ids[0][0])
            
            return success, message, data
        else:
            print(f'success: {success} message: {message}')
            return success, message, None

    
    # def start_sync(self, pending):
        
    #     total_pending = len(pending)
    #     current_pending = 0
    #     # progress = 
    #     # url = "http://localhost/id_availability_portal/api/upload.php"
    #     url = "http://192.168.137.1/id_availability_portal/api/upload.php"
        
        
    #     for record in pending:
    #         signature = record[0]
    #         id_number = record[1]
    #         data = {
    #             "id_number": id_number,
    #             "availability_status": "Available"
    #         }
            
    #         success, message, responce = self.sync_to_client_portal(data, url)
    #         if success:
    #             # progress =
    #             pass
                
        
    
    def sync_to_client_portal(self, data, url):
        
        headers = {
            "Content-Type": "application/json"
            # "Authorization": "Bearer YOUR_API_KEY"  # Uncomment if your API requires authentication
        }

        try:
            response = requests.post(url, headers=headers, json=data)

            # Print the response for debugging
            # print("Response Status Code:", response.status_code)
            
            # print("Response Content:", response.content)

            if response.status_code == 200:
                print("Request successful:", response.json())
                return True, "Request successful", response.json
            else:
                print("Request failed:", response.text)
                return False, "Request failed", response.text

        except requests.exceptions.RequestException as e:
            print("An error occurred:", e)
            return False, f"An error occurred: {e}", None
        
    def update_client_portal(self, signature):
        
        uploaded_on = str(datetime.now())
        uploaded_by = self.app.user_details['id_number']
        
        
        query = f"REPLACE INTO client_portal (signature, uploaded_on, uploaded_by) VALUES ('{signature}', '{uploaded_on}', '{uploaded_by}')"
        
        success, message, response = self.custom_query(query)
        if success:
            print(query)
            return success, message, response
        
        else:
            return success, message, None
        
            
        
    
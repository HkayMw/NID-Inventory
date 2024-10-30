from controller.controller import Controller
from model.model import Model
from datetime import datetime, timedelta


class ReportController(Controller):
    def __init__(self):
        super().__init__(Model())
        
    def load_report(self, start_date, end_date):
        
        added_query = F"SELECT COUNT(*) AS Added FROM id WHERE DATE(created_on) >= '{start_date}' AND DATE(created_on) <= '{end_date}'"
        in_storage_query = "SELECT COUNT(*) AS Total_inventory FROM id WHERE status != 'Issued'"
        issued_query = F"SELECT COUNT(*) AS Issued FROM collection WHERE DATE(issued_out_on) >= '{start_date}' AND DATE(issued_out_on) <= '{end_date}'"

        sms_query = F"SELECT COUNT(*) FROM id WHERE DATE(notified_on) >= '{start_date}' AND DATE(notified_on) <= '{end_date}'"
        
        notified_issued_query = F"SELECT COUNT(*) AS Issued FROM id join collection on id.signature = collection.signature WHERE DATE(collection.issued_out_on) >= '{start_date}' AND DATE(collection.issued_out_on) <= '{end_date}' and id.notified_on != ''"
        
        report_data = {}
        
        success, message, data = self.custom_query(added_query)
        if success:
            # print(int(data[0][0]))
            # print(added_query)

            report_data['ids_added'] = int(data[0][0])
        else:
            # print(f'success: {success} message: {message}')
            return success, message, None
        
        success, message, data = self.custom_query(in_storage_query)
        if success:
            # print(int(data[0][0]))
            # print(in_storage_query)

            report_data['ids_in_storage'] = int(data[0][0])
        else:
            # print(f'success: {success} message: {message}')
            return success, message, None
        
        success, message, data = self.custom_query(issued_query)
        if success:
            # print(int(data[0][0]))
            # print(issued_query)

            report_data['ids_issued'] = int(data[0][0])
        else:
            # print(f'success: {success} message: {message}')
            return success, message, None
        
        success, message, data = self.custom_query(sms_query)
        if success:
            # print(int(data[0][0]))
            # print(in_storage_query)

            report_data['sent_sms'] = int(data[0][0])
        else:
            # print(f'success: {success} message: {message}')
            return success, message, None
        
        success, message, data = self.custom_query(notified_issued_query)
        if success:
            # print(int(data[0][0]))
            # print(in_storage_query)

            report_data['notified_ids_issued'] = int(data[0][0])
        else:
            # print(f'success: {success} message: {message}')
            return success, message, None
        
        return success, message, report_data
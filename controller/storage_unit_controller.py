#controller/storage_unit_controller.py

from controller.controller import Controller
from model.storage_unit_model import StorageUnitModel
import datetime


class StorageUnitController(Controller):
    def __init__(self):
        super().__init__(StorageUnitModel())
        # self.storage_unit_controller = StorageUnitController()
    
    
    def get_storage_units(self):
        storage_units = []
        
        query = """
                SELECT 
                    storage_unit.id AS storage_unit_id,
                    storage_unit.label AS storage_unit_label,
                    SUM(batch.count) AS total_count
                FROM 
                    storage_unit
                LEFT JOIN 
                    batch ON storage_unit.id = batch.storage
                GROUP BY 
                    storage_unit.id, storage_unit.label
          """
                # ORDER BY
                #     total_count ASC;
        success, message, rows = self.custom_query(query)
        #   print(f"success: {success} message: {message} rows: {rows}")
        if success:
            # print("Rows from db:", rows)
            for row in rows:
                # print(row,"from db")
                storage_units.append({"id": row[0], "label": row[1], "count": row[2]})
          
        else:
            return success, message, None
        
        return success, message, storage_units
        
    def create_storage_units(self, number_of_units):
        storage_units = []
        created_on = str(datetime.datetime.now())
        
        success, message, old_storage_units = self.read()
        # print(old_storage_units)
        
        # If you want to check for existing units, handle that logic here if needed
        
        for i in range(1, number_of_units + 1):
            unit = {
                'label': str(i),
                'created_on': created_on,
                'created_by': 'WT3E6MQF'  # Adjust this as necessary
            }
            
            success, message, record_id = self.create(unit)
            
            if success:
                storage_units.append({"id": record_id, "label": unit['label'], "created_on": created_on})
            else:
                return False, message, None  # Return on failure after attempting all inserts

        return True, "All records added successfully", storage_units  # Return after loop completes

            
    
          
          
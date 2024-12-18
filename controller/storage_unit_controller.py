#controller/storage_unit_controller.py

from kivymd.app import MDApp
from controller.controller import Controller
from model.storage_unit_model import StorageUnitModel
import datetime


class StorageUnitController(Controller):
    def __init__(self):
        super().__init__(StorageUnitModel())
        self.app = MDApp.get_running_app()
        # self.storage_unit_controller = StorageUnitController()
    
    
    def get_storage_units(self, sort_by = None):
        storage_units = []
        if sort_by:
            if sort_by == 'count':
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
                        ORDER BY
                            total_count DESC;
                        """
            if sort_by == 'id':
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
                        ORDER BY
                            storage_unit.id DESC;
                        """
                        
        else:
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
                            storage_unit.id, storage_unit.label;
                        """
                        
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
    
    def get_storage_unit(self, id):
        
        where_clause = 'id = :id'
        params = {'id': id}
        
        success, message, result = self.read(where_clause, params)
    
        if success:
            storage = {'id': result[0][0], 'label': result[0][1], 'created_on': result[0][2], 'updated_on': result[0][3], 'created_by': result[0][4], 'updated_by': result[0][5]}
            
            return success, message, storage
        else:
            return success, message, None
            
        
    def create_storage_units(self, number_of_units):
        storage_units = []
        created_on = str(datetime.datetime.now())
        created_by = self.app.user_details['id_number']
        
        success, message, old_storage_units = self.read()
        # print(old_storage_units)
        existing_units = len(old_storage_units)
        
        # If you want to check for existing units, handle that logic here if needed
        
        for i in range(1 + existing_units, number_of_units + existing_units + 1):
            unit = {
                'label': str(i),
                'created_on': created_on,
                'created_by': created_by
            }
            
            success, message, record_id = self.create(unit)
            
            if success:
                storage_units.append({"id": record_id, "label": unit['label'], "created_on": created_on})
            else:
                return False, message, None  # Return on failure after attempting all inserts

        return True, "All records added successfully", storage_units  # Return after loop completes

    def delete_storage_units(self, ids):
        # print(ids)
        placeholders = ', '.join(['?'] * len(ids))  # `?` for each item in id_list
        where_clause = f"id IN ({placeholders})"  # Adjust `id_column` to match your actual column name
        params = ids  # Params list, same as id_list here
        
        success, message, data = self.delete(where_clause, params)
        
        if success:
            return success, message, data
        else:
            return False, message, None
    
          
          
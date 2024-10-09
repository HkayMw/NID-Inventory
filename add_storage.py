from controller.storage_unit_controller import StorageUnitController
import hashlib
import datetime


storage_controller = StorageUnitController()
number_of_units = 30  # Example number of units to create
created_units = storage_controller.create_storage_units(number_of_units)
print(created_units)
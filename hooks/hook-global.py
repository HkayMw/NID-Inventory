# from PyInstaller.utils.hooks import collect_data_files
# import pkgutil

# # Initialize an empty list to collect data files
# datas = []

# # Loop through all installed packages and collect their data files
# for importer, package_name, ispkg in pkgutil.iter_modules():
#     # Skip built-in modules and packages
#     if ispkg:
#         # Collect data files from the package
#         collected_data = collect_data_files(package_name)
#         # Adjust the destination to the root folder
#         for data in collected_data:
#             # Each entry is a tuple (source, destination)
#             # Set the destination to empty for root
#             datas.append((data[0], ''))  # Appending with root destination

# # Optional: Remove duplicates if needed
# # This step might be useful if multiple packages share data files
# datas = list({tuple(data) for data in datas})

# # The `datas` variable will be used by PyInstaller to include the collected files

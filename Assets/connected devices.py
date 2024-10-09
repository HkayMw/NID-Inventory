# import usb.core
# import usb.util

# # Find all USB devices
# devices = usb.core.find(find_all=True)

# for device in devices:
#     vendor_id = hex(device.idVendor)
#     product_id = hex(device.idProduct)
#     usb_class = device.bDeviceClass  # Get the USB class code
    
    





# # Find the printer device by vendor and product ID
# printer = usb.core.find(idVendor=0x0483, idProduct=0x5720)

# if printer is None:
#     raise ValueError("Printer not found!")

# # Set the active configuration. Some devices may have multiple configurations
# printer.set_configuration()

# # Loop through configurations and endpoints to identify available endpoints
# for cfg in printer:
#     for intf in cfg:
#         print(f"Interface {intf.bInterfaceNumber}:")
#         for ep in intf:
#             print(f"    Endpoint Address: {hex(ep.bEndpointAddress)}")




# from escpos
# # Connect to the printer (replace with your printer's details)
# p = escpos.Usb(0x0483, 0x5720)

# # Print text
# p.text("Hello, World!\n")

# # Cut the paper
# p.cut()

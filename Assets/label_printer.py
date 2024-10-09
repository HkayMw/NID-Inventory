# import qrcode
from PIL import Image as PILImage, ImageDraw, ImageFont
# from kivy.core.image import Image as CoreImage

# import win32print
# import win32api
# import win32gui
# from io import BytesIO

from escpos.printer import Usb
import usb.core
import usb.util

class LabelPrinter():
    # def __init__(self):
    #     self.img = label_qrcode
        

    # # data = "Batch Name: October2024_19, Allocated Storage: 15"

    # # Create QR code instance
    # qr = qrcode.QRCode(
    #     version=1,  # Controls the size of the QR code. Higher number means bigger code.
    #     error_correction=qrcode.constants.ERROR_CORRECT_L,  # Error correction level
    #     box_size=10,  # Size of each box in the QR code
    #     border=2,  # Thickness of the border
    # )

    # # Add data to the QR code
    # qr.add_data(self.data)
    # qr.make(fit=True)

    # # Create an image from the QR code
    # img = qr.make_image(fill="black", back_color="white")

    def make_label(self, img, qr_text):
        # Create a blank image for the label (80mm x 25mm at 300 DPI)
        label_width_mm = 75
        label_height_mm = 20
        dpi = 200

        # Convert dimensions from mm to pixels for the image
        label_width_px = int((label_width_mm / 25.4) * dpi)
        label_height_px = int((label_height_mm / 25.4) * dpi)

        # Create a new blank white image
        label_img = PILImage.new('RGB', (label_width_px, label_height_px), "white")

        # Resize the QR code to fit on the left (25mm x 25mm at 300 DPI)
        qr_size_mm = label_height_mm
        qr_size_px = int((qr_size_mm / 25.4) * dpi)
        qr_img = img.resize((qr_size_px, qr_size_px))

        # Paste the QR code on the left of the label image
        label_img.paste(qr_img, (0, 0))

        # Draw text on the right side of the image
        draw = ImageDraw.Draw(label_img)

        # Use a default font (you can specify a custom TTF file if needed)
        try:
            font = ImageFont.truetype("arial.ttf", 27)  # Adjust font size based on your needs
        except IOError:
            font = ImageFont.load_default()  # Fallback to default font if arial.ttf is not available

        # Split the text at commas and strip any extra spaces
        text_lines = [line.strip() for line in qr_text.split(',')]

        # Calculate position for the text (leaving space for the QR code)
        text_x = qr_size_px + 10  # Start drawing text just after the QR code

        # Get the line height from the bounding box of a sample line of text
        sample_text_bbox = draw.textbbox((0, 0), "A", font=font)
        line_height = sample_text_bbox[3] - sample_text_bbox[1]  # Height of a single line of text
        padding = line_height  # Set padding equal to line height for spacing

        # Draw each line of text, stacked vertically
        for i, line in enumerate(text_lines):
            text_bbox = draw.textbbox((text_x, 0), line, font=font)
            text_y = (label_height_px - (line_height * len(text_lines))) // 2 + i * line_height  # Vertically center the text
            text_y = (label_height_px - ((line_height + padding) * len(text_lines))) // 2 + i * (line_height + padding)

            draw.text((text_x, text_y), line, font=font, fill="black")

        # Convert the image to monochrome (1-bit black and white)
        label_img = label_img.convert('1')  # Convert to 1-bit black/white image

        # Save the combined image as a temporary BMP file
        temp_file = "temp_batch_qrcode.bmp"
        label_img.save(temp_file, "BMP")  # Save as BMP in 1-bit black/white format
        return True,"Lable Created Successfully",{"label_width":label_width_px,"label_height": label_height_px,"file_path": temp_file}

    # Print the image using the specified printer
    def print_label(self, file_path ="temp_batch_qrcode.bmp", label_width_px = 590, label_height_px = 157):
        # Get printer details
        vendor_id, product_id, out_endpoint = self.find_printer()
        
        if vendor_id:
        
            # media_width = label_width_px  # Ensure this matches your media width
            # media_height=label_height_px
            p = Usb(vendor_id, product_id, timeout=0, out_ep=out_endpoint, media_width = label_width_px, media_height=label_height_px)

            # Reset the printer, set alignment, and set margins to 0
            p._raw(b'\x1B\x40')  # ESC @ (reset the printer)


            # # Set left margin to 0
            p._raw(b'\x1D\x4C\x00\x00')  # GS L nL nH (left margin to 0)


            # Set line spacing to 0 (may help reduce top margin)
            p._raw(b'\x1B\x33\x13')  # ESC 3 n (line spacing to 0)

            image = PILImage.open(file_path)

            # Print the image
            p.image(image)
            p.cut()
            return True, "Sticker Printed", None
        else:
            return False, "Please connect Printer and try again", None

        
    def find_printer(self):
        # Find all connected USB devices
        devices = usb.core.find(find_all=True)
        
        for device in devices:
            # Check if the device has the attributes matching your printer 
            if device.idVendor == 0x0483 and device.idProduct == 0x5720:  
                
                # Set the active configuration
                device.set_configuration()
                
                # Find the OUT endpoint in the interfaces
                for cfg in device:
                    for intf in cfg:
                        for ep in intf:
                            # Check if this is an OUT endpoint (bit 7 is 0 for OUT)
                            if usb.util.endpoint_direction(ep.bEndpointAddress) == usb.util.ENDPOINT_OUT:
                                # Ensure that the endpoint address is formatted as 0x02 (two-digit hex)
                                out_endpoint = ep.bEndpointAddress
                                return device.idVendor, device.idProduct, out_endpoint

        print("Printer not found.")
        return None, None, None


# Call the print function to print the label
# print_label(temp_file, label_width_px, label_height_px)
# vendor_id, product_id, out_endpoint = find_printer()


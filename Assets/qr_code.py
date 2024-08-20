# Assets/qr_code.py


import re
from typing import List, Tuple, Optional

class QRCode:
    def __init__(self, qr_code: str):
        self.qr_code = qr_code

    def process(self) -> Optional[Tuple[str, str, str, str, str, str]]:
        array = self.qr_code.split('~') if '~' in self.qr_code else self.qr_code.split(',')
        array = [element.strip() for element in array]  # Clean up any extra spaces
        
        # print(f"Length: {len(array)}\n{array}")

        # Runs if it is ID QR Code
        if '03' in self.qr_code[:4]:
            if self.qr_code[0] != '~':
                if len(array) == 12:
                    type = array[0]
                    firstname = array[6]
                    othernames = array[7]
                    lastname = array[4]
                    gender = array[8]
                    id_number = array[5]
                    d_o_b = self.db_date(array[9])
                elif len(array) == 11:
                    type = array[0]
                    firstname = array[6]
                    othernames = ''
                    lastname = array[4]
                    gender = array[7]
                    id_number = array[5]
                    d_o_b = self.db_date(array[8])
                else:
                    return None  # or handle the "noId" case as needed
            else:
                if len(array) == 13:
                    type = array[1]
                    firstname = array[7]
                    othernames = array[8]
                    lastname = array[5]
                    gender = array[9]
                    id_number = array[6]
                    d_o_b = self.db_date(array[10])
                elif len(array) == 12:
                    type = array[1]
                    firstname = array[7]
                    othernames = ''
                    lastname = array[5]
                    gender = array[8]
                    id_number = array[6]
                    d_o_b = self.db_date(array[9])
                else:
                    return None  # or handle the "noId" case as needed

            # Extract sorting key from surname
            sorting_key= lastname[:3]
            
            return {'type': type, 'firstname': firstname, 'othernames': othernames, 'lastname': lastname, 'gender': gender, 'id_number': id_number, 'd_o_b': d_o_b, "sorting_key": sorting_key}
        
        #Runs if it is General Sticker QR Code
        elif '01' in self.qr_code[:4]:
            
            #For new General Stickers
            if 'Renewal Processed' in self.qr_code[:4]:
                pass
            
            #For old General Stickers
            else:
                pass
            
        
        #Runs if it is ID Number Sticker QR Code
        elif '10' in self.qr_code[:4]:
            
            #For new ID Number Stickers
            if 'Renewal Processed' in self.qr_code[:4]:
                pass
            
            #For old ID Number Stickers
            else:
                pass

    def db_date(self, date_str: str) -> str:
        # Convert the date string to the desired format for the database
        # Placeholder implementation; adjust based on your specific date format requirements
        try:
            return re.sub(r'(\d{2})/(\d{2})/(\d{4})', r'\3-\2-\1', date_str)
        except Exception:
            return date_str  # Return the original date string if formatting fails

# # Example usage
# qr_processor = QRCode("~03~I<############<<<<<<<<<<<<<<<~##############MWI<<<<<<<<<<<4~DOE<<JOHN<<<<<<<<<<<<<<~DOE~A1B23C4D~JOHN~MALE~01 Jan 1991~01 jan 2017~")
# result = qr_processor.process()
# print(result)

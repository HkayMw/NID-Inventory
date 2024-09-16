class IDSorter:
    def __init__(self, database_connection):
        """
        Initialize the IDSorter class.
        
        Args:
        - database_connection: A connection object to interact with the database.
        """
        self.db = database_connection

    def get_high_count_surnames(self, threshold=50):
        """
        Fetch surnames with a count greater than the threshold and are exactly the same.

        Args:
        - threshold: The minimum count of IDs with the same surname.
        
        Returns:
        - List of surnames that meet the criteria.
        """
        query = """
        SELECT lastName
        FROM idrecords
        GROUP BY lastName
        HAVING COUNT(*) > %s AND MIN(lastName) = MAX(lastName)
        """
        cursor = self.db.cursor()
        cursor.execute(query, (threshold,))
        return [row[0] for row in cursor.fetchall()]

    def get_ids_with_lastname(self, last_name):
        """
        Fetch IDs with a specific last name.

        Args:
        - last_name: The last name to filter by.
        
        Returns:
        - List of records matching the last name.
        """
        query = "SELECT * FROM idrecords WHERE lastName = %s"
        cursor = self.db.cursor()
        cursor.execute(query, (last_name,))
        return cursor.fetchall()

    def set_sorting_key(self, records, key):
        """
        Set the sorting key for a list of records.

        Args:
        - records: List of ID records.
        - key: The sorting key to assign.
        """
        for record in records:
            query = "UPDATE idrecords SET sorting_key = %s WHERE id = %s"
            cursor = self.db.cursor()
            cursor.execute(query, (key, record['id']))
        self.db.commit()

    def sort_with_firstname(self, last_name):
        """
        Sort IDs with the same last name using first name letters.

        Args:
        - last_name: The surname of the IDs to be sorted.
        """
        records = self.get_ids_with_lastname(last_name)
        
        for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            filtered_records = [r for r in records if r['firstName'].upper().startswith(letter)]
            count = len(filtered_records)
            
            if 10 < count <= 50:
                self.set_sorting_key(filtered_records, last_name + "_" + letter)
            elif count > 50:
                self.recursively_sort_by_firstname(filtered_records, last_name + "_" + letter)
            else:
                self.set_sorting_key(filtered_records, "misc")

    def recursively_sort_by_firstname(self, records, key):
        """
        Recursively sort using letters from the first name when counts are high.

        Args:
        - records: List of records to sort further.
        - key: Current sorting key.
        """
        for record in records:
            firstname = record['firstName'].upper()
            for index, char in enumerate(firstname):
                new_key = key + char
                filtered = [r for r in records if r['firstName'].upper().startswith(new_key)]
                count = len(filtered)
                
                if 10 < count <= 50:
                    self.set_sorting_key(filtered, new_key)
                    return
                elif count > 50:
                    self.recursively_sort_by_firstname(filtered, new_key)
                else:
                    self.set_sorting_key(filtered, "misc")

    def sort_by_surname(self):
        """
        Sort IDs by their surnames, using additional surname letters if necessary.
        """
        for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            query = "SELECT * FROM idrecords WHERE lastName LIKE %s"
            cursor = self.db.cursor()
            cursor.execute(query, (letter + '%',))
            records = cursor.fetchall()
            count = len(records)
            
            if 10 < count <= 50:
                self.set_sorting_key(records, letter)
            elif count > 50:
                self.recursively_sort_by_surname(records, letter)
            else:
                self.set_sorting_key(records, "misc")

    def recursively_sort_by_surname(self, records, key):
        """
        Recursively sort using additional letters from the surname.

        Args:
        - records: List of records to sort further.
        - key: Current sorting key.
        """
        for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            new_key = key + letter
            filtered = [r for r in records if r['lastName'].upper().startswith(new_key)]
            count = len(filtered)
            
            if 10 < count <= 50:
                self.set_sorting_key(filtered, new_key)
            elif count > 50:
                self.recursively_sort_by_surname(filtered, new_key)
            else:
                self.set_sorting_key(filtered, "misc")

    def sort(self):
        """
        Main method to handle the sorting process.
        """
        # First, handle surnames with high counts and identical surnames
        high_count_surnames = self.get_high_count_surnames()
        for surname in high_count_surnames:
            self.sort_with_firstname(surname)
        
        # Then, sort the remaining records by surname
        self.sort_by_surname()

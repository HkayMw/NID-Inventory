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

    def count_ids_by_name(self, last_name, first_name_pattern='', issue_date=None):
        """
        Count the IDs with a specific last name and optional first name pattern.

        Args:
        - last_name: The last name pattern to filter by.
        - first_name_pattern: The pattern for first names, defaults to empty.
        - issue_date: Specific issue date to filter records.
        
        Returns:
        - The count of records matching the criteria.
        """
        query = """
        SELECT COUNT(*)
        FROM idrecords
        WHERE lastName LIKE %s AND firstName LIKE %s
        """
        params = [last_name, first_name_pattern + '%']
        
        if issue_date:
            query += " AND issueDate = %s"
            params.append(issue_date)
        
        cursor = self.db.cursor()
        cursor.execute(query, tuple(params))
        return cursor.fetchone()[0]

    def set_sorting_key(self, last_name_pattern, first_name_pattern, issue_date, sorting_key):
        """
        Set the sorting key for records based on patterns.

        Args:
        - last_name_pattern: Pattern for the last name.
        - first_name_pattern: Pattern for the first name.
        - issue_date: Issue date of the IDs.
        - sorting_key: The sorting key to be assigned.
        """
        query = """
        UPDATE idrecords
        SET sorting_key = %s
        WHERE lastName LIKE %s AND firstName LIKE %s AND issueDate = %s
        """
        cursor = self.db.cursor()
        cursor.execute(query, (sorting_key, last_name_pattern, first_name_pattern + '%', issue_date))
        self.db.commit()

    def sort_by_firstname(self, last_name, issue_date):
        """
        Sort IDs with the same last name using first name letters.

        Args:
        - last_name: The surname of the IDs to be sorted.
        - issue_date: The issue date of the IDs.
        """
        for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            count = self.count_ids_by_name(last_name, letter, issue_date)
            
            if 10 < count <= 50:
                sorting_key = f"{last_name}_{letter}_{issue_date.replace('-', '_')}"
                self.set_sorting_key(last_name, letter, issue_date, sorting_key)
            elif count > 50:
                self.recursively_sort_by_firstname(last_name, letter, issue_date, f"{last_name}_{letter}")
            else:
                sorting_key = f"{last_name}_misc_{issue_date.replace('-', '_')}"
                self.set_sorting_key(last_name, '', issue_date, sorting_key)

    def recursively_sort_by_firstname(self, last_name, first_name_pattern, issue_date, key):
        """
        Recursively sort using letters from the first name when counts are high.

        Args:
        - last_name: The surname of the IDs.
        - first_name_pattern: Current pattern for the first name.
        - issue_date: The issue date of the IDs.
        - key: The current sorting key being built.
        """
        for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            new_pattern = first_name_pattern + letter
            count = self.count_ids_by_name(last_name, new_pattern, issue_date)
            
            if 10 < count <= 50:
                sorting_key = f"{key}_{letter}_{issue_date.replace('-', '_')}"
                self.set_sorting_key(last_name, new_pattern, issue_date, sorting_key)
                return
            elif count > 50:
                self.recursively_sort_by_firstname(last_name, new_pattern, issue_date, f"{key}_{letter}")
            else:
                sorting_key = f"{key}_misc_{issue_date.replace('-', '_')}"
                self.set_sorting_key(last_name, new_pattern, issue_date, sorting_key)

    def sort_by_surname(self, issue_date):
        """
        Sort IDs by their surnames, using additional surname letters if necessary.

        Args:
        - issue_date: The issue date of the IDs.
        """
        for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            count = self.count_ids_by_name(letter + '%', '', issue_date)
            
            if 10 < count <= 50:
                sorting_key = f"{letter}_{issue_date.replace('-', '_')}"
                self.set_sorting_key(letter + '%', '', issue_date, sorting_key)
            elif count > 50:
                self.recursively_sort_by_surname(letter, issue_date)
            else:
                sorting_key = f"misc_{issue_date.replace('-', '_')}"
                self.set_sorting_key(letter + '%', '', issue_date, sorting_key)

    def recursively_sort_by_surname(self, last_name_pattern, issue_date):
        """
        Recursively sort using additional letters from the surname.

        Args:
        - last_name_pattern: Current pattern for the surname.
        - issue_date: The issue date of the IDs.
        """
        for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            new_pattern = last_name_pattern + letter
            count = self.count_ids_by_name(new_pattern + '%', '', issue_date)
            
            if 10 < count <= 50:
                sorting_key = f"{new_pattern}_{issue_date.replace('-', '_')}"
                self.set_sorting_key(new_pattern + '%', '', issue_date, sorting_key)
            elif count > 50:
                self.recursively_sort_by_surname(new_pattern, issue_date)
            else:
                sorting_key = f"{new_pattern}_misc_{issue_date.replace('-', '_')}"
                self.set_sorting_key(new_pattern + '%', '', issue_date, sorting_key)

    def sort(self, issue_date):
        """
        Main method to handle the sorting process.

        Args:
        - issue_date: The issue date of the IDs to be sorted.
        """
        # First, handle surnames with high counts and identical surnames
        high_count_surnames = self.get_high_count_surnames()
        for surname in high_count_surnames:
            self.sort_by_firstname(surname, issue_date)
        
        # Then, sort the remaining records by surname
        self.sort_by_surname(issue_date)


# Assuming `db` is a valid database connection object
sorter = IDSorter(db)
sorter.sort('2024-08')

from controller.controller import Controller
from model.model import Model
from datetime import datetime, timedelta


class DashboardController(Controller):
    def __init__(self):
        super().__init__(Model())

    def load_dashboard(self, period):

        if period == 'Day':

            date_today = datetime.today().date()
            # print(date_today)
            # print(dir(date_today))

            all_query = "SELECT COUNT(*) AS Total_inventory FROM id WHERE status != 'Issued'"
            added_query = F"SELECT COUNT(*) AS Added_today FROM id WHERE created_on LIKE '%{date_today}%'"
            issued_query = F"SELECT COUNT(*) AS Issued_today FROM collection WHERE issued_out_on LIKE '%{date_today}%'"

            sms_query = F"SELECT COUNT(*) FROM id WHERE notified_on LIKE '%{date_today}%'"

            users_query = "SELECT COUNT(*) FROM user"

            batch_query = "SELECT COUNT(*) FROM batch"

            storage_query = "SELECT COUNT(*) FROM storage_unit"

            data = {}

            success, message, total_ids = self.custom_query(all_query)
            if success:
                # print(int(total_ids[0][0]))
                # print(all_query)

                data['total_ids'] = int(total_ids[0][0])
            else:
                print(f'success: {success} message: {message}')
                return success, message, None

            success, message, added_ids = self.custom_query(added_query)
            if success:
                # print(int(added_ids[0][0]))
                # print(added_query)

                data['added_ids'] = int(added_ids[0][0])
            else:
                print(f'success: {success} message: {message}')
                return success, message, None

            success, message, issued_ids = self.custom_query(issued_query)
            if success:
                # print(int(issued_ids[0][0]))
                # print(issued_query)

                data['issued_ids'] = int(issued_ids[0][0])

            else:
                print(f'success: {success} message: {message}')
                return success, message, None

            success, message, sent_sms = self.custom_query(sms_query)
            if success:
                # print(int(sent_sms[0][0]))
                # print(sms_query)

                data['sent_sms'] = int(sent_sms[0][0])
            else:
                print(f'success: {success} message: {message}')
                return success, message, None

            success, message, users = self.custom_query(users_query)
            if success:
                # print(int(users[0][0]))
                # print(users_query)

                data['users'] = int(users[0][0])
            else:
                print(f'success: {success} message: {message}')
                return success, message, None

            success, message, batches = self.custom_query(batch_query)
            if success:
                # print(int(batches[0][0]))
                # print(users_query)

                data['batches'] = int(batches[0][0])
            else:
                print(f'success: {success} message: {message}')
                return success, message, None

            success, message, storage_units = self.custom_query(storage_query)
            if success:
                # print(int(storage_units[0][0]))
                # print(storage_query)

                data['storage_units'] = int(storage_units[0][0])
            else:
                print(f'success: {success} message: {message}')
                return success, message, None

            return success, message, data

            # cursor.execute(query, (date_today,))
        elif period == 'Week':

            year = datetime.today().year
            week = datetime.today().isocalendar()[1]

            week_start = datetime.strptime(f'{year}-W{week}-1', "%Y-W%W-%w").date()

            # Calculate the last day of the week (Sunday)
            week_end = week_start + timedelta(days=6)

            # print(week_start, ' ', week_end)

            all_query = "SELECT COUNT(*) AS Total_inventory FROM id WHERE status != 'Issued'"
            added_query = F"SELECT COUNT(*) AS Added_today FROM id WHERE DATE(created_on) >= '{week_start}' AND DATE(created_on) <= '{week_end}'"
            issued_query = F"SELECT COUNT(*) AS Issued FROM collection WHERE DATE(issued_out_on) >='{week_start}' AND DATE(issued_out_on) <= '{week_end}'"

            sms_query = F"SELECT COUNT(*) FROM id WHERE DATE(notified_on) >= '{week_start}' AND DATE(notified_on) <= '{week_end}'"

            users_query = "SELECT COUNT(*) FROM user"

            batch_query = "SELECT COUNT(*) FROM batch"

            storage_query = "SELECT COUNT(*) FROM storage_unit"

            data = {}

            success, message, total_ids = self.custom_query(all_query)
            if success:
                # print(int(total_ids[0][0]))
                # print(all_query)

                data['total_ids'] = int(total_ids[0][0])
            else:
                print(f'success: {success} message: {message}')
                return success, message, None

            success, message, added_ids = self.custom_query(added_query)
            if success:
                # print(int(added_ids[0][0]))
                # print(added_query)

                data['added_ids'] = int(added_ids[0][0])
            else:
                print(f'success: {success} message: {message}')
                return success, message, None

            success, message, issued_ids = self.custom_query(issued_query)
            if success:
                # print(int(issued_ids[0][0]))
                # print(issued_query)

                data['issued_ids'] = int(issued_ids[0][0])

            else:
                print(f'success: {success} message: {message}')
                return success, message, None

            success, message, sent_sms = self.custom_query(sms_query)
            if success:
                # print(int(sent_sms[0][0]))
                # print(sms_query)

                data['sent_sms'] = int(sent_sms[0][0])
            else:
                print(f'success: {success} message: {message}')
                return success, message, None

            success, message, users = self.custom_query(users_query)
            if success:
                # print(int(users[0][0]))
                # print(users_query)

                data['users'] = int(users[0][0])
            else:
                print(f'success: {success} message: {message}')
                return success, message, None

            success, message, batches = self.custom_query(batch_query)
            if success:
                # print(int(batches[0][0]))
                # print(users_query)

                data['batches'] = int(batches[0][0])
            else:
                print(f'success: {success} message: {message}')
                return success, message, None

            success, message, storage_units = self.custom_query(storage_query)
            if success:
                # print(int(storage_units[0][0]))
                # print(storage_query)

                data['storage_units'] = int(storage_units[0][0])
            else:
                print(f'success: {success} message: {message}')
                return success, message, None

            return success, message, data

            # cursor.execute(query, (current_week,))
        elif period == 'Month':
            # Fetch data for the last 4 weeks, changes each week
            year = datetime.today().year
            month = datetime.today().month

            current_month = f'{year}-{month}'

            # print(current_month)
            # cursor.execute(query, (current_month,))

            all_query = "SELECT COUNT(*) AS Total_inventory FROM id WHERE status != 'Issued'"
            added_query = F"SELECT COUNT(*) AS Added_today FROM id WHERE DATE(created_on) LIKE '%{current_month}%'"
            issued_query = F"SELECT COUNT(*) AS Issued_today FROM collection WHERE DATE(issued_out_on) LIKE '%{current_month}%'"

            sms_query = F"SELECT COUNT(*) FROM id WHERE DATE(notified_on) LIKE '%{current_month}%'"

            users_query = "SELECT COUNT(*) FROM user"

            batch_query = "SELECT COUNT(*) FROM batch"

            storage_query = "SELECT COUNT(*) FROM storage_unit"

            data = {}

            success, message, total_ids = self.custom_query(all_query)
            if success:
                # print(int(total_ids[0][0]))
                # print(all_query)

                data['total_ids'] = int(total_ids[0][0])
            else:
                print(f'success: {success} message: {message}')
                return success, message, None

            success, message, added_ids = self.custom_query(added_query)
            if success:
                # print(int(added_ids[0][0]))
                # print(added_query)

                data['added_ids'] = int(added_ids[0][0])
            else:
                print(f'success: {success} message: {message}')
                return success, message, None

            success, message, issued_ids = self.custom_query(issued_query)
            if success:
                # print(int(issued_ids[0][0]))
                # print(issued_query)

                data['issued_ids'] = int(issued_ids[0][0])

            else:
                print(f'success: {success} message: {message}')
                return success, message, None

            success, message, sent_sms = self.custom_query(sms_query)
            if success:
                # print(int(sent_sms[0][0]))
                # print(sms_query)

                data['sent_sms'] = int(sent_sms[0][0])
            else:
                print(f'success: {success} message: {message}')
                return success, message, None

            success, message, users = self.custom_query(users_query)
            if success:
                # print(int(users[0][0]))
                # print(users_query)

                data['users'] = int(users[0][0])
            else:
                print(f'success: {success} message: {message}')
                return success, message, None

            success, message, batches = self.custom_query(batch_query)
            if success:
                # print(int(batches[0][0]))
                # print(users_query)

                data['batches'] = int(batches[0][0])
            else:
                print(f'success: {success} message: {message}')
                return success, message, None

            success, message, storage_units = self.custom_query(storage_query)
            if success:
                # print(int(storage_units[0][0]))
                # print(storage_query)

                data['storage_units'] = int(storage_units[0][0])
            else:
                print(f'success: {success} message: {message}')
                return success, message, None

            return success, message, data

        elif period == 'Year':
            # Fetch data for the last 12 months, changes each month
            current_year = datetime.today().year
            # print(current_year)
            # cursor.execute(query, (current_year,))

            all_query = "SELECT COUNT(*) AS Total_inventory FROM id WHERE status != 'Issued'"
            added_query = F"SELECT COUNT(*) AS Added_today FROM id WHERE DATE(created_on) LIKE '%{current_year}%'"
            issued_query = F"SELECT COUNT(*) AS Issued_today FROM collection WHERE DATE(issued_out_on) LIKE '%{current_year}%'"

            sms_query = F"SELECT COUNT(*) FROM id WHERE DATE(notified_on) LIKE '%{current_year}%'"

            users_query = "SELECT COUNT(*) FROM user"

            batch_query = "SELECT COUNT(*) FROM batch"

            storage_query = "SELECT COUNT(*) FROM storage_unit"

            data = {}

            success, message, total_ids = self.custom_query(all_query)
            if success:
                # print(int(total_ids[0][0]))
                # print(all_query)

                data['total_ids'] = int(total_ids[0][0])
            else:
                print(f'success: {success} message: {message}')
                return success, message, None

            success, message, added_ids = self.custom_query(added_query)
            if success:
                # print(int(added_ids[0][0]))
                # print(added_query)

                data['added_ids'] = int(added_ids[0][0])
            else:
                print(f'success: {success} message: {message}')
                return success, message, None

            success, message, issued_ids = self.custom_query(issued_query)
            if success:
                # print(int(issued_ids[0][0]))
                # print(issued_query)

                data['issued_ids'] = int(issued_ids[0][0])

            else:
                print(f'success: {success} message: {message}')
                return success, message, None

            success, message, sent_sms = self.custom_query(sms_query)
            if success:
                # print(int(sent_sms[0][0]))
                # print(sms_query)

                data['sent_sms'] = int(sent_sms[0][0])
            else:
                print(f'success: {success} message: {message}')
                return success, message, None

            success, message, users = self.custom_query(users_query)
            if success:
                # print(int(users[0][0]))
                # print(users_query)

                data['users'] = int(users[0][0])
            else:
                print(f'success: {success} message: {message}')
                return success, message, None

            success, message, batches = self.custom_query(batch_query)
            if success:
                # print(int(batches[0][0]))
                # print(users_query)

                data['batches'] = int(batches[0][0])
            else:
                print(f'success: {success} message: {message}')
                return success, message, None

            success, message, storage_units = self.custom_query(storage_query)
            if success:
                # print(int(storage_units[0][0]))
                # print(storage_query)

                data['storage_units'] = int(storage_units[0][0])
            else:
                print(f'success: {success} message: {message}')
                return success, message, None

            return success, message, data

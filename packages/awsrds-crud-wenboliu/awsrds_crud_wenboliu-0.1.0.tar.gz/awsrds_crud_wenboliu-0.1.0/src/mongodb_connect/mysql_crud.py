import pymysql

class mysql_crud:

    def __init__(self, uri: str, port: int, user: str, password: str, database: str):
        self.db = self.create_database(uri, port, user, password)
        self.cursor = self.create_cursor(self.db)
        # Create the database (if it doesn't exist)
        sql = f"CREATE DATABASE IF NOT EXISTS {database}"
        self.cursor.execute(sql)
        self.cursor.close()
        self.db.close()
        self.db = self.create_database1(uri, port, user, password, database)
        self.cursor = self.db.cursor()

    def create_database(self, uri, port, user, password):
        return pymysql.connect(
            host=uri,
            port=port,
            user=user,
            password=password
        )

    def create_database1(self, uri, port, user, password, database):
        return pymysql.connect(
            host=uri,
            port=port,
            user=user,
            password=password,
            database=database
        )

    def create_cursor(self, db):
        return db.cursor()

    def create_table(self, table_name, columns):
        column_definitions = []
        for column in columns:
            column_definition = f"{column['name']} {column['data_type']}"
            if 'constraints' in column:
                for constraint, value in column['constraints'].items():
                    column_definition += f" {constraint} {value}"
            column_definitions.append(column_definition)

        sql = f"CREATE TABLE {table_name} ({', '.join(column_definitions)})"

        try:
            self.cursor.execute(sql)
            print(f"Table '{table_name}' created successfully.")
        except pymysql.Error as e:
            print(f"Error creating table: {e}")

    def create_record(self, table_name, data):
        """Creates a new record in the specified table."""
        columns = ', '.join(data.keys())
        values = ', '.join(['%s' for _ in data.values()])
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
        try:
            self.cursor.execute(sql, tuple(data.values()))
            self.db.commit()
            print("Record created successfully.")
        except pymysql.Error as e:
            print(f"Error creating record: {e}")

    def read_records(self, table_name):
        """Retrieves all records from the specified table."""
        sql = f"SELECT * FROM {table_name}"
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            for row in results:
                print(row)
            return results
        except pymysql.Error as e:
            print(f"Error reading records: {e}")
            return None

    def update_record(self, table_name, condition, data):
        """Updates a record in the specified table based on the given condition."""
        set_clause = ', '.join([f"{key} = %s" for key in data.keys()])
        sql = f"UPDATE {table_name} SET {set_clause} WHERE {condition}"
        try:
            self.cursor.execute(sql, tuple(data.values()))
            self.db.commit()
            print("Record updated successfully.")
        except pymysql.Error as e:
            print(f"Error updating record: {e}")

    def delete_record(self, table_name, condition):
        """Deletes a record from the specified table based on the given condition."""
        sql = f"DELETE FROM {table_name} WHERE {condition}"
        try:
            self.cursor.execute(sql)
            self.db.commit()
            print("Record deleted successfully.")
        except pymysql.Error as e:
            print(f"Error deleting record: {e}")
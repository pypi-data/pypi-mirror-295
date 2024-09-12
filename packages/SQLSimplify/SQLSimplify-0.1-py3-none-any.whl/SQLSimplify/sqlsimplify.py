import mysql.connector
import os
import subprocess

class Get:
    def __init__(self , mydb , database_name=None):
        self.mydb = mydb
        self.database_name = database_name

    def database(self):
        """List all databases."""
        self.mycursor = self.mydb.cursor()
        self.mycursor.execute("SHOW DATABASES")
        print("Databases:")
        for database in self.mycursor:
            print(database[0])

    def tables(self , database_name=None):
        """List all tables in the specified or connected database."""
        self.mycursor = self.mydb.cursor()
        db_to_use = database_name or self.database_name

        if db_to_use:
            self.mycursor.execute(f"USE {db_to_use}")
            self.mycursor.execute("SHOW TABLES")
            print(f"Tables in database '{db_to_use}':")
            for table in self.mycursor:
                print(table[0])
        else:
            print("No database specified.")

    def columns(self , table_name , database_name=None):
        """List all columns in the specified table."""
        self.mycursor = self.mydb.cursor()
        db_to_use = database_name or self.database_name

        if db_to_use:
            self.mycursor.execute(f"USE {db_to_use}")
            self.mycursor.execute(f"DESCRIBE {table_name}")
            print(f"Columns in table '{table_name}':")
            for column in self.mycursor:
                print(column)
        else:
            print("No database specified.")

    def row_count(self , table_name , database_name=None):
        """Count the number of rows in the specified table."""
        self.mycursor = self.mydb.cursor()
        db_to_use = database_name or self.database_name

        if db_to_use:
            self.mycursor.execute(f"USE {db_to_use}")
            self.mycursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = self.mycursor.fetchone()[0]
            print(f"Row count in table '{table_name}': {count}")
        else:
            print("No database specified.")

    def table_status(self , database_name=None):
        """Get the status of all tables in the specified or connected database."""
        self.mycursor = self.mydb.cursor()
        db_to_use = database_name or self.database_name

        if db_to_use:
            self.mycursor.execute(f"USE {db_to_use}")
            self.mycursor.execute("SHOW TABLE STATUS")
            print(f"Status of tables in database '{db_to_use}':")
            for status in self.mycursor:
                print(status)
        else:
            print("No database specified.")

    def indexes(self , table_name , database_name=None):
        """List all indexes in the specified table."""
        self.mycursor = self.mydb.cursor()
        db_to_use = database_name or self.database_name

        if db_to_use:
            self.mycursor.execute(f"USE {db_to_use}")
            self.mycursor.execute(f"SHOW INDEX FROM {table_name}")
            print(f"Indexes in table '{table_name}':")
            for index in self.mycursor:
                print(index)
        else:
            print("No database specified.")

    def procedures(self , database_name=None):
        """List all stored procedures in the specified or connected database."""
        self.mycursor = self.mydb.cursor()
        db_to_use = database_name or self.database_name

        if db_to_use:
            self.mycursor.execute(f"USE {db_to_use}")
            self.mycursor.execute("SHOW PROCEDURE STATUS WHERE Db = %s" , (db_to_use ,))
            print(f"Stored procedures in database '{db_to_use}':")
            for proc in self.mycursor:
                print(proc)
        else:
            print("No database specified.")

    def functions(self , database_name=None):
        """List all stored functions in the specified or connected database."""
        self.mycursor = self.mydb.cursor()
        db_to_use = database_name or self.database_name

        if db_to_use:
            self.mycursor.execute(f"USE {db_to_use}")
            self.mycursor.execute("SHOW FUNCTION STATUS WHERE Db = %s" , (db_to_use ,))
            print(f"Stored functions in database '{db_to_use}':")
            for func in self.mycursor:
                print(func)
        else:
            print("No database specified.")

class Create:
    def __init__(self, mydb, database_name=None):
        self.mydb = mydb
        self.database_name = database_name

    def database(self, database_name):
        """Create a new database."""
        self.mycursor = self.mydb.cursor()
        try:
            self.mycursor.execute(f"CREATE DATABASE {database_name}")
            print(f"Database '{database_name}' created successfully.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def table(self, table_name, columns, database_name=None):
        """
        Create a new table.
        :param table_name: Name of the table to create.
        :param columns: A dictionary where keys are column names and values are column types (e.g., {'id': 'INT AUTO_INCREMENT PRIMARY KEY', 'name': 'VARCHAR(100)'}).
        :param database_name: Optional database name. Uses the connected database if not specified.
        """
        self.mycursor = self.mydb.cursor()
        db_to_use = database_name or self.database_name

        if db_to_use:
            self.mycursor.execute(f"USE {db_to_use}")
            columns_def = ', '.join([f"{col} {typ}" for col, typ in columns.items()])
            try:
                self.mycursor.execute(f"CREATE TABLE {table_name} ({columns_def})")
                print(f"Table '{table_name}' created successfully in database '{db_to_use}'.")
            except mysql.connector.Error as err:
                print(f"Error: {err}")
        else:
            print("No database specified.")

    def index(self, index_name, table_name, columns, index_type='INDEX', database_name=None):
        """
        Create a new index on a table.
        :param index_name: Name of the index to create.
        :param table_name: Name of the table on which to create the index.
        :param columns: A list of column names on which to create the index.
        :param index_type: Type of the index (e.g., 'INDEX', 'UNIQUE', 'FULLTEXT').
        :param database_name: Optional database name. Uses the connected database if not specified.
        """
        self.mycursor = self.mydb.cursor()
        db_to_use = database_name or self.database_name

        if db_to_use:
            self.mycursor.execute(f"USE {db_to_use}")
            columns_str = ', '.join(columns)
            try:
                self.mycursor.execute(f"CREATE {index_type} {index_name} ON {table_name} ({columns_str})")
                print(f"Index '{index_name}' created successfully on table '{table_name}' in database '{db_to_use}'.")
            except mysql.connector.Error as err:
                print(f"Error: {err}")
        else:
            print("No database specified.")

    def stored_procedure(self, procedure_name, procedure_body, database_name=None):
        """
        Create a new stored procedure.
        :param procedure_name: Name of the stored procedure.
        :param procedure_body: SQL body of the stored procedure.
        :param database_name: Optional database name. Uses the connected database if not specified.
        """
        self.mycursor = self.mydb.cursor()
        db_to_use = database_name or self.database_name

        if db_to_use:
            self.mycursor.execute(f"USE {db_to_use}")
            try:
                self.mycursor.execute(f"DELIMITER // CREATE PROCEDURE {procedure_name} {procedure_body} // DELIMITER ;")
                print(f"Stored procedure '{procedure_name}' created successfully in database '{db_to_use}'.")
            except mysql.connector.Error as err:
                print(f"Error: {err}")
        else:
            print("No database specified.")

    def function(self, function_name, function_body, database_name=None):
        """
        Create a new stored function.
        :param function_name: Name of the function.
        :param function_body: SQL body of the function.
        :param database_name: Optional database name. Uses the connected database if not specified.
        """
        self.mycursor = self.mydb.cursor()
        db_to_use = database_name or self.database_name

        if db_to_use:
            self.mycursor.execute(f"USE {db_to_use}")
            try:
                self.mycursor.execute(f"DELIMITER // CREATE FUNCTION {function_name} {function_body} // DELIMITER ;")
                print(f"Function '{function_name}' created successfully in database '{db_to_use}'.")
            except mysql.connector.Error as err:
                print(f"Error: {err}")
        else:
            print("No database specified.")

    def foreign_key(self, table_name, fk_name, column_name, ref_table, ref_column, database_name=None):
        """
        Create a foreign key constraint on a table.
        :param table_name: Name of the table to add the foreign key.
        :param fk_name: Name of the foreign key constraint.
        :param column_name: Name of the column to be constrained.
        :param ref_table: Name of the referenced table.
        :param ref_column: Name of the referenced column in the referenced table.
        :param database_name: Optional database name. Uses the connected database if not specified.
        """
        self.mycursor = self.mydb.cursor()
        db_to_use = database_name or self.database_name

        if db_to_use:
            self.mycursor.execute(f"USE {db_to_use}")
            try:
                self.mycursor.execute(
                    f"ALTER TABLE {table_name} ADD CONSTRAINT {fk_name} FOREIGN KEY ({column_name}) REFERENCES {ref_table}({ref_column})"
                )
                print(f"Foreign key '{fk_name}' added successfully to table '{table_name}' in database '{db_to_use}'.")
            except mysql.connector.Error as err:
                print(f"Error: {err}")
        else:
            print("No database specified.")

class Delete:
    def __init__(self, mydb, database_name=None):
        self.mydb = mydb
        self.database_name = database_name

    def database(self, database_name):
        """Delete an existing database."""
        self.mycursor = self.mydb.cursor()
        try:
            self.mycursor.execute(f"DROP DATABASE {database_name}")
            print(f"Database '{database_name}' deleted successfully.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def table(self, table_name, database_name=None):
        """Delete a table from the specified or connected database."""
        self.mycursor = self.mydb.cursor()
        db_to_use = database_name or self.database_name

        if db_to_use:
            self.mycursor.execute(f"USE {db_to_use}")
            try:
                self.mycursor.execute(f"DROP TABLE {table_name}")
                print(f"Table '{table_name}' deleted successfully from database '{db_to_use}'.")
            except mysql.connector.Error as err:
                print(f"Error: {err}")
        else:
            print("No database specified.")

    def row(self, table_name, condition, database_name=None):
        """
        Delete rows from a table based on a condition.
        :param table_name: Name of the table from which rows should be deleted.
        :param condition: SQL condition to match rows for deletion (e.g., "id = 1").
        :param database_name: Optional database name. Uses the connected database if not specified.
        """
        self.mycursor = self.mydb.cursor()
        db_to_use = database_name or self.database_name

        if db_to_use:
            self.mycursor.execute(f"USE {db_to_use}")
            try:
                self.mycursor.execute(f"DELETE FROM {table_name} WHERE {condition}")
                self.mydb.commit()
                print(f"Rows deleted from table '{table_name}' where {condition}.")
            except mysql.connector.Error as err:
                print(f"Error: {err}")
        else:
            print("No database specified.")

    def index(self, index_name, table_name, database_name=None):
        """
        Delete an index from a table.
        :param index_name: Name of the index to delete.
        :param table_name: Name of the table from which to delete the index.
        :param database_name: Optional database name. Uses the connected database if not specified.
        """
        self.mycursor = self.mydb.cursor()
        db_to_use = database_name or self.database_name

        if db_to_use:
            self.mycursor.execute(f"USE {db_to_use}")
            try:
                self.mycursor.execute(f"DROP INDEX {index_name} ON {table_name}")
                print(f"Index '{index_name}' deleted successfully from table '{table_name}' in database '{db_to_use}'.")
            except mysql.connector.Error as err:
                print(f"Error: {err}")
        else:
            print("No database specified.")

    def stored_procedure(self, procedure_name, database_name=None):
        """
        Delete an existing stored procedure.
        :param procedure_name: Name of the stored procedure to delete.
        :param database_name: Optional database name. Uses the connected database if not specified.
        """
        self.mycursor = self.mydb.cursor()
        db_to_use = database_name or self.database_name

        if db_to_use:
            self.mycursor.execute(f"USE {db_to_use}")
            try:
                self.mycursor.execute(f"DROP PROCEDURE IF EXISTS {procedure_name}")
                print(f"Stored procedure '{procedure_name}' deleted successfully in database '{db_to_use}'.")
            except mysql.connector.Error as err:
                print(f"Error: {err}")
        else:
            print("No database specified.")

    def function(self, function_name, database_name=None):
        """
        Delete an existing stored function.
        :param function_name: Name of the function to delete.
        :param database_name: Optional database name. Uses the connected database if not specified.
        """
        self.mycursor = self.mydb.cursor()
        db_to_use = database_name or self.database_name

        if db_to_use:
            self.mycursor.execute(f"USE {db_to_use}")
            try:
                self.mycursor.execute(f"DROP FUNCTION IF EXISTS {function_name}")
                print(f"Function '{function_name}' deleted successfully in database '{db_to_use}'.")
            except mysql.connector.Error as err:
                print(f"Error: {err}")
        else:
            print("No database specified.")

    def foreign_key(self, table_name, fk_name, database_name=None):
        """
        Delete a foreign key constraint from a table.
        :param table_name: Name of the table to remove the foreign key from.
        :param fk_name: Name of the foreign key constraint.
        :param database_name: Optional database name. Uses the connected database if not specified.
        """
        self.mycursor = self.mydb.cursor()
        db_to_use = database_name or self.database_name

        if db_to_use:
            self.mycursor.execute(f"USE {db_to_use}")
            try:
                self.mycursor.execute(f"ALTER TABLE {table_name} DROP FOREIGN KEY {fk_name}")
                print(f"Foreign key '{fk_name}' deleted successfully from table '{table_name}' in database '{db_to_use}'.")
            except mysql.connector.Error as err:
                print(f"Error: {err}")
        else:
            print("No database specified.")

class Update:
    def __init__(self, mydb, database_name=None):
        self.mydb = mydb
        self.database_name = database_name

    def row(self, table_name, updates, condition, database_name=None):
        """
        Update rows in a table based on a condition.
        :param table_name: Name of the table where rows will be updated.
        :param updates: A dictionary where keys are column names and values are the new values (e.g., {'column1': 'new_value', 'column2': 10}).
        :param condition: SQL condition to match rows for update (e.g., "id = 1").
        :param database_name: Optional database name. Uses the connected database if not specified.
        """
        self.mycursor = self.mydb.cursor()
        db_to_use = database_name or self.database_name

        if db_to_use:
            self.mycursor.execute(f"USE {db_to_use}")
            set_clause = ', '.join([f"{col} = %s" for col in updates.keys()])
            values = list(updates.values())
            query = f"UPDATE {table_name} SET {set_clause} WHERE {condition}"
            try:
                self.mycursor.execute(query, values)
                self.mydb.commit()
                print(f"Rows updated in table '{table_name}' where {condition}.")
            except mysql.connector.Error as err:
                print(f"Error: {err}")
        else:
            print("No database specified.")

    def column(self, table_name, column_name, new_type, database_name=None):
        """
        Modify the data type or properties of a column.
        :param table_name: Name of the table containing the column.
        :param column_name: Name of the column to modify.
        :param new_type: New data type or properties of the column (e.g., 'VARCHAR(255)', 'INT NOT NULL').
        :param database_name: Optional database name. Uses the connected database if not specified.
        """
        self.mycursor = self.mydb.cursor()
        db_to_use = database_name or self.database_name

        if db_to_use:
            self.mycursor.execute(f"USE {db_to_use}")
            try:
                self.mycursor.execute(f"ALTER TABLE {table_name} MODIFY COLUMN {column_name} {new_type}")
                print(f"Column '{column_name}' modified successfully in table '{table_name}'.")
            except mysql.connector.Error as err:
                print(f"Error: {err}")
        else:
            print("No database specified.")

    def table_name(self, old_name, new_name, database_name=None):
        """
        Rename a table.
        :param old_name: Current name of the table.
        :param new_name: New name for the table.
        :param database_name: Optional database name. Uses the connected database if not specified.
        """
        self.mycursor = self.mydb.cursor()
        db_to_use = database_name or self.database_name

        if db_to_use:
            self.mycursor.execute(f"USE {db_to_use}")
            try:
                self.mycursor.execute(f"RENAME TABLE {old_name} TO {new_name}")
                print(f"Table '{old_name}' renamed to '{new_name}' in database '{db_to_use}'.")
            except mysql.connector.Error as err:
                print(f"Error: {err}")
        else:
            print("No database specified.")

class Backup:
    def __init__(self , mydb , database_name=None):
        self.mydb = mydb
        self.database_name = database_name

    def backup_database(self , backup_file , database_name=None):
        """
        Create a backup of the entire database.
        :param backup_file: Path to the file where the backup will be saved.
        :param database_name: Optional database name. Uses the connected database if not specified.
        """
        db_to_backup = database_name or self.database_name
        if db_to_backup:
            try:
                command = f"mysqldump -h {self.mydb.server_host} -u {self.mydb.user} --password={self.mydb.password} {db_to_backup} > {backup_file}"
                subprocess.run(command , shell=True , check=True)
                print(f"Database '{db_to_backup}' backed up successfully to '{backup_file}'.")
            except subprocess.CalledProcessError as err:
                print(f"Error: {err}")
        else:
            print("No database specified.")

    def backup_table(self , table_name , backup_file , database_name=None):
        """
        Create a backup of a specific table.
        :param table_name: Name of the table to back up.
        :param backup_file: Path to the file where the table backup will be saved.
        :param database_name: Optional database name. Uses the connected database if not specified.
        """
        db_to_backup = database_name or self.database_name
        if db_to_backup:
            try:
                command = f"mysqldump -h {self.mydb.server_host} -u {self.mydb.user} --password={self.mydb.password} {db_to_backup} {table_name} > {backup_file}"
                subprocess.run(command , shell=True , check=True)
                print(f"Table '{table_name}' backed up successfully to '{backup_file}'.")
            except subprocess.CalledProcessError as err:
                print(f"Error: {err}")
        else:
            print("No database specified.")

    def restore_database(self , backup_file , database_name=None):
        """
        Restore a database from a backup file.
        :param backup_file: Path to the backup file.
        :param database_name: Optional database name. Uses the connected database if not specified.
        """
        db_to_restore = database_name or self.database_name
        if db_to_restore:
            try:
                command = f"mysql -h {self.mydb.server_host} -u {self.mydb.user} --password={self.mydb.password} {db_to_restore} < {backup_file}"
                subprocess.run(command , shell=True , check=True)
                print(f"Database '{db_to_restore}' restored successfully from '{backup_file}'.")
            except subprocess.CalledProcessError as err:
                print(f"Error: {err}")
        else:
            print("No database specified.")

    def restore_table(self , table_name , backup_file , database_name=None):
        """
        Restore a specific table from a backup file.
        :param table_name: Name of the table to restore.
        :param backup_file: Path to the backup file.
        :param database_name: Optional database name. Uses the connected database if not specified.
        """
        db_to_restore = database_name or self.database_name
        if db_to_restore:
            try:
                # Create a temporary database for restoring the table
                temp_db = f"temp_{db_to_restore}"
                command = f"mysql -h {self.mydb.server_host} -u {self.mydb.user} --password={self.mydb.password} -e 'CREATE DATABASE IF NOT EXISTS {temp_db}; USE {temp_db}; SOURCE {backup_file};' "
                subprocess.run(command , shell=True , check=True)

                # Copy table from temporary database to the target database
                command = f"mysqldump -h {self.mydb.server_host} -u {self.mydb.user} --password={self.mydb.password} {temp_db} {table_name} | mysql -h {self.mydb.server_host} -u {self.mydb.user} --password={self.mydb.password} {db_to_restore}"
                subprocess.run(command , shell=True , check=True)

                # Drop the temporary database
                command = f"mysql -h {self.mydb.server_host} -u {self.mydb.user} --password={self.mydb.password} -e 'DROP DATABASE {temp_db};'"
                subprocess.run(command , shell=True , check=True)

                print(f"Table '{table_name}' restored successfully from '{backup_file}'.")
            except subprocess.CalledProcessError as err:
                print(f"Error: {err}")
        else:
            print("No database specified.")

class Query:
    def __init__(self, mydb, database_name=None):
        self.mydb = mydb
        self.database_name = database_name

    def execute(self, query, params=None, database_name=None):
        """
        Execute a raw SQL query.
        :param query: The SQL query to execute.
        :param params: Optional parameters for the query.
        :param database_name: Optional database name. Uses the connected database if not specified.
        :return: Result of the query execution.
        """
        self.mycursor = self.mydb.cursor()
        db_to_use = database_name or self.database_name

        if db_to_use:
            self.mycursor.execute(f"USE {db_to_use}")
            try:
                self.mycursor.execute(query, params or ())
                result = self.mycursor.fetchall()
                self.mydb.commit()
                return result
            except mysql.connector.Error as err:
                print(f"Error: {err}")
                return None
        else:
            print("No database specified.")
            return None

    def select(self, table_name, columns='*', condition=None, database_name=None):
        """
        Perform a SELECT query.
        :param table_name: Name of the table to select from.
        :param columns: Columns to select (default is '*').
        :param condition: Optional SQL condition for filtering results.
        :param database_name: Optional database name. Uses the connected database if not specified.
        :return: Result of the SELECT query.
        """
        condition_clause = f"WHERE {condition}" if condition else ""
        query = f"SELECT {columns} FROM {table_name} {condition_clause}"
        return self.execute(query, database_name=database_name)

    def insert(self, table_name, data, database_name=None):
        """
        Perform an INSERT query.
        :param table_name: Name of the table to insert into.
        :param data: Dictionary of column-value pairs to insert.
        :param database_name: Optional database name. Uses the connected database if not specified.
        """
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        values = tuple(data.values())
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        self.execute(query, values, database_name=database_name)

    def update(self, table_name, data, condition, database_name=None):
        """
        Perform an UPDATE query.
        :param table_name: Name of the table to update.
        :param data: Dictionary of column-value pairs to update.
        :param condition: SQL condition for filtering rows to update.
        :param database_name: Optional database name. Uses the connected database if not specified.
        """
        set_clause = ', '.join([f"{col} = %s" for col in data.keys()])
        values = tuple(data.values())
        query = f"UPDATE {table_name} SET {set_clause} WHERE {condition}"
        self.execute(query, values, database_name=database_name)

    def delete(self, table_name, condition, database_name=None):
        """
        Perform a DELETE query.
        :param table_name: Name of the table to delete from.
        :param condition: SQL condition for filtering rows to delete.
        :param database_name: Optional database name. Uses the connected database if not specified.
        """
        query = f"DELETE FROM {table_name} WHERE {condition}"
        self.execute(query, database_name=database_name)

    def create_table(self, table_name, schema, database_name=None):
        """
        Create a new table.
        :param table_name: Name of the new table.
        :param schema: Schema definition for the new table (e.g., 'id INT PRIMARY KEY, name VARCHAR(100)').
        :param database_name: Optional database name. Uses the connected database if not specified.
        """
        query = f"CREATE TABLE {table_name} ({schema})"
        self.execute(query, database_name=database_name)

    def drop_table(self, table_name, database_name=None):
        """
        Drop a table.
        :param table_name: Name of the table to drop.
        :param database_name: Optional database name. Uses the connected database if not specified.
        """
        query = f"DROP TABLE {table_name}"
        self.execute(query, database_name=database_name)

    def truncate_table(self, table_name, database_name=None):
        """
        Truncate a table (remove all rows).
        :param table_name: Name of the table to truncate.
        :param database_name: Optional database name. Uses the connected database if not specified.
        """
        query = f"TRUNCATE TABLE {table_name}"
        self.execute(query, database_name=database_name)

class Connect:
    def __init__(self , host , username , password , database=None):
        mydb = mysql.connector.connect(
            host=host ,
            user=username ,
            password=password ,
            database=database
        )
        self.get = Get(mydb , database)
        self.create = Create(mydb , database)
        self.delete = Delete(mydb , database)
        self.update = Update(mydb , database)
        self.backup = Backup(mydb , database)
        self.query = Query(mydb , database)

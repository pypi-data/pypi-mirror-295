# SQLSimplify Python Library

The SQLSimplify Python library provides a comprehensive and flexible interface for interacting with MySQL databases. It simplifies common database operations such as querying, creating, updating, deleting, backing up, and restoring databases and tables.

## Features

- Fetch and manage databases and tables
- Create and modify tables and columns
- Insert, update, and delete rows in tables
- Backup and restore databases and tables
- Execute raw SQL queries

## Installation

You can install the library using pip:

```bash
pip install SQLSimplify
```

## Usage
Importing the Library
```python
import SQLSimplify
```

## Connecting to MySQL
To use the library, create an instance of the SQLSimplify.
Connect class by providing the host, username, password, and optionally the database name.

```Python
db = SQLSimplify.Connect(host='localhost', username='root', password='yourpassword', database='yourdatabase') 
#database not required for initial connection
```

## Get Class
Fetch Databases

```Python
db.get.database()
```

## Fetch Tables in a Database
```Python
db.get.tables('yourdatabase')
```
## Create Class
### Create a New Table

```Python
db.create.table('new_table', 'id INT PRIMARY KEY, name VARCHAR(100), age INT')
```
### Add a Column to a Table

```Python
db.create.column('existing_table', 'new_column', 'VARCHAR(255)')
```
## Delete Class
### Delete a Table

```Python
db.delete.table('table_to_delete')
```
### Delete a Column from a Table

```Python
db.delete.column('table_name', 'column_to_delete')
```
### Delete Rows from a Table

```Python
db.delete.row('table_name', 'condition')
```
## Update Class
### Update Rows in a Table

```Python
db.update.row('table_name', {'column1': 'new_value', 'column2': 10}, 'id = 1')
```
### Modify a Column

```Python
db.update.column('table_name', 'column_name', 'VARCHAR(255)')
```
### Rename a Table

```Python
db.update.table_name('old_table_name', 'new_table_name')
```
## Backup Class
### Backup a Database

```Python
db.backup.backup_database('/path/to/backup.sql')
```
### Backup a Table

```Python
db.backup.backup_table('table_name', '/path/to/table_backup.sql')
```
### Restore a Database

```Python
db.backup.restore_database('/path/to/backup.sql')
```
### Restore a Table

```Python
db.backup.restore_table('table_name', '/path/to/table_backup.sql')
```
## Query Class
### Execute a Raw SQL Query

```Python
db.query.execute('SELECT * FROM table_name')
```
### Perform a SELECT Query

```Python
results = db.query.select('table_name', 'column1, column2', 'column1 = value')
print(results)
```
### Perform an INSERT Query

```Python
db.query.insert('table_name', {'column1': 'value1', 'column2': 'value2'})
```
### Perform an UPDATE Query

```Python
db.query.update('table_name', {'column1': 'new_value'}, 'condition')
```
### Perform a DELETE Query

```Python
db.query.delete('table_name', 'condition')
```
### Create a Table

```Python
db.query.create_table('new_table', 'id INT PRIMARY KEY, name VARCHAR(100)')
```
### Drop a Table

```Python
db.query.drop_table('table_name')
```
### Truncate a Table

```Python
db.query.truncate_table('table_name')
```

# PyWithMySQL

PyWithMySQL is a simple and easy-to-use Python library for working with MySQL databases. It provides methods for connecting to the database, performing CRUD operations, and handling MySQL queries efficiently.

## Installation

You can install the library using pip:

```bash
pip install pywithmysql
```
## Features
Easy connection setup with MySQL
Supports basic CRUD operations (Create, Read, Update, Delete)
Flexible and extensible methods
Error handling for database operations

## Usage
Here is a quick example of how to use the library:

```python
from pywithmysql.settings import SettingsTable
from pywithmysql.config import DataBaseConfig

# Define your database configuration
config = DataBaseConfig(
    host="localhost",
    port=3306,
    user="root",
    password="password",
    db_name="test_db"
)

# Initialize the settings table with the table name
table = SettingsTable(config, "users")

# Connect to the database
table.connect()

# Create a new entry in the table
table.create(names=["name", "age"], values=["'Alice'", "30"])

# Read all entries from the table
rows = table.read_all()
for row in rows:
    print(row)

# Update an entry
table.update_data(names=("age",), values=("31",), id=1)

# Delete an entry by id
table.delete_for_id(id=1)

# Disconnect from the database
table.disconnect()
```

# Creating a Table
To create a table, use the ```Table``` class along with the ```Column``` class to define columns. Here’s a code example:
```python
from pywithmysql.models import Table, Column
from pywithmysql.types import IntegerField, CharField
from pywithmysql.config import DataBaseConfig

# Database connection settings
config = DataBaseConfig(
    host="localhost",
    port=3306,
    user="user",
    password="password",
    db_name="db_name"
)

# Initialize Table
table = Table(
    "users",
    config,
    Column(name="username", CharField, max_length=45, nullable=False, unique=True),
    Column(name="age", IntegerField, default=18),
    Column(name="email", CharField, max_length=100, unique=True, nullable=False),
    Column(name="phone_number", CharField, unique=True)
    
)


# Create the table
table.create_table()
```
## Methods
```connect() ```
Establishes a connection to the MySQL database using the provided configuration.

```create(names: list, values: list)```
Inserts a new row into the table. You must provide column names and their corresponding values.

```read_all()```
Fetches all rows from the table.

```update_data(names: tuple, values: tuple, id: int)```
Updates specific fields for a row with the given id.

```delete_for_id(id: int)```
Deletes a row from the table based on the provided id.

```disconnect()```
Closes the connection to the MySQL database.

## License
This project is licensed under the MIT License.
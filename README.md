# Bookstore-database-populator
The generator automates the creation and filling of data for the bookstore database.
<p align="center">
      <img src="https://i.ibb.co/SQ11TKV/image.png" alt="Project Logo" width="764">
</p>
<p align="center">
   <img src="https://img.shields.io/badge/IDE-VS%20Code-2B7FB8" alt="Engine">
   <img src="https://img.shields.io/badge/Database-Oracle-FFA500" alt="Database">
   <img src="https://img.shields.io/badge/IDE Database-SQL Developer-708090" alt="Database">
</p>

# About

Generate and populate tables in an Oracle database with sample data. 
It includes functionalities to create various types of data, such as accounts, addresses, books, customers, orders, and reviews.

## Libraries
**-** **`pandas 2.2.1`**, **`cx_Oracle 8.3.0`**, **`faker 24.9.0`**

## Setup
### Step 1
Open a terminal or command prompt and run the following command.
  ```bash
  git clone https://github.com/SharkelDarya/bookstore-database-populator.git
  ```
### Step 2
Navigate to the directory, then run the command to install the dependencies.
  ```bash
  cd bookstore-database-populator
  pip install -r requirements.txt
  ```
### Step 3
Make sure you have the appropriate software installed and follow the instructions in the CRUD.txt file to create the database and tables.
### Step 4
File databaseconfig.json contains data for connecting to your database. Edit this file.
### Step 5
Run the main script.
  ```bash
  python main.py
  ```
Follow the on-screen instructions to choose the desired action:
Enter 0 to add 100 records to all tables.
Enter 1 to add 1,000 records to the REVIEW table.
Once the script completes execution, the database tables will be populated with the generated data.

## Project Structure
### **`connector_db.py`**
- File contains the ConnectorDB class, which serves as a connector to the Oracle database. 
It provides methods to establish a connection, execute SQL queries, insert data from CSV files into the database, and close the connection.

### **`csv_writer.py`**
- File contains the CSVWriter class, responsible for generating data and creating CSV files for each table.
It includes methods to generate different types of data, such as passwords, dates, ISBNs, and foreign keys

### **`main.py`**
- File provides a menu interface for the user to choose actions, and coordinates the generation and insertion of data into the database.

## Developers

- Darya Sharkel (https://github.com/SharkelDarya)


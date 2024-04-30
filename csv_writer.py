import pandas as pd
import random
from random import uniform
import string
import hashlib
from random import randint
import datetime
import warnings
import os
from faker import Faker
fake = Faker()

# Suppression of warnings
warnings.filterwarnings("ignore", category=FutureWarning)

class CSVWriter:
    logins = []
    def __init__(self, connector):
            self.connector = connector
    
    ################################################
    # These functions generate various data.
    # generate_and_hash_password: Generate a random password and hashes it using SHA-256.
    # generate_random_date: Generate a random date within a specified range and returns it in the format "DD-MMM-YYYY".
    # generate_ISBN13: Generates a random ISBN-13.
    # generate_foreign_keys: This function retrieves foreign key values from a specified column in a database table.
    #                        Returns a list of id.
    # create_csv_file: Create a CSV file from a DataFrame and saves it with the specified filename.
    # delete_files: Delete a list of specified files.
    ################################################

    def generate_and_hash_password(self):
        characters = string.ascii_letters + string.digits
        password = ''.join(random.choice(characters) for _ in range(8))
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        return hashed_password
    
    def generate_random_date(self, start_date, end_date):
        month_abbr = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']

        num_days = (end_date - start_date).days
        rand_days = random.randint(1, num_days)
        result_date = start_date + datetime.timedelta(days=rand_days)
    
        month_name = month_abbr[result_date.month - 1]
    
        return f"{result_date.day}-{month_name}-{result_date.year}"

    def generate_ISBN13(self):
        range_start = 10**(13-1)
        range_end = (10**13)-1
        return randint(range_start, range_end)
    
    def generate_foreign_keys(self, column, name_child):
        ids = self.connector.select_query(name_child, column)
        return ids

    def create_csv_file(self, filename, df):
        df.to_csv(f'data\{filename}.csv', index=False)

    def delete_files(self):
        files = ['ACCOUNTS.csv', 'ADDRESS.csv', 'AUTHOR.csv', 'BOOK_AUTHORS.csv', 'BOOK.csv', 'CART.csv', 'COUNTRY.csv',
                 'CUST_ADDRESS.csv', 'CUST_ORDER.csv', 'CUSTOMER.csv', 'ORDER_HISTORY.csv', 'ORDER_STATUS.csv', 'REVIEW.csv', 'SHIPPING_METHOD.csv']
        try:
            for file in files:
                os.remove(file)
            print('Deletion completed.')
        except:
            print('Cannot delete files.')
    
    ##########################################################################################
    #These functions generate data for all tables in database
    ##########################################################################################
    def create_data_ACCOUNTS(self):
        df = pd.DataFrame(columns=['LOGIN', 'PASSWORD'])

        for i in range(100):
            profile = fake.simple_profile()
            login = profile['username']
            password = self.generate_and_hash_password()
            df = df._append({'LOGIN': login, 
                             'PASSWORD': password}, ignore_index=True)
        
        self.create_csv_file('ACCOUNTS', df)
       
    def create_data_COUNTRY(self):
        countries = ['Czechy', 'Niemcy', 'Polska', 'Litwa', 'Slowacja']
        
        df = pd.DataFrame(data=countries, columns=['COUNTRY_NAME'])
        
        self.create_csv_file('COUNTRY', df)

    def create_data_ADDRESS(self):
        #Getting data
        foreign_ids = self.generate_foreign_keys('COUNTRY_ID', 'COUNTRY')
        df = pd.DataFrame(columns=['CITY', 'STREET_NAME', 'STREET_NUMBER', 'COUNTRY_COUNTRY_ID'])

        #Populate table
        for i in range(100):
            df = df._append({'CITY': fake.city(), 
                             'STREET_NAME': fake.street_name(),
                             'STREET_NUMBER': fake.building_number(), 
                             'COUNTRY_COUNTRY_ID': random.choice(foreign_ids)}, ignore_index=True)
            
        #create csv_file with filinhg data
        self.create_csv_file('ADDRESS', df)

    def create_data_AUTHOR(self):
        df = pd.DataFrame(columns=['AUTHOR_NAME'])
        #Populate table
        for i in range(100):
            df = df._append({'AUTHOR_NAME': fake.name()}, ignore_index=True)

        #save as csv file
        self.create_csv_file('AUTHOR', df)

    def create_data_BOOK(self):
        df = pd.DataFrame(columns=['TITLE', 'ISBN13', 'NUM_PAGES', 'PUBLICATION_DATE', 'COVER', 'DESCRIPTION', 'AMOUNT', 'PRICE'])
        #Populate table
        for i in range(100):
            df = df._append({'TITLE': fake.text(max_nb_chars=20), 
                             'ISBN13': self.generate_ISBN13(), 
                             'NUM_PAGES': randint(30, 500),
                             'PUBLICATION_DATE': self.generate_random_date(datetime.date(1990, 1, 1), datetime.date(2015, 11, 30)), 
                             'COVER': 'No cover',
                             'DESCRIPTION': fake.text(max_nb_chars=400), 
                             'AMOUNT': randint(0, 200), 
                             'PRICE': round(uniform(0, 100), 2)}, ignore_index=True)
        #Save as csv file    
        self.create_csv_file('BOOK', df)
    
    def create_data_BOOK_AUTHORS(self):
        book_ids = self.generate_foreign_keys('BOOK_ID', 'BOOK')
        author_ids = self.generate_foreign_keys('AUTHOR_ID', 'AUTHOR')
        used_combinations = set()

        df = pd.DataFrame(columns=['BOOK_BOOK_ID', 'AUTHOR_AUTHOR_ID'])
        for i in range(100):
            while True:
                book_id = random.choice(book_ids) 
                author_id = random.choice(author_ids)
                # Check if this combination has already been used
                if (book_id, author_id) not in used_combinations:
                    used_combinations.add((book_id, author_id))  # Add the combination to the set of used
                    df = df._append({'BOOK_BOOK_ID': book_id, 'AUTHOR_AUTHOR_ID': author_id}, ignore_index=True)
                    break
        
        self.create_csv_file('BOOK_AUTHORS', df)

    def create_data_CUST_ADDRESS(self):
        customer_ids = self.generate_foreign_keys('CUSTOMER_ID', 'CUSTOMER')
        address_ids =  self.generate_foreign_keys('ADDRESS_ID', 'ADDRESS')

        df = pd.DataFrame(columns=['CUSTOMER_CUSTOMER_ID', 'ADDRESS_ADDRESS_ID'])
        for i in range(100):
            customer_id = random.choice(customer_ids)
            address_id = random.choice(address_ids)
            df = df._append({'CUSTOMER_CUSTOMER_ID': customer_id, 
                             'ADDRESS_ADDRESS_ID': address_id}, ignore_index=True)
        
        self.create_csv_file('CUST_ADDRESS', df)

    def create_data_SHIPPING_METHOD(self):
        df = pd.DataFrame(columns=['METHOD_NAME', 'COST'])

        df = df.dropna(axis=1, how='all')
        methods = ['Courier', 'Mail', 'Same Day', 'Next Day', 'Parcel locker']
        for method in methods:
            df = df._append({'METHOD_NAME': method, 
                             'COST': round(uniform(3, 29), 2)}, ignore_index=True)

        self.create_csv_file('SHIPPING_METHOD', df)

    def create_data_REVIEW(self):
        book_ids = self.generate_foreign_keys('BOOK_ID', 'BOOK')

        df = pd.DataFrame(columns=['REVIEW_VALUE', 'BOOK_BOOK_ID', 'APPRASIAL'])
        for i in range(100):
            book_id = random.choice(book_ids)
            df = df._append({'REVIEW_VALUE': fake.text(max_nb_chars=100), 
                             'BOOK_BOOK_ID': book_id, 
                             'APPRASIAL': randint(1,6)}, ignore_index=True)

        self.create_csv_file('REVIEW', df)

    def create_data_CUSTOMER(self):
        account_ids = self.generate_foreign_keys('ACCOUNT_ID', 'ACCOUNTS')

        df = pd.DataFrame(columns=['FIRST_NAME', 'LAST_NAME', 'EMAIL', 'ACCOUNTS_ACCOUNT_ID'])
        for account_id in account_ids:
            first_name = fake.first_name()
            last_name = fake.last_name()
            email = f'{first_name.lower()}.{last_name.lower()}@gmail.com'
            df = df._append({'FIRST_NAME': first_name, 
                             'LAST_NAME': last_name, 
                             'EMAIL': email, 
                             'ACCOUNTS_ACCOUNT_ID': account_id}, ignore_index=True)

        self.create_csv_file('CUSTOMER', df)

    def create_data_CUST_ORDER(self):
        customer_ids = self.generate_foreign_keys('CUSTOMER_ID', 'CUSTOMER')
        method_ids = self.generate_foreign_keys('METHOD_ID', 'SHIPPING_METHOD')
        address_ids = self.generate_foreign_keys('ADDRESS_ID', 'ADDRESS')

        df = pd.DataFrame(columns=['ORDER_DATE', 'CUSTOMER_CUSTOMER_ID', 'SHIPPING_METHOD_METHOD_ID', 'ADDRESS_ADDRESS_ID'])
        for i in range(100):
            df = df._append({'ORDER_DATE': self.generate_random_date(datetime.date(2020, 1, 1), datetime.date(2022, 11, 30)),
                             'CUSTOMER_CUSTOMER_ID': random.choice(customer_ids),
                             'SHIPPING_METHOD_METHOD_ID': random.choice(method_ids), 
                             'ADDRESS_ADDRESS_ID': random.choice(address_ids) }, ignore_index=True)

        self.create_csv_file('CUST_ORDER', df)

    def create_data_ORDER_STATUS(self): 
        order_status = ['In processing', 'Delivered', 'Canceled', 'In review']
        df = pd.DataFrame(data=order_status, columns=['STATUS_VALUE'])

        self.create_csv_file('ORDER_STATUS', df)

    def create_data_ORDER_HISTORY(self): 
        order_ids = self.generate_foreign_keys('ORDER_ID', 'CUST_ORDER')
        status_ids = self.generate_foreign_keys('STATUS_ID', 'ORDER_STATUS')

        df = pd.DataFrame(columns=['STATUS_DATE', 'CUST_ORDER_ORDER_ID', 'ORDER_STATUS_STATUS_ID'])
        for i in range(100):
            df = df._append({'STATUS_DATE': self.generate_random_date(datetime.date(2022, 1, 1), datetime.date(2024, 11, 30)), 
                             'CUST_ORDER_ORDER_ID': random.choice(order_ids), 
                             'ORDER_STATUS_STATUS_ID': random.choice(status_ids)}, ignore_index=True)
        
        self.create_csv_file('ORDER_HISTORY', df)

    def create_data_CART(self): 
        customer_ids = self.generate_foreign_keys('CUSTOMER_ID', 'CUSTOMER')
        book_ids = self.generate_foreign_keys('BOOK_ID', 'BOOK')
        order_ids = self.generate_foreign_keys('ORDER_ID', 'CUST_ORDER')

        df = pd.DataFrame(columns=['QUANTITY', 'CUSTOMER_CUSTOMER_ID', 'BOOK_BOOK_ID', 'CUST_ORDER_ORDER_ID'])
        for i in range(100):
            df = df._append({'QUANTITY': randint(1, 15), 
                             'CUSTOMER_CUSTOMER_ID': random.choice(customer_ids), 
                             'BOOK_BOOK_ID': random.choice(book_ids), 
                             'CUST_ORDER_ORDER_ID': random.choice(order_ids)}, ignore_index=True)
        
        self.create_csv_file('CART', df)

    def generate_data_thousand_records(self):
        book_ids = self.generate_foreign_keys('BOOK_ID', 'BOOK')

        df = pd.DataFrame(columns=['REVIEW_VALUE', 'BOOK_BOOK_ID', 'APPRASIAL'])
        for i in range(1000):
            df = df._append({'REVIEW_VALUE': fake.text(max_nb_chars=100), 
                             'BOOK_BOOK_ID': random.choice(book_ids), 
                             'APPRASIAL': randint(1, 6)}, ignore_index=True)

        self.create_csv_file('REVIEW_THOUSAND', df)

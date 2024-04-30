import connector_db 
import csv_writer

connector = connector_db.ConnectorDB()
writer = csv_writer.CSVWriter(connector)

#####################################
#   MENU
#####################################

howMany = int(input(" 0 - Add 100 records to all tables \n" " 1 - Add 1,000 records to the REVIEW table\n"))

if howMany == 0:
    writer.delete_files()

    writer.create_data_ACCOUNTS()
    connector.insert_csv_to_database('ACCOUNTS', 'ACCOUNTS.csv')
    print('ACCOUNTS done.')

    writer.create_data_COUNTRY()
    connector.insert_csv_to_database('COUNTRY', 'COUNTRY.csv')
    print('COUNTRY done.')

    writer.create_data_ADDRESS()
    connector.insert_csv_to_database('ADDRESS', 'ADDRESS.csv')
    print('ADDRESS done.')

    writer.create_data_AUTHOR()
    connector.insert_csv_to_database('AUTHOR', 'AUTHOR.csv')
    print('AUTHOR done.')

    writer.create_data_BOOK()
    connector.insert_csv_to_database('BOOK', 'BOOK.csv')
    print('BOOK done.')

    writer.create_data_BOOK_AUTHORS()
    connector.insert_csv_to_database('BOOK_AUTHORS', 'BOOK_AUTHORS.csv')
    print('BOOK_AUTHORS done.')

    writer.create_data_CUSTOMER()
    connector.insert_csv_to_database('CUSTOMER', 'CUSTOMER.csv')
    print('CUSTOMER done.')

    writer.create_data_CUST_ADDRESS()
    connector.insert_csv_to_database('CUST_ADDRESS', 'CUST_ADDRESS.csv')
    print('CUST_ADDRESS done.')

    writer.create_data_SHIPPING_METHOD()
    connector.insert_csv_to_database('SHIPPING_METHOD', 'SHIPPING_METHOD.csv')
    print('SHIPPING_METHOD done.')

    writer.create_data_REVIEW()
    connector.insert_csv_to_database('REVIEW', 'REVIEW.csv')
    print('REVIEW done.')

    writer.create_data_CUST_ORDER()
    connector.insert_csv_to_database('CUST_ORDER', 'CUST_ORDER.csv')
    print('CUST_ORDER done.')

    writer.create_data_ORDER_STATUS()
    connector.insert_csv_to_database('ORDER_STATUS', 'ORDER_STATUS.csv')
    print('ORDER_STATUS done.')

    writer.create_data_ORDER_HISTORY()
    connector.insert_csv_to_database('ORDER_HISTORY', 'ORDER_HISTORY.csv')
    print('ORDER_HISTORY done.')

    writer.create_data_CART() 
    connector.insert_csv_to_database('CART', 'CART.csv')
    print('CART done.')

    print('All done.')
elif howMany == 1:
    writer.generate_data_thousand_records()
    connector.insert_csv_to_database('REVIEW', 'REVIEW_THOUSAND.csv')
    print('Done.')

else:
    print("There is no such option to choose")

connector.close_connection()
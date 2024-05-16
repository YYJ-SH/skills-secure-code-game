'''
Please note:

The first file that you should run in this level is tests.py for database creation, with all tests passing.
Remember that running the hack.py will change the state of the database, causing some tests inside tests.py
to fail.

If you like to return to the initial state of the database, please delete the database (level-4.db) and run 
the tests.py again to recreate it.
'''

import unittest
import code as c

class TestDatabase(unittest.TestCase): 
  
    # tests for correct retrieval of stock info given a symbol
    def test_1(self):
        op = c.DB_CRUD_ops()
        expected_output = "[METHOD EXECUTED] get_stock_info\n[QUERY] SELECT * FROM stocks WHERE symbol = 'MSFT'\n[RESULT] ('2022-01-06', 'MSFT', 300.0)"
        actual_output = op.get_stock_info('MSFT')
        self.assertEqual(actual_output, expected_output)

    # tests for correct defense against SQLi in the case where a user passes more than one query or restricted characters
    def test_2(self):
        op = c.DB_CRUD_ops()
        expected_output = "[METHOD EXECUTED] get_stock_info\n[QUERY] SELECT * FROM stocks WHERE symbol = 'MSFT'; UPDATE stocks SET price = '400' WHERE symbol = 'MSFT'--'\nCONFIRM THAT THE ABOVE QUERY IS NOT MALICIOUS TO EXECUTE"
        actual_output = op.get_stock_info("MSFT'; UPDATE stocks SET price = '400' WHERE symbol = 'MSFT'--")
        self.assertEqual(actual_output, expected_output)

    # tests for correct retrieval of stock price
    def test_3(self):
        op = c.DB_CRUD_ops()
       
        expected_output = "[METHOD EXECUTED] get_stock_price\n[QUERY] SELECT price FROM stocks WHERE symbol = 'MSFT'\n[RESULT] (300.0,)\n"
        actual_output = op.get_stock_price("MSFT")
        self.assertEqual(actual_output, expected_output)

    # tests for correct update of stock price given symbol and updated price
    def test_4(self):
        op = c.DB_CRUD_ops()
        expected_output = "[METHOD EXECUTED] update_stock_price\n[QUERY] UPDATE stocks SET price = '300' WHERE symbol = 'MSFT'\n"
        actual_output = op.update_stock_price('MSFT', 300.0)
        self.assertEqual(actual_output, expected_output)
    
    # tests for correct execution of multiple queries
    def test_5(self):
        op = c.DB_CRUD_ops()
        query_1 = "[METHOD EXECUTED] exec_multi_query\n[QUERY]SELECT price FROM stocks WHERE symbol = 'MSFT'\n[RESULT] (300.0,) "
        query_2 = "[QUERY] SELECT * FROM stocks WHERE symbol = 'MSFT'\n[RESULT] ('2022-01-06', 'MSFT', 300.0) "
        expected_output = query_1 + query_2
        actual_output = op.exec_multi_query("SELECT price FROM stocks WHERE symbol = 'MSFT'; SELECT * FROM stocks WHERE symbol = 'MSFT'")
        self.assertEqual(actual_output, expected_output)
    
    # tests for correct execution of user script
    def test_6(self):
        op = c.DB_CRUD_ops()
        expected_output = "[METHOD EXECUTED] exec_user_script\n[QUERY] SELECT price FROM stocks WHERE symbol = 'MSFT'\n[RESULT] (300.0,)"
        actual_output = op.exec_user_script("SELECT price FROM stocks WHERE symbol = 'MSFT'")
        self.assertEqual(actual_output, expected_output) 
    # def test_sql_injection(self):
    #     op = c.DB_CRUD_ops()
    #     print("test_8 is activating_sql injection trying...")
    #     # SQL 인젝션 공격을 시도하는 입력 값
    #     sql_injection_input = "MSFT'; UPDATE stocks SET price = 500 WHERE symbol = 'MSFT'--"
    #     actual_output = op.get_stock_price(sql_injection_input)

    #     # SQL 인젝션 공격이 성공했는지 확인
    #     if "UPDATE" in actual_output and "300" not in actual_output:
    #         print("SQL 인젝션 공격 성공: MSFT 심볼의 가격이 변경되었습니다.")
    #     else:
    #         print("SQL 인젝션 공격 실패")


    #     # 데이터베이스 상태 확인
    #     check_output = op.get_stock_info("MSFT")
    #     print(check_output)
    # def test_sql_injection_get_stock_info_update(self):
    #     op = c.DB_CRUD_ops()
    #     print("test_9")
        
    #     # Test case: MSFT'; UPDATE stocks SET price = 400.0 WHERE symbol = 'MSFT'--
    #     malicious_input = "MSFT'; UPDATE stocks SET price = 400.0 WHERE symbol = 'MSFT'--"
    #     expected_output = "[METHOD EXECUTED] get_stock_info\n" + \
    #                     "[QUERY] SELECT * FROM stocks WHERE symbol = 'MSFT'; UPDATE stocks SET price = 400.0 WHERE symbol = 'MSFT'--'\n"
    #     actual_output = op.get_stock_info(malicious_input)
    #     self.assertIn(expected_output, actual_output)
        
    #     # Check if the price has been updated
    #     expected_price = 400.0
    #     actual_price = op.get_stock_price('MSFT')
    #     self.assertIn(str(expected_price), actual_price)
    def test_10(self):
        op = c.DB_CRUD_ops()
        expected_output = "[METHOD EXECUTED] get_stock_info\n[QUERY] SELECT * FROM stocks WHERE symbol = 'MSFT'; UPDATE stocks SET price = '400' WHERE symbol = 'MSFT'--'\nCONFIRM THAT THE ABOVE QUERY IS NOT MALICIOUS TO EXECUTE"
        actual_output = op.get_stock_info("MSFT'; UPDATE stocks SET price = '400' WHERE symbol = 'MSFT'--")
        # self.assertEqual(actual_output, expected_output)
        print(actual_output,":얘가첫번째")
        expected_price = 400.0
        actual_price = op.get_stock_price('MSFT')
        self.assertIn(str(expected_price), actual_price)
    def test_sql_injection_get_stock_info_bypasses(self):
        op = c.DB_CRUD_ops()
        
        # Test case 1: Mixed case bypass
        malicious_input_1 = "MsFt' Or 1=1--"
        expected_output_1 = "[METHOD EXECUTED] get_stock_info\n" + \
                            "[QUERY] SELECT * FROM stocks WHERE symbol = 'MsFt' Or 1=1--'\n" + \
                            "CONFIRM THAT THE ABOVE QUERY IS NOT MALICIOUS TO EXECUTE"
        actual_output_1 = op.get_stock_info(malicious_input_1)
        self.assertEqual(actual_output_1, expected_output_1)
        
        # Test case 2: URL encoding bypass
        malicious_input_2 = "MS%46T' OR 1=1--"
        expected_output_2 = "[METHOD EXECUTED] get_stock_info\n" + \
                            "[QUERY] SELECT * FROM stocks WHERE symbol = 'MS%46T' OR 1=1--'\n" + \
                            "CONFIRM THAT THE ABOVE QUERY IS NOT MALICIOUS TO EXECUTE"
        actual_output_2 = op.get_stock_info(malicious_input_2)
        self.assertEqual(actual_output_2, expected_output_2)
        
        # Test case 3: Inline comment bypass
        malicious_input_3 = "MSFT'/**/OR/**/1=1--"
        expected_output_3 = "[METHOD EXECUTED] get_stock_info\n" + \
                            "[QUERY] SELECT * FROM stocks WHERE symbol = 'MSFT'/**/OR/**/1=1--'\n" + \
                            "CONFIRM THAT THE ABOVE QUERY IS NOT MALICIOUS TO EXECUTE"
        actual_output_3 = op.get_stock_info(malicious_input_3)
        self.assertEqual(actual_output_3, expected_output_3)
        
        # Test case 4: Semicolon bypass (Using WAITFOR DELAY as an example, which is specific to SQL Server)
        malicious_input_4 = "MSFT';WAITFOR DELAY '0:0:5'--"
        expected_output_4 = "[METHOD EXECUTED] get_stock_info\n" + \
                            "[QUERY] SELECT * FROM stocks WHERE symbol = 'MSFT';WAITFOR DELAY '0:0:5'--'\n" + \
                            "CONFIRM THAT THE ABOVE QUERY IS NOT MALICIOUS TO EXECUTE"
        actual_output_4 = op.get_stock_info(malicious_input_4)
        self.assertEqual(actual_output_4, expected_output_4)
        
        # Test case 5: Parentheses bypass
        malicious_input_5 = "MSFT' AND (1=1 OR 1=1)--"
        expected_output_5 = "[METHOD EXECUTED] get_stock_info\n" + \
                            "[QUERY] SELECT * FROM stocks WHERE symbol = 'MSFT' AND (1=1 OR 1=1)--'\n" + \
                            "CONFIRM THAT THE ABOVE QUERY IS NOT MALICIOUS TO EXECUTE"
        actual_output_5 = op.get_stock_info(malicious_input_5)
        self.assertEqual(actual_output_5, expected_output_5)
        
if __name__ == '__main__':    
    unittest.main()
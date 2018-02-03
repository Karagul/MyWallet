import unittest
# from wallet_app import *
from sandbox import *


class WalletUnitTest(unittest.TestCase):

    def test_spend(self):
        transaction = Transaction('10', 'cash(default)','test')
        self.assertEqual(wallet.spend(wallet.account_list['cash(default)'], transaction.transaction_value), '-90.00',"not equal")


if __name__ == '__main__':
    unittest.main()


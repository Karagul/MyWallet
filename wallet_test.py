import unittest
# from wallet_app import *
from sandbox import *


class WalletUnitTest(unittest.TestCase):

    def test_spend(self):
        transaction = Transaction('10', 'test','test')
        account = Account('test', '100')
        self.assertEqual(wallet.spend(account.account_value, transaction.transaction_value), '90.00', "not equal")


if __name__ == '__main__':
    unittest.main()


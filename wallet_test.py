import unittest
from wallet_app import *



class WalletUnitTest(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        """Set up for class"""
        print("setUpClass")
        print("==========")

    @classmethod
    def tearDownClass(cls):
        """Tear down for class"""
        print("==========")
        print("tearDownClass")

    def setUp(self):
        """Set up for test"""
        print("Set up for [" + self.shortDescription() + "]")

    def tearDown(self):
        """Tear down for test"""
        print("Tear down for [" + self.shortDescription() + "]")
        print("")

    def test_spend(self):
        """test of spend method"""
        transaction = Transaction('10', 'test','test')
        account = Account('test', '100')
        self.assertEqual(wallet.spend(account.account_value, transaction.transaction_value), '90.00', "not equal")


if __name__ == '__main__':
    unittest.main()


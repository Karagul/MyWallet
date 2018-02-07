import pytest
from .wallet_app import *


def setup_module(module):
    #init_something()
    pass

def teardown_module(module):
    #teardown_something()
    pass


def test_spend():
    transaction = Transaction('10', 'test', 'test')
    account = Account('test', '100')
    assert wallet.spend(account.account_value, transaction.transaction_value) == '90.00'

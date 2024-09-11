from .bill import Bill
from .company import Company
from .product import Product

class Ready2OrderAPI:
    def __init__(self, account_token):
        self.bill = Bill(account_token)
        self.company = Company(account_token)
        self.product = Product(account_token)
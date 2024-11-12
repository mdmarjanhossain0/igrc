import random

from account.models import (
    Account,
)

def mobile_check(mobile):
    return Account.objects.filter(mobile=mobile).exists()


def generate_otp():
    otp = f"{random.randint(1000, 9999)}"
    return otp
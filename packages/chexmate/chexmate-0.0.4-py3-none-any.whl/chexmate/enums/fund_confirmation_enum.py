from enum import Enum


class FundConfirmation(Enum):

    SUFFICIENT_FUNDS        = 0
    INSUFFICIENT_FUNDS      = 1
    NON_PARTICIPATING_BANK  = 2
    ACCOUNT_CLOSED          = 3
    INVALID_ACCOUNT_NUMBER  = 4
    INVALID_CHECK_NUMBER    = 5
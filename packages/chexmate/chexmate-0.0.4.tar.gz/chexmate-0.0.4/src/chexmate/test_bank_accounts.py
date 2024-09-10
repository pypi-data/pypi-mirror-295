from chexmate.enums.risk_enum import Risk
from chexmate.enums.fund_confirmation_enum import FundConfirmation
from chexmate.enums.routing_number_enum import RoutingNumber

# NOTE: The keys are the account numbers


account_data = {
    1111000001: {
        "routing_number": RoutingNumber.TEST_ROUTING_NUMBER,
        "risk": Risk.RISKY,
        "fund_confirmation": FundConfirmation.INSUFFICIENT_FUNDS,
        "description": "Negative information was found in the account’s history"
    },
    1111000002: {
        "routing_number": RoutingNumber.TEST_ROUTING_NUMBER,
        "risk": Risk.FAIL,
        "fund_confirmation": FundConfirmation.NON_PARTICIPATING_BANK,
        "description": "Routing number is not assigned to a financial institution"
    },
    1111000003: {
        "routing_number": RoutingNumber.TEST_ROUTING_NUMBER,
        "risk":  Risk.RISKY,
        "fund_confirmation": FundConfirmation.ACCOUNT_CLOSED,
        "description": "Account found in your API user’s Private Bad Checks list"
    },
    1111000004: {
        "routing_number": RoutingNumber.TEST_ROUTING_NUMBER,
        "risk": Risk.FAIL,
        "fund_confirmation": FundConfirmation.NON_PARTICIPATING_BANK,
        "description": "Invalid/Unassigned routing number"
    },
    1111000005: {
        "routing_number": RoutingNumber.TEST_ROUTING_NUMBER,
        "risk": Risk.FAIL,
        "fund_confirmation": FundConfirmation.INVALID_ACCOUNT_NUMBER,
        "description": "Invalid account number"
    },
    1111000006: {
        "routing_number": RoutingNumber.TEST_ROUTING_NUMBER,
        "risk": Risk.RISKY,
        "fund_confirmation": None,
        "description": "Invalid check number"
    },
    1111000007: {
        "routing_number": RoutingNumber.TEST_ROUTING_NUMBER,
        "risk": Risk.FAIL,
        "fund_confirmation": None,
        "description": "Invalid check amount"
    },
    1111000008: {
        "routing_number": RoutingNumber.TEST_ROUTING_NUMBER,
        "risk": Risk.PASS,
        "fund_confirmation": None,
        "description": "No positive or negative information available for the account information"
    },
    1111000009: {
        "routing_number": RoutingNumber.TEST_ROUTING_NUMBER,
        "risk": Risk.FAIL,
        "fund_confirmation": FundConfirmation.NON_PARTICIPATING_BANK,
        "description": "Routing number can only be valid for a US Government institution"
    },
    1111000010: {
        "routing_number": RoutingNumber.TEST_ROUTING_NUMBER,
        "risk": Risk.FAIL,
        "fund_confirmation": FundConfirmation.SUFFICIENT_FUNDS,
        "description": "Routing number is participating bank, but account number not located"
    },
    1111000011: {
        "routing_number": RoutingNumber.TEST_ROUTING_NUMBER,
        "risk": Risk.RISKY,
        "fund_confirmation": FundConfirmation.INSUFFICIENT_FUNDS,
        "description": "Account should be declined based on the risk factor reported"
    },
    1111000012: {
        "routing_number": RoutingNumber.TEST_ROUTING_NUMBER,
        "risk": Risk.FAIL,
        "fund_confirmation": FundConfirmation.INSUFFICIENT_FUNDS,
        "description": "Item (Check Number) should be declined based on the risk factor reported"
    },
    1111000013: {
        "routing_number": RoutingNumber.TEST_ROUTING_NUMBER,
        "risk": Risk.RISKY,
        "fund_confirmation": FundConfirmation.INSUFFICIENT_FUNDS,
        "description": "Current negative data exists on the account. Ex: NSF or recent returns"
    },
    1111000014: {
        "routing_number": RoutingNumber.TEST_ROUTING_NUMBER,
        "risk": Risk.FAIL,
        "fund_confirmation": FundConfirmation.INSUFFICIENT_FUNDS,
        "description": "Non-Demand Deposit Account (Post No Debits)"
    },
    1111000015: {
        "routing_number": RoutingNumber.TEST_ROUTING_NUMBER,
        "risk": Risk.RISKY,
        "fund_confirmation": FundConfirmation.INSUFFICIENT_FUNDS,
        "description": "Recent negative data exists on the account. Ex: NSF or recent returns"
    },
    1111000016: {
        "routing_number": RoutingNumber.TEST_ROUTING_NUMBER,
        "risk": Risk.PASS,
        "fund_confirmation": FundConfirmation.SUFFICIENT_FUNDS,
        "description": "Account Verified – Open and valid checking or savings account"
    },
    1111000017: {
        "routing_number": RoutingNumber.TEST_ROUTING_NUMBER,
        "risk": Risk.FAIL,
        "fund_confirmation": FundConfirmation.NON_PARTICIPATING_BANK,
        "description": "AMEX – The account is an American Express Travelers Cheque account"
    },
    1111000018: {
        "routing_number": RoutingNumber.TEST_ROUTING_NUMBER,
        "risk": Risk.PASS,
        "fund_confirmation": FundConfirmation.SUFFICIENT_FUNDS,
        "description": "Non-Participant Provider – Account reported as having positive data"
    },
    1111000019: {
        "routing_number": RoutingNumber.TEST_ROUTING_NUMBER,
        "risk": Risk.FAIL,
        "fund_confirmation": FundConfirmation.NON_PARTICIPATING_BANK,
        "description": "Savings Account Verified – Open and valid savings account"
    },
    1111000020: {
        "routing_number": RoutingNumber.TEST_ROUTING_NUMBER,
        "risk": Risk.PASS,
        "fund_confirmation": FundConfirmation.SUFFICIENT_FUNDS,
        "description": "Checking or savings account was found to have positive historical data"
    },
    1111000021: {
        "routing_number": RoutingNumber.TEST_ROUTING_NUMBER,
        "risk": Risk.FAIL,
        "fund_confirmation": FundConfirmation.NON_PARTICIPATING_BANK,
        "description": "Savings account was found to have positive historical data"
    },
    1111000022: {
        "routing_number": RoutingNumber.TEST_ROUTING_NUMBER,
        "risk": Risk.PASS,
        "fund_confirmation": FundConfirmation.SUFFICIENT_FUNDS,
        "description": "Account reported as having positive historical data"
    }
}
from enum import Enum

class OperationType(Enum):
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdraw"
    TRANSFER_IN = "transfer_in"
    TRANSFER_OUT = "transfer_out"
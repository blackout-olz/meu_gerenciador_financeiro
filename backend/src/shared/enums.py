from enum import StrEnum

class TransactionType(StrEnum):
    """
    Enumeração dos tipos de transação financeira suportados no sistema.

    Herda de StrEnum (Python 3.11+) para garantir conversão automática em string,
    facilitando a serialização JSON no Pydantic e FastAPI sem necessidade de cast manual.
    """
    INCOME = "INCOME"
    EXPENSE = "EXPENSE"
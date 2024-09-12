from decimal import Decimal, getcontext

getcontext().prec = 10


class KRRIMath:
    @staticmethod
    def divide_precision(a: float, b: float) -> int:
        return int(Decimal(a) / Decimal(b))

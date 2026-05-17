import bisect

class ProgressiveDuty(IDutyCalculator):
    # Пороги сум (обов'язково відсортовані за зростанням)
    THRESHOLDS = [10000, 50000, 100000, 500000, 1000000]
    # Відповідні ставки для кожного порогу + ставка за замовчуванням (0.55) в кінці
    RATES = [0.10, 0.12, 0.15, 0.20, 0.25, 0.55]

    def calculate(self, app: Application) -> float:
        amt = app.invoice_amount
        
        # bisect_left повертає індекс діапазону, в який потрапляє сума.
        # Наприклад: для 5000 індекс буде 0, для 10000 індекс 0, для 10001 індекс 1.
        index = bisect.bisect_left(self.THRESHOLDS, amt)
        
        return amt * self.RATES[index]
    

    class ProgressiveDuty(IDutyCalculator):
    # Таблиця тарифів у форматі (верхня_межа, ставка)
    TIERS = [
        (10000, 0.10),
        (50000, 0.12),
        (100000, 0.15),
        (500000, 0.20),
        (1000000, 0.25),
        (float('inf'), 0.55)  # float('inf') означає нескінченність (для всього, що більше 1 000 000)
    ]

    def calculate(self, app: Application) -> float:
        amt = app.invoice_amount
        
        # Функція next() поверне першу ставку, для якої сума менша або дорівнює межі
        rate = next(r for limit, r in self.TIERS if amt <= limit)
        
        return amt * rate
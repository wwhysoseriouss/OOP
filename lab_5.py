import json
import csv
import random
from abc import ABC, abstractmethod
from typing import List, Dict, Any


class Application:
    """Клас, що описує заявку на митний контроль."""
    def __init__(self, app_id: str, invoice_amount: float, auto: str, driver: str, category: str, urgency_days: int):
        self.app_id = app_id
        self.invoice_amount = invoice_amount
        self.auto = auto
        self.driver = driver
        self.category = category
        self.urgency_days = urgency_days

    def calculate_priority(self) -> float:
        """Алгоритм обчислення пріоритету (менше значення = вищий пріоритет)."""
        # Важливість категорій: ліки і гуманітарка - найвищі (1), продукти (2), промислові (3)
        category_weights = {"гуманітарна допомога": 1, "ліки": 1, "продукти": 2, "промислові товари": 3}
        weight = category_weights.get(self.category.lower(), 4)
        # Формула: вага категорії + терміновість (чим менше днів, тим вищий пріоритет)
        return weight + (self.urgency_days * 0.1)

    def to_dict(self) -> dict:
        return vars(self)

    @classmethod
    def from_dict(cls, data: dict):
        return cls(data['app_id'], float(data['invoice_amount']), data['auto'], 
                   data['driver'], data['category'], int(data['urgency_days']))

    def __str__(self):
        return f"[{self.app_id}] {self.category.upper()} | Сума: {self.invoice_amount} | Авто: {self.auto}"



class IDataStorage(ABC):
    """Інтерфейс для збереження та зчитування даних."""
    @abstractmethod
    def save(self, data: List[Application], filename: str): pass

    @abstractmethod
    def load(self, filename: str) -> List[Application]: pass


class IDutyCalculator(ABC):
    """Інтерфейс для розрахунку мита (Патерн Strategy)."""
    @abstractmethod
    def calculate(self, app: Application) -> float: pass


class IProcessingAlgorithm(ABC):
    """Інтерфейс для алгоритмів обробки черг (Патерн Strategy)."""
    @abstractmethod
    def process(self, terminals: List['Terminal'], system: 'CustomsSystem'): pass



class ZeroDuty(IDutyCalculator):
    def calculate(self, app: Application) -> float:
        return 0.0

class PercentageDuty(IDutyCalculator):
    def __init__(self, percentage: float):
        self.percentage = percentage

    def calculate(self, app: Application) -> float:
        return app.invoice_amount * (self.percentage / 100)

class ProgressiveDuty(IDutyCalculator):
    def calculate(self, app: Application) -> float:
        amt = app.invoice_amount
        if amt <= 10000: return amt * 0.10
        elif amt <= 50000: return amt * 0.12
        elif amt <= 100000: return amt * 0.15
        elif amt <= 500000: return amt * 0.20
        elif amt <= 1000000: return amt * 0.25
        else: return amt * 0.55



class QueueInterface(ABC):
    @abstractmethod
    def push(self, app: Application): pass
    
    @abstractmethod
    def pop(self) -> Application: pass
    
    @abstractmethod
    def is_empty(self) -> bool: pass

class FifoQueue(QueueInterface):
    """Черга за порядком надходження (FIFO)."""
    def __init__(self):
        self.items = []

    def push(self, app: Application):
        self.items.append(app)

    def pop(self) -> Application:
        return self.items.pop(0) if self.items else None

    def is_empty(self) -> bool:
        return len(self.items) == 0

class PriorityQueue(QueueInterface):
    """Черга з пріоритетом."""
    def __init__(self):
        self.items = []

    def push(self, app: Application):
        self.items.append(app)
        # Сортуємо при кожному додаванні (найменше значення пріоритету - перше)
        self.items.sort(key=lambda x: x.calculate_priority())

    def pop(self) -> Application:
        return self.items.pop(0) if self.items else None

    def is_empty(self) -> bool:
        return len(self.items) == 0


class Terminal:
    """Митний термінал (Агрегує в собі чергу)."""
    def __init__(self, terminal_id: str, queue_type: QueueInterface):
        self.terminal_id = terminal_id
        self.queue = queue_type



class AlgorithmOne(IProcessingAlgorithm):
    """Перший: за одну ітерацію з кожної черги береться одна (перша) заявка."""
    def process(self, terminals: List[Terminal], system: 'CustomsSystem'):
        print("\n--- Виконання Алгоритму 1 (По одній заявці з терміналу) ---")
        for terminal in terminals:
            if not terminal.queue.is_empty():
                app = terminal.queue.pop()
                system.process_application(app)

class AlgorithmTwo(IProcessingAlgorithm):
    """Другий: опрацьовуються всі заявки заданої категорії."""
    def __init__(self, target_category: str):
        self.target_category = target_category

    def process(self, terminals: List[Terminal], system: 'CustomsSystem'):
        print(f"\n--- Виконання Алгоритму 2 (Категорія: {self.target_category}) ---")
        for terminal in terminals:
            # Збираємо ті, що не підходять, щоб повернути їх назад
            retained = []
            while not terminal.queue.is_empty():
                app = terminal.queue.pop()
                if app.category.lower() == self.target_category.lower():
                    system.process_application(app)
                else:
                    retained.append(app)
            # Повертаємо невідповідні заявки до черги
            for app in retained:
                terminal.queue.push(app)

class AlgorithmThree(IProcessingAlgorithm):
    """Третій: по одній заявці, випадково: пропустити або на доопрацювання."""
    def process(self, terminals: List[Terminal], system: 'CustomsSystem'):
        print("\n--- Виконання Алгоритму 3 (Випадкове доопрацювання) ---")
        for terminal in terminals:
            if not terminal.queue.is_empty():
                app = terminal.queue.pop()
                if random.choice([True, False]): # 50/50 шанс
                    print(f"Заявка {app.app_id} пройшла перевірку.")
                    system.process_application(app)
                else:
                    print(f"Заявка {app.app_id} відправлена на доопрацювання! (Повертається в систему)")
                    system.add_application(app)



class JsonStorage(IDataStorage):
    def save(self, data: List[Application], filename: str):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump([app.to_dict() for app in data], f, ensure_ascii=False, indent=4)
        print(f"Дані збережено у {filename}")

    def load(self, filename: str) -> List[Application]:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"Дані завантажено з {filename}")
        return [Application.from_dict(item) for item in data]

class CsvStorage(IDataStorage):
    def save(self, data: List[Application], filename: str):
        if not data: return
        with open(filename, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=data[0].to_dict().keys())
            writer.writeheader()
            writer.writerows([app.to_dict() for app in data])
        print(f"Дані збережено у {filename}")

    def load(self, filename: str) -> List[Application]:
        apps = []
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                apps.append(Application.from_dict(row))
        print(f"Дані завантажено з {filename}")
        return apps



class CustomsSystem:
    def __init__(self, terminals: List[Terminal]):
        self.terminals = terminals
        self.total_duty_collected = 0.0
        
        # Налаштування митної політики для категорій
        self.duty_policies = {
            "гуманітарна допомога": ZeroDuty(),
            "ліки": PercentageDuty(5.0), # 5% пільгове
            "продукти": ProgressiveDuty(),
            "промислові товари": ProgressiveDuty()
        }

    def add_application(self, app: Application):
        """Рівномірний розподіл заявок по терміналах."""
        # Знаходимо термінал з найменшою кількістю заявок у черзі
        target_terminal = min(self.terminals, key=lambda t: len(t.queue.items))
        target_terminal.queue.push(app)

    def process_application(self, app: Application):
        """Нарахування мита та облік."""
        calculator = self.duty_policies.get(app.category.lower(), ProgressiveDuty())
        duty = calculator.calculate(app)
        self.total_duty_collected += duty
        print(f"Опрацьовано: {app} | Нараховано мито: {duty:.2f} грн")

    def run_algorithm(self, algorithm: IProcessingAlgorithm):
        algorithm.process(self.terminals, self)

    def display_status(self):
        print(f"\n[СТАТУС СИСТЕМИ] Загальна сума зібраного мита: {self.total_duty_collected:.2f} грн")
        for t in self.terminals:
            print(f"Термінал {t.terminal_id} | Заявок у черзі: {len(t.queue.items)}")


if __name__ == "__main__":
    # 1. Генерація початкових даних
    dummy_apps = [
        Application("A001", 15000, "Volvo", "Іванов", "промислові товари", 5),
        Application("A002", 5000, "MAN", "Петров", "гуманітарна допомога", 2),
        Application("A003", 60000, "DAF", "Сидоров", "ліки", 1),
        Application("A004", 120000, "Scania", "Коваленко", "продукти", 10),
        Application("A005", 8000, "Renault", "Мельник", "продукти", 3)
    ]

    # 2. Робота зі сховищем (Запис і читання)
    storage = JsonStorage() # Можна легко змінити на CsvStorage()
    storage.save(dummy_apps, "customs_data.json")
    loaded_apps = storage.load("customs_data.json")

    # 3. Ініціалізація системи та терміналів
    t1 = Terminal("T-1_Пріоритетний", PriorityQueue())
    t2 = Terminal("T-2_Звичайний", FifoQueue())
    
    customs = CustomsSystem([t1, t2])

    # 4. Завантаження заявок у систему (рівномірний розподіл)
    for app in loaded_apps:
        customs.add_application(app)

    customs.display_status()

    # 5. Демонстрація алгоритмів
    customs.run_algorithm(AlgorithmOne())
    customs.display_status()

    customs.run_algorithm(AlgorithmTwo("продукти"))
    customs.display_status()

    customs.run_algorithm(AlgorithmThree())
    customs.display_status()
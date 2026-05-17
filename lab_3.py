from abc import ABC, abstractmethod

# Абстрактний базовий клас
class PersonalCabinet(ABC):
    def __init__(self, name: str, used_kwh: float, base_rate: float):
        self.name = name
        self.used_kwh = used_kwh
        self.base_rate = base_rate

    @abstractmethod
    def calculate_payment(self) -> float:
        """Абстрактний метод для розрахунку плати за електроенергію"""
        pass

    @abstractmethod
    def display_info(self):
        """Абстрактний метод для виведення інформації про споживача"""
        pass


# Похідний клас 1: Фізична особа
class Individual(PersonalCabinet):
    def __init__(self, name: str, used_kwh: float, base_rate: float):
        super().__init__(name, used_kwh, base_rate)

    def calculate_payment(self) -> float:
        # Оплата лише за фактично спожиту електроенергію
        return self.used_kwh * self.base_rate

    def display_info(self):
        print(f"[Фізична особа] {self.name} | Використано: {self.used_kwh} кВт·год | До сплати: {self.calculate_payment():.2f} грн")


# Похідний клас 2: Юридична особа
class LegalEntity(PersonalCabinet):
    def __init__(self, name: str, used_kwh: float, base_rate: float, norm_kwh: float, over_norm_rate: float):
        super().__init__(name, used_kwh, base_rate)
        self.norm_kwh = norm_kwh
        self.over_norm_rate = over_norm_rate

    def calculate_payment(self) -> float:
        # Оплата за встановлену норму плюс за понаднормове використання, якщо таке є
        base_payment = self.norm_kwh * self.base_rate
        overage_payment = 0.0
        
        if self.used_kwh > self.norm_kwh:
            overage = self.used_kwh - self.norm_kwh
            overage_payment = overage * self.over_norm_rate
            
        return base_payment + overage_payment

    def display_info(self):
        print(f"[Юридична особа] {self.name} | Використано: {self.used_kwh} кВт·год (Норма: {self.norm_kwh}) | До сплати: {self.calculate_payment():.2f} грн")


# Клас-контейнер (Патерн Registry)
class ConsumerRegistry:
    def __init__(self):
        # Використовуємо словник для зберігання (ім'я -> об'єкт)
        self._consumers = {}

    def register(self, consumer: PersonalCabinet):
        """Реєстрація нового споживача у контейнері"""
        if not isinstance(consumer, PersonalCabinet):
            print("Помилка: Об'єкт має наслідувати клас PersonalCabinet.")
            return

        if consumer.name in self._consumers:
            print(f"Помилка: Споживач з іменем '{consumer.name}' вже зареєстрований.")
        else:
            self._consumers[consumer.name] = consumer
            print(f"Зареєстровано споживача: {consumer.name}")

    def unregister(self, name: str):
        """Видалення (зняття з реєстрації) споживача"""
        if name in self._consumers:
            del self._consumers[name]
            print(f"Видалено споживача: {name}")
        else:
            print(f"Споживача '{name}' не знайдено.")

    def replace(self, old_name: str, new_consumer: PersonalCabinet):
        """Заміна існуючого споживача на нового"""
        if old_name in self._consumers:
            # Видаляємо старого запис
            del self._consumers[old_name]
            # Реєструємо нового (перевірки відбудуться всередині методу register)
            print(f"Споживача '{old_name}' замінюємо на '{new_consumer.name}'...")
            self.register(new_consumer)
        else:
            print(f"Споживача '{old_name}' не знайдено для заміни.")

    def get_consumer(self, name: str) -> PersonalCabinet:
        """Отримання об'єкта споживача за іменем"""
        return self._consumers.get(name)

    def process_all(self):
        """Демонстрація однотипної обробки екземплярів класів-потомків"""
        print("\n--- Обробка всіх споживачів (Демонстрація поліморфізму) ---")
        if not self._consumers:
            print("Реєстр порожній.")
        for consumer in self._consumers.values():
            consumer.display_info()
        print("----------------------------------------------------\n")


# Основна програма
if __name__ == "__main__":
    # Тарифи
    STANDARD_RATE = 2.64
    COMMERCIAL_OVERAGE_RATE = 5.50

    # 1. Створення екземплярів
    indiv1 = Individual("Іван Франко", 150, STANDARD_RATE)
    indiv2 = Individual("Леся Українка", 320, STANDARD_RATE)
    
    legal1 = LegalEntity("ТОВ 'ТехноБуд'", 1200, STANDARD_RATE, norm_kwh=1000, over_norm_rate=COMMERCIAL_OVERAGE_RATE)
    legal2 = LegalEntity("Пекарня 'Хліб'", 400, STANDARD_RATE, norm_kwh=500, over_norm_rate=COMMERCIAL_OVERAGE_RATE)

    # 2. Ініціалізація реєстру-контейнера та додавання споживачів
    registry = ConsumerRegistry()
    registry.register(indiv1)
    registry.register(legal1)
    registry.register(legal2)
    
    # Спроба зареєструвати того ж самого користувача (перевірка захисту)
    registry.register(indiv1)
    
    # 3. Демонстрація однотипної обробки
    registry.process_all()

    # 4. Демонстрація заміни
    new_indiv = Individual("Тарас Шевченко", 210, STANDARD_RATE)
    registry.replace("ТОВ 'ТехноБуд'", new_indiv)
    
    # 5. Демонстрація видалення
    registry.unregister("Пекарня 'Хліб'")
    
    # 6. Обробка фінального стану
    registry.process_all()
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


# Клас-контейнер
class ConsumersContainer:
    def __init__(self):
        self.consumers_list = []

    def add_consumer(self, consumer: PersonalCabinet):
        if isinstance(consumer, PersonalCabinet):
            self.consumers_list.append(consumer)
            print(f"Додано споживача: {consumer.name}")
        else:
            print("Помилка: Об'єкт має наслідувати клас PersonalCabinet.")

    def remove_consumer(self, name: str):
        initial_length = len(self.consumers_list)
        self.consumers_list = [c for c in self.consumers_list if c.name != name]
        if len(self.consumers_list) < initial_length:
            print(f"Видалено споживача: {name}")
        else:
            print(f"Споживача {name} не знайдено.")

    def replace_consumer(self, old_name: str, new_consumer: PersonalCabinet):
        for index, consumer in enumerate(self.consumers_list):
            if consumer.name == old_name:
                self.consumers_list[index] = new_consumer
                print(f"Споживача '{old_name}' замінено на '{new_consumer.name}'.")
                return True
        print(f"Споживача '{old_name}' не знайдено для заміни.")
        return False

    def process_all(self):
        """Демонстрація однотипної обробки екземплярів класів-потомків"""
        print("\n--- Обробка всіх споживачів (Демонстрація поліморфізму) ---")
        for consumer in self.consumers_list:
            # Цикл перебирає екземпляри, і правильний метод викликається автоматично
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

    # 2. Ініціалізація контейнера та додавання споживачів
    container = ConsumersContainer()
    container.add_consumer(indiv1)
    container.add_consumer(legal1)
    container.add_consumer(legal2)
    
    # 3. Демонстрація однотипної обробки
    container.process_all()

    # 4. Демонстрація заміни
    new_indiv = Individual("Тарас Шевченко", 210, STANDARD_RATE)
    container.replace_consumer("ТОВ 'ТехноБуд'", new_indiv)
    
    # 5. Демонстрація видалення
    container.remove_consumer("Пекарня 'Хліб'")
    
    # 6. Обробка фінального стану
    container.process_all()
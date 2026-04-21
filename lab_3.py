from abc import ABC, abstractmethod

# Abstract Base Class
class PersonalCabinet(ABC):
    def __init__(self, name: str, used_kwh: float, base_rate: float):
        self.name = name
        self.used_kwh = used_kwh
        self.base_rate = base_rate

    @abstractmethod
    def calculate_payment(self) -> float:
        """Abstract method to calculate electricity bill"""
        pass

    @abstractmethod
    def display_info(self):
        """Abstract method to display consumer info"""
        pass


# Derived Class 1: Individual Consumer
class Individual(PersonalCabinet):
    def __init__(self, name: str, used_kwh: float, base_rate: float):
        super().__init__(name, used_kwh, base_rate)

    def calculate_payment(self) -> float:
        # Pays only for the actually used electricity
        return self.used_kwh * self.base_rate

    def display_info(self):
        print(f"[Individual] {self.name} | Used: {self.used_kwh} kWh | Total Bill: {self.calculate_payment():.2f} UAH")


# Derived Class 2: Legal Entity
class LegalEntity(PersonalCabinet):
    def __init__(self, name: str, used_kwh: float, base_rate: float, norm_kwh: float, over_norm_rate: float):
        super().__init__(name, used_kwh, base_rate)
        self.norm_kwh = norm_kwh
        self.over_norm_rate = over_norm_rate

    def calculate_payment(self) -> float:
        # Pays for the established norm regardless, plus overage if applicable
        base_payment = self.norm_kwh * self.base_rate
        overage_payment = 0.0
        
        if self.used_kwh > self.norm_kwh:
            overage = self.used_kwh - self.norm_kwh
            overage_payment = overage * self.over_norm_rate
            
        return base_payment + overage_payment

    def display_info(self):
        print(f"[Legal Entity] {self.name} | Used: {self.used_kwh} kWh (Norm: {self.norm_kwh}) | Total Bill: {self.calculate_payment():.2f} UAH")


# Container Class
class ConsumersContainer:
    def __init__(self):
        self.consumers_list = []

    def add_consumer(self, consumer: PersonalCabinet):
        if isinstance(consumer, PersonalCabinet):
            self.consumers_list.append(consumer)
            print(f"Added consumer: {consumer.name}")
        else:
            print("Error: Object must inherit from PersonalCabinet.")

    def remove_consumer(self, name: str):
        initial_length = len(self.consumers_list)
        self.consumers_list = [c for c in self.consumers_list if c.name != name]
        if len(self.consumers_list) < initial_length:
            print(f"Removed consumer: {name}")
        else:
            print(f"Consumer {name} not found.")

    def replace_consumer(self, old_name: str, new_consumer: PersonalCabinet):
        for index, consumer in enumerate(self.consumers_list):
            if consumer.name == old_name:
                self.consumers_list[index] = new_consumer
                print(f"Replaced consumer '{old_name}' with '{new_consumer.name}'.")
                return True
        print(f"Consumer '{old_name}' not found for replacement.")
        return False

    def process_all(self):
        """Demonstrates uniform processing of descendant instances"""
        print("\n--- Processing All Consumers (Polymorphism Demo) ---")
        for consumer in self.consumers_list:
            # The loop iterates over instances, and the correct method is called automatically
            consumer.display_info()
        print("----------------------------------------------------\n")


# Main Program
if __name__ == "__main__":
    # Rates
    STANDARD_RATE = 2.64
    COMMERCIAL_OVERAGE_RATE = 5.50

    # 1. Create instances
    indiv1 = Individual("John Doe", 150, STANDARD_RATE)
    indiv2 = Individual("Jane Smith", 320, STANDARD_RATE)
    
    legal1 = LegalEntity("TechCorp LLC", 1200, STANDARD_RATE, norm_kwh=1000, over_norm_rate=COMMERCIAL_OVERAGE_RATE)
    legal2 = LegalEntity("Small Bakery", 400, STANDARD_RATE, norm_kwh=500, over_norm_rate=COMMERCIAL_OVERAGE_RATE)

    # 2. Initialize container and add consumers
    container = ConsumersContainer()
    container.add_consumer(indiv1)
    container.add_consumer(legal1)
    container.add_consumer(legal2)
    
    # 3. Demonstrate uniform processing
    container.process_all()

    # 4. Demonstrate replacement
    new_indiv = Individual("Alan Turing", 210, STANDARD_RATE)
    container.replace_consumer("TechCorp LLC", new_indiv)
    
    # 5. Demonstrate removal
    container.remove_consumer("Small Bakery")
    
    # 6. Final state processing
    container.process_all()
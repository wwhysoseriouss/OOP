class CrewMember:
    def __init__(self, name, role):
        self.name = name
        self.role = role

    def __str__(self):
        return f"{self.role}: {self.name}"


class Airplane:
    def __init__(self, model):
        self.model = model
        # Агрегація: літак має екіпаж, але члени екіпажу існують незалежно
        self.crew = [] 

    def assign_crew(self, crew_list):
        self.crew = crew_list

    def display_info(self):
        print(f"--- Літак: {self.model} ---")
        if self.crew:
            print("Екіпаж на поточний рейс:")
            for member in self.crew:
                print(f"  - {member}")
        else:
            print("Екіпаж не призначено!")

    def perform_flight(self):
        if not self.crew:
            print(f"Помилка: Рейс скасовано. Літак {self.model} не має екіпажу.\n")
            return False
        return True


# --- Наслідування для уникнення дублювання коду ---

class PassengerPlane(Airplane):
    def __init__(self, model, passenger_capacity):
        super().__init__(model)
        self.passenger_capacity = passenger_capacity

    def perform_flight(self):
        if super().perform_flight():
            print(f"Виконується пасажирський рейс. Транспортування до {self.passenger_capacity} пасажирів.\n")


class CargoPlane(Airplane):
    def __init__(self, model, payload_capacity_tons):
        super().__init__(model)
        self.payload_capacity_tons = payload_capacity_tons

    def perform_flight(self):
        if super().perform_flight():
            print(f"Виконується вантажний рейс. Транспортування {self.payload_capacity_tons} тонн вантажу.\n")


class MilitaryPlane(Airplane):
    def __init__(self, model, weapon_type):
        super().__init__(model)
        self.weapon_type = weapon_type

    def perform_flight(self):
        if super().perform_flight():
            print(f"Виконується військове патрулювання з використанням озброєння: {self.weapon_type}.\n")


# --- Прикладна програма для демонстрації функціонування ---
if __name__ == "__main__":
    pilot1 = CrewMember("Іван Коваленко", "Головний пілот")
    pilot2 = CrewMember("Олена Петрів", "Другий пілот")
    pilot3 = CrewMember("Дмитро Сидор", "Військовий пілот")
    steward1 = CrewMember("Анна Мельник", "Бортпровідник")
    navigator = CrewMember("Олег Бойко", "Штурман")

    boeing = PassengerPlane("Boeing 737", 189)
    antonov = CargoPlane("AN-124 Ruslan", 120)
    f16 = MilitaryPlane("F-16 Fighting Falcon", "Ракети 'повітря-повітря'")

    # --- Демонстрація роботи та зміни екіпажів (Агрегація) ---

    boeing.assign_crew([pilot1, steward1])
    boeing.display_info()
    boeing.perform_flight()

    boeing.assign_crew([pilot2, steward1, navigator])
    boeing.display_info()
    boeing.perform_flight()

    antonov.assign_crew([pilot1, navigator])
    antonov.display_info()
    antonov.perform_flight()

    f16.assign_crew([pilot3])
    f16.display_info()
    f16.perform_flight()

    f16.assign_crew([]) # Екіпаж знято
    f16.display_info()
    f16.perform_flight()
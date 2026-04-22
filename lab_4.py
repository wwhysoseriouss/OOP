import time
import functools

def time_method(func):
    """
    Стандартний декоратор функції, який вимірює та виводить 
    час виконання обгорнутої функції.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        print(f"[ЛОГ ЧАСУ] Метод '{func.__name__}' виконано за {execution_time:.4f} секунд.\n")
        return result
    return wrapper

def TimeMethods(cls):
    """
    Декоратор класу, який перебирає атрибути класу 
    та застосовує декоратор 'time_method' до всіх публічних методів.
    """
    for attr_name, attr_value in vars(cls).items():
        # Застосовуємо хронометраж лише до методів (callable), ігноруючи магічні методи (dunder)
        if callable(attr_value) and not attr_name.startswith("__"):
            setattr(cls, attr_name, time_method(attr_value))
    return cls

# --- Демонстрація ---

@TimeMethods
class NetworkDeviceConfig:
    """
    Приклад класу, що представляє інструмент конфігурації мережевого обладнання, 
    для демонстрації автоматичного хронометражу методів.
    """
    def __init__(self, ip_address: str):
        self.ip_address = ip_address
        # Примітка: __init__ не буде хронометруватися, оскільки починається з "__"

    def establish_connection(self):
        print(f"Підключення до пристрою {self.ip_address}...")
        time.sleep(0.3)  # Імітація затримки мережі
        print("Підключення успішно встановлено.")

    def parse_ospf_topology(self):
        print("Отримання та парсинг логів топології OSPF...")
        time.sleep(0.6)  # Імітація обробки даних
        print("Топологію OSPF розпарсено.")

    def deploy_bgp_rules(self):
        print("Розгортання нових правил маршрутизації BGP...")
        time.sleep(0.2)  # Імітація часу запису конфігурації
        print("Правила BGP розгорнуто.")


if __name__ == "__main__":
    # Ініціалізація об'єкта маршрутизатора
    router = NetworkDeviceConfig("10.0.0.1")
    
    # Виклик методів для демонстрації роботи декоратора у реальному часі
    router.establish_connection()
    router.parse_ospf_topology()
    router.deploy_bgp_rules()
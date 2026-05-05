import threading
import time
import copy

class ThreadSafeMemento:
    def __init__(self, state: dict):
        # Використовуємо глибоку копію, щоб уникнути зміни за посиланням
        self._state = copy.deepcopy(state)

    def get_state(self) -> dict:
        return self._state

class SharedConfiguration:
    def __init__(self):
        self._config = {"users": 0, "status": "init"}
        self._lock = threading.Lock() # Блокування для безпеки потоків

    def update_config(self, users_add: int, status: str):
        with self._lock: # Блокуємо доступ для інших потоків під час зміни
            self._config["users"] += users_add
            self._config["status"] = status
            print(f"[{threading.current_thread().name}] Оновлено конфіг: {self._config}")
            time.sleep(0.1) # Симуляція довгої роботи

    def save(self) -> ThreadSafeMemento:
        with self._lock: # Блокуємо доступ під час зняття знімка (snapshot)
            print(f"[{threading.current_thread().name}] Створення бекапу...")
            return ThreadSafeMemento(self._config)

    def restore(self, memento: ThreadSafeMemento):
        with self._lock: # Блокуємо доступ під час відновлення
            self._config = copy.deepcopy(memento.get_state())
            print(f"[{threading.current_thread().name}] Відновлено конфіг: {self._config}")

class ConfigManager:
    def __init__(self, config: SharedConfiguration):
        self._history = []
        self._config = config
        self._lock = threading.Lock() # Блокування для безпеки історії

    def backup(self):
        memento = self._config.save()
        with self._lock:
            self._history.append(memento)

    def undo(self):
        with self._lock:
            if not self._history:
                return
            memento = self._history.pop()
        self._config.restore(memento)

# --- Демонстрація (Багатопоточна) ---
def worker(config: SharedConfiguration, manager: ConfigManager):
    config.update_config(10, "running")
    manager.backup()
    config.update_config(5, "error")
    manager.undo() # Скасовуємо "error"

if __name__ == "__main__":
    print("--- БАГАТОПОТОЧНА ДЕМОНСТРАЦІЯ ---")
    shared_config = SharedConfiguration()
    manager = ConfigManager(shared_config)

    # Створюємо кілька потоків, які одночасно працюють зі спільним об'єктом
    threads = []
    for i in range(3):
        t = threading.Thread(target=worker, args=(shared_config, manager), name=f"Потік-{i+1}")
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
        
    print(f"Фінальний стан: {shared_config._config}")
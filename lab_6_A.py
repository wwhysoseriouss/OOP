import copy

# 1. Клас Memento (Зберігач)
class EditorMemento:
    def __init__(self, content: str):
        self._content = content

    def get_content(self) -> str:
        return self._content

# 2. Клас Originator (Створювач)
class TextEditor:
    def __init__(self):
        self._content = ""

    def type_words(self, words: str):
        self._content += words

    def get_content(self) -> str:
        return self._content

    # Збереження стану
    def save(self) -> EditorMemento:
        return EditorMemento(self._content)

    # Відновлення стану
    def restore(self, memento: EditorMemento):
        self._content = memento.get_content()

# 3. Клас Caretaker (Опікун)
class HistoryCaretaker:
    def __init__(self, editor: TextEditor):
        self._history = []
        self._editor = editor

    def backup(self):
        print("Caretaker: Збереження стану...")
        self._history.append(self._editor.save())

    def undo(self):
        if not self._history:
            print("Caretaker: Немає збережених станів.")
            return
        
        memento = self._history.pop()
        print("Caretaker: Відновлення попереднього стану...")
        self._editor.restore(memento)

# --- Демонстрація (Однопоточна) ---
if __name__ == "__main__":
    print("--- ОДНОПОТОЧНА ДЕМОНСТРАЦІЯ ---")
    editor = TextEditor()
    history = HistoryCaretaker(editor)

    editor.type_words("Привіт, ")
    history.backup() # Зберегли: "Привіт, "

    editor.type_words("Світ! ")
    history.backup() # Зберегли: "Привіт, Світ! "

    editor.type_words("Це помилка.")
    print(f"Поточний текст: '{editor.get_content()}'")

    history.undo()
    print(f"Після першого скасування: '{editor.get_content()}'")

    history.undo()
    print(f"Після другого скасування: '{editor.get_content()}'\n")
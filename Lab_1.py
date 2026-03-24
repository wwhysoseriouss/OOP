class ArithmeticProgression:
    instances = []

    def __init__(self, a, b):
        if b == 0:
            raise ValueError("Різниця не може дорівнювати нулю")
        self.a = a
        self.b = b
        ArithmeticProgression.instances.append(self)

    def get_first(self):
        return self.a

    def get_nth(self, n):
        return self.a + (n - 1) * self.b

    def get_sequence(self, k, m):
        return [self.get_nth(i) for i in range(k, m + 1)]

    def change_parameters(self, a, b):
        if b == 0:
            raise ValueError("Різниця не може дорівнювати нулю")
        self.a = a
        self.b = b

    @staticmethod
    def show_instances():
        for instance in ArithmeticProgression.instances:
            print(instance)

    def __str__(self):
        first_7 = [str(self.get_nth(i)) for i in range(1, 8)]
        return f"# {self.a}, {self.b}: {{{', '.join(first_7)} ...}}"

    def __eq__(self, other):
        return self.a == other.a and self.b == other.b


p1 = ArithmeticProgression(2, 3)
p2 = ArithmeticProgression(10, -2)
p3 = ArithmeticProgression(2, 3)

print("Існуючі екземпляри:")
ArithmeticProgression.show_instances()

print("\n1-ий елемент p1:", p1.get_first())
print("5-ий елемент p1:", p1.get_nth(5))
print("Послідовність від 2 до 4 для p1:", p1.get_sequence(2, 4))

p2.change_parameters(0, 5)
print("\nПісля зміни параметрів p2:", p2)

print("\nПеревірка на рівність:")
print("p1 == p2:", p1 == p2)
print("p1 == p3:", p1 == p3)
from abc import ABC, abstractmethod

class Beverage(ABC):

    def prepare_recipe(self) -> None:
        self.boil_water()
        self.brew()
        self.pour_in_cup()
        if self.customer_wants_condiments():  # Используем хук
            self.add_condiments()
        print("Ваш напиток готов!")

    def boil_water(self) -> None:
        print("Кипячение воды...")

    def pour_in_cup(self) -> None:
        print("Наливание в чашку...")

    @abstractmethod
    def brew(self) -> None:
        pass

    @abstractmethod
    def add_condiments(self) -> None:
        pass

    def customer_wants_condiments(self) -> bool:
        return True  # По умолчанию добавки всегда нужны


class Tea(Beverage):
    def brew(self) -> None:
        print("Заваривание чая...")

    def add_condiments(self) -> None:
        print("Добавление лимона...")


class Coffee(Beverage):
    def brew(self) -> None:
        print("Заваривание кофе...")

    def add_condiments(self) -> None:
        print("Добавление сахара и молока...")

    def customer_wants_condiments(self) -> bool:
        try:
            answer = input("Хотите добавить сахар и молоко? (yes/no): ").lower()
            return answer.startswith('y')
        except Exception:
            print("Ошибка ввода. Добавки не будут добавлены.")
            return False


class HotChocolate(Beverage):
    def brew(self) -> None:
        print("Растворение какао-порошка...")

    def add_condiments(self) -> None:
        print("Добавление зефира...")


if __name__ == "__main__":
    tea = Tea()
    print("--- Приготовление чая ---")
    tea.prepare_recipe()

    print("\n" + "=" * 25 + "\n")

    coffee = Coffee()
    print("--- Приготовление кофе ---")
    coffee.prepare_recipe()

    print("\n" + "=" * 25 + "\n")

    hot_chocolate = HotChocolate()
    print("--- Приготовление горячего шоколада ---")
    hot_chocolate.prepare_recipe()
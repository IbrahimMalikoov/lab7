from abc import ABC, abstractmethod
from typing import List, Dict

class IMediator(ABC):
    @abstractmethod
    def send_message(self, message: str, sender: Colleague):
        pass


class Colleague(ABC):
    def __init__(self, mediator: IMediator, name: str):
        self._mediator = mediator
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    @abstractmethod
    def receive_message(self, message: str):
        pass


class User(Colleague):
    def send(self, message: str):
        print(f"[{self.name}] отправляет: '{message}'")
        self._mediator.send_message(message, self)

    def receive_message(self, message: str):
        print(f"[{self.name}] получил сообщение: '{message}'")


class ChatMediator(IMediator):
    def __init__(self):
        self._users: List[User] = []
        self._message_log: List[str] = []

    def register_user(self, user: User):
        if user not in self._users:
            print(f"--- Участник {user.name} присоединился к чату ---")
            self._users.append(user)
        else:
            print(f"--- Участник {user.name} уже в чате ---")

    def unregister_user(self, user: User):
        if user in self._users:
            print(f"--- Участник {user.name} покинул чат ---")
            self._users.remove(user)

    def send_message(self, message: str, sender: Colleague):
        log_entry = f"От {sender.name}: {message}"
        self._message_log.append(log_entry)

        for user in self._users:
            if user is not sender:
                user.receive_message(f"(от {sender.name}): {message}")

    def send_private_message(self, message: str, sender: Colleague, recipient_name: str):
        recipient: User = None
        for user in self._users:
            if user.name == recipient_name:
                recipient = user
                break

        if recipient:
            if recipient is not sender:
                recipient.receive_message(f"(личное от {sender.name}): {message}")
            else:
                sender.receive_message("(Система): Нельзя отправить личное сообщение самому себе.")
        else:
            sender.receive_message(f"(Система): Пользователь с именем '{recipient_name}' не найден.")

    def show_history(self):
        print("\n--- История переписки ---")
        for msg in self._message_log:
            print(msg)
        print("------------------------")


if __name__ == "__main__":
    chat = ChatMediator()

    alice = User(chat, "Алиса")
    bob = User(chat, "Боб")
    charlie = User(chat, "Чарли")

    chat.register_user(alice)
    chat.register_user(bob)
    chat.register_user(charlie)

    print("\n--- Общение в чате ---")
    alice.send("Привет всем!")
    bob.send("Привет, Алиса!")

    print("\n--- Приватные сообщения ---")
    charlie.send_private_message = lambda msg, to: chat.send_private_message(msg, charlie, to)
    charlie.send_private_message("Боб, как дела?", "Боб")
    charlie.send_private_message("Есть кто?", "Дэвид")  # Попытка отправить сообщение несуществующему пользователю

    print("\n--- Участник покидает чат ---")
    chat.unregister_user(bob)
    alice.send("Боб, ты здесь?") 

    chat.show_history()
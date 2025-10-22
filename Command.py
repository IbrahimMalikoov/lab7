import time
from abc import ABC, abstractmethod
from typing import List, Optional

class ICommand(ABC):
    @abstractmethod
    def execute(self) -> None: pass

    @abstractmethod
    def undo(self) -> None: pass


class Light:

    def on(self):
        print("Свет включен")

    def off(self):
        print("Свет выключен")


class Television:
    def on(self):
        print("Телевизор включен")

    def off(self):
        print("Телевизор выключен")


class AirConditioner:

    def on(self):
        print("Кондиционер включен")

    def off(self):
        print("Кондиционер выключен")

    def set_eco_mode(self):
        print("Кондиционер: включен режим экономии энергии")

class LightOnCommand(ICommand):
    def __init__(self, light: Light):
        self._light = light

    def execute(self) -> None:
        self._light.on()

    def undo(self) -> None:
        self._light.off()


class LightOffCommand(ICommand):
    def __init__(self, light: Light):
        self._light = light

    def execute(self) -> None:
        self._light.off()

    def undo(self) -> None:
        self._light.on()


class TelevisionOnCommand(ICommand):
    def __init__(self, television: Television):
        self._tv = television

    def execute(self) -> None:
        self._tv.on()

    def undo(self) -> None:
        self._tv.off()


class TelevisionOffCommand(ICommand):
    def __init__(self, television: Television):
        self._tv = television

    def execute(self) -> None:
        self._tv.off()

    def undo(self) -> None:
        self._tv.on()


class AirConditionerOnCommand(ICommand):
    def __init__(self, ac: AirConditioner):
        self._ac = ac

    def execute(self) -> None:
        self._ac.on()

    def undo(self) -> None:
        self._ac.off()


class AirConditionerEcoModeCommand(ICommand):
    def __init__(self, ac: AirConditioner):
        self._ac = ac

    def execute(self) -> None:
        self._ac.set_eco_mode()

    def undo(self) -> None:
        self._ac.off()


class NoCommand(ICommand):
    def execute(self) -> None:
        print("На эту кнопку не назначена команда.")

    def undo(self) -> None:
        print("На эту кнопку не назначена команда.")


class MacroCommand(ICommand):
    def __init__(self, commands: List[ICommand]):
        self._commands = commands

    def execute(self) -> None:
        print("--- Выполнение макрокоманды ---")
        for command in self._commands:
            command.execute()
        print("--- Макрокоманда выполнена ---")

    def undo(self) -> None:
        print("--- Отмена макрокоманды ---")
        for command in reversed(self._commands):
            command.undo()
        print("--- Макрокоманда отменена ---")


class RemoteControl:

    def __init__(self, num_slots: int = 7):
        no_command = NoCommand()
        self._on_commands: List[ICommand] = [no_command] * num_slots
        self._off_commands: List[ICommand] = [no_command] * num_slots
        self._undo_command: ICommand = no_command
        self._command_log: List[str] = []

    def _log_command(self, action: str, command: ICommand):
        log_entry = f"{time.ctime()}: {action} -> {command.__class__.__name__}"
        self._command_log.append(log_entry)
        print(f"(Лог: {log_entry})")

    def set_command(self, slot: int, on_command: ICommand, off_command: ICommand):
        if 0 <= slot < len(self._on_commands):
            self._on_commands[slot] = on_command
            self._off_commands[slot] = off_command
        else:
            print(f"Ошибка: Слот {slot} не существует.")

    def press_on_button(self, slot: int):
        command = self._on_commands[slot]
        self._log_command("Execute", command)
        command.execute()
        self._undo_command = command

    def press_off_button(self, slot: int):
        command = self._off_commands[slot]
        self._log_command("Execute", command)
        command.execute()
        self._undo_command = command

    def press_undo_button(self):
        self._log_command("Undo", self._undo_command)
        self._undo_command.undo()
        self._undo_command = NoCommand()  # Отменить можно только один раз

    def show_logs(self):
        print("\n--- Журнал команд ---")
        for entry in self._command_log:
            print(entry)
        print("--------------------")


if __name__ == "__main__":
    remote = RemoteControl()

    living_room_light = Light()
    tv = Television()
    ac = AirConditioner()

    light_on = LightOnCommand(living_room_light)
    light_off = LightOffCommand(living_room_light)
    tv_on = TelevisionOnCommand(tv)
    tv_off = TelevisionOffCommand(tv)
    ac_on = AirConditionerOnCommand(ac)
    ac_eco = AirConditionerEcoModeCommand(ac)

    remote.set_command(0, light_on, light_off)
    remote.set_command(1, tv_on, tv_off)
    remote.set_command(2, ac_on, NoCommand())  # Кнопка Off для AC не назначена
    remote.set_command(3, ac_eco, NoCommand())

    # --- Тестирование ---
    print("--- Управление светом ---")
    remote.press_on_button(0)
    remote.press_off_button(0)
    print("--- Нажимаем отмену ---")
    remote.press_undo_button()

    print("\n--- Управление телевизором ---")
    remote.press_on_button(1)
    remote.press_undo_button()

    print("\n--- Обработка ошибок ---")
    remote.press_on_button(5)

    # --- Тестирование макрокоманды ---
    print("\n--- Создание макрокоманды 'Я ухожу' (выключить все) ---")
    leave_home_macro = MacroCommand([light_off, tv_off, AirConditionerOnCommand(ac).undo])

    light_on.execute()
    tv_on.execute()
    ac_on.execute()

    remote.set_command(4, leave_home_macro, NoCommand())
    remote.press_on_button(4)

    print("\n--- Отмена макрокоманды 'Я ухожу' ---")
    remote.press_undo_button()
    remote.show_logs()
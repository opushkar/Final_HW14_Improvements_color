from typing import Callable, Any
from colorama import Fore, Style, init

# Ініціалізація colorama з автоматичним скиданням стилів після кожного принту
init(autoreset=True)

def input_error(func: Callable[..., Any]) -> Callable[..., Any]:
    """Декоратор для обробки помилок введення з кольоровим оформленням."""
    def inner(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            # Червоний та Жирний (Bright) колір для помилок валідації
            return f"{Fore.RED}{Style.BRIGHT}Error: {e}"
        except KeyError as e:
            # Помаранчевий (Orange у терміналі) колір для попереджень (контакт не знайдено)
            return f"{Fore.YELLOW}Warning: Contact {e} not found."
        except IndexError:
            return f"{Fore.RED}{Style.BRIGHT}Error: Not enough arguments provided. Please check the command format."
        except Exception as e:
            return f"{Fore.RED}{Style.BRIGHT}An unexpected error occurred: {e}"
    return inner

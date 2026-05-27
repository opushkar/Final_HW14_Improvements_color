from typing import Callable, Any

def input_error(func: Callable[..., Any]) -> Callable[..., Any]:
    """Декоратор для обробки виключень, що виникають під час введення команд."""
    def inner(*args: Any, **kwargs: Any) -> str:
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return f"Error: {e}"
        except IndexError:
            return "Error: Enter user name and phone number."
        except KeyError as e:
            return f"Error: Contact {e} not found."
        except Exception as e:
            return f"An unexpected error occurred: {e}"
    return inner

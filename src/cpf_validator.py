import re

CPF_LENGTH = 11
BLOCKLIST = {str(digit) * CPF_LENGTH for digit in range(10)}


def only_digits(cpf: str) -> str:
    return re.sub(r"\D", "", cpf)


def is_valid(cpf: str | None) -> bool:
    digits = only_digits(cpf or "")

    if len(digits) != CPF_LENGTH or digits in BLOCKLIST:
        return False

    first_digit = _check_digit(digits[:9], initial_weight=10)
    second_digit = _check_digit(digits[:10], initial_weight=11)

    return first_digit == int(digits[9]) and second_digit == int(digits[10])


def mask(cpf_digits: str) -> str:
    """Ofusca o CPF para logs: 529.***.***-25."""
    return f"{cpf_digits[:3]}.***.***-{cpf_digits[-2:]}"


def _check_digit(digits: str, initial_weight: int) -> int:
    total = sum(int(digit) * (initial_weight - index) for index, digit in enumerate(digits))
    remainder = (total * 10) % 11
    return 0 if remainder == 10 else remainder

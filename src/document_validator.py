import re

CPF_LENGTH = 11
CNPJ_LENGTH = 14
CPF_BLOCKLIST = {str(digit) * CPF_LENGTH for digit in range(10)}
CNPJ_BLOCKLIST = {str(digit) * CNPJ_LENGTH for digit in range(10)}


def only_digits(document: str) -> str:
    return re.sub(r"\D", "", document)


def is_valid(document: str | None) -> bool:
    digits = only_digits(document or "")

    if len(digits) == CPF_LENGTH:
        return _is_valid_cpf(digits)
    if len(digits) == CNPJ_LENGTH:
        return _is_valid_cnpj(digits)
    return False


def mask(document_digits: str) -> str:
    """Ofusca o documento para logs: 529.***.***-25 ou 12.***.***/0001-25."""
    if len(document_digits) == CNPJ_LENGTH:
        return f"{document_digits[:2]}.***.***/{document_digits[8:12]}-{document_digits[-2:]}"
    return f"{document_digits[:3]}.***.***-{document_digits[-2:]}"


def _is_valid_cpf(digits: str) -> bool:
    if digits in CPF_BLOCKLIST:
        return False

    first_digit = _cpf_check_digit(digits[:9], initial_weight=10)
    second_digit = _cpf_check_digit(digits[:10], initial_weight=11)

    return first_digit == int(digits[9]) and second_digit == int(digits[10])


def _cpf_check_digit(digits: str, initial_weight: int) -> int:
    total = sum(int(digit) * (initial_weight - index) for index, digit in enumerate(digits))
    remainder = (total * 10) % 11
    return 0 if remainder == 10 else remainder


def _is_valid_cnpj(digits: str) -> bool:
    if digits in CNPJ_BLOCKLIST:
        return False

    first_digit = _cnpj_check_digit(digits[:12], weights=[5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2])
    second_digit = _cnpj_check_digit(digits[:13], weights=[6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2])

    return first_digit == int(digits[12]) and second_digit == int(digits[13])


def _cnpj_check_digit(digits: str, weights: list[int]) -> int:
    total = sum(int(digit) * weight for digit, weight in zip(digits, weights))
    remainder = total % 11
    return 0 if remainder < 2 else 11 - remainder
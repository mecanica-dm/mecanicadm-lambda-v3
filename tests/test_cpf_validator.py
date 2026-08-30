import pytest

from src.cpf_validator import is_valid

@pytest.mark.parametrize("cpf", [
    "529.982.247-25",
    "52998224725",
    "11144477735",
])
def test_cpf_valido(cpf):
    assert is_valid(cpf) is True


@pytest.mark.parametrize("cpf", [
    "000.000.000-00",
    "11111111111",
    "123.456.789-00",
    "123",
    "",
    None,
    "abc.def.ghi-jk",
])
def test_cpf_invalido(cpf):
    assert is_valid(cpf) is False

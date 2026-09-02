import pytest

from src.document_validator import is_valid

@pytest.mark.parametrize("document", [
    "529.982.247-25",
    "52998224725",
    "11144477735",
    "12.345.678/0001-95",
    "12345678000195",
    "11.222.333/0001-81",
])
def test_documento_valido(document):
    assert is_valid(document) is True


@pytest.mark.parametrize("document", [
    "000.000.000-00",
    "11111111111",
    "123.456.789-00",
    "123",
    "",
    None,
    "abc.def.ghi-jk",
    "00.000.000/0000-00",
    "11111111111111",
    "12.345.678/0001-00",
])
def test_documento_invalido(document):
    assert is_valid(document) is False
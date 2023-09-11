from pydantic import BaseModel
from typing import Optional, List
from model import Pessoa


class PessoaSchema(BaseModel):
    """Define como um novo funcionario a ser inserido deve ser representado"""

    nome: str = "Joao da Silva"
    cpf: str = "123456789-10"
    cep: str = "XXXXX-XXX"
    rua: str = "Rua Alguma coisa"
    bairro: str = "Baixo algum"
    cidade: str = "Rio de Janeiro"
    estado: str = "RJ"


class PessoaBuscaSchema(BaseModel):
    """Define como deve ser a estrutura que representa a busca da pessoa.

    A busca é feita baseada no CPF da pesssoa
    """

    cpf: str = "111111111-11"

class ListagemPessoasSchema(BaseModel):
    """Lista dos dados das pessoas cadastradas no banco."""

    pessoas: List[PessoaSchema]


class PessoaViewSchema(BaseModel):
    """Define como um funcinário será retornado"""

    nome: str = "Joao da Silva"
    cpf: str = "123456789-10"
    cep: str = "XXXXX-XXX"
    rua: str = "Rua Alguma coisa"
    bairo: str = "Baixo algum"
    cidade: str = "Rio de Janeiro"
    estado: str = "RJ"


def apresenta_pessoas(pessoas: List[Pessoa]):
    """Retorna um dicionario com todos as pessoas cadastradas no banco e seus respectivos capos."""
    result = []

    for pessoa in pessoas:
        result.append(apresenta_pessoa(pessoa))

    return {"Pessoas": result}


def apresenta_pessoa(pessoa: Pessoa):
    """Retorna os campos que representam o funcionaro."""
    return {
        "nome": pessoa.nome,
        "cpf": pessoa.cpf,
        "cep": pessoa.cep,
        "rua": pessoa.rua,
        "bairro": pessoa.bairro,
        "cidade": pessoa.cidade,
        "estado": pessoa.estado,
    }

class InterfaceParaEndereco(BaseModel):
    """Retorna os campos que representam o endereço."""

    Rua: str = "Rua Alguma coisa"
    Bairro: str = "Bairro CX"
    Cidade: str = "Rio de Janeiro"
    Estado: str = "RJ"


class CepBuscaSchema(BaseModel):
    """Define como deve ser a estrutura que representa a busca do CEP.

    A busca é feita baseada no login do funcionario
    """

    cep: str = "20021-000"

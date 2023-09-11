from sqlalchemy import Column, String, Integer
from model import Base

"""
    Classe Pessoa
    A classe cria uma representação genérica de uma pessoa, com os campos de nome,
    cpf e senha. 
    Cria a tabela de nome pessoa para retenção desses dados no banco.
"""


class Pessoa(Base):
    __tablename__ = "pessoa"

    id = Column("id_pessoa", Integer, primary_key=True)
    nome = Column("nome", String(60), nullable=False)
    cpf = Column("cpf", String(15), unique=True, nullable=False)
    cep = Column("cep", String(9), nullable=False)
    rua = Column("rua", String(20), nullable=False)
    bairro = Column("bairro", String(15), nullable=False)
    cidade = Column("cidade", String(15), nullable=False)
    estado = Column("estado", String(15), nullable=False)

    def __init__(
        self,
        nome: str,
        cpf: str,
        cep: str,
        rua: str,
        bairro: str,
        cidade: str,
        estado: str,
    ) -> None:
        super().__init__()
        self.nome = nome
        self.cpf = cpf
        self.cep = cep
        self.rua = rua
        self.bairro = bairro
        self.cidade = cidade
        self.estado = estado

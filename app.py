from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

import requests, json

from sqlalchemy.exc import IntegrityError

from model import Session, pessoa, Pessoa

from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="API Cadastro de pessoas. Autor: Daniel Leite", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(
    name="Documentação",
    description="Documentação da API com a ferramenta Swagger",
)
pessoa_tag = Tag(
    name="Pessoa",
    description="Adição, visualização e remoção de pessoas da base. Dados pessoais, como nome, endereço e cpf",
)


@app.get("/", tags=[home_tag])
def home():
    """Redireciona para /openapi, tela de documentação."""
    return redirect("/openapi/swagger#/")


@app.post(
    "/pessoa",
    tags=[pessoa_tag],
    responses={"200": PessoaViewSchema, "409": ErrorSchema, "400": ErrorSchema},
)
def add_pessoa(form: PessoaSchema):
    """Adiciona uma nova Pessoa à base de dados

    Retorna uma representação da Pessoa, em caso de sucesso, ou uma mensagem de erro, em caso de falha.

    """

    pessoa = Pessoa(
        nome=form.nome,
        cpf=form.cpf,
        cep=form.cep,
        rua=form.rua,
        bairro=form.bairro,
        cidade=form.cidade,
        estado=form.estado,
    )
    logger.debug(f"Tentativa de adicionar pessoa de nome: '{pessoa.nome}'")
    logger.warning(apresenta_pessoa(pessoa))
    try:
        # criando conexão com a base
        session = Session()

        # adicionando produto
        session.add(pessoa)

        # efetivando o camando de adição de novo item na tabela
        session.commit()

        logger.debug(f"Adicionado pessoa de nome: '{pessoa.nome}'")
        return apresenta_pessoa(pessoa), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "pessoa de mesmo cpf já salvo na base:"
        logger.warning(f"Erro tentar cadastrar: '{pessoa.nome}', {error_msg}")
        return {"message": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(
            f"Erro ao tentar cadastrar o pessoa: '{pessoa.nome}', {error_msg}"
        )
        return {"message": error_msg}, 400


@app.get(
    "/pessoas",
    tags=[pessoa_tag],
    responses={"200": ListagemPessoasSchema, "404": ErrorSchema},
)
def get_pessoas():
    """Faz a busca por todos os pessoas cadastrados

    Retorna uma representação da listagem de pessoas, em caso de sucesso.
    """

    logger.debug("Coletando pessoas do banco")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    pessoas = session.query(Pessoa).all()

    if not pessoas:
        # se não há produtos cadastrados
        return {"pessoas": []}, 200
    else:
        logger.debug("%d pessoas econtrados" % len(pessoas))
        # retorna a representação de produto
        # print(pessoas)
        return apresenta_pessoas(pessoas), 200


@app.get(
    "/pessoa",
    tags=[pessoa_tag],
    responses={"200": PessoaViewSchema, "404": ErrorSchema},
)
def get_pessoa(query: PessoaBuscaSchema):
    """Realiza a leitura dos dados cadastrais de uma dada pessoa

    Utiliza como campo de busca, o cpf da pessoa
    Retorna os dados da pessoa, em casso de sucesso, ou uma mensagem de erro, em caso de falha,

    """

    logger.debug(f"Validando cpf:  #{query.cpf}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    pessoa = session.query(Pessoa).filter(Pessoa.cpf == query.cpf).first()

    if not pessoa:
        # se o produto não foi encontrado
        error_msg = "pessoa não encontrado na base :/"
        logger.warning(f"Erro ao buscar cpf '{query.cpf}', {error_msg}")
        return {"message": error_msg}, 404

    else:
        # logger.warning(f"Login realizado com sucesso'{form.login}' e senha '{form.senha}', {error_msg}")
        logger.warning(f"Carregando pessoa: '{pessoa.nome}'")
        # retorna a representação de produto
        return apresenta_pessoa(pessoa), 200


@app.put(
    "/pessoa_atualiza_cpf",
    tags=[pessoa_tag],
    responses={
        "200": PessoaViewSchema,
        "404": ErrorSchema,
        "400": ErrorSchema,
    },
)
def altera_cpf(query: PessoaBuscaSchema, form: PessoaBuscaSchema):
    """Altera os dados da pessoa do banco de dados. O item de busca para encontrar a pessoa é o CPF

    Retorna uma representação dos pessoas.
    """

    pessoa_cpf = query.cpf
    pessoa = busca_por_cpf(pessoa_cpf)

    if not pessoa:
        # se o produto não foi encontrado
        error_msg = "pessoa não encontrado na base :/"
        logger.warning(f"Erro ao buscar login '{pessoa_cpf}', {error_msg}")
        return {"message": error_msg}, 404

    try:
        # criando conexão com a base
        session = Session()
        session.query(Pessoa).filter(Pessoa.cpf == pessoa_cpf).update(
            {
                Pessoa.cpf: form.cpf,
            }
        )
        session.commit()
        logger.debug(f"Alterada a senha do pessoa: '{pessoa.cpf}'")
        pessoa_atualizada = busca_por_cpf(form.cpf)
        return apresenta_pessoa(pessoa_atualizada), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Nao foi possivel alterar o cpf do pessoa. Verifique se o campo cpf está correto.:/"
        logger.warning(f"Erro ao alterar cpf do pessoa: '{pessoa.nome}', {error_msg}")
        return {"message": error_msg}, 404

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Erro ao atualizar a cpf :/"
        logger.warning(f"Erro ao alterar a cpf do '{pessoa.nome}', {error_msg}")
        return {"message": error_msg}, 400


@app.put(
    "/pessoa_atualiza",
    tags=[pessoa_tag],
    responses={
        "200": PessoaViewSchema,
        "400": ErrorSchema,
        "404": ErrorSchema,
    },
)
def altera_dados(form: PessoaSchema):
    """Altera os dados cadastrais da pessoa.

    Recebe os dados da pessoa e utiliza o campo cpf para busca do banco.

    Para alterar o cpf, é necessário utilizar a rota cpf.

    Retorna uma representação do pessoa.
    """

    cpf = form.cpf
    logger.warning(f"Busca por cpf '{cpf}'")
    pessoa = busca_por_cpf(cpf)

    if not pessoa:
        # se o produto não foi encontrado
        error_msg = "pessoa não encontrado na base"
        logger.warning(f"Erro ao buscar cpf '{cpf}', {error_msg}")
        return {"mesage": error_msg}, 404

    try:
        # Salva o CPF do pessoa para fazer a relaçaõ entra a tebela pessoa e a tabela pessoa
        # cpf = pessoa.cpf

        # criando conexão com a base
        session = Session()

        # realiza a atualização da base

        session.query(Pessoa).filter(Pessoa.cpf == cpf).update(
            {
                Pessoa.nome: form.nome,
                # Pessoa.cpf: form.cpf,
                Pessoa.cep: form.cep,
                Pessoa.rua: form.rua,
                Pessoa.bairro: form.bairro,
                Pessoa.cidade: form.cidade,
                Pessoa.estado: form.estado,
            }
        )

        session.commit()

        # Faz uma nova busca no banco para imprimir o resultado atualzado
        pessoa_atualizado = busca_por_cpf(form.cpf)
        logger.debug(f"Alterados os dados o pessoa: '{pessoa_atualizado.nome}'")
        return apresenta_pessoa(pessoa_atualizado), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Nao foi possivel alterar os dados da pessoa. Verifique se o campo login está correto.:/"
        logger.warning(f"Erro ao alterar dados do pessoa: '{pessoa.nome}', {error_msg}")
        return {"mesage": error_msg}, 404

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Erro ao atualizar os dados do pessoa :/"
        logger.warning(f"Erro dados do pessoa: '{pessoa.nome}', {error_msg}")
        return {"mesage": error_msg}, 400


@app.delete(
    "/pessoa_excluir",
    tags=[pessoa_tag],
    responses={
        "200": ErrorSchema,
        "400": ErrorSchema,
        "404": ErrorSchema,
        "409": ErrorSchema,
    },
)
def exclui_pessoa(query: PessoaBuscaSchema):
    """Apaga o pessoa da base de dados

    Utiliza o campo cpf como filtro para busca da pessoa que será excluída

    Retorna uma mensagem com a confirmação da exclusão ou informação do erro
    """

    pessoa_cpf = query.cpf
    pessoa = busca_por_cpf(pessoa_cpf)

    if not pessoa:
        # se o produto não foi encontrado
        error_msg = f"pessoa não encontrado na base: '{query.cpf}'"
        logger.warning(f"Erro ao buscar login '{pessoa_cpf}', {error_msg}")
        return {"message": error_msg}, 404

    try:
        # Salva o CPF do pessoa para fazer a relaçaõ entra a tebela pessoa e a tabela pessoa
        cpf = pessoa.cpf
        # criando conexão com a base
        session = Session()

        session.query(Pessoa).filter(Pessoa.cpf == cpf).delete()

        session.commit()

        logger.debug(f"pessoa excluido com sucesso: '{pessoa.login}'")
        error_msg = f"pessoa exlcuido com sucesso: '{pessoa.login}'"
        return {"message": error_msg}, 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Nao foi excluir a pessoa. Verifique se o campo cpf está correto.:/"
        logger.warning(f"Erro ao excluir o pessoa: '{pessoa.login}', {error_msg}")
        return {"message": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = f"Erro ao excluir os dados da pessoa '{pessoa.cpf}"
        logger.warning(f"Erro ao buscar: '{pessoa.cpf}', {error_msg}")
        return {"message": error_msg}, 400


# Função auxiliar para buscar pessoa
def busca_por_cpf(cpf: str) -> Pessoa:
    logger.debug(f"Procurando senha do pessoa de login:  #{cpf}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    return session.query(Pessoa).filter(Pessoa.cpf == cpf).first()


@app.get(
    "/pessoa_cep",
    tags=[pessoa_tag],
    responses={"200": InterfaceParaEndereco, "404": ErrorSchema},
)
def get_endreco(query: CepBuscaSchema):
    """Realiza consulta de CEP por meio de API externa: https://apicep.com/api-de-consulta/

    API externa livre para uso comercial, para executar em qualquer end-point, sem restrição de CORS.

    Retorna o preenchimento dos dados de rua, bairro, cidade e estado, em caso de cep válido. Formato do CEP: "XXXXX-XXX"
    """

    url = f"https://cdn.apicep.com/file/apicep/{query.cep}.json"

    logger.warning(url)
    response = requests.get(url)

    if response.status_code == 200:
        endereco = json.loads(response.text)

        logger.warning("Endereço encontrado para o CEP:")

        return {
            "Rua": endereco["address"],
            "Bairro": endereco["district"],
            "Cidade": endereco["city"],
            "Estado": endereco["state"],
        }, 200
    else:
        error_msg = (
            "Não foi encontrado endereço para o CEP informado. Verifique o campo CEP. "
        )
        logger.warning(f"CEP: '{query.cep}', {error_msg}")
        return {"message": error_msg}, 404

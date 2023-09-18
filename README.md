
# API para cadastro de funcionários

Esse projeto apresenta o MVP de requisido para conclusão da sprint 3 da curso de  **Engenharia de Softaware**  oferecido pela **PUC-Rio**

Para tal, foi criado uma API em python, utilizando como base as bibliotecas flask e sqlalchemy. 

Essa API tem como objetivo prover ferramentas para criação de um sistema de cadastro de dados pessoais, como nome, cpf e endereço. 

Para auxílio do prencimento do endereço, essa API faz a busca por CEP por uma API externa (https://apicep.com/api-de-consulta/)

**Essa API externa, apiCEP, é livre para uso comercial, para executar em qualquer end-point, sem restrição de CORS.**

Essa Api externa possui apenas uma rota get, cuja url padrão pode ser observada abaixo:

* Padrão da URL	https://cdn.apicep.com/file/apicep/`[cep]`.json

Como retorno, será exposto um json com as informações do endereço, conforme exemplo abaixo:
* Exemplo:	https://cdn.apicep.com/file/apicep/06233-030.json


        {
            "code":"06233-030",
            "state":"SP",
            "city":"Osasco",
            "district":"Piratininga",
            "address":"Rua Paula Rodrigues",
            "status":200,
            "ok":true,
            "statusText":"ok"
        }

Maiores informações sobre a api externa, podem ser encontrada no [`site`](https://apicep.com/api-de-consulta/) do fabricante

Para interação da API com o banco e front-end, foram criadas diversas rodas, entre elas:


>**/pessoa** - para incluir uma nova pessoa à base

>**/pessoa** - para ler os dados de uma dada pessoa, baseado em seu CPF

>**/pessoas** - para obter uma lista com os dados de cada pessoa

>**/pessoa_cep** - para consumir a api externa [`apiCEP`](https://apicep.com/api-de-consulta/), obtendo as informações do endereço, a partir do cep

>**/pessoa_excluir** - para apagar uma bpessoa, baseado no CPF

>**/pessoa_atualiza** - para alterar os campos de dados de uma dada pessoa, exceto o CPF

>**/pessoa_atualiza_cpf** - para alterar o CPF de uma dada pessoa

---
## Banco

Para realizar a rentenção dos dados, a API cria um banco .sqlite3, caso o mesmo não exista.

Banco, possui a tabela `pessoa`, com os seguintes campos:

* (nome, cpf, rua, bairro, cidade, estado)

---
## Como executar 


Será necessário ter todas as libs python listadas no `requirements.txt` instaladas.
Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.

> É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

```
(env)$ pip install -r requirements.txt
```

Este comando instala as dependências/bibliotecas, descritas no arquivo `requirements.txt`.

Para executar a API  basta executar:

```
(env)$ flask run --host 0.0.0.0 --port 5000
```

Abra o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador para verificar o status da API em execução nas três vesões disponíveis (Sswagger, ReDoc, RapiDoc).

Para versão `Swagger` abra o link [http://localhost:5000/openapi/swagger#/](http://localhost:5000/openapi/swagger#/) no navegador

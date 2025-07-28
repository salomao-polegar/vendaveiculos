# 🚗 Sistema de Venda de Veículos - SOAT6

Este projeto é uma aplicação web desenvolvida com Django que permite o gerenciamento da venda de veículos de uma concessionária. 

A autenticação dos usuários - clientes e administradores - é realizada através do Auth0, que gera token de acesso para o acesso aos endpoints.

---

## ✅ Funcionalidades administrativas

- Cadastrar veículos para venda (marca, modelo, ano, cor, preço)
- Editar dados dos veículos cadastrados
- Excluir veículos
- Visualizar veículos vendidos
- Visualizar veículos à venda
- Cadastrar novos compradores

## ✅ Funcionalidades dos clientes

- Listagem de veículos disponíveis para venda, ordenados por preço (crescente)
- Comprar veículos (somente usuários cadastrados)

## 🛠️ Tecnologias Utilizadas

- [Docker](https://www.docker.com/)
- [Python 3.11+](https://www.python.org/)
- [Django Rest Framework](https://www.django-rest-framework.org/)
- Postgres (como banco de dados de produção) ou sqlite (como banco de dados local)

---

## 📁 Clonando o Projeto

```bash
git clone https://github.com/salomao-software/vendaveiculos/
cd vendaveiculos
```

## Rodar o projeto com Docker

```bash
docker build -t api-veiculos .
docker run -p 8000:8000 api-veiculos
```

## Endpoints do projeto

Considerando que o projeto está rodando no localhost:8000

--> endpoints, com exceção de /pessoas/login/, devem enviar o Bearer Token recebido no login.
Para testes, o usuário administrativo é admin@lojaveiculos.com.br com a senha abcdef@123456

### Login 

POST http://localhost:8000/pessoas/login/

Body:
```bash
{
  "email": "email@email.com",
  "senha": "suasenha"
}
```
### Cadastro de Clientes

POST http://localhost:8000/pessoas/cadastro/

body:
```bash
{
  "nome": "Maria Silva",
  "email": "mariasilva10@gmail.com",
  "senha": "abcdef@123456",
  "cpf_cnpj": "01928291829",
  "data_nascimento": "1996-07-23"
}
```


### Cadastro de veículos

POST http://localhost:8000/veiculos

Obs.: recebe uma lista de veículos
```bash
[
  {
    "marca": "Toyota",
    "modelo": "Corolla",
    "ano": 2022,
    "cor": "Prata",
    "preco": "95000",
    "vendido": false
  },
]
```

GET http://localhost:8000/veiculos/

PUT http://localhost:8000/veiculos/{id}/

DELETE http://localhost:8000/veiculos/{id}/delete

### Venda de Veículos
POST http://localhost:8000/veiculos/comprar/
```bash
{
    "veiculo_id" : 1
}
```

## Deploy
O deploy do sistema é realizado automaticamente no Railway, sempre que há uma alteração na branch main do GitHub do projeto.

O sistema está disponível no endpoint https://vendaveiculos-production.up.railway.app (disponível via API).

A branch main é protegita, e deve ser realizado push em outras branchs (como desenvolvimento) para cração de pull requests.
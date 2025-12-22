# Documentação Técnica - API

## API REST para gestão de profissionais de saúde e consultas médicas

<p>Este projeto é uma API de agendamentos desenvolvida com Django Rest Framework, focada em escalabilidade, segurança e automação via Docker. </p>

## Índice

1. Setup do Ambiente
2. Instruções para Rodar o Projeto
3. Testes Automatizados
4. Decisões Técnicas
5. Deploy e CI/CD
6. Erros Encontrados e Soluções
7. Melhorias Propostas
8. Acesse a aplicação
9. Agradecimentos

#### Setup do ambiente

#### Pré-requisitos
* Docker e Docker Compose instalados.
* Git para clonagem.
* Arquivo .env.dev configurado na pasta dotenv_files/.
#### Configuração Inicial
a. Clone o repositório:
```
git clone <url-do-repositorio>
cd api-appointments
```
b. Configure as variáveis de ambiente: Crie o arquivo .env.dev dentro da pasta dotenv_files/ seguindo o modelo do .env.example.

### Instruções para Rodar o Projeto

#### Rodar docker
```
docker compose up -d --build
```


### Testes Automatizados

#### Testes no docker 
```
docker compose exec api python manage.py test
```

#### Testes sem docker(Local)
```
cd api-drf
poetry run python manage.py test
```
### Decisões Técnicas


### Deploy e CI/CD
Embora o foco atual seja o ambiente local, a estrutura foi preparada para produção:

* GitHub Actions: Configuração de workflow em ```.github/workflows/ci-cd.yml``` para validação de código (Pylint) e testes em cada commit.

* Configuração de Produção: Arquivo ```docker-compose.prod.yml``` pronto para ser utilizado com Nginx como Proxy Reverso em instâncias AWS EC2.

### Erros Encontrados e Soluções



### Melhorias Propostas
* **Deploy na AWS**: Realizar o deploy da infraestrutura em uma instância EC2, utilizando o docker-compose.prod.yml e configurando o Nginx como Proxy Reverso.
* **Cache com Redis**: Integrar o Redis para cachear consultas frequentes, como a listagem de profissionais de saúde, melhorando o tempo de resposta da API.

### Acesse a Aplicação

Após rodar aplicação com sucesso:
acesse:

- Swagger UI: http://localhost:8000/api/docs/
- ReDoc: http://localhost:8000/api/redoc/
- Admin: http://localhost:8000/admin/

#### Credenciais padrão:

Username: admin <br>
Password: admin123


### Agradecimentos

Meu sincero agradecimento à Lacrei Saúde pela oportunidade de aprendizado e desenvolvimento. Este projeto foi fundamental para consolidar meus conhecimentos em infraestrutura moderna e automação. É uma honra poder apoiar tecnicamente uma ONG que realiza um trabalho tão vital para a comunidade.

🏳️‍🌈 Conheça o projeto: https://lacreisaude.com.br/

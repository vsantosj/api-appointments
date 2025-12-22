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
8. Agradecimentos
9. Como Contribuir com o projeto

### 1. Setup do ambiente

#### Pré-requisitos

- Docker e Docker Compose instalados.
- Git para clonagem.
- Arquivo .env.dev configurado na pasta dotenv_files/.

#### Configuração Inicial

a. Clone o repositório:

```bash
git clone <url-do-repositorio>
cd api-appointments

# instalar as dependências do projeto
poetry install
```

b. Configure as variáveis de ambiente: Crie o arquivo .env.dev dentro da pasta dotenv_files/ seguindo o modelo do .env.example.

### 2. Instruções para Rodar o Projeto

#### a. Rodar com docker

```bash
docker compose up -d --build
```

#### b. Acesse a Aplicação

Após rodar aplicação com sucesso a api:
acesse:

- Swagger UI: http://localhost:8000/api/docs/
- ReDoc: http://localhost:8000/api/redoc/
- Admin: http://localhost:8000/admin/

Login de acesso:

```bash
{
  "username": "admin",
  "password": "sua_senha_segura"
}
```

### 3. Testes Automatizados

#### Testes no docker

```
docker compose exec api python manage.py test
```

### 4. Decisões Técnicas

1. Arquitetura e Design
   Django REST Framework
   Decisão: Usar Django REST Framework em vez de FastAPI ou Flask.
   Justificativa:

- Maturidade: Framework consolidado com 10+ anos
- Documentação: Excelente documentação e comunidade ativa
- Baterias Incluídas: Admin, ORM, autenticação out-of-the-box
- Serializers: Validação robusta e automática
- Browsable API: Interface web para testar endpoints

JWT (SimpleJWT)
Decisão: Usar JWT em vez de sessões Django.
Justificativa:

- Stateless: Não requer armazenamento de sessões
- Escalável: Facilita microsserviços futuros
- Mobile-friendly: Ideal para apps mobile
- Padrão: Amplamente adotado na indústria

### 5. Deploy e CI/CD

Embora o foco atual seja o ambiente local, a estrutura foi preparada para produção:

- GitHub Actions: Configuração de workflow em `.github/workflows/ci-cd.yml` para validação de código (Pylint) e testes em cada commit.

- Configuração de Produção: Arquivo `docker-compose.prod.yml` pronto para ser utilizado com Nginx como Proxy Reverso em instâncias AWS EC2.

```bash
docker compose exec -T web python manage.py migrate
```

#### Exemplo de Saída dos Testes

```bash
$ python manage.py test

Creating test database for alias 'default'...
System check identified no issues (0 silenced).
..........................
----------------------------------------------------------------------
Ran 26 tests in 20.565s

OK
Destroying test database for alias 'default'...
```

---

#### Fluxo de deploy (CI/CD)

```
┌─────────────────────────────────────────────────────┐
│  t=0s: Developer faz push para main                 │
└─────────────────┬───────────────────────────────────┘
                  │
        ┌─────────▼──────────┐
        │  GitHub detecta    │
        │  inicia workflow   │
        └─────────┬──────────┘
                  │
┌─────────────────▼───────────────────────────────────┐
│  t=10s: JOB 1 - LINT                                │
│  - Checkout código           (5s)                   │
│  - Setup Python              (10s)                  │
│  - Install Poetry            (15s)                  │
│  - Install Dependencies      (30s)                  │
│  - Run Pylint                (30s)                  │
│  Total: ~1min 30s                                   │
└─────────────────┬───────────────────────────────────┘
                  │
                  ├──❌ Score < 8.0 → FALHA (para aqui)
                  │
                  └──✅ Score >= 8.0 → Continua
                            │
        ┌─────────────────▼─────────────────┐
        │  Aguarda Job Lint terminar        │
        └─────────────────┬─────────────────┘
                          │
┌─────────────────────────▼───────────────────────────┐
│  t=2min: JOB 2 - TESTS                              │
│  - Start PostgreSQL service  (10s)                  │
│  - Checkout código           (5s)                   │
│  - Setup Python              (10s)                  │
│  - Install Dependencies      (30s)                  │
│  - Run Tests                 (120s)                 │
│    • Creating test database                         │
│    • Run 26 tests                                   │
│    • Destroying test database                       │
│  Total: ~3min                                       │
└─────────────────────────┬───────────────────────────┘
                          │
                          ├──❌ Algum teste falhou → FALHA
                          │
                          └──✅ 26/26 testes OK → Continua
                                    │
                  ┌─────────────────▼─────────────────┐
                  │  JOB 3 - DEPLOY (se ativo)        │
                  │  - SSH para EC2          (5s)     │
                  │  - Git pull              (10s)    │
                  │  - Docker build          (120s)   │
                  │  - Docker up             (30s)    │
                  │  - Migrate               (10s)    │
                  │  Total: ~3min                     │
                  └─────────────────┬─────────────────┘
                                    │
                          ┌─────────▼─────────┐
                          │  ✅ DEPLOY OK     │
                          │  Aplicação no ar  │
                          └───────────────────┘

TEMPO TOTAL (sem deploy): ~4-5 minutos
TEMPO TOTAL (com deploy): ~7-10 minutos
```

---

### 6. Erros Encontrados e Soluções

### 7. Melhorias Propostas

- **Deploy na AWS**: Realizar o deploy da infraestrutura em uma instância EC2, utilizando o docker-compose.prod.yml e configurando o Nginx como Proxy Reverso.
- **Cache com Redis**: Integrar o Redis para cachear consultas frequentes, como a listagem de profissionais de saúde, melhorando o tempo de resposta da API.

### 8. Agradecimentos

Meu sincero agradecimento à Lacrei Saúde pela oportunidade de aprendizado e desenvolvimento. Este projeto foi fundamental para consolidar meus conhecimentos em infraestrutura moderna e automação. É uma honra poder apoiar tecnicamente uma ONG que realiza um trabalho tão vital para a comunidade.

🏳️‍🌈 Conheça o projeto: https://lacreisaude.com.br/

### 9. 🤝 Como Contribuir com o projeto

Quer contribuir com a api de agendamentos? Toda ajuda é bem-vinda! Aqui estão algumas formas de colaborar:

Para mais detalhes sobre como contribuir, consulte o arquivo [CONTRIBUTING.md](.github/CONTRIBUTING.md).

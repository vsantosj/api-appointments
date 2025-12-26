FROM python:3.12-slim

# Metadados
LABEL maintainer="github.com/vsantosj"
LABEL description="API REST para gestão de profissionais de saúde e consultas"

# Variáveis de ambiente Python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Instala dependências do sistema necessárias para psycopg2 e Poetry
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    postgresql-client \
    libpq-dev \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry==1.8.3

# Configura Poetry para não criar virtualenv (já estamos em container)
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=0 \
    POETRY_VIRTUALENVS_CREATE=0 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

# Define diretório de trabalho
WORKDIR /app

# Copia apenas arquivos de dependências primeiro (melhor cache do Docker)
COPY pyproject.toml poetry.lock ./

# Instala dependências do projeto
RUN poetry install --no-root --only main && rm -rf $POETRY_CACHE_DIR

# Copia o código da aplicação Django
COPY ./api-drf /app/

# Cria pastas necessárias
RUN mkdir -p /app/logs /data/web/static /data/web/media

# Define permissões (importante para produção)
RUN addgroup --system django && \
    adduser --system --ingroup django django && \
    chown -R django:django /app /data

# Copia script de entrada
COPY scripts/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh && chown django:django /entrypoint.sh

USER django

# Expõe a porta 8000
EXPOSE 8000

ENTRYPOINT ["entrypoint.sh"]

CMD ["entrypoint.sh"]

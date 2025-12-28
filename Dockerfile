FROM python:3.12-slim

# Metadados
LABEL maintainer="github.com/vsantosj"
LABEL description="API REST para gestão de profissionais de saúde e consultas"

# Variáveis de ambiente do Poetry
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=0 \
    POETRY_VIRTUALENVS_CREATE=0 \
    POETRY_CACHE_DIR=/tmp/poetry_cache \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /djangoapi

# Instala dependências do sistema (netcat para o script)
RUN apt-get update && apt-get install -y \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --upgrade pip \
    && pip install poetry==2.2.1

#Copia arquivos de dependências PRIMEIRO (otimização de cache)
COPY djangoapi/pyproject.toml djangoapi/poetry.lock* ./

# Instala dependências
RUN poetry install --no-root --only main && rm -rf $POETRY_CACHE_DIR

# Agora copia o código e scripts
COPY djangoapi .
COPY scripts /scripts

# Configura permissões e usuário
RUN adduser --disabled-password --no-create-home duser \
    && chmod -R +x /scripts \
    && chown -R duser:duser /djangoapi

ENV PATH="/scripts:$PATH"

EXPOSE 8000

USER duser

# Comando padrão
CMD ["commands.sh"]

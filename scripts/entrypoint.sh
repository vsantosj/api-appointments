#!/bin/bash
set -e

echo "Iniciando aplicação..."

echo "...Aguardando PostgreSQL..."
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
    sleep 0.1
done
echo "PostgreSQL está pronto!"

# Executa migrações
echo "Executando migrações..."
python manage.py migrate --noinput

# Coleta arquivos estáticos
echo "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput --clear

# Cria superusuário se não existir (apenas em dev)
if [ "$DJANGO_SUPERUSER_USERNAME" ] && [ "$DJANGO_SUPERUSER_PASSWORD" ]; then
    echo "👤 Criando superusuário..."
    python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists():
    User.objects.create_superuser('$DJANGO_SUPERUSER_USERNAME', '$DJANGO_SUPERUSER_EMAIL', '$DJANGO_SUPERUSER_PASSWORD')
    print('Superusuário criado!')
else:
    print('Superusuário já existe.')
END
fi

echo "Aplicação pronta!"

# Inicia o servidor
if [ "$DEBUG" = "1" ]; then
    echo "Modo DEBUG - Iniciando servidor de desenvolvimento..."
    exec python manage.py runserver 0.0.0.0:8000
else
    echo "Modo PRODUÇÃO - Iniciando Gunicorn..."
    exec gunicorn core.wsgi:application \
        --bind 0.0.0.0:8000 \
        --workers 4 \
        --timeout 60 \
        --access-logfile - \
        --error-logfile - \
        --log-level info
fi

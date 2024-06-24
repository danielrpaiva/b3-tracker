# b3-tracker

Requer redis-server instalado: sudo apt install redis-server

Criar ambiente virtual python e ativá-lo

Rodar pip install -r requirements.txt (na pasta raiz do projeto django com o ambiente ativado)

Iniciar redis caso não esteja: systemctl start redis.service

Rodar migração do banco: python manage.py migrate

Renomear o .example.env para .env e setar os valores corretos das variaveis, necessita de um token
para a acessar a api do brapi de onde as informações do mercado financeiro são puxadas: https://brapi.dev/dashboard